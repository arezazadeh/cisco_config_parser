import re
import ipaddress
from .obj import *
from .regex import *


def parse_routed_port(port_list):
    routed_port_list = []
    obj_list = []
    for i in port_list:
        interface_parent = SPLIT_ON_LINE.split(i)
        for line in interface_parent:
            if "ip address" in line or "ipv4 address" in line:
                routed_port_list.append(i)
                
    for line in routed_port_list:
        routed_port_obj = RoutedPort()

        helper_list = []
        split_line = SPLIT_ON_LINE.split(line.strip())
        intf_addresses = []
        for ent in split_line:
            if ent.strip().startswith("shutdown"):
                routed_port_obj.state = "disabled"
                
            elif ent.strip().startswith("interface"):
                intf_name = re.search("interface\s(.*)", ent.strip())
                routed_port_obj.intf = intf_name.group(1)
                
            elif ent.strip().startswith("description"):
                description = re.search("description\s(.*)", ent.strip())
                routed_port_obj.description = description.group(1)
                
            elif ent.strip().startswith("ip address"):
                if "secondary" in ent.strip():
                    address = ent.split("ip address")[1].split("secondary")[0]
                    addr_mask = address.split()
                    routed_port_obj.sec_ip = addr_mask[0]
                    routed_port_obj.sec_mask = addr_mask[1]
                    routed_port_obj.sec_subnet = ipaddress.ip_network(f"{routed_port_obj.sec_ip}/{routed_port_obj.sec_mask}", strict=False)
                else:
                    address = ent.split("ip address")[1]
                    addr_mask = address.split()
                    routed_port_obj.ip = addr_mask[0]
                    routed_port_obj.mask = addr_mask[1]
                    routed_port_obj.subnet = ipaddress.ip_network(f"{routed_port_obj.ip}/{routed_port_obj.mask}", strict=False)
                
            elif ent.strip().startswith("standby"):
                vip_regex = re.search("^standby\s\d+\sip\s(\S+)", ent.strip())
                if vip_regex:
                    vip_ip = vip_regex.group(1)
                    routed_port_obj.vip = vip_ip

            elif ent.strip().startswith("vrrp"):
                vip_regex = re.search("^vrrp\s\d+\sip\s(\S+)", ent.strip())
                if vip_regex:
                    vip_ip = vip_regex.group(1)
                    routed_port_obj.vip = vip_ip


            elif ent.strip().startswith("ipv4 address"):
                address = ent.split("ipv4 address")[1]
                addr_mask = address.split()
                routed_port_obj.ip = addr_mask[0]
                routed_port_obj.mask = addr_mask[1]
                routed_port_obj.subnet = ipaddress.ip_network(f"{routed_port_obj.ip}/{routed_port_obj.mask}", strict=False)
                
            elif ent.strip().startswith("ip helper-address"):
                helper_list.append(ent)
                
            elif ent.strip().startswith("ip vrf forwarding"):
                vrf_name = re.search("ip\svrf\sforwarding\s(\S+)", ent.strip())
                routed_port_obj.vrf = vrf_name.group(1)
                
            elif ent.strip().startswith("vrf member"):
                vrf_name = re.search("vrf\smember\s(\S+)", ent.strip())
                routed_port_obj.vrf = vrf_name.group(1)

            elif ent.strip().startswith("vrf forwarding"):
                vrf_name = re.search("vrf\sforwarding\s(\S+)", ent.strip())
                routed_port_obj.vrf = vrf_name.group(1)

            elif ent.strip().startswith("vrf"):
                vrf_name = re.search("vrf\s(\S+)", ent.strip())
                routed_port_obj.vrf = vrf_name.group(1)
                
        if routed_port_obj.state is None:
            routed_port_obj.state = "enabled"
            
        routed_port_obj.helper = helper_list
        
        obj_list.append(routed_port_obj)
    return obj_list


def parse_switch_port(port_list, mode):
    trunk_port_list = []
    access_port_list = []
    switchport_interface_list = []

    for i in port_list:
        interface_parent = SPLIT_ON_LINE.split(i)
        for line in interface_parent:
            if "switchport mode" in line:
                switchport_interface_list.append(i)

    for line in switchport_interface_list:
        if "switchport mode trunk" in line:
            trunk_port_list.append(line)

        if "switchport mode access" in line:
            access_port_list.append(line)

    if mode == "access":
        access_obj_list = is_access_port(access_port_list)
        return access_obj_list

    if mode == "trunk":
        trunk_obj_list = is_trunk_port(trunk_port_list)
        return trunk_obj_list


