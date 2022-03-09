from .exceptions import *
from .ssh import *
from .parse import *


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

    def __init__(self, **kwargs):
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

        self.obj_list_2 = []
        self.ssh = kwargs.get("ssh") or False
        self.host = kwargs.get("host") or None
        self.user = kwargs.get("user") or None
        self.password = kwargs.get("password") or None
        self.device_type = kwargs.get("device_type") or "cisco_ios"

        if self.ssh:
            try:
                self.ssh_to = MySSH(self.host, self.user, self.password, self.device_type)
            except Exception:
                raise SSHError(self.host)

        if self.file:
            if not self.file.endswith(".txt"):
                raise FileReadError(self.file)

    def _read_file(self):
        with open(self.file, "r") as f:
            content = f.read()
            return content

    def find_parent_child(self, regex):
        """
        :param regex: parsing the file based on the input regex
        :return: List (obj_list)
        """
        if self.ssh:
            content = self.ssh_to.ssh("show running-config")
            self.ssh_to.ssh_conn.disconnect()
            obj_list = split_content(content, regex)
            return obj_list
        else:
            content = self.read_file()
            obj_list = split_content(content, regex)
            return obj_list

    def get_switchport(self, **kwargs):
        
        mode = kwargs.get("mode")
        
        if self.ssh:
            content = self.ssh_to.ssh("show running-config")
            port_list = get_interface(content)
            if len(port_list) > 0:
                obj_list = parse_switch_port(port_list, mode)
                return obj_list
        
        else:
            content = self.read_file()
            port_list = get_interface(content)

            if len(port_list) > 0:
                obj_list = parse_switch_port(port_list, mode)
                return obj_list

    def get_routed_port(self):
        if self.ssh:
            content = self.ssh_to.ssh("show running-config")
            port_list = get_interface(content)
            if len(port_list) > 0:
                obj_list = parse_routed_port(port_list)
                return obj_list
        else:
            content = self.read_file()
            port_list = get_interface(content)

            if len(port_list) > 0:
                obj_list = parse_routed_port(port_list)
                return obj_list

    def get_svi_objects(self):
        if self.ssh:
            content = self.ssh_to.ssh("show running-config")
            obj_list = get_svi(content)
            if len(obj_list) > 0:
                return obj_list
        else:
            content = self.read_file()
            obj_list = get_svi(content)
            if len(obj_list) > 0:
                return obj_list



