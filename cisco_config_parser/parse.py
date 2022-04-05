import re
import ipaddress
from .obj import *


def parse_routed_port(port_list):
    routed_port_list = []
    obj_list = []
    for i in port_list:
        interface_parent = re.split("\n", i)
        for line in interface_parent:
            if "ip address" in line or "ipv4 address" in line:
                routed_port_list.append(i)
                
    for line in routed_port_list:
        routed_port_obj = RoutedPort()

        helper_list = []
        split_line = re.split("\n", line.strip())
        
        for ent in split_line:
            if ent.strip().startswith("shutdown"):
                routed_port_obj.state = ent
                
            if ent.strip().startswith("interface"):
                routed_port_obj.intf = ent
                
            if ent.strip().startswith("description"):
                routed_port_obj.description = ent
                
            if ent.strip().startswith("ip address"):
                address = ent.split("ip address")[1]
                addr_mask = address.split()
                routed_port_obj.ip_add = addr_mask[0]
                routed_port_obj.mask = addr_mask[1]
                routed_port_obj.subnet = ipaddress.ip_network(f"{routed_port_obj.ip_add}/{routed_port_obj.mask}", strict=False)
                
            if ent.strip().startswith("ipv4 address"):
                address = ent.split("ipv4 address")[1]
                addr_mask = address.split()
                routed_port_obj.ip_add = addr_mask[0]
                routed_port_obj.mask = addr_mask[1]
                routed_port_obj.subnet = ipaddress.ip_network(f"{routed_port_obj.ip_add}/{routed_port_obj.mask}", strict=False)
                
            if ent.strip().startswith("ip helper-address"):
                helper_list.append(ent)
                
            if ent.strip().startswith("ip vrf for"):
                routed_port_obj.vrf_member = ent
                
            if ent.strip().startswith("vrf"):
                routed_port_obj.vrf_member = ent
                
            if ent.strip().startswith("vrf member"):
                routed_port_obj.vrf_member = ent
                
        if routed_port_obj.state is None:
            routed_port_obj.state = "no shutdown"
            
        routed_port_obj.helper = helper_list
        
        obj_list.append(routed_port_obj)
    return obj_list


def parse_switch_port(port_list, mode):
    trunk_port_list = []
    access_port_list = []
    switchport_interface_list = []

    for i in port_list:
        interface_parent = re.split("\n", i)
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


def split_content(content, regex):
    obj_list = []
    split_on_bang = re.split("^!$", content, flags=re.MULTILINE)
    for i in split_on_bang:
        regex_result = re.match(regex, i.strip())
        if regex_result:
            if i.strip().startswith(regex_result.group()):
                regex_parent_child = re.split("\n", i.strip())
                parent = regex_parent_child[0]
                regex_parent_child.pop(0)
                child = regex_parent_child
                obj_list.append(ParentObj(parent, child))
    return obj_list


def get_interface(content):
    """
    :return: port_list which is the interface config block
    """
    port_list = []

    split_on_bang = re.split("^!$", content, flags=re.MULTILINE)
    for obj in split_on_bang:
        parent_obj = re.findall("^interface\s+(.*)", obj, flags=re.MULTILINE)
        if parent_obj:
            port_list.append(obj)
    return port_list


def get_svi(content):
    obj_list = []
    intf_vlan_list = []
    split_on_bang = re.split("^!$", content, flags=re.MULTILINE)
    for obj in split_on_bang:
        parent_obj = re.findall("^interface Vlan(.*)", obj, flags=re.MULTILINE)
        if parent_obj:
            intf_vlan_list.append(obj)

    for i in intf_vlan_list:
        interface_obj = IntObj()
        helper_list = []
        
        line = re.split("\n", i.strip())
        
        for ent in line:
            if ent.strip().startswith("shutdown"):
                interface_obj.state = ent
                
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
            interface_obj.state = " no shutdown"
        
        interface_obj.helper = helper_list
        obj_list.append(interface_obj)

    return obj_list