def get_parent_child(content, regex):
    obj_list = []
    split_on_bang = SPLIT_ON_FIRST_BANG_MULTILINE.split(content)
    for i in split_on_bang:
        regex_result = re.match(regex, i.strip())
        if regex_result:
            if i.strip().startswith(regex_result.group()):
                child_regex = SPLIT_ON_LINE.split(i.strip())
                parent = child_regex[0]
                child_regex.pop(0)
                child = child_regex
                obj_list.append(ParentObj(parent, child))
    return obj_list


def get_interface(content):
    """
    :return: port_list which is the interface config block
    """
    port_list = []

    split_on_bang = SPLIT_ON_FIRST_BANG_MULTILINE.split(content)
    for obj in split_on_bang:
        parent_obj = INTERFACE_MULTILINE_REGEX.findall(obj)
        if parent_obj:
            port_list.append(obj)
    return port_list


def get_svi(content):
    obj_list = []
    intf_vlan_list = []
    split_on_bang = SPLIT_ON_FIRST_BANG_MULTILINE.split(content)
    for obj in split_on_bang:
        parent_obj = VLAN_SVI_INTERFACE_MULTILINE_REGEX.findall(obj)
        if parent_obj:
            intf_vlan_list.append(obj)

    for i in intf_vlan_list:
        interface_obj = IntObj()
        helper_list = []
        
        line = SPLIT_ON_LINE.split(i.strip())
        
        for ent in line:
            if ent.strip().startswith("shutdown"):
                interface_obj.state = "disabled"
                
            if ent.strip().startswith("interface Vlan"):
                interface_obj.intf = ent
                
            if ent.strip().startswith("description"):
                interface_obj.description = ent
                
            if ent.strip().startswith("ip address"):
                interface_obj.ip_add = ent
                
            if ent.strip().startswith("ip helper-address"):
                helper_list.append(ent)
                
            if ent.strip().startswith("ip vrf for"):
                interface_obj.vrf_member = ent
                
        if interface_obj.state is None:
            interface_obj.state = "enabled"
        
        interface_obj.helper = helper_list
        obj_list.append(interface_obj)

    return obj_list



def is_trunk_port(port_list):
    obj_list = []
    for line in port_list:
        trunk_obj = SwitchPortTrunk()

        split_line = SPLIT_ON_LINE.split(line.strip())
        trunk_obj.port = split_line[0]
        
        for i in split_line:
            if "description" in i:
                trunk_obj.description = i

            if "switchport trunk allowed" in i:
                trunk_obj.allowed_vlan = i

            if i.strip().startswith("shutdown"):
                trunk_obj.state = "disabled"
                
        if trunk_obj.state is None:
            trunk_obj.state = "enabled"

        obj_list.append(trunk_obj)
    return obj_list


def is_access_port(port_list):
    obj_list = []
    for line in port_list:
        access_obj = SwitchPortAccess()
        
        split_line = SPLIT_ON_LINE.split(line.strip())
        access_obj.port = split_line[0]
        for i in split_line:

            if "description" in i:
                access_obj.description = i.split("description")[1].strip()

            if "voice vlan" in i:
                voice_vlan_id = i.split("voice")[1]
                access_obj.voice = f"Voice {voice_vlan_id}"

            if "switchport access vlan" in i:
                vlan_id = i.split("access vlan")[1]
                access_obj.vlan = f"Vlan {vlan_id}"

            if i.strip().startswith("shutdown"):
                access_obj.state = "disabled"

        if access_obj.state is None:
            access_obj.state = "enabled"

        obj_list.append(access_obj)
    return obj_list


class _ParentChildren:
    def __init__(self, **kwargs):
        self.parent = kwargs.get("parent")
        self.children = kwargs.get("children")


