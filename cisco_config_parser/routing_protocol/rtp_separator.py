from cisco_config_parser.separator import Separator
from cisco_config_parser.parser_regex.regex import *







class IOSRoutingProtocolSeparator(Separator):
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
        dynamic_routing_protocol_regex = RTP_REGEX.search(section)
        static_routing_protocol_regex = RTP_IOS_STATIC_REGEX.search(section)

        if dynamic_routing_protocol_regex or static_routing_protocol_regex:
            return True
        return False

    def _is_static_route_section(self, section):
        static_route_regex = RTP_IOS_STATIC_REGEX.search(section)
        if static_route_regex:
            return True
        return False

    def _is_ospf_section(self, section):
        ospf_section_regex = RTP_IOS_OSPF_REGEX.search(section)
        if ospf_section_regex:
            return True
        return False

    def _is_eigrp_section(self, section):
        eigrp_section_regex = RTP_EIGRP_REGEX.search(section)
        if eigrp_section_regex:
            return True
        return False

    def _is_isis_section(self, section):
        isis_section_regex = RTP_ISIS_REGEX.search(section)
        if isis_section_regex:
            return True
        return False

    def _is_rip_section(self, section):
        rip_section_regex = RTP_RIP_REGEX.search(section)
        if rip_section_regex:
            return True
        return False

    def _is_bgp_section(self, section):
        bgp_section_regex = RTP_BGP_REGEX.search(section)
        if bgp_section_regex:
            return True
        return False

    def _find_routing_protocols(self):
        """
        Find all the routing protocols in the config file:
        1. split the config file into sections with "!" between each section
        2. forloop through each section and check if the section is a routing protocol section
        3. if the section is a routing protocol section, append it to the list
        4. return the list
        """
        for section in SPLIT_ON_BANG_MULTILINE.split(self._sections):
            if self._is_routing_protocol_section(section):
                self._routing_protocol_sections.append(section)

    def find_static_routes(self):
        """
        Find all the static routes in the config file
        :return: list of static routes
        """
        self.find_all_routing_protocols()
        static_routes_section = []
        for i in self._routing_protocol_sections:
            if self._is_static_route_section(i):
                static_routes_section.append(i)

        return static_routes_section


    def find_ospf_config(self):
        """
        Find all the OSPF configurations in the config file
        :return: list of OSPF configurations
        """
        self.find_all_routing_protocols()
        ospf_section = []
        for i in self._routing_protocol_sections:
            if self._is_ospf_section(i):
                ospf_section.append(i)

        return ospf_section


    def find_eigrp_config(self):
        """
        Find all the EIGRP configurations in the config file
        :return: list of EIGRP configurations
        """
        self.find_all_routing_protocols()
        eigrp_section = []
        for i in self._routing_protocol_sections:
            if self._is_eigrp_section(i):
                eigrp_section.append(i)

        return eigrp_section


    def find_bgp_config(self):
        """
        Find all the BGP configurations in the config file
        :return: list of BGP configurations
        """
        self.find_all_routing_protocols()
        bgp_section = []
        for i in self._routing_protocol_sections:
            if self._is_bgp_section(i):
                bgp_section.append(i)

        return bgp_section


    def find_all_routing_protocols(self):
        self._find_routing_protocols()
        return self._routing_protocol_sections

