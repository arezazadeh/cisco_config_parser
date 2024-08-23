from .utils import Parser


class ConfigParser(Parser):
    def find_parent_child(self, regex):
        return self.parent_child_relationship(regex)

    def ios_get_banner_login(self):
        return self.ios_fetch_banner_login()

    def ios_get_switchport(self, **kwargs):
        return self.ios_fetch_switchport(**kwargs)

    def ios_get_routed_port(self):
        return self.ios_fetch_routed_port()

    def ios_get_svi_objects(self):
        return self.ios_fetch_svi_objects()

    def nxos_get_vlan_info(self):
        return self.nxos_fetch_vlan_info()

    def nxos_get_vlan(self):
        return self.nxos_fetch_vlan_list()

    def nxos_get_l3_int(self):
        return self.nxos_fetch_l3_int()

    def nxos_get_routing_protocol(self):
        return self.nxos_fetch_routing_protocol()

