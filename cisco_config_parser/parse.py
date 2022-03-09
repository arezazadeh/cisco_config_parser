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

