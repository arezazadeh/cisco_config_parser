from .exceptions import *
from .ssh import *
from .parse import *


class ConfigParser:
    """
    - Example: Finding Routing Protocol
    my_file = "switch01_running_config.txt"

    parse = ConfigParser(method="file", content=my_file)

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
        self.platform = kwargs.get("platform") or "ios"
        
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

    def find_parent_child(self, **kwargs):
        """
        :param regex: parsing the file based on the input regex
        :return: List (obj_list)
        """
        regex = kwargs.get("regex")
        if self.method == "int_ssh":
            if self.platform == "nxos":
                if self.ssh:
                    content = self.ssh_to.ssh("show running-config")
                    self.ssh_to.ssh_conn.disconnect()
                    obj = GetParent(content)
                    return obj
            else:
                if self.ssh:
                    content = self.ssh_to.ssh("show running-config")
                    self.ssh_to.ssh_conn.disconnect()
                    obj_list = split_content(content, regex)
                    return obj_list

        elif self.method == "file":
            if self.platform == "nxos":
                content = self._read_file()
                obj = GetParent(content)
                return obj
            content = self._read_file()
            obj_list = split_content(content, regex)
            return obj_list

        elif self.method == "ext_ssh":
            if self.platform == "nxos":
                obj = GetParent(self.content)
                return obj
            obj_list = split_content(self.content, regex)
            return obj_list

    def get_switchport(self, **kwargs):
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
            if self.platform == "nxos":
                content = self._read_file()
                obj_list = GetParent(content)
            content = self._read_file()
            port_list = get_interface(content)
            if len(port_list) > 0:
                obj_list = parse_switch_port(port_list, mode)
                return obj_list

        elif self.method == "ext_ssh":
            port_list = get_interface(self.content)
            obj_list = parse_switch_port(port_list, mode)
            return obj_list

    def get_routed_port(self):

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

    def get_svi_objects(self):

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