class _L3IntfParentChildren:
    def __init__(self, **kwargs):
        self.intf = kwargs.get("intf")
        self.vrf = kwargs.get("vrf")
        self.ip = kwargs.get("ip")
        self.mask = kwargs.get("mask")
        self.subnet = kwargs.get("subnet")
        self.description = kwargs.get("description")
        self.state = kwargs.get("state")
        self.sec_ip = kwargs.get("sec_ip")
        self.sec_subnet = kwargs.get("sec_subnet")
        self.sec_mask = kwargs.get("sec_mask")


class _VLAN:
    def __init__(self, **kwargs):
        self.vlan = kwargs.get("vlan")
        self.description = kwargs.get("description") or f"  {None}"
        self.vn = kwargs.get("vn") or f"  {None}"
        
    
class _VLANInfo:
    def __init__(self, **kwargs):
        self._config = kwargs.get("_config")
        self._vlan = "all"


    @property
    def vlan(self):
        if self._vlan == "all":
            return "Please specify VLAN ID"

        split_on_bang = SPLIT_ON_BANG_MULTILINE.split(self._config)
        vlan_related_info = ""
        nve_config = ""
        evpn_config = ""
        for i in split_on_bang:

            if "nve" in i:
                split_line = SPLIT_ON_LINE_MULTILINE.split(i)
                for line in split_line:
                    parent = NVE_MEMBER_VNI_PARENT_REGEX.search(line)
                    children = NVE_MEMBER_VNI_CHILDREN_REGEX.search(line)
                    if parent:
                        nve_config += "!\n"
                        nve_config += f"{parent.group()}\n"
                    if children:
                        nve_config += f"{children.group()}\n"

            evpn_search = BGP_EVPN_REGEX.search(i.strip())
            if evpn_search:
                split_evpn_lines = SPLIT_ON_LINE_MULTILINE.split(i)
                for evpn_line in split_evpn_lines:
                    vni_parent = BGP_EVPN_PARENT_REGEX.search(evpn_line)
                    vni_children = CHILDREN_WITH_4_SPACE_REGEX.search(evpn_line)
                    if vni_parent:
                        evpn_config += "!\n"
                        evpn_config += f"{vni_parent.group()}\n"
                    if vni_children:
                        evpn_config += f"{vni_children.group()}\n"

            if self._vlan.strip() in i and not "nve" in i and not "vni" in i:
                vlan_related_info += "!\n"
                vlan_related_info += f"{i}\n"

        split_nve_on_bang = SPLIT_ON_BANG_MULTILINE.split(nve_config)
        for i in split_nve_on_bang:
            if self._vlan.strip() in i.strip():
                vlan_related_info += "!\n"
                vlan_related_info += "int nve1"
                vlan_related_info += f"{i}\n"

        split_evpn_on_bang = SPLIT_ON_BANG_MULTILINE.split(evpn_config)
        for i in split_evpn_on_bang:
            if self._vlan.strip() in i.strip():
                vlan_related_info += "!\n"
                vlan_related_info += "evpn"
                vlan_related_info += f"{i}\n"

        return vlan_related_info


    @vlan.setter
    def vlan(self, vlan):
        if self._vlan == "":
            self._vlan = "all"

        self._vlan = vlan


class _NeighborInfo:
    def __init__(self, **kwargs):
        self._neighbor_segment = kwargs.get("_neighbor_segment")
        self._neighbor = "all"

    @property
    def neighbor(self):
        neighbor_stringify = self._stringify_neighbor()
        neighbor = self._find_neighbor_section(neighbor_stringify)
        return neighbor


    @neighbor.setter
    def neighbor(self, neighbor):
        self._neighbor = neighbor


    def _stringify_neighbor(self):
        neighbor_stringify = ""

        split_neighbor = SPLIT_ON_LINE_MULTILINE.split(self._neighbor_segment.strip())
        for i in split_neighbor:

            neighbor_ip = BGP_NEIGHBOR_REGEX.search(i)
            neighbor_section = CHILDREN_WITH_5_SPACE_REGEX.search(i)

            if neighbor_ip:
                neighbor_stringify += f"!\n"
                neighbor_stringify += f"{neighbor_ip.group().strip()}\n"

            if neighbor_section:
                neighbor_stringify += f" {neighbor_section.group().strip()}\n"

        return neighbor_stringify


    def _find_neighbor_section(self, neighbor_string):

        if self._neighbor == "all":
            return neighbor_string

        split_on_bang = SPLIT_ON_BANG_MULTILINE.split(neighbor_string)
        for i in split_on_bang:
            if self._neighbor.strip() in i.strip():
                return i



