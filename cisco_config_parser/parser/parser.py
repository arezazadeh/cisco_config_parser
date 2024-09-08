from cisco_config_parser.layer3_interface import L3InterfaceParser
from cisco_config_parser.layer2_interface import L2InterfaceParser
from cisco_config_parser.parent_child import ParentChildParser
from cisco_config_parser.global_search import GlobalParser



class Parser:
    def __init__(self, _content):
        self._content = _content
        self._l3_parser_obj = L3InterfaceParser(self._content)
        self._l2_parser_obj = L2InterfaceParser(self._content)
        self._parent_child_parser_obj = ParentChildParser(self._content)
        self._global_parser = GlobalParser(self._content)



    def _get_vlan_info(self):
        """
        Get the vlan information from the config file
        :return: list of vlan objects
        """
        return self._global_parser._fetch_vlan_info()


    def _get_banner(self):
        """
        Get the banner from the config file
        :return: banner object
        """
        return self._global_parser._fetch_banner()

    def _get_parent_child(self, **kwargs):
        """
        Get parent child from the config file
        :return: list of parent child objects
        """
        return self._parent_child_parser_obj._fetch_parent_child(**kwargs)


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




