from .parser import Parser




class ConfigParser(Parser):
    def __init__(self, _content, platform=None):
        super().__init__(_content, platform=platform)


    def get_static_config(self, return_json=False):
        """
        Get the static routes from the config file
        :return: list of static route objects
        """
        return self._get_static_config(return_json=return_json)


    def get_ospf_config(self, return_json=False):
        """
        Get the ospf configuration from the config file
        :return: list of ospf objects or json
        """
        return self._get_ospf_config(return_json=return_json)


    def get_eigrp_config(self, return_json=False):
        """
        Get the eigrp configuration from the config file
        :return: list of eigrp objects or json
        """
        return self._get_eigrp_config(return_json=return_json)


    def get_bgp_config(self, return_json=False):
        """
        Get the eigrp configuration from the config file
        :return: list of eigrp objects or json
        """
        return self._get_bgp_config(return_json=return_json)



    def get_vlan_info(self):
        """
        Get the vlan information from the config file
        :return: list of vlan objects
        """
        return self._get_vlan_info()

    def get_banner(self):
        """
        Get the banner from the config file
        :return: banner object
        """
        return self._get_banner()

    def get_parent_child(self, **kwargs):
        """
        Get parent child from the config file
        :return: list of parent child objects
        """
        return self._get_parent_child(**kwargs)


    def get_subnet_and_usage(self, include_subnet_count=False):
        """
        Fetch the subnet usage from the config file
        return: dictionary of subnet usage
        """
        return self._get_subnet_and_usage(include_subnet_count=include_subnet_count)


    def get_l3_interfaces(self, **kwargs):
        """
        Get L3 interfaces from the config file
        :return: list of L3 interface objects
        """
        return self._get_l3_interfaces(**kwargs)

    def get_l3_interface_details(self):
        """
        Get the L3 interface details
        :return: dictionary of L3 interface details
        """
        return self._get_l3_interface_details()

    def get_l2_access_interfaces(self, **kwargs):
        """
        Get L2 access interfaces from the config file
        :return: list of L2 access interface objects
        """
        return self._get_l2_access_interfaces(**kwargs)

    def get_l2_access_interface_details(self):
        """
        Get the L2 interface details
        :return: dictionary of L2 interface details
        """
        return self._get_l2_access_interface_details()

    def get_l2_trunk_interfaces(self, **kwargs):
        """
        Get L2 trunk interfaces from the config file
        :return: list of L2 trunk interface objects
        """
        return self._get_l2_trunk_interfaces(**kwargs)

    def get_l2_trunk_interface_details(self):
        """
        Get the L2 interface details
        :return: dictionary of L2 interface details
        """
        return self._get_l2_trunk_interface_details()




from cisco_config_parser.old_version.utils import OldParser

class ConfigParserOld(OldParser):
    def find_parent_child(self, regex):
        return self._parent_child_relationship(regex)

    def ios_get_banner_login(self):
        return self._ios_fetch_banner_login()

    def ios_get_switchport(self, **kwargs):
        return self._ios_fetch_switchport(**kwargs)

    def ios_get_routed_port(self):
        return self._ios_fetch_routed_port()

    def ios_get_svi_objects(self):
        return self._ios_fetch_svi_objects()

    def nxos_get_vlan_info(self):
        return self._nxos_fetch_vlan_info()

    def nxos_get_vlan(self):
        return self._nxos_fetch_vlan_list()

    def nxos_get_l3_int(self):
        return self._nxos_fetch_l3_int()

    def nxos_get_routing_protocol(self):
        return self._nxos_fetch_routing_protocol()






