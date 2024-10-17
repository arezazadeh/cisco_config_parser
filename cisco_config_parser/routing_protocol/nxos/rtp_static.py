from .rtp_nxos_rtp_obj import StaticRoute
from cisco_config_parser.parser_regex import *
from dataclasses import dataclass
from cisco_config_parser.routing_protocol.utils import *
from cisco_config_parser.routing_protocol.utils.rtp_nxos_separator import NXOSRoutingProtocolSeparator

@dataclass
class NXOSStaticRouteConfig:
    content: str = None


    def _rewrite_static_route_section(self, section):
        """
        Rewrite static route section
        :param section: section of the config file
        :return: str
        """
        cleaned_section = [line.strip() for line in section.split("\n") if line.strip()]
        return "\n".join(cleaned_section)


    def _process_static_route_alone(self, section):
        """
        Process static route alone
        :param section: section of the config file
        :return: dict
        """
        cleaned_section = self._rewrite_static_route_section(section)
        result = RTP_NXOS_STATIC_REGEX.findall(cleaned_section)
        print(result)



    def _process_static_route(self, section, obj):
        """
        Description:
            the global static routes come to this function one line at a time
        """
        static_alone = RTP_NXOS_STATIC_REGEX.findall(section)
        static_with_name = RTP_NXOS_STATIC_NAME_REGEX.findall(section)
        static_with_ad = RTP_NXOS_STATIC_AD_REGEX.findall(section)
        static_with_name_ad = RTP_NXOS_STATIC_NAME_AD_REGEX.findall(section)
        print(static_alone)
        print(static_with_name)
        print(static_with_ad)
        print(static_with_name_ad)

        pass



    def _fetch_static_route_config(self, return_json=False):
        """
        Fetch static route configuration
        :param return_json: return the output in json format
        :return: str or dict
        """

        static_route_obj_list = []
        static_route_sections = NXOSRoutingProtocolSeparator(self.content).find_static_route_section()

        global_routes = []
        for section in static_route_sections:
            static_route_obj = StaticRoute()

            # Process Global Static Route
            if RTP_NXOS_GLOBAL_STATIC_ROUTE_REGEX.findall(section):

                # some global static route might have vrf in them,
                # so we will ignore them while processing global static route
                # and process them in vrf context
                if "vrf" not in section:
                    global_routes.append(section)

        global_results = self._process_static_route(
            "\n".join(global_routes), static_route_obj
        )


            # # Process VRF Static Route
            # elif RTP_NXOS_VRF_CONTEXT_REGEX.search(section):
            #     static_route_obj = self._process_static_route(section, static_route_obj)
            #     static_route_obj.vrf = RTP_NXOS_VRF_CONTEXT_REGEX.search(section).group(1)
            #     static_route_obj_list.append(static_route_obj)

        if return_json:
            return [obj.__dict__.copy() for obj in static_route_obj_list]

        return static_route_obj_list


