from cisco_config_parser.routing_protocol.rtp_separator import IOSRoutingProtocolSeparator
from cisco_config_parser.routing_protocol.rtp_ios_obj import (
    StaticRoute,
    OSPFConfig,
    EIGRPConfig,
    EIGRPVrfChildren,
)
from cisco_config_parser.parser_regex.regex import *
from dataclasses import dataclass
from cisco_config_parser.layer3_interface import L3InterfaceParser
import ipaddress



class NotImplementedError(Exception):
    pass



@dataclass
class IOSRouteParser:
    """
    StaticRouteParser class to parse the static routes in the config file
    :param content: str
    :return: list of StaticRoute objects
    """
    content: str = None


    def _get_subnet(self, network, mask):
        """
        Get the subnet from the network and mask
        :param network: str
        :param mask: str
        :return: str
        """
        return str(ipaddress.ip_network((network, mask), strict=False))


    def _convert_wildcard_to_mask(self, wildcard_mask):
        """
        Convert the wildcard mask to a subnet mask
        :param wildcard_mask: str
        :return: str
        """
        wildcard_mask = wildcard_mask.split(".")
        wildcard_mask = [str(255 - int(i)) for i in wildcard_mask]
        return ".".join(wildcard_mask)

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
            obj.subnet = self._get_subnet(obj.network, obj.mask)

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

    def _fetch_ospf_config(self, return_json=False):
        """
        Fetch the OSPF configuration from the config file
        :param return_json: bool
        :return: list of OSPFConfig objects
        """

        ospf_config_section = IOSRoutingProtocolSeparator(self.content).find_ospf_config()

        def process_network_statements(ospf_section, net_list):
            """
            Process the network statements in the OSPF section
            Splits the line and extracts the network, wildcard mask and area
            It will then convert the wildcard mask to a subnet mask and append it to the list
            :param ospf_section: list
            :param net_list: list
            :return: list of dictionaries
            """
            ospf_process_section = SPLIT_ON_LINE_MULTILINE.split(ospf_section)
            for line in ospf_process_section:
                network_line_regex = RTP_IOS_OSPF_NETWORK_REGEX.search(line)
                if network_line_regex:
                    network_statement = network_line_regex.group().strip()
                    network_statement = network_statement.replace("network", "")
                    network_statement = network_statement.replace("area", "")
                    network_statement = network_statement.split()
                    if len(network_statement) == 3:
                        network = network_statement[0]
                        wildcard_mask = network_statement[1]
                        subnet_mask = self._convert_wildcard_to_mask(wildcard_mask)
                        area = network_statement[2]
                        net_list.append({
                            "network": network,
                            "subnet_mask": subnet_mask,
                            "wildcard_mask": wildcard_mask,
                            "area": area
                        })
            return net_list

        def process_no_passive_interface(ospf_process_section, no_passive_list):
            """
            Process the no passive interface statements in the OSPF section
            :param ospf_process_section: list
            :param no_passive_list: list
            :return: list of passive interfaces
            """
            ospf_process_section = SPLIT_ON_LINE_MULTILINE.split(ospf_process_section)
            for line in ospf_process_section:
                passive_interface = RTP_IOS_OSPF_NO_PASSIVE_INTERFACE_REGEX.search(line)
                if passive_interface:
                    no_passive_list.append({
                        "interface": passive_interface.group(1).strip()
                    })
            return no_passive_list


        def process_passive_interface(ospf_process_section, passive_list):
            """
            Process the passive interface statements in the OSPF section
            :param ospf_process_section: list
            :param passive_list: list
            :return: list of passive interfaces
            """
            ospf_process_section = SPLIT_ON_LINE_MULTILINE.split(ospf_process_section)
            for line in ospf_process_section:
                passive_interface = RTP_IOS_OSPF_PASSIVE_INTERFACE_REGEX.search(line)
                if passive_interface:
                    passive_list.append({
                        "interface": passive_interface.group(1).strip()
                    })
            return passive_list


        def find_ospf_interfaces(ospf_obj):
            """
            Find all the layer3 interfaces that are part of the OSPF process
            If there is interface that is part of the OSPF process,
            then it will extract the area and process id
            :param ospf_obj: OSPFConfig object
            :return: list of interfaces
            """
            layer_3_interfaces = L3InterfaceParser(self.content)._fetch_l3_interfaces()
            ospf_interfaces = []
            for l3_intf in layer_3_interfaces:
                ospf_intf_dict = {}
                intf_children = "\n".join(l3_intf.children)
                ospf_interfaces_regex = RTP_IOS_OSPF_INTERFACES_REGEX.search(intf_children)
                if ospf_interfaces_regex:
                    intf_ospf_area_regex = RTP_IOS_OSPF_INTERFACES_AREA_REGEX.search(intf_children)
                    intf_ospf_process_id_regex = RTP_IOS_OSPF_INTERFACES_PROCESS_ID_REGEX.search(intf_children)
                    if intf_ospf_process_id_regex.group(1).strip() == ospf_obj.process_id:

                        ospf_intf_dict["interface"] = l3_intf.name
                        if intf_ospf_area_regex:
                            ospf_intf_dict["area"] = intf_ospf_area_regex.group(1).strip()
                        if intf_ospf_process_id_regex:
                            ospf_intf_dict["process_id"] = intf_ospf_process_id_regex.group(1).strip()

                        ospf_interfaces.append(ospf_intf_dict)

            ospf_obj.interfaces = ospf_interfaces
            return ospf_obj

        ospf_object_list = []
        for ospf_process in ospf_config_section:
            """
            the ospf_config_section is a list of ospf sections, if there are more than one ospf process
            looping over those sections and extracting the ospf configuration
            """

            ospf_config_obj = OSPFConfig()
            network_list = []
            no_passive_interface_list = []
            passive_interface_list = []

            # extract the process id from the ospf section and assign it to the object
            ospf_process_regex = RTP_IOS_OSPF_REGEX.search(ospf_process).group(1).strip()
            ospf_config_obj.process_id = ospf_process_regex if ospf_process_regex else None
            ospf_process = ospf_process.replace(f"router ospf {ospf_process_regex}", "")

            # extract the router id from the ospf section and assign it to the object
            router_id_regex = RTP_IOS_OSPF_ROUTER_ID_REGEX.search(ospf_process)
            ospf_config_obj.router_id = router_id_regex.group(1).strip() if router_id_regex else None

            # extract the network statements from the ospf section and assign it to the object
            network_regex = RTP_IOS_OSPF_NETWORK_REGEX.search(ospf_process)
            if network_regex:
                network_list = process_network_statements(ospf_process, network_list)
            ospf_config_obj.network = network_list

            # extract the no passive-interface statements from the ospf section and assign it to the object
            no_passive_interface_regex = RTP_IOS_OSPF_NO_PASSIVE_INTERFACE_REGEX.search(ospf_process)
            if no_passive_interface_regex:
                no_passive_interface_list = process_no_passive_interface(ospf_process, no_passive_interface_list)
            ospf_config_obj.no_passive_interface = no_passive_interface_list

            # extract the passive-interface statements from the ospf section and assign it to the object
            passive_interface_regex = RTP_IOS_OSPF_PASSIVE_INTERFACE_REGEX.search(ospf_process)
            if passive_interface_regex:
                passive_interface_list = process_passive_interface(ospf_process, passive_interface_list)
            ospf_config_obj.passive_interface = passive_interface_list

            # extract the auto-cost reference-bandwidth from the ospf section and assign it to the object
            auto_cost_regex = RTP_IOS_OSPF_AUTO_COST_REGEX.search(ospf_process)
            ospf_config_obj.auto_cost = auto_cost_regex.group(1).strip() if auto_cost_regex else None

            # extract children from the ospf section and assign it to the object
            ospf_config_obj.children = [
                child.strip() for child
                in SPLIT_ON_LINE_MULTILINE.split(ospf_process)
                if child.strip()
            ]

            ospf_config_obj = find_ospf_interfaces(ospf_config_obj)

            ospf_object_list.append(ospf_config_obj)

        if return_json:
            return [obj.__dict__ for obj in ospf_object_list]

        return ospf_object_list


    def _fetch_eigrp_config(self, return_json=False):
        """
        Fetch the EIGRP configuration from the config file
        :param return_json: bool
        :return: list of EIGRPConfig objects or json
        """

        def process_eigrp_network_statements(eigrp_vrf_section, net_list):
            """
            Process the network statements in the EIGRP section
            Splits the line and extracts the network, wildcard mask and area
            It will then convert the wildcard mask to a subnet mask and append it to the list
            :param eigrp_vrf_section: list
            :param net_list: list
            :return: list of dictionaries
            """
            eigrp_vrf_section_split = SPLIT_ON_LINE_MULTILINE.split(eigrp_vrf_section)
            for line in eigrp_vrf_section_split:
                network_line_regex = RTP_IOS_EIGRP_NETWORK_REGEX.search(line)

                if network_line_regex:
                    network_statement = network_line_regex.group().strip()
                    network_statement = network_statement.replace("network", "")
                    network_statement = network_statement.split()
                    if len(network_statement) == 2:
                        network = network_statement[0]
                        wildcard_mask = network_statement[1]
                        subnet_mask = self._convert_wildcard_to_mask(wildcard_mask)
                        net_list.append({
                            "network": network,
                            "subnet_mask": subnet_mask,
                            "wildcard_mask": wildcard_mask
                        })
            return net_list

        def process_eigrp_global_section(eigrp_section, global_net_list, global_obj):
            """
            Process the global eigrp section
            :param eigrp_section: str
            :param global_obj: EIGRPConfig object
            :param global_net_list: EIGRPConfig object
            :return: global network list
            """
            global_obj.children = [
                child.strip() for child in SPLIT_ON_LINE_MULTILINE.split(eigrp_section)
                if child.strip() and not RTP_EIGRP_REGEX.search(child)
            ]

            global_net_list = process_eigrp_network_statements(eigrp_section, global_net_list)
            return global_net_list


        def process_eigrp_vrf_sections(section, vrf_obj):
            """
            Process the EIGRP VRF sections
            :param section: str
            :param vrf_obj: EIGRPVrfChildren object
            :return: EIGRPVrfChildren object
            """
            vrf_section_children = [
                child.strip() for child
                in SPLIT_ON_LINE_MULTILINE.split(section)
                if child.strip() and not RTP_IOS_EIGRP_VRF_REGEX.search(child)
            ]
            vrf_obj.children = vrf_section_children

            vrf_network_regex = RTP_IOS_EIGRP_NETWORK_REGEX.search(section)

            if vrf_network_regex:
                vrf_network_list = []
                vrf_network_list = process_eigrp_network_statements(section, vrf_network_list)
                vrf_obj.network = vrf_network_list

            return vrf_obj

        def process_eigrp_sections(section, obj):
            """
            Processing both Global and VRF EIGRP sections
            :param section: str
            :param obj: EIGRPConfig object
            :return: str
            """
            vrf_sections = SPLIT_ON_SECOND_BANG_MULTILINE.split(section)
            eigrp_vrf_children_list = []
            if vrf_sections:
                obj.has_vrf = True
                obj.vrf_count = len(vrf_sections)
                for vrf_section in vrf_sections:
                    eigrp_vrf_children_obj = EIGRPVrfChildren()

                    # Processing Global EIGRP Section
                    if RTP_EIGRP_REGEX.search(vrf_section):
                        global_network_list = []
                        global_network_list = process_eigrp_global_section(vrf_section, global_network_list, obj)
                        obj.network = global_network_list
                        continue

                    # Processing VRF EIGRP Section
                    eigrp_vrf_regex = RTP_IOS_EIGRP_VRF_REGEX.search(vrf_section)
                    if eigrp_vrf_regex:
                        eigrp_vrf_children_obj.vrf = eigrp_vrf_regex.group(1).strip()
                        eigrp_vrf_children_obj = process_eigrp_vrf_sections(vrf_section, eigrp_vrf_children_obj)

                    eigrp_vrf_children_list.append(eigrp_vrf_children_obj)

            obj.vrf_children = eigrp_vrf_children_list
            return obj


        # IOSRoutingProtocolSeparator will return a list of eigrp sections
        # if there are more than one process in the config
        eigrp_config_section = IOSRoutingProtocolSeparator(self.content).find_eigrp_config()
        eigrp_object_list = []
        for eigrp_process in eigrp_config_section:
            eigrp_obj = EIGRPConfig()
            eigrp_obj = process_eigrp_sections(eigrp_process, eigrp_obj)

            eigrp_object_list.append(eigrp_obj)

        return eigrp_object_list


    def _fetch_isis_config(self):
        raise NotImplementedError("ISIS not implemented yet")


    def _fetch_rip_config(self):
        raise NotImplementedError("ISIS not implemented yet")


    def _fetch_bgp_config(self):
        bgp_config_section = IOSRoutingProtocolSeparator(self.content).find_bgp_config()
        print(bgp_config_section)

        pass














