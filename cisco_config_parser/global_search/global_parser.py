from .global_separator import GlobalSeparator
from dataclasses import dataclass
from cisco_config_parser.parser_regex.regex import *
from .global_obj import BannerObj, VLANObj





@dataclass
class GlobalParser:
    content: str = None

    def _fetch_banner(self, **kwargs):
        banner_obj = BannerObj()
        banner_lines = []
        split_line = self.content.splitlines()
        banner_found = False
        for line in split_line:
            strip_line = line.strip()
            if strip_line.startswith("banner"):
                banner_found = True
                banner_lines.append(strip_line)
            elif banner_found:
                if strip_line.startswith("^C"):
                    banner_found = False
                    banner_lines.append(strip_line)
                else:
                    banner_lines.append(strip_line)
        banner_obj.banner = banner_lines
        return banner_obj


    def _fetch_vlan_info(self, **kwargs):
        """
        Fetch the vlan information from the config file
        :return: list of vlan objects
        """
        global_separator = GlobalSeparator(self.content)
        vlan_sections = global_separator._find_vlan_section()
        vlan_objects = []
        for vlan_section in vlan_sections:
            vlan_obj = VLANObj()

            vlan_regex = VLAN_REGEX.search(vlan_section)
            if vlan_regex:
                vlan_obj.vlan = vlan_regex.group()

            vlan_obj.children = [
                line.strip() for line in vlan_section.splitlines()
                if line.strip() and not line.strip().startswith("vlan")
            ]
            vlan_objects.append(vlan_obj)

        return vlan_objects


