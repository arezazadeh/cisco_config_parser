# Description: This file contains the implementation of the RTP EIGTP class.


from dataclasses import dataclass
from .rtp_ospf import IOSRoutingProtocolSeparator
from cisco_config_parser.parser_regex.regex import *
from cisco_config_parser.routing_protocol.utils import *
from .rtp_ios_rtp_obj import EIGRPConfig, EIGRPVrfChildren




@dataclass
class IOSEIGRPConfig:
    """
    EIGRPConfig class to parse the EIGRP configuration in the config file
    :param content: str
    :return: list of EIGRPConfig objects
    """
    content: str = None

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
                        subnet_mask = convert_wildcard_to_mask(wildcard_mask)
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








