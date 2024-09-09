import json

from .l3_interface_separator import L3InterfaceSeparator
from .l3_interface_obj import L3Interface
from .l3_section_parser import _L3SectionParser
from cisco_config_parser.parser_regex.regex import *
from dataclasses import dataclass
import re, ipaddress










@dataclass
class L3InterfaceParser:
    """
    L3InterfaceParser class to parse the L3 interfaces in the config file
    :param content: str
    :return: list of L3Interface objects
    """
    content: str = None


    def _fetch_l3_interfaces(self, **kwargs):
        """
        Fetch the L3 interfaces from the config file
        return: list of L3Interface objects
        """


        l3_intf = L3InterfaceSeparator(self.content)
        l3_interfaces = l3_intf.find_all_l3_interfaces()
        l3_intf_objects = []

        for l3_interface in l3_interfaces:

            # create an instance of the L3Interface class
            l3_intf_cls = L3Interface()

            # split the l3_interface section into lines
            # remove the first line which is the interface name
            # and store the rest of the lines in the children attribute of the l3_intf_cls object
            l3_intf_split_line = SPLIT_ON_LINE.split(l3_interface)
            l3_intf_cls.children = [
                line.strip() for line in l3_intf_split_line
                if line and not line.startswith("interface")
            ]

            # search for the regex in the l3_interface section
            interface_regex = INTERFACE_MULTILINE_REGEX.search(l3_interface)
            description_regex = DESCRIPTION_REGEX.search(l3_interface)
            ip_address_regex = IP_ADDRESS_REGEX.search(l3_interface)
            vrf_regex = VRF_REGEX.search(l3_interface)
            helper_address_regex = HELPER_ADDRESS_REGEX.search(l3_interface)
            sec_ip_address_regex = SECONDARY_IP_ADDRESS_REGEX.search(l3_interface)


            # if the regex is found, parse the line and store the value in the l3_intf_cls object
            ip_address_kwargs = {
                "ip_address_line_regex": ip_address_regex,
                "l3_interface_obj": l3_intf_cls,
                "primary": True
            }

            if ip_address_regex:
                l3_intf_cls = _L3SectionParser._parse_ip_address_line(**ip_address_kwargs)


            if sec_ip_address_regex:
                # set the primary flag to False to indicate that the ip address is a secondary ip address
                ip_address_kwargs["primary"] = False
                l3_intf_cls = _L3SectionParser._parse_ip_address_line(**ip_address_kwargs)

            if vrf_regex:
                l3_intf_cls = _L3SectionParser._parse_vrf_line(vrf_line_regex=vrf_regex, l3_interface_obj=l3_intf_cls)

            if helper_address_regex:
                l3_intf_cls = _L3SectionParser._parse_helper_address_line(l3_interface_obj=l3_intf_cls, section=l3_interface)

            if interface_regex:
                l3_intf_cls.name = interface_regex.group(1).strip()

            if description_regex:
                l3_intf_cls.description = description_regex.group(1).strip()


            # if there are custom kwargs, search for the custom regex in the l3_interface section
            # if the regex is found, parse the line and store the value in the l3_intf_cls object
            if kwargs:
                for k, v in kwargs.items():
                    custom_field_regex = re.search(v, l3_interface, flags=re.MULTILINE)
                    custom_regex_kwargs = {
                        "custom_field_name": k,
                        "custom_field_regex": custom_field_regex,
                        "l3_interface_obj": l3_intf_cls
                    }
                    l3_intf_cls = _L3SectionParser._parse_custom_regex(**custom_regex_kwargs)


            # append the l3_intf_cls object to the l3_intf_objects list
            l3_intf_objects.append(l3_intf_cls)

        return l3_intf_objects


    def _fetch_subnet_and_usage(self, include_subnet_count=False):
        """
        Fetch the subnet usage from the config file
        return: dictionary of subnet usage
        """

        subnet_usage = {}
        subnet_count = {}
        l3_interfaces = self._fetch_l3_interfaces()
        for i in l3_interfaces:
            if i.subnet:
                cidr = str(ipaddress.IPv4Network(i.subnet, strict=False).prefixlen)
                subnet_usage[i.name] = i.subnet
                if subnet_count.get(f"/{cidr}"):
                    subnet_count[f"/{cidr}"] += 1
                else:
                    subnet_count[f"/{cidr}"] = 1

        if include_subnet_count:
            subnet_usage["subnet_count"] = subnet_count

        return subnet_usage

