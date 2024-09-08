from .parser import Parser




class ConfigParser(Parser):
    def __init__(self, _content):
        super().__init__(_content)

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







