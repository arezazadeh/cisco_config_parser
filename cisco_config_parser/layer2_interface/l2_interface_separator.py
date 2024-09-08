from cisco_config_parser.separator import Separator
from cisco_config_parser.parser_regex.regex import *


class L2InterfaceSeparator(Separator):
    def __init__(self, content):
        super().__init__(_content=content)

        self._add_bang_between_section()
        self._l2_interface_sections: list = []

    def _is_l2_interface_section(self, section):
        """
        Check if the section is an L2 interface section
        :param section: str
        :return: bool
        """
        interface_regex = INTERFACE_REGEX.search(section)
        if interface_regex:
            l2_interface_regex = SWITCHPORT_REGEX.search(section)
            if l2_interface_regex:
                return True
            return False
        return False

    def _is_access_interface_section(self, section):
        """
        Check if the section is an access interface section
        :param section: str
        :return: bool
        """
        access_interface_regex = SWITCHPORT_ACCESS_REGEX.search(section)
        if access_interface_regex:
            return True
        return False

    def _is_trunk_interface_section(self, section):
        """
        Check if the section is a trunk interface section
        :param section: str
        :return: bool
        """
        trunk_interface_regex = SWITCHPORT_TRUNK_REGEX.search(section)
        if trunk_interface_regex:
            return True
        return False

    def _find_l2_interfaces(self):
        """
        Find all the L2 interfaces in the config file:
        1. split the config file into sections with "!" between each section
        2. forloop through each section and check if the section is a L2 interface section
        3. if the section is a L2 interface section, append it to the list
        4. return the list
        """
        for section in SPLIT_ON_BANG_MULTILINE.split(self._sections):
            if self._is_l2_interface_section(section):
                self._l2_interface_sections.append(section)

    def find_all_l2_interfaces(self):
        """
        Find all the L2 interfaces in the config file
        :return: list of L2 interfaces
        """
        self._find_l2_interfaces()
        return self._l2_interface_sections

    def find_all_access_interfaces(self):
        """
        Find all the access interfaces in the config file
        :return: list of access interfaces
        """
        all_l2_interfaces = self.find_all_l2_interfaces()
        access_interfaces = []
        for l2_interface in all_l2_interfaces:
            if self._is_access_interface_section(l2_interface):
                access_interfaces.append(l2_interface)
        return access_interfaces

    def find_all_trunk_interfaces(self):
        """
        Find all the trunk interfaces in the config file
        :return: list of trunk interfaces
        """
        all_l2_interfaces = self.find_all_l2_interfaces()
        trunk_interfaces = []
        for l2_interface in all_l2_interfaces:
            if self._is_trunk_interface_section(l2_interface):
                trunk_interfaces.append(l2_interface)
        return trunk_interfaces