def is_trunk_port(port_list):
    obj_list = []
    for line in port_list:
        trunk_obj = SwitchPortTrunk()

        split_line = re.split("\n", line.strip())
        trunk_obj.port = split_line[0]
        
        for i in split_line:
            if "description" in i:
                trunk_obj.description = i

            if "switchport trunk allowed" in i:
                trunk_obj.allowed_vlan = i

            if i.strip().startswith("shutdown"):
                trunk_obj.state = "shutdown"
                
        if trunk_obj.state is None:
            trunk_obj.state = " no shutdown"

        obj_list.append(trunk_obj)
    return obj_list


def is_access_port(port_list):
    obj_list = []
    for line in port_list:
        access_obj = SwitchPortAccess()
        
        split_line = re.split("\n", line.strip())
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
                access_obj.state = "shutdown"

        if access_obj.state is None:
            access_obj.state = "no shutdown"

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
        self.description = kwargs.get("description")


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

        split_on_bang = re.split("!", self._config, flags=re.MULTILINE)
        vlan_related_info = ""
        nve_config = ""
        evpn_config = ""
        nve_vlan_config = ""
        evpn_regex = re.compile("vni [0-9]{7} l2")
        for i in split_on_bang:

            if "nve" in i:
                split_line = re.split("\n", i, flags=re.MULTILINE)
                for line in split_line:
                    parent = re.search("^\s{2}member vni [0-9]{7}$", line)
                    children = re.search("\s{3}.*", line)
                    if parent:
                        nve_config += "!\n"
                        nve_config += f"{parent.group()}\n"
                    if children:
                        nve_config += f"{children.group()}\n"

            evpn_search = evpn_regex.search(i.strip())
            if evpn_search:
                split_evpn_lines = re.split("\n", i, flags=re.MULTILINE)
                for evpn_line in split_evpn_lines:
                    vni_parent = re.search("\s{2}vni [0-9]{7} l2", evpn_line)
                    vni_children = re.search("\s{4}.*", evpn_line)
                    if vni_parent:
                        evpn_config += "!\n"
                        evpn_config += f"{vni_parent.group()}\n"
                    if vni_children:
                        evpn_config += f"{vni_children.group()}\n"

            if self._vlan.strip() in i and not "nve" in i and not "vni" in i:
                vlan_related_info += "!\n"
                vlan_related_info += f"{i}\n"

        split_nve_on_bang = re.split("!", nve_config, flags=re.MULTILINE)
        for i in split_nve_on_bang:
            if self._vlan.strip() in i.strip():
                vlan_related_info += "!\n"
                vlan_related_info += "int nve1"
                vlan_related_info += f"{i}\n"

        split_evpn_on_bang = re.split("!", evpn_config, flags=re.MULTILINE)
        for i in split_evpn_on_bang:
            if self._vlan.strip() in i.strip():
                vlan_related_info += "!\n"
                vlan_related_info += "evpn"
                vlan_related_info += f"{i}\n"

        return vlan_related_info


    @vlan.setter
    def vlan(self, vlan):
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

        split_neighbor = re.split("\n", self._neighbor_segment.strip(), flags=re.MULTILINE)
        for i in split_neighbor:

            neighbor_ip = re.search("^(\s{4}neighbor\s\d+.\d+.\d+.\d+)", i)
            neighbor_section = re.search("^\s{5}.*", i)

            if neighbor_ip:
                neighbor_stringify += f"!\n"
                neighbor_stringify += f"{neighbor_ip.group().strip()}\n"

            if neighbor_section:
                neighbor_stringify += f" {neighbor_section.group().strip()}\n"

        return neighbor_stringify


    def _find_neighbor_section(self, neighbor_string):

        if self._neighbor == "all":
            return neighbor_string

        split_on_bang = re.split("!", neighbor_string, flags=re.MULTILINE)
        for i in split_on_bang:
            if self._neighbor.strip() in i.strip():
                return i



class _RoutingProtocol:
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
        split_on_bang = re.split("!", self._vrf_segment, flags=re.MULTILINE)
        vrf = self._vrf
        vrf_list = []
        for i in split_on_bang:

            if "vrf " in i.strip():
                if vrf == "vrf":
                    vrf_regex = re.search("^vrf\s(.*)", i.strip())
                    if vrf_regex:
                        vrf_list.append(vrf_regex.group())

                else:
                    vrf_regex = re.search(f"^(vrf {vrf.upper()}.*)", i.strip())
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


