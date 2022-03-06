import re

class ParentObj:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child


class ConfigParser:

    def __init__(self, file):
        self.file = file
        self.obj_list = []

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
                        self.obj_list.append(ParentObj(parent, child))

        return self.obj_list


