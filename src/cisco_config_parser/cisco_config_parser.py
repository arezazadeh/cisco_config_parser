import re
import ipaddress
from .obj import *
from .exceptions import *
from .ssh import *


class ConfigParser:
    """
    - Example: Finding Routing Protocol
    my_file = "stnhlv-21-sa01_running_config.txt"

    parse = ConfigParser(my_file)

    obj_list = parse.find_parent_child("^router")

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

    def __init__(self, *kwargs):
        """
        :param file: text file with .txt extension
        :param kwargs:
        file:Text File with .txt extension
        ssh:bool => default False
        host:str => default None
        user:str => default None
        password:str => default None
        device_type:str => default cisco_ios (cisco_ios, cisco_xe, cisco_xr)
        """
        
        self.file = kwargs.get("file") or None
        self.ssh = kwargs.get("ssh") or False
        self.host = kwargs.get("host") or None
        self.user = kwargs.get("user") or None
        self.password = kwargs.get("password") or None
        self.device_type = kwargs.get("device_type") or "cisco_ios"
        
        if self.ssh:
            self.ssh_to = MySSH(self.host, self.user, self.password, self.device_type)

        if self.file:
            if not self.file.endswith(".txt"):
                raise FileReadError(self.file)


    def read_file(self):
        with open(self.file, "r") as f:
            content = f.read()
            return content

    def split_content(self, content, regex):
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


    def find_parent_child(self, regex):
        """
        :param regex: parsing the file based on the input regex
        :return: List (obj_list)
        """
        if self.ssh:
            content = self.ssh_to.ssh("show running-config")
            self.ssh_to.ssh_conn.disconnect()
            obj_list = self.split_content(content, regex)
            return obj_list
        else:
            content = self.read_file()
            obj_list = self.split_content(content, regex)
            return obj_list

    def get_interface(self):
        port_list = []

        content = self.read_file()
        
        split_on_bang = re.split("^!$", content, flags=re.MULTILINE)
        for obj in split_on_bang:
            parent_obj = re.findall("^interface\s+(.*)", obj, flags=re.MULTILINE)
            if parent_obj:
                port_list.append(obj)

        return port_list

    def get_switchport(self):
        obj_list = []
        switchport_interface_list = []
        port_list = self.get_interface()

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

            obj_list.append(SwitchPort(port, 
                                       vlan=vlan, 
                                       description=description, 
                                       voice=voice, 
                                       mode=mode
                                       )
                            )

        return obj_list

    def get_routed_port(self):
        obj_list = []
        port_list = self.get_interface()
        routed_port_list = []
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
                    
                if ent.strip().startswith(" ip address"):
                    address = ent.split("ip address")[1]
                    addr_mask = address.split()
                    ip_add = addr_mask[0]
                    mask = addr_mask[1]
                    subnet = ipaddress.ip_network(f"{ip_add}/{mask}", strict=False)

                if ent.strip().startswith(" ipv4 address"):
                    address = ent.split("ipv4 address")[1]
                    addr_mask = address.split()
                    ip_add = addr_mask[0]
                    mask = addr_mask[1]
                    subnet = ipaddress.ip_network(f"{ip_add}/{mask}", strict=False)
                
                if ent.strip().startswith("ip helper-address"):
                    helper_list.append(ent)
                    
                if ent.strip().startswith("ip vrf for"):
                    vrf_member = ent
                    
                if ent.strip().startswith("vrf member"):
                    vrf_member = ent
                
                if ent.strip().startswith("vrf"):
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

    def get_svi_objects(self):
        obj_list = []
        """
        :return: list of "obj_list" where you can forloop over and use IntObj methods to access the values

        :example:
        file = "switch_01-run_config.txt"

        obj = get_int_obj(file)
        for i in obj:
            if "lan200" in i.intf:
                print(i.intf)
                print(i.ip_add)
                print(i.vrf)
                print(i.description)
                print(i.helper)

        """
        intf_vlan_list = []

        content = self.read_file()
        
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