class GetParent:
    """
    --------------------------------------------------------------------------
        file = "STNMED2-MTR-BL01_running.txt"

        parser = ConfigParser(content=file, method="file", platform="nxos")
        obj = parser.find_parent_child()

        vlan_info = obj.get_vlan_info()
        vlan_info.vlan = "2626"
        print(vlan_info.vlan)
    --------------------------------------------------------------------------


    """
    def __init__(self, content):
        self._result = content


    def get_vlan_info(self):
        parser = Parser(self._result)
        sectioned_config = parser._add_bang_between_section()
        vlan_obj = _VLANInfo(_config=sectioned_config)
        return vlan_obj

    def get_vlan(self):
        parser = Parser(self._result)
        sectioned_config = parser._add_bang_between_section()
        split_line = re.split("!", sectioned_config, flags=re.MULTILINE)
        vlan_list = []
        for i in split_line:
            vlan_info_obj = _VLAN()
            vlan_reg = re.search("^(vlan\s[0-9]+)", i.strip())
            no_vlan = re.search("^vlan\s[0-9]+,.*", i.strip())
            if not no_vlan and vlan_reg:
                vlan_segment = re.split("\n", i.strip())
                vlan_info_obj.vlan = vlan_segment[0]
                for seg in vlan_segment:
                    if "name" in seg:
                        vlan_info_obj.description = seg

                    if "vn-segment" in seg:
                        vlan_info_obj.vn = seg
                vlan_list.append(vlan_info_obj)
        return vlan_list

    def get_l3_int(self):
        parser = Parser(self._result)
        sectioned_config = parser._add_bang_between_section()
        split_line = re.split("!", sectioned_config, flags=re.MULTILINE)
        intf_obj_list = []
        for i in split_line:
            if i.strip().startswith("interface"):
                if "ip address" in i.strip():
                    intf_parent_child = _L3IntfParentChildren()
                    intf = re.split("\n", i.strip())
                    intf_parent_child.intf = intf[0]
                    for item in intf:
                        if "vrf member" in item.strip():

                            intf_parent_child.vrf = item
                        if "ip address" in item.strip():
                            intf_parent_child.ip = item

                        if "description" in item.strip():
                            intf_parent_child.description = item

                    intf_obj_list.append(intf_parent_child)

        return intf_obj_list


    def _get_router_segment(self):
        parser = Parser(self._result)
        split_on_bang = re.split("!", parser, flags=re.MULTILINE)
        bgp_string = ""
        for i in split_on_bang:
            if "router bgp" in i.strip():
                bgp_segment = re.split("\n", i)
                for seg in bgp_segment:
                    bgp_process = re.search("^router bgp(.*)", seg)
                    if bgp_process:
                        bgp_string += f"{bgp_process.group()}\n"
                    bgp_vrf = re.search("^\s{2}vrf\s(.*)", seg)
                    if bgp_vrf:
                        bgp_string += "!\n"
                        bgp_string += f"{bgp_vrf.group()}\n"

                    bgp_vrf_child = re.search("^\s{3}.*", seg)
                    if bgp_vrf_child:
                        bgp_string += f"{bgp_vrf_child.group()}\n"

        return bgp_string


    def get_routing_protocol(self):
        routing_segment = self._get_router_segment()
        routing_protocol = _RoutingProtocol(_vrf_segment=routing_segment)
        return routing_protocol


class Parser:
    def __init__(self, content):
        self.content = content

    def _add_bang_between_section(self):
        sectioned_content = ""
        splited_on_line = re.split("\n", self.content)
        for i in splited_on_line:
            parent_regex = re.search("^(\w+.*)", i)
            children_regex = re.search("^\s+(.*)$", i)

            if parent_regex:
                sectioned_content += "!\n"
                sectioned_content += f"{parent_regex.group()}\n"

            if children_regex:
                sectioned_content += f"{children_regex.group()}\n"

        return sectioned_content
