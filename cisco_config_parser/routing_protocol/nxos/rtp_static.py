from .rtp_nxos_rtp_obj import StaticRoute
from cisco_config_parser.parser_regex import *
from dataclasses import dataclass
from cisco_config_parser.routing_protocol.utils.rtp_nxos_separator import NXOSRoutingProtocolSeparator

@dataclass
class NXOSStaticRouteConfig:
    content: str = None


    def _process_global_static_route(self, section, obj):
        """
        Process global static route
        :param section: section of the config file
        :param obj: object to store the data
        :return: None
        """
        static_route_with_name = RTP_NXOS_STATIC_W_NAME_REGEX.search(section)
        static_route_with_name_and_ad = RTP_NXOS_STATIC_W_NAME_AD_REGEX.search(section)
        static_route = RTP_NXOS_STATIC_WO_NAME_REGEX.search(section)
        print(section)
        if static_route_with_name:
            obj.network = static_route_with_name.group(1)
            obj.mask = static_route_with_name.group(2)
            obj.name = static_route_with_name.group(3)
        if static_route:
            print("no name")
            print(static_route.groups())
            obj.network = static_route.group(1)
            obj.mask = static_route.group(2)




    def _fetch_static_route_config(self, return_json=False):
        """
        Fetch static route configuration
        :param return_json: return the output in json format
        :return: str or dict
        """

        static_route_obj_list = []
        static_route_sections = NXOSRoutingProtocolSeparator(self.content).find_static_route_section()
        for section in static_route_sections:
            static_route_obj = StaticRoute()
            if RTP_NXOS_GLOBAL_STATIC_ROUTE_REGEX.search(section):
                static_route_obj = self._process_global_static_route(section, static_route_obj)


