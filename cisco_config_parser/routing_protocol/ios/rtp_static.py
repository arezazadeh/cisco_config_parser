from dataclasses import dataclass
from cisco_config_parser.parser_regex.regex import *
from cisco_config_parser.routing_protocol.utils.rtp_separator import IOSRoutingProtocolSeparator
from cisco_config_parser.routing_protocol.ios.rtp_ios_rtp_obj import StaticRoute




@dataclass
class IOSStaticRouteConfig:
    """
    StaticRouteParser class to parse the static routes in the config file
    :param content: str
    :return: list of StaticRoute objects
    """
    content: str = None


    def _fetch_static_route_config(self, return_json=False):
        """
        Fetch the static routes from the config file
        :param return_json: bool
        return: list of StaticRoute objects
        """

        static_routes = IOSRoutingProtocolSeparator(self.content).find_static_routes()

        def _contains_admin_distance(static_rt_line):
            """
            Check if the static route has an admin distance
            :param static_rt_line: str
            :return: str
            """
            admin_distance = RTP_IOS_STATIC_AD_REGEX.search(static_rt_line)
            if admin_distance:
                return admin_distance.group(1).strip()
            return None

        def _contains_vrf(static_rt_line):
            """
            Check if the static route has a vrf
            :param static_rt_line: str
            :return: str
            """
            vrf = RTP_IOS_STATIC_VRF_REGEX.search(static_rt_line)
            if vrf:
                return vrf.group(1).strip()
            return None

        def _contains_name(static_rt_line):
            """
            Check if the static route has a name or description
            :param static_rt_line: str
            :return: str
            """
            name = RTP_IOS_STATIC_NAME_REGEX.search(static_rt_line)
            if name:
                return name.group(1).strip()
            return None

        def assign(static_route_list, obj):
            """
            Assign the values to the object
            :param static_route_list: list
            :param obj: StaticRoute object
            :return: StaticRoute object
            """
            obj.network = static_route_list[0].strip()
            obj.mask = static_route_list[1].strip()
            obj.nexthop_ip = static_route_list[2].strip()
            obj.subnet = get_subnet(obj.network, obj.mask)

            # check if the static route has an admin distance
            obj.admin_distance = _contains_admin_distance(static_route_line)
            obj.name = _contains_name(static_route_line)
            return obj

        static_route_objects = []

        for static_route_line in static_routes:
            static_route_obj = StaticRoute()

            # split the static route line into a list
            # ['vrf', 'grn200', '10.245.1.150', '255.255.255.255', '10.243.99.186', 'name', 'Lo202_STNHOV-11-CP-SA01']
            # ['10.245.1.150', '255.255.255.255', '10.243.99.186', 'name', 'Lo202_STNHOV-11-CP-SA01']
            static_route_config = static_route_line.split()[2:]

            # check if the static route has a vrf
            route_vrf = _contains_vrf(static_route_line)
            if route_vrf:
                static_route_obj.vrf = route_vrf

                # removing both vrf and vrf_name from the list to unify the order of items in the list
                static_route_config.remove("vrf")
                static_route_config.remove(route_vrf)
                static_route_obj = assign(static_route_config, static_route_obj)

            else:
                static_route_obj.vrf = "default"
                static_route_obj = assign(static_route_config, static_route_obj)

            static_route_objects.append(static_route_obj)

        if return_json:
            return [obj.__dict__ for obj in static_route_objects]

        return static_route_objects