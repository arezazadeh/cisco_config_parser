from cisco_config_parser.layer3_interface import L3InterfaceParser
from cisco_config_parser.layer2_interface import L2InterfaceParser
from cisco_config_parser.parent_child import ParentChildParser
from cisco_config_parser.global_search import GlobalParser
from cisco_config_parser.routing_protocol.ios.rtp_ospf import IOSOSPFConfig
from cisco_config_parser.routing_protocol.ios.rtp_eigtp import IOSEIGRPConfig
from cisco_config_parser.routing_protocol.ios.rtp_static import IOSStaticRouteConfig
from cisco_config_parser.routing_protocol.ios.rtp_bgp import IOSBGPConfig


from cisco_config_parser.parser_regex.regex import *


class Parser:
    def __init__(self, _content, platform=None):
        self._content = _content
        self._platform = platform
        self._l3_parser_obj = L3InterfaceParser(self._content)
        self._l2_parser_obj = L2InterfaceParser(self._content)
        self._parent_child_parser_obj = ParentChildParser(self._content)
        self._global_parser_obj = GlobalParser(self._content)



    def determine_platform(self, TARGET_CLASS):
        """
        Determine the platform of the device
        IOS, NXOS, IOSXR
        :return: string
        - IOS running_config will have "Current configuration : <digts> bytes" at the beginning
        - NXOS running_config will have "!Command: show running-config" at the beginning or we can look for "feature" keyword
        - IOSXR running_config will have "!! IOS XR Configuration 6.2.3" at the beginning or we can look for "prefix-set" or "route-policy" keyword
        """

        if IOS_PLATFORM_REGEX_1.search(self._content):
            return TARGET_CLASS

        elif NXOS_PLATFORM_REGEX_1.search(self._content) or NXOS_PLATFORM_REGEX_2.search(self._content):
            return "NXOS"

        elif XR_PLATFORM_REGEX_1.search(self._content) \
                or XR_PLATFORM_REGEX_2.search(self._content) \
                or XR_PLATFORM_REGEX_3.search(self._content):
            return "XR"

        raise ValueError("""
            ------------------------------------------------------------------------------------------------------
                                Not able to determine the platform of the device. 
            Please pass the platform='IOS' or platform='NXOS' or platform='XR' as an argument to the Parser class
            ------------------------------------------------------------------------------------------------------
            """)


    def _get_static_config(self, return_json=False):
        """
        Get the static routes from the config file
        :return: list of static route objects
        """
        if self._platform:
            """
            if user provides the platform, then use the platform to fetch the static routes
            """
            if "ios" in self._platform.lower():
                return IOSStaticRouteConfig(self._content)._fetch_static_route_config(return_json=return_json)

        """
        if platform is not provided, then use internal logic to determine the platform
        """
        relevant_object = self.determine_platform(IOSStaticRouteConfig)
        return relevant_object(self._content)._fetch_static_route_config(return_json=return_json)


    def _get_ospf_config(self, return_json=False):
        """
        Get the static routes from the config file
        :return: list of static route objects
        """
        if self._platform:
            """
            if user provides the platform, then use the platform to fetch the static routes
            """
            if "ios" in self._platform.lower():
                return IOSOSPFConfig(self._content)._fetch_ospf_config(return_json=return_json)

        """
        if platform is not provided, then use internal logic to determine the platform
        """
        relevant_object = self.determine_platform(IOSOSPFConfig)
        return relevant_object(self._content)._fetch_ospf_config(return_json=return_json)



    def _get_eigrp_config(self, return_json=False):
        """
        Get the static routes from the config file
        :return: list of static route objects
        """
        if self._platform:
            """
            if user provides the platform, then use the platform to fetch the static routes
            """
            if "ios" in self._platform.lower():
                return IOSEIGRPConfig(self._content)._fetch_eigrp_config(return_json=return_json)

        """
        if platform is not provided, then use internal logic to determine the platform
        """
        relevant_object = self.determine_platform(IOSEIGRPConfig)
        return relevant_object(self._content)._fetch_eigrp_config(return_json=return_json)


    def _get_bgp_config(self, return_json=False):
        """
        Get the static routes from the config file
        :return: list of static route objects
        """
        if self._platform:
            """
            if user provides the platform, then use the platform to fetch the static routes
            """
            if "ios" in self._platform.lower():
                return IOSBGPConfig(self._content)._fetch_bgp_config(return_json=return_json)

        """
        if platform is not provided, then use internal logic to determine the platform
        """
        relevant_object = self.determine_platform(IOSBGPConfig)
        return relevant_object(self._content)._fetch_bgp_config(return_json=return_json)




    def _get_vlan_info(self):
        """
        Get the vlan information from the config file
        :return: list of vlan objects
        """
        return self._global_parser_obj._fetch_vlan_info()


    def _get_banner(self):
        """
        Get the banner from the config file
        :return: banner object
        """
        return self._global_parser_obj._fetch_banner()

    def _get_parent_child(self, **kwargs):
        """
        Get parent child from the config file
        :return: list of parent child objects
        """
        return self._parent_child_parser_obj._fetch_parent_child(**kwargs)


    def _get_subnet_and_usage(self, include_subnet_count=False):
        """
        Fetch the subnet usage from the config file
        return: dictionary of subnet usage and subnet count
        """

        return self._l3_parser_obj._fetch_subnet_and_usage(include_subnet_count=include_subnet_count)


    def _get_l3_interfaces(self, **kwargs):
        """
        Get L3 interfaces from the config file
        :return: list of L3 interface objects
        """
        return self._l3_parser_obj._fetch_l3_interfaces(**kwargs)

    def _get_l3_interface_details(self):
        """
        Get the L3 interface details
        :return: dictionary of L3 interface details
        """
        l3_interfaces = self._get_l3_interfaces()

        if not l3_interfaces:
            return {}  # Return an empty dictionary if no interfaces are found

        return {interface.name: interface.children for interface in l3_interfaces}

    def _get_l2_access_interfaces(self, **kwargs):
        """
        Get L2 interfaces from the config file
        :return: list of L2 interface objects
        """
        return self._l2_parser_obj._fetch_l2_access_interfaces(**kwargs)

    def _get_l2_access_interface_details(self):
        """
        Get the L2 interface details
        :return: dictionary of L2 interface details
        """
        l2_access_interfaces = self._get_l2_access_interfaces()

        if not l2_access_interfaces:
            return {}

        return {interface.name: interface.children for interface in l2_access_interfaces}


    def _get_l2_trunk_interfaces(self, **kwargs):
        """
        Get L2 interfaces from the config file
        :return: list of L2 interface objects
        """
        return self._l2_parser_obj._fetch_l2_trunk_interfaces(**kwargs)

    def _get_l2_trunk_interface_details(self):
        """
        Get the L2 interface details
        :return: dictionary of L2 interface details
        """
        l2_trunk_interfaces = self._get_l2_trunk_interfaces()

        if not l2_trunk_interfaces:
            return {}

        return {interface.name: interface.children for interface in l2_trunk_interfaces}




