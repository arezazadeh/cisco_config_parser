from cisco_config_parser.separator import Separator
from cisco_config_parser.parser_regex.regex import *




class GlobalSeparator(Separator):
    def __init__(self, content):
        super().__init__(_content=content)

        self._add_bang_between_section()
        self._global_sections: list = []

    def _get_split_sections(self):
        """
        Get the split sections
        :return: list
        """
        return self._sections.split("!")


    def _find_vlan_section(self):
        """
        Find the vlan section in the config file
        :return: list
        """
        vlan_sections = []
        for section in self._get_split_sections():

            # lower the section since sometimes IOS has the first letter of the vlan in uppercase
            if VLAN_REGEX.search(section.lower()):
                vlan_sections.append(section)

        return vlan_sections