class RoutingProtocol:
    def __init__(self, **kwargs):
        self._vrf_segment = kwargs.get("_vrf_segment")
        self._vrf = "vrf"
        self.neighbor = kwargs.get("neighbor") or "all"


    @property
    def vrf(self):

        """
        getter: gets neighbors for the given VRF
        :return:
        """
        split_on_bang = SPLIT_ON_BANG_MULTILINE.split(self._vrf_segment)
        vrf = self._vrf
        vrf_list = []
        for i in split_on_bang:

            if "vrf " in i.strip():
                if vrf == "vrf":
                    vrf_regex = ROUTER_BGP_VRF_CONFIG_REGEX.search(i.strip())
                    if vrf_regex:
                        vrf_list.append(vrf_regex.group())

                else:
                    vrf_regex = find_vrf_section(vrf, i.strip())
                    if vrf_regex:
                        neighbor_info = _NeighborInfo(_neighbor_segment=i)
                        neighbor_info.neighbor = self.neighbor
                        return neighbor_info

        if len(vrf_list) != 0:
            return vrf_list
        else:
            return f"VRF {self._vrf} was not found"


    @vrf.setter
    def vrf(self, vrf):
        """
        setter: sets VRF to receive neighbors
        :param vrf:
        :return:
        """
        self._vrf = vrf


class NXOSGetParent:
    """
    --------------------------------------------------------------------------
        file = "STNMED2-MTR-BL01_running.txt"

        ConfigLineSeparator = ConfigConfigLineSeparator(content=file, method="file", platform="nxos")
        obj = ConfigLineSeparator.find_parent_child()

        vlan_info = obj.get_vlan_info()
        vlan_info.vlan = "2626"
        print(vlan_info.vlan)
    --------------------------------------------------------------------------


    """
    def __init__(self, content):
        self._content = content


    def _get_vlan_info(self):

        nxos_config_separator = ConfigLineSeparator(self._content)
        sectioned_config = nxos_config_separator._add_bang_between_section()
        vlan_obj = _VLANInfo(_config=sectioned_config)
        return vlan_obj

    def _get_vlan(self):
        nxos_config_separator = ConfigLineSeparator(self._content)
        sectioned_config = nxos_config_separator._add_bang_between_section()
        split_line = SPLIT_ON_BANG_MULTILINE.split(sectioned_config)
        vlan_list = []
        for i in split_line:
            vlan_info_obj = _VLAN()
            vlan_regex = VLAN_CONFIG_REGEX.search(i.strip())
            no_vlan = EXCLUDED_VLAN_CONFIG_REGEX.search(i.strip())
            if not no_vlan and vlan_regex:
                vlan_segment = SPLIT_ON_LINE.split(i.strip())
                vlan_info_obj.vlan = vlan_segment[0]
                for seg in vlan_segment:
                    if "name" in seg:
                        vlan_info_obj.description = seg

                    if "vn-segment" in seg:
                        vlan_info_obj.vn = seg
                vlan_list.append(vlan_info_obj)
        return vlan_list

    def _get_l3_int(self):
        nxos_config_separator = ConfigLineSeparator(self._content)
        sectioned_config = nxos_config_separator._add_bang_between_section()
        split_line = SPLIT_ON_BANG_MULTILINE.split(sectioned_config)
        intf_obj_list = []
        for i in split_line:
            if i.strip().startswith("interface"):
                if "ip address" in i.strip():
                    intf_parent_child = _L3IntfParentChildren()
                    res = re.findall("^\s+no\sshutdown", i, flags=re.MULTILINE)
                    if res:
                        intf_parent_child.state = "enabled"
                    else:
                        intf_parent_child.state = "disabled"


                    intf = SPLIT_ON_LINE.split(i.strip())
                    intf_name = re.search("interface\s(\S+)", intf[0].strip())
                    intf_parent_child.intf = intf_name.group(1)

                    for item in intf:
                        if "vrf member" in item.strip():
                            vrf_name = re.search("vrf\smember\s(\S+)", item.strip())
                            intf_parent_child.vrf = vrf_name.group(1)

                        if "ip address" in item.strip():
                            if "secondary" in item.strip():
                                intf_ip = re.search("ip\saddress\s(\d+\.\d+\.\d+\.\d+)/(\d+)", item.strip())
                                intf_parent_child.sec_subnet = ipaddress.IPv4Interface(f"{intf_ip.group(1)}/{intf_ip.group(2)}").network
                                intf_parent_child.sec_ip = intf_ip.group(1)
                                intf_parent_child.sec_mask = intf_ip.group(2)
                            else:
                                intf_ip = re.search("ip\saddress\s(\d+\.\d+\.\d+\.\d+)/(\d+)", item.strip())

                                intf_parent_child.subnet = ipaddress.IPv4Interface(f"{intf_ip.group(1)}/{intf_ip.group(2)}").network
                                intf_parent_child.ip = intf_ip.group(1)
                                intf_parent_child.mask = intf_ip.group(2)


                        if "description" in item.strip():
                            description = re.search("description\s+(.*)", item.strip())
                            intf_parent_child.description = description.group(1)

                    intf_obj_list.append(intf_parent_child)

        return intf_obj_list


    def _get_routing_protocol(self):
        nxos_parser = ConfigLineSeparator(content=self._content)
        routing_segment = nxos_parser._get_router_segment()
        routing_protocol = RoutingProtocol(_vrf_segment=routing_segment)
        return routing_protocol


