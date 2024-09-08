from cisco_config_parser.separator import Separator
from cisco_config_parser.parser_regex.regex import *


class L3InterfaceSeparator(Separator):
    def __init__(self, content):
        super().__init__(_content=content)

        self._add_bang_between_section()
        self._l3_interface_sections: list = []

    def _is_l3_interface_section(self, section):
        interface_regex = re.search(r"^interface", section, flags=re.MULTILINE)
        if interface_regex:
            l3_interface_regex = re.search(r"ip address", section, flags=re.MULTILINE)
            if l3_interface_regex:
                return True
            return False
        return False

    def _find_l3_interfaces(self):
        """
        Find all the L3 interfaces in the config file:
        1. split the config file into sections with "!" between each section
        2. forloop through each section and check if the section is a L3 interface section
        3. if the section is a L3 interface section, append it to the list
        4. return the list
        """
        for section in SPLIT_ON_BANG_MULTILINE.split(self._sections):
            if self._is_l3_interface_section(section):
                self._l3_interface_sections.append(section)

    def find_all_l3_interfaces(self):
        self._find_l3_interfaces()
        return self._l3_interface_sections
