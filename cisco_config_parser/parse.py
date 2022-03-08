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
        intf = ""
        description = ""
        ip_add = ""
        mask = ""
        subnet = ""
        vrf_member = ""
        state = ""
        helper_list = []
        split_line = re.split("\n", line.strip())
        
        for ent in split_line:
            if ent.strip().startswith("shutdown"):
                state = ent
                
            if ent.strip().startswith("interface "):
                intf = ent
                
            if ent.strip().startswith("description"):
                description = ent
                
            if ent.strip().startswith("ip address"):
                address = ent.split("ip address")[1]
                addr_mask = address.split()
                ip_add = addr_mask[0]
                mask = addr_mask[1]
                subnet = ipaddress.ip_network(f"{ip_add}/{mask}", strict=False)
                
            if ent.strip().startswith("ipv4 address"):
                address = ent.split("ipv4 address")[1]
                addr_mask = address.split()
                ip_add = addr_mask[0]
                mask = addr_mask[1]
                subnet = ipaddress.ip_network(f"{ip_add}/{mask}", strict=False)
                
            if ent.strip().startswith("ip helper-address"):
                helper_list.append(ent)
                
            if ent.strip().startswith("ip vrf for"):
                vrf_member = ent
                
            if ent.strip().startswith("vrf"):
                vrf_member = ent
                
            if ent.strip().startswith("vrf member"):
                vrf_member = ent
                
        if state == "":
            state = " no shutdown"
            
        obj_list.append(RoutedPort(intf,
                                   ip_add=ip_add,
                                   mask=mask,
                                   subnet=subnet,
                                   description=description,
                                   vrf=vrf_member,
                                   helper_list=helper_list,
                                   state=state
                                   )
                        )
    return obj_list


def parse_switch_port(port_list):
    obj_list = []
    switchport_interface_list = []
    for i in port_list:
        interface_parent = re.split("\n", i)
        for line in interface_parent:
            if "switchport" in line:
                switchport_interface_list.append(i)

    for line in switchport_interface_list:
        port = ""
        vlan = ""
        voice = ""
        description = ""
        mode = ""
        
        split_line = re.split("\n", line.strip())
        port = split_line[0]
        
        for i in split_line:
            if i.strip().startswith("shutdown"):
                state = i
                
            if "description" in i:
                description = i

            if "voice vlan" in i:
                voice_vlan_id = i.split("voice")[1]
                voice = f"Voice {voice_vlan_id}"

            if "switchport access vlan" in i:
                vlan_id = i.split("access vlan")[1]
                vlan = f"Vlan {vlan_id}"

            if "switchport access" in i:
                mode = "Access Port"
            if "switchport trunk" in i:
                mode = "Trunk Port"
        if state == "":
            state = " no shutdown"

        switchport_obj = SwitchPort(port,
                                    vlan=vlan,
                                    description=description,
                                    voice=voice,
                                    mode=mode,
                                    state=state
                                    )

        obj_list.append(switchport_obj)

    return obj_list


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
        intf = ""
        description = ""
        ip_add = ""
        vrf_member = ""
        state = ""
        helper_list = []
        
        line = re.split("\n", i.strip())
        
        for ent in line:
            if ent.strip().startswith("shutdown"):
                state = ent
                
            if ent.strip().startswith("interface Vlan"):
                intf = ent
                
            if ent.strip().startswith("description"):
                description = ent
                
            if ent.strip().startswith("ip address"):
                ip_add = ent
                
            if ent.strip().startswith("ip helper-address"):
                helper_list.append(ent)
                
            if ent.strip().startswith("ip vrf for"):
                vrf_member = ent
                
        if state == "":
            state = " no shutdown"
            
        intf_entity = IntObj(intf, ip_add, description, vrf_member, helper_list, state)
        obj_list.append(intf_entity)

    return obj_list