class ConfigLineSeparator:
    def __init__(self, content):
        self.content = content
        self.sectioned_content = ""
    
    def _add_bang_between_section(self):
        splited_on_line = SPLIT_ON_LINE.split(self.content)
        for i in splited_on_line:
            parent_regex = PARENT_LINE_REGEX.search(i)
            children_regex = CHILDREN_LINE_REGEX.search(i)
            if parent_regex:
                self.sectioned_content += "!\n"
                self.sectioned_content += f"{parent_regex.group()}\n"
            if children_regex:
                self.sectioned_content += f"{children_regex.group()}\n"
        return self.sectioned_content


    def _get_router_segment(self):
        sectioned_config = self._add_bang_between_section()
        split_on_bang = SPLIT_ON_BANG_MULTILINE.split(sectioned_config)
        bgp_string = ""
        for i in split_on_bang:
            if "router bgp" in i.strip():
                bgp_segment = SPLIT_ON_LINE.split(i)
                for seg in bgp_segment:
                    bgp_vrf = ROUTER_BGP_VRF_REGEX.search(seg)
                    bgp_process = ROUTER_BGP_PARENT_REGEX.search(seg)
                    if bgp_process:
                        bgp_string += f"{bgp_process.group()}\n"
                    if bgp_vrf:
                        bgp_string += "!\n"
                        bgp_string += f"{bgp_vrf.group()}\n"

                    bgp_vrf_child = CHILDREN_WITH_3_SPACE_REGEX.search(seg)
                    if bgp_vrf_child:
                        bgp_string += f"{bgp_vrf_child.group()}\n"

        return bgp_string



class _CheckPointAddBang:
    def __init__(self, content):
        self.content = content
        self._section = ""

    def _get_banged(self):
        intf_section = re.split("\n", self.content)
        for section in intf_section:
            intf_name = re.search("^(\S+.*)", section)
            child = re.search("^\s+(.*)", section)

            if intf_name:
                self._section += "!\n"
                self._section += f"{intf_name.group()}\n"
            if child:
                self._section += f"{child.group()}\n"
                self._section += "\n"

        return self._section


class CheckPointIntfInfo:
    def __init__(self, **kwargs):
        self.intf = kwargs.get("intf")
        self.ip = kwargs.get("ip")


def get_cp_int_ip(content):
    intf_info = []
    obj = _CheckPointAddBang(content)
    res = obj._get_banged()
    sectioned = re.split("!", res, flags=re.MULTILINE)
    for section in sectioned:
        cp = CheckPointIntfInfo()
        intf_name = re.search("^Interface\s(\S+)", section, flags=re.MULTILINE)
        ip_addr = re.search("^\s+ipv4-address\s(.*)", section, flags=re.MULTILINE)
        if intf_name:
            if ip_addr:
                cp.intf = intf_name.group(1)
                cp.ip = ip_addr.group(1)
                intf_info.append(cp)

    return intf_info