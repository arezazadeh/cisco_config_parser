from cisco_config_parser.separator import Separator
from cisco_config_parser.parser_regex import *




class NXOSRoutingProtocolSeparator(Separator):

    def __init__(self, content):
        """
        IOSRoutingProtocolSeparator class
        :param content: content of the config file
        :return: list of selected section
        """

        super().__init__(_content=content)

        self._add_bang_between_section()
        self._routing_protocol_sections: list = []


    def _is_routing_protocol_section(self, section):
        """
        Check if the section is a routing protocol section
        :param section: section of the config file
        :return: True if the section is a dynamic or static routing protocol section, False otherwise
        """
        dynamic_routing_protocol_regex = RTP_NXOS_REGEX.search(section)
        global_static_routing_protocol_regex = RTP_NXOS_GLOBAL_STATIC_ROUTE_REGEX.search(section)
        vrf_static_routing_protocol_regex = RTP_NXOS_VRF_STATIC_ROUTE_REGEX.search(section)
        if any([dynamic_routing_protocol_regex, global_static_routing_protocol_regex, vrf_static_routing_protocol_regex]):
            return True
        return False



    def _is_static_route_section(self, section):
        static_route_regex = RTP_NXOS_STATIC_ROUTE_REGEX.search(section)
        if static_route_regex:
            return True
        return False


    def _find_routing_protocol_section(self):
        """
        Find the routing protocol section
        :return: list of routing protocol section
        """
        split_on_bang = SPLIT_ON_BANG_MULTILINE.split(self._sections)
        for section in split_on_bang:
            if self._is_routing_protocol_section(section):
                self._routing_protocol_sections.append(section)

        return self._routing_protocol_sections

    def find_static_route_section(self):
        """
        Find the global static route section
        :return: list of global static route section
        """
        global_static_routes = []
        routing_protocol_sections = self._find_routing_protocol_section()
        for rtp_section in routing_protocol_sections:
            if self._is_static_route_section(rtp_section):
                global_static_routes.append(rtp_section)
        return global_static_routes


