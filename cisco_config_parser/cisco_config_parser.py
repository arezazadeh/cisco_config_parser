from .exceptions import *
from .ssh import *
from .parse import *


class ConfigParser:
    """
    - Example: Finding Routing Protocol
    my_file = "switch01_running_config.txt"

    parse = ConfigParser(method="file", content=my_file)

    obj_list = parse.find_parent_child_w_regex("^router")

    for i in obj_list:
        print(i.parent)
        for child_obj in i.child:
            print(child_obj)

    - Finding Interface and Helper address Example

    for i in obj_list:
        vlan_200 = re.search("Vlan200", i.parent)
        if vlan_200:
            print(i.parent)
            for c_obj in i.child:
                if str(c_obj).startswith(" ip helper"):
                    print(str(c_obj))
    """

    def __init__(self, **kwargs):
        """
        :param file: text file with .txt extension
        :param kwargs:
        method:str => options: "int_ssh" (ssh by the module), "ext_ssh" (ssh by the user) or "file"
        content:options: output of ssh (ext_ssh) or Text File with .txt extension. this is only needed if you choose
                "ext_ssh" or "file" as method
        ssh:bool => default False
        platform:str => "nxos" default "ios"
        host:str => default None
        user:str => default None
        password:str => default None
        device_type:str => default cisco_ios (cisco_ios, cisco_xe, cisco_xr)
        """
        self.content = kwargs.get("content") or None
        self.method = kwargs.get("method") or None
        self.ssh = kwargs.get("ssh") or False
        self.host = kwargs.get("host") or None
        self.user = kwargs.get("user") or None
        self.password = kwargs.get("password") or None
        self.device_type = kwargs.get("device_type") or "cisco_ios"
        
        # if self.method is None:
        #     Exception
        
        if self.method == "int_ssh":
            if self.ssh:
                try:
                    self.ssh_to = MySSH(self.host, self.user, self.password, self.device_type)
                except Exception:
                    raise SSHError(self.host)
                
        elif self.method == "file":
            if self.content is None:
                raise ContentMissingError()
            else:
                if not self.content.endswith(".txt"):
                    raise FileReadError(self.content)

        elif self.method == "ext_ssh":
            if self.content is None:
                raise ContentMissingError()

    def _read_file(self):
        with open(self.content, "r") as f:
            content = f.read()
            return content

    def find_parent_child(self, regex):
        """
        :param regex: parsing the file based on the input regex
        :return: List (obj_list)
        """
        try:
            if self.method == "int_ssh":
                if self.ssh:
                    content = self.ssh_to.ssh("show running-config")
                    self.ssh_to.ssh_conn.disconnect()
                    nxos_config_obj = ConfigLineSeparator(content)
                    nxos_config = nxos_config_obj._add_bang_between_section()
                    obj_list = get_parent_child(nxos_config, regex)
                    return obj_list
 

            elif self.method == "file":
                content = self._read_file()
                nxos_config_obj = ConfigLineSeparator(content)
                nxos_config = nxos_config_obj._add_bang_between_section()
                obj_list = get_parent_child(nxos_config, regex)
                return obj_list


            elif self.method == "ext_ssh":
                nxos_config_obj = ConfigLineSeparator(content)
                nxos_config = nxos_config_obj._add_bang_between_section()
                obj_list = get_parent_child(nxos_config, regex)

        except Exception:
            raise PlatformError()


    def ios_get_switchport(self, **kwargs):
        """

        :param kwargs: str:mode=trunk/access - default access
        :return:
        """
        mode = kwargs.get("mode")
        if not mode:
            raise SwitchPortModeError()

        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                port_list = get_interface(content)
                if len(port_list) > 0:
                    obj_list = parse_switch_port(port_list, mode)
                    return obj_list

        elif self.method == "file":
            content = self._read_file()
            port_list = get_interface(content)
            if len(port_list) > 0:
                obj_list = parse_switch_port(port_list, mode)
                return obj_list

        elif self.method == "ext_ssh":
            port_list = get_interface(self.content)
            obj_list = parse_switch_port(port_list, mode)
            return obj_list

    def ios_get_routed_port(self):

        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                port_list = get_interface(content)
                if len(port_list) > 0:
                    obj_list = parse_routed_port(port_list)
                    return obj_list

        elif self.method == "file":
            content = self._read_file()
            port_list = get_interface(content)
            if len(port_list) > 0:
                obj_list = parse_routed_port(port_list)
                return obj_list

        elif self.method == "ext_ssh":
            port_list = get_interface(self.content)
            obj_list = parse_routed_port(port_list)
            return obj_list

    def ios_get_svi_objects(self):

        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                obj_list = get_svi(content)
                if len(obj_list) > 0:
                    return obj_list

        elif self.method == "file":
            content = self._read_file()
            obj_list = get_svi(content)
            if len(obj_list) > 0:
                return obj_list

        elif self.method == "ext_ssh":
            obj_list = get_svi(self.content)
            return obj_list



    def nxos_get_vlan_info(self):
        """
        >>> nxos_parser = ConfigParser(method="file", content=file1, platform="nxos")
        >>> vlan_info = nxos_parser.nxos_get_vlan_info()
        >>> vlan_info.vlan = "2626"
        >>> print(vlan_info.vlan)
        :return:
        !
        vlan 2626
          name GRN200_nonPROD_APP_01
          vn-segment 2002626
        !
        interface Vlan2626
          description grn200 nonPROD App Servers 01
          no shutdown
          mtu 9216
          vrf member GRN200
          no ip redirects
          ip address 10.147.148.1/24
          no ipv6 redirects
          fabric forwarding mode anycast-gateway
        !
        int nve1
          member vni 2002626
            suppress-arp
            ingress-replication protocol bgp
        !
        evpn
          vni 2002626 l2
            rd auto
            route-target import auto
            route-target export auto

        """
        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                vlan_info_obj = NXOSGetParent(content=content)
                vlan_info = vlan_info_obj._get_vlan_info()
                return vlan_info

        elif self.method == "file":
            content = self._read_file()
            vlan_info_obj = NXOSGetParent(content=content)
            vlan_info = vlan_info_obj._get_vlan_info()
            return vlan_info

        elif self.method == "ext_ssh":
            vlan_info_obj = NXOSGetParent(content=self.content)
            vlan_info = vlan_info_obj._get_vlan_info()
            return vlan_info


    def nxos_get_vlan(self):
        """
        >>> nxos_parser = ConfigParser(method="file", content=file1, platform="nxos")
        >>> vlan_info = nxos_parser.nxos_get_vlan()
        >>> for i in vlan_info:
                print(i.vlan)

        :return:

        vlan 3622
        vlan 3623
        vlan 3624
        vlan 3625
        vlan 3626
        """
        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                vlan_obj = NXOSGetParent(content=content)
                vlan_obj_list = vlan_obj._get_vlan()
                return vlan_obj_list

        elif self.method == "file":
            content = self._read_file()
            vlan_obj = NXOSGetParent(content=content)
            vlan_obj_list = vlan_obj._get_vlan()
            return vlan_obj_list

        elif self.method == "ext_ssh":
            vlan_obj = NXOSGetParent(content=self.content)
            vlan_obj_list = vlan_obj._get_vlan()
            return vlan_obj_list

    def nxos_get_l3_int(self):
        """
        >>> nxos_parser = ConfigParser(method="file", content=file1, platform="nxos")
        >>> l3_intf = nxos_parser.nxos_get_l3_int()
        >>> for i in l3_intf:
                print(i.intf)
        :return: list of vlan objects
        interface Vlan12
        interface Vlan15
        interface Vlan16
        interface Vlan17
        """
        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                l3_intf_obj = NXOSGetParent(content=content)
                l3_intf_obj_list = l3_intf_obj._get_l3_int()
                return l3_intf_obj_list

        elif self.method == "file":
            content = self._read_file()
            l3_intf_obj = NXOSGetParent(content=content)
            l3_intf_obj_list = l3_intf_obj._get_l3_int()
            return l3_intf_obj_list

        elif self.method == "ext_ssh":
            l3_intf_obj = NXOSGetParent(content=self.content)
            l3_intf_obj_list = l3_intf_obj._get_l3_int()
            return l3_intf_obj_list

    def nxos_get_routing_protocol(self):
        """
        >>> nxos_parser = ConfigParser(method="file", content=file1, platform="nxos")
        >>> bgp_rp = nxos_parser.nxos_get_routing_protocol()
        >>> bgp_rp.vrf = "grn200"
        >>> bgp_rp.neighbor = "10.147.234.241"
        >>> print(bgp_rp.vrf.neighbor)

        :return:
        neighbor 10.147.234.241
         inherit peer CP_EBGP
         no shutdown
         update-source Vlan2806
         address-family ipv4 unicast
         allowas-in 3
         route-map GRN200_BGP_RM_INBOUND_FROM_DMZ_TRANSIT_FW in
         route-map GRN200_BGP_RM_OUTBOUND_TO_DMZ_TRANSIT_FW out

        """
        if self.method == "int_ssh":
            if self.ssh:
                content = self.ssh_to.ssh("show running-config")
                bgp_obj = NXOSGetParent(content=content)
                bgp_routing_protocol_obj = bgp_obj._get_routing_protocol()
                return bgp_routing_protocol_obj

        elif self.method == "file":
            content = self._read_file()
            bgp_obj = NXOSGetParent(content=content)
            bgp_routing_protocol_obj = bgp_obj._get_routing_protocol()
            return bgp_routing_protocol_obj

        elif self.method == "ext_ssh":
            bgp_obj = NXOSGetParent(content=self.content)
            bgp_routing_protocol_obj = bgp_obj._get_routing_protocol()
            return bgp_routing_protocol_obj