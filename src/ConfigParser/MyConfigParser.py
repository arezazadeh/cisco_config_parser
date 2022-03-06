import re


class ParentObj:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child


class IntObj:
    def __init__(self, intf, ip_add, description, vrf, helper):
        self.intf = intf
        self.ip_add = ip_add
        self.description = description
        self.vrf = vrf
        self.helper = helper

    def __str__(self):
        return f"IntObj Class - {self.intf}"


class ConfigParser:
    """
    :Example: 
    - Finding Routing Protocol
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

    def __init__(self, file):
        self.file = file
        self.obj_list_1 = []
        self.obj_list_2 = []

    def find_parent_child(self, regex):
        """
        :param regex: parsing the file based on the input regex
        :return: List (obj_list)
        """
        with open(self.file, "r") as f:
            content = f.read()
            split_on_bang = re.split("^!$", content, flags=re.MULTILINE)

            for i in split_on_bang:
                regex_result = re.match(regex, i.strip())
                if regex_result:
                    if i.strip().startswith(regex_result.group()):
                        regex_parent_child = re.split("\n", i.strip())
                        parent = regex_parent_child[0]
                        regex_parent_child.pop(0)
                        child = regex_parent_child
                        self.obj_list_1.append(ParentObj(parent, child))

        return self.obj_list_1

    def get_svi_objects(self):
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

        with open(self.file, "r") as f:
            content = f.read()
            split_on_bang = re.split("^!$", content, flags=re.MULTILINE)
            for obj in split_on_bang:
                parent_obj = re.findall("^interface Vlan(.*)", obj, flags=re.MULTILINE)
                if parent_obj:
                    intf_vlan_list.append(obj)

        intf = ""
        description = ""
        ip_add = ""
        vrf_member = ""
        for i in intf_vlan_list:
            helper_list = []
            line = re.split("\n", i)
            for ent in line:
                if ent:
                    if ent.startswith("interface Vlan"):
                        intf = ent
                    if ent.startswith(" description"):
                        description = ent

                    if ent.startswith(" ip address"):
                        ip_add = ent

                    if ent.startswith(" ip helper-address"):
                        helper_list.append(ent)

                    if ent.startswith(" ip vrf for"):
                        vrf_member = ent

            intf_entity = IntObj(intf, ip_add, description, vrf_member, helper_list)
            self.obj_list_2.append(intf_entity)

        return self.obj_list_2


