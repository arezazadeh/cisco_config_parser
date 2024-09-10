from cisco_config_parser.routing_protocol.utils.rtp_separator import IOSRoutingProtocolSeparator
from cisco_config_parser.routing_protocol.ios.rtp_ios_rtp_obj import *
from cisco_config_parser.parser_regex.regex import *
from dataclasses import dataclass
from cisco_config_parser.layer3_interface import L3InterfaceParser


@dataclass
class IOSOSPFConfig:
    """
    OSPFConfig class to parse the OSPF configuration in the config file
    :param content: str
    :return: list of OSPFConfig objects
    """
    content: str = None

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
                        subnet_mask = convert_wildcard_to_mask(wildcard_mask)
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


















