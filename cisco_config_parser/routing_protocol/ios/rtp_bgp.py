# Description: This file contains the class to parse BGP configuration from Cisco IOS configuration files.

from cisco_config_parser.routing_protocol.ios.rtp_ospf import IOSRoutingProtocolSeparator
from cisco_config_parser.parser_regex.regex import *
from .rtp_ios_rtp_obj import BGPConfig, BGPVrfChildren
from cisco_config_parser.routing_protocol.utils.utils import *
from dataclasses import dataclass



@dataclass
class IOSBGPConfig:
    content: str = None

    def _fetch_bgp_config(self, return_json=False):
        """
        Fetch the BGP configuration from the config file
        :return: list of BGPConfig objects
        """

        def process_network_statements(cfg_section, net_list):
            """
            Process the network statements in the BGP section
            Splits the line and extracts the network, wildcard mask and area
            It will then convert the wildcard mask to a subnet mask and append it to the list
            :param cfg_section: list
            :param net_list: list
            :return: list of dictionaries
            """
            bgp_network_list = RTP_IOS_BGP_NETWORK_REGEX.findall(cfg_section)
            for network in bgp_network_list:
                subnet = network[0]
                mask = network[1]
                subnet = get_subnet(subnet, mask)
                net_list.append(subnet)
            return net_list


        def process_neighbor_details(cfg_section, obj):
            """
            Process the neighbor details in the BGP section
            :param cfg_section: str
            :param obj: BGPConfig object
            :return: BGPConfig object
            """
            vrf_name = None
            vrf_name_regex = RTP_IOS_BGP_VRF_REGEX.search(cfg_section)
            if vrf_name_regex:
                vrf_name = vrf_name_regex.group(1).strip()

            vrf_neighbor_ip_list = set()

            # iterating over the neighbor ip addresses and collecting a unique list of neighbors
            for neighbor in RTP_IOS_BGP_NEIGHBOR_IP_REGEX.finditer(cfg_section):
                neighbor_ip = neighbor.group(1).strip()
                vrf_neighbor_ip_list.add(neighbor_ip)

            # iterating over the unique list of neighbors and extracting the neighbor details
            for neighbor_ip in vrf_neighbor_ip_list:

                neighbor_obj = {
                    "vrf": vrf_name,
                    "ip": neighbor_ip,
                    "remote_as": "",
                    "description": "",
                    "update_source": "",
                    "route_map": {"in": "", "out": ""}
                }

                # Separating the neighbor sections based on the neighbor ip and extracting the neighbor details
                neighbor_sections = ""
                for i in RTP_IOS_BGP_NEIGHBOR_IP_REGEX.finditer(cfg_section):
                    if i and i.group(1).strip() == neighbor_ip:
                        neighbor_sections += i.group()

                # Extracting the remote-as from the neighbor
                neighbor_ra_regex = RTP_IOS_BGP_NEIGHBOR_REMOTE_AS_REGEX.search(neighbor_sections)
                if neighbor_ra_regex and neighbor_ra_regex.group(1).strip() == neighbor_ip:
                    neighbor_obj["remote_as"] = neighbor_ra_regex.group(2).strip()

                # Extracting the neighbor description
                neighbor_dscr_regex = RTP_IOS_BGP_NEIGHBOR_DESCR_REGEX.search(neighbor_sections)
                if neighbor_dscr_regex and neighbor_dscr_regex.group(1).strip() == neighbor_ip:
                    neighbor_obj["description"] = neighbor_dscr_regex.group(2).strip()

                # Extracting the update-source from the neighbor
                neighbor_update_src_regex = RTP_IOS_BGP_NEIGHBOR_UPDATE_SRC_REGEX.search(neighbor_sections)
                if neighbor_update_src_regex and neighbor_update_src_regex.group(1).strip() == neighbor_ip:
                    neighbor_obj["update_source"] = neighbor_update_src_regex.group(2).strip()

                # Extracting the route-map inbound and outbound from the neighbor
                neighbor_rm_in_regex = RTP_IOS_BGP_NEIGHBOR_RM_INBOUND_REGEX.search(neighbor_sections)
                if neighbor_rm_in_regex and neighbor_rm_in_regex.group(1).strip() == neighbor_ip:
                    neighbor_obj["route_map"]["in"] = neighbor_rm_in_regex.group(2).strip()

                neighbor_rm_out_regex = RTP_IOS_BGP_NEIGHBOR_RM_OUTBOUND_REGEX.search(neighbor_sections)
                if neighbor_rm_out_regex and neighbor_rm_out_regex.group(1).strip() == neighbor_ip:
                    neighbor_obj["route_map"]["out"] = neighbor_rm_out_regex.group(2).strip()

                # Appending the neighbor dict to the neighbors list
                obj.neighbors.append(neighbor_obj)
            return obj




        def process_peer_groups(cfg_section, obj):
            """
            Process the peer groups in the BGP section
            :param cfg_section: str
            :return: list of dictionaries
            """
            peer_groups = RTP_IOS_BGP_PEER_GROUP_REGEX.findall(cfg_section)
            peer_group_details = []
            # Extracting the peer group details
            for pg in peer_groups:
                pg_info = {
                    "peer_group": {
                        "name": pg,
                        "remote_as": "",
                        "update_source": "",
                        "route_map": {"in": "", "out": ""},
                        "neighbors": [],
                }}

                # Extracting the remote-as from the peer group
                remote_as_regex = RTP_IOS_BGP_PG_REMOTE_AS_REGEX.search(cfg_section)
                if remote_as_regex and remote_as_regex.group(1) == pg:
                    pg_info["peer_group"]["remote_as"] = remote_as_regex.group(2)

                # Extracting the update-source  from the peer group
                update_source_regex = RTP_IOS_BGP_PG_UPDATE_SRC_REGEX.search(cfg_section)
                if update_source_regex and update_source_regex.group(1) == pg:
                    pg_info["peer_group"]["update_source"] = update_source_regex.group(2)

                # Extracting route-map inbound and outbound from the peer group
                pg_rm_in_regex = RTP_IOS_BGP_PG_RM_IN_REGEX.search(cfg_section)
                if pg_rm_in_regex and pg_rm_in_regex.group(1) == pg:
                    pg_info["peer_group"]["route_map"]["in"] = pg_rm_in_regex.group(2)

                pg_rm_out_regex = RTP_IOS_BGP_PG_RM_OUT_REGEX.search(cfg_section)
                if pg_rm_out_regex and pg_rm_out_regex.group(1) == pg:
                    pg_info["peer_group"]["route_map"]["out"] = pg_rm_out_regex.group(2)

                # Extracting the neighbors and neighbor description from the peer group
                for neighbor in RTP_IOS_BGP_PG_NEIGHBOR_REGEX.finditer(cfg_section):
                    neighbor_info = {}
                    if neighbor and neighbor.group(2).strip() == pg:
                        neighbor_info["ip"] = neighbor.group(1)

                        for neighbor_dscr in RTP_IOS_BGP_PG_NEIGHBOR_DESCR_REGEX.finditer(cfg_section):
                            if neighbor_dscr.group(1).strip() == neighbor.group(1).strip():
                                neighbor_info["description"] = neighbor_dscr.group(2)

                        pg_info["peer_group"]["neighbors"].append(neighbor_info)

                peer_group_details.append(pg_info)

            obj.peer_group = peer_group_details
            return obj

        def process_redistribute(cfg_section, obj):
            redistribute_regex = RTP_IOS_BGP_REDISTRIBUTE_REGEX.findall(cfg_section)
            if redistribute_regex:
                for redistribute_line in redistribute_regex:
                    redistribute_w_rm_regex = RTP_IOS_BGP_REDISTRIBUTE_W_RM_REGEX.search(redistribute_line)
                    if redistribute_w_rm_regex:
                        obj.redistribute.append({
                            "vrf": obj.vrf,
                            "protocol": redistribute_w_rm_regex.group(1),
                            "route_map": redistribute_w_rm_regex.group(2)
                        })
                    else:
                        redistribute_wo_rm_regex = RTP_IOS_BGP_REDISTRIBUTE_WO_RM_REGEX.search(redistribute_line)
                        if redistribute_wo_rm_regex:
                            obj.redistribute.append({
                                "vrf": obj.vrf,
                                "protocol": redistribute_wo_rm_regex.group(1),
                                "route_map": ""
                            })
            return obj

        def process_global_bgp_config(cfg_section, obj):
            """
            Process the global BGP section
            :param cfg_section: str
            :param obj: BGPConfig object
            :return: BGPConfig object
            """

            # Extract Global BGP Children
            bgp_children = [
                child.strip() for child
                in SPLIT_ON_LINE_MULTILINE.split(cfg_section)
                if child.strip() and not RTP_BGP_REGEX.search(child)
            ]
            obj.children = {"Global": bgp_children}

            # Extracting the router id from the BGP section
            bgp_router_id = RTP_BGP_ROUTER_ID_REGEX.search(cfg_section)
            if bgp_router_id:
                obj.router_id = bgp_router_id.group(1).strip()

            # Extracting the peer groups from the BGP section
            has_peer_group = RTP_IOS_BGP_PEER_GROUP_REGEX.search(cfg_section)
            if has_peer_group:
                obj = process_peer_groups(cfg_section, obj)

            # Extracting the network statements from the BGP section
            global_network_list = []
            bgp_network = RTP_IOS_BGP_NETWORK_REGEX.search(cfg_section)
            if bgp_network:
                global_network_list = process_network_statements(cfg_section, global_network_list)
            obj.network = global_network_list
            obj = process_redistribute(cfg_section, obj)
            return obj

        def process_vrf_bgp_config(cfg_section, vrf_obj):
            """
            Process the BGP VRF sections
            :param cfg_section: str
            :param vrf_obj: BGPVrfChildren object
            :return: BGPVrfChildren object
            """


            # Extracting the VRF name from the BGP VRF section
            vrf_name_regex = RTP_IOS_BGP_VRF_REGEX.search(cfg_section)
            if vrf_name_regex:
                vrf_obj.vrf = vrf_name_regex.group(1).strip()

            # Extract VRF Children
            vrf_children = [
                child.strip() for child in SPLIT_ON_LINE_MULTILINE.split(cfg_section)
                if child.strip() and not RTP_IOS_BGP_VRF_REGEX.search(child)
            ]

            has_peer_group = RTP_IOS_BGP_PEER_GROUP_REGEX.search(cfg_section)
            if has_peer_group:
                vrf_obj = process_peer_groups(cfg_section, vrf_obj)


            vrf_obj.children = {vrf_obj.vrf: vrf_children}

            # Extracting the network statements from the BGP section
            vrf_network_list = []
            vrf_network_list = process_network_statements(cfg_section, vrf_network_list)
            vrf_obj.network = vrf_network_list

            # Extracting the neighbors from the BGP VRF section
            vrf_neighbor_regex = RTP_IOS_BGP_NEIGHBOR_IP_REGEX.search(cfg_section)
            if vrf_neighbor_regex:
                vrf_obj = process_neighbor_details(cfg_section, vrf_obj)

            vrf_obj = process_redistribute(cfg_section, vrf_obj)

            return vrf_obj


        # Processing BGP Configuration
        bgp_process_list = []
        bgp_config_section = IOSRoutingProtocolSeparator(self.content).find_bgp_config() # returns a list of BGP sections if there are multiple BGP processes
        for bgp_section in bgp_config_section:
            bgp_obj = BGPConfig()

            # Extracting VRF names from the BGP section
            bgp_obj.vrf_list = RTP_IOS_BGP_VRF_REGEX.findall(bgp_section)

            global_bgp_config = ""
            bgp_section_split_on_bang = SPLIT_ON_SECOND_BANG_MULTILINE.split(bgp_section)
            vrf_obj_list = []
            for config_section in bgp_section_split_on_bang:
                bgp_vrf_obj = BGPVrfChildren()
                if RTP_BGP_REGEX.search(config_section):
                    global_bgp_config += config_section

                if RTP_IOS_BGP_GLOBAL_IPV4_REGEX.search(config_section):
                    global_bgp_config += config_section

                if RTP_IOS_BGP_VRF_REGEX.search(config_section):
                    bgp_vrf_obj = process_vrf_bgp_config(config_section, bgp_vrf_obj)
                    vrf_obj_list.append(bgp_vrf_obj)

                    bgp_obj.vrf_children = vrf_obj_list

            bgp_obj = process_global_bgp_config(global_bgp_config, bgp_obj)
            bgp_process_list.append(bgp_obj)

        if return_json:
            return [bgp.get_dict() for bgp in bgp_process_list]

        return bgp_process_list


