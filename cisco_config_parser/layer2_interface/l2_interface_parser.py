from .l2_interface_separator import L2InterfaceSeparator
from .l2_interface_obj import L2TrunkInterface, L2AccessInterface
from .l2_section_parser import _L2AccessSectionParser, _L2TrunkSectionParser
from cisco_config_parser.parser_regex.regex import *
from dataclasses import dataclass








@dataclass
class L2InterfaceParser:
    """
    L2InterfaceParser class to parse the L2 interfaces in the config file
    :param content: str
    :return: list of L2Interface objects
    """
    content: str = None


    def _fetch_l2_access_interfaces(self, **kwargs):
        """
        Fetch the L2 interfaces from the config file
        return: list of L2AccessInterface objects
        """
        l2_intf = L2InterfaceSeparator(self.content)
        l2_access_interfaces = l2_intf.find_all_access_interfaces()

        l2_access_intf_objects = []

        for l2_access_interface in l2_access_interfaces:

            # create an instance of the L2Interface class
            l2_access_intf_cls = L2AccessInterface()

            # split the l2_interface section into lines
            # remove the first line which is the interface name
            # and store the rest of the lines in the children attribute of the l2_intf_cls object
            l2_intf_split_line = SPLIT_ON_LINE.split(l2_access_interface)
            l2_access_intf_cls.children = [
                line.strip() for line in l2_intf_split_line
                if line and not line.startswith("interface")
            ]
            
            # search for the regex in the l2_interface section
            interface_regex = INTERFACE_MULTILINE_REGEX.search(l2_access_interface)
            description_regex = DESCRIPTION_REGEX.search(l2_access_interface)
            data_vlan = SWITCHPORT_ACCESS_VLAN_REGEX.search(l2_access_interface)
            voice_vlan = SWITCHPORT_VOICE_VLAN_REGEX.search(l2_access_interface)
            native_vlan = SWITCHPORT_TRUNK_NATIVE_VLAN_REGEX.search(l2_access_interface)
            allowed_vlan = SWITCHPORT_TRUNK_ALLOWED_VLAN_REGEX.search(l2_access_interface)

            if interface_regex:
                l2_access_intf_cls.name = interface_regex.group(1)

            if description_regex:
                l2_access_intf_cls.description = description_regex.group(1)

            if data_vlan:
                l2_access_intf_cls.data_vlan = data_vlan.group(1)

            if voice_vlan:
                l2_access_intf_cls.voice_vlan = voice_vlan.group(1)

            if native_vlan:
                l2_access_intf_cls.native_vlan = native_vlan.group(1)

            if allowed_vlan:
                l2_access_intf_cls.allowed_vlan = allowed_vlan.group(1)

            # if there are custom kwargs, search for the custom regex in the l2_access_interface section
            # if the regex is found, parse the line and store the value in the l2_access_intf_cls object
            if kwargs:
                for k, v in kwargs.items():
                    custom_field_regex = re.search(v, l2_access_interface, flags=re.MULTILINE)
                    custom_regex_kwargs = {
                        "custom_field_name": k,
                        "custom_field_regex": custom_field_regex,
                        "l2_access_interface_obj": l2_access_intf_cls
                    }
                    l2_access_intf_cls = _L2AccessSectionParser._parse_custom_regex(**custom_regex_kwargs)

            l2_access_intf_objects.append(l2_access_intf_cls)

        return l2_access_intf_objects

    def _fetch_l2_trunk_interfaces(self, **kwargs):
        """
        Fetch the L2 interfaces from the config file
        return: list of L2TrunkInterface objects
        """

        l2_intf = L2InterfaceSeparator(self.content)
        l2_trunk_interfaces = l2_intf.find_all_trunk_interfaces()
        l2_trunk_intf_objects = []

        for l2_trunk_interface in l2_trunk_interfaces:

            # create an instance of the L2Interface class
            l2_trunk_intf_cls = L2TrunkInterface()

            # split the l2_interface section into lines
            # remove the first line which is the interface name
            # and store the rest of the lines in the children attribute of the l2_intf_cls object
            l2_intf_split_line = SPLIT_ON_LINE.split(l2_trunk_interface)
            l2_trunk_intf_cls.children = [
                line.strip() for line in l2_intf_split_line
                if line and not line.startswith("interface")
            ]

            # search for the regex in the l2_interface section
            interface_regex = INTERFACE_MULTILINE_REGEX.search(l2_trunk_interface)

            # search for description in the l2_interface section
            description_regex = DESCRIPTION_REGEX.search(l2_trunk_interface)

            # search for allowed vlan in the l2_interface section
            allowed_vlan_regex = TRUNK_ALLOWED_VLAN_REGEX.search(l2_trunk_interface)

            # search for native vlan in the l2_interface section
            native_vlan_regex = TRUNK_NATIVE_VLAN_REGEX.search(l2_trunk_interface)

            # search for dhcp relay in the l2_interface section
            dhcp_relay_regex = SWITCHPORT_TRUNK_DHCP_RELAY_REGEX.search(l2_trunk_interface)

            # search for snooping in the l2_interface section
            snooping_regex = SWITCHPORT_TRUNK_SNOOPING_REGEX.search(l2_trunk_interface)

            if interface_regex:
                l2_trunk_intf_cls.name = interface_regex.group(1)

            if description_regex:
                l2_trunk_intf_cls.description = description_regex.group(1)

            if allowed_vlan_regex:
                l2_trunk_intf_cls.allowed_vlan = allowed_vlan_regex.group(1)

            if native_vlan_regex:
                l2_trunk_intf_cls.native_vlan = native_vlan_regex.group(1)

            if dhcp_relay_regex:
                l2_trunk_intf_cls.dhcp_relay = dhcp_relay_regex.group(1)

            if snooping_regex:
                l2_trunk_intf_cls.snooping = snooping_regex.group(1)

            # if there are custom kwargs, search for the custom regex in the l2_access_interface section
            # if the regex is found, parse the line and store the value in the l2_access_intf_cls object
            if kwargs:
                for k, v in kwargs.items():
                    custom_field_regex = re.search(v, l2_trunk_interface, flags=re.MULTILINE)
                    custom_regex_kwargs = {
                        "custom_field_name": k,
                        "custom_field_regex": custom_field_regex,
                        "l2_trunk_interface_obj": l2_trunk_intf_cls
                    }
                    l2_trunk_intf_cls = _L2TrunkSectionParser._parse_custom_regex(**custom_regex_kwargs)

            l2_trunk_intf_objects.append(l2_trunk_intf_cls)

        return l2_trunk_intf_objects






