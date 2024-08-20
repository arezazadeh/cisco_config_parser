class ParentObj:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child


class IntObj:
    def __init__(self, **kwargs):
        self.intf = kwargs.get("intf") or None
        self.ip_add = kwargs.get("ip_add") or None
        self.description = kwargs.get("description") or None
        self.vrf = kwargs.get("vrf") or None
        self.helper = kwargs.get("helper") or None
        self.state = kwargs.get("state") or None

    def __str__(self):
        return f"IntObj Class - {self.intf}"



class SwitchPortAccess:
    def __init__(self, **kwargs):
        self.port = kwargs.get("port", None)
        self.vlan = kwargs.get("vlan", None)
        self.voice = kwargs.get("voice", None)
        self.description = kwargs.get("description", None)
        self.state = kwargs.get("state", None)
        self.spanning_tree = kwargs.get("spanning_tree", None)

    def __str__(self):
        return f"SwitchPortAccess Class - {self.port}"

    @property
    def get_access(self):
        return f"""
{self.port}
  {self.description}
  {self.vlan}
  {self.voice}
  {self.state}
!
"""


class SwitchPortTrunk:
    def __init__(self, **kwargs):
        self.port = kwargs.get("port", None)
        self.description = kwargs.get("description", None)
        self.allowed_vlan = kwargs.get("allowed_vlan", None)
        self.state = kwargs.get("state")
        self.dhcp_snooping = kwargs.get("dhcp_snooping", None)
        self.dhcp_relay = kwargs.get("dhcp_relay", None)

    def __str__(self):
        return f"SwitchPortTrunk Class - {self.port}"

    @property
    def get_trunk(self):
        return f"""
{self.port}
  {self.description}
  {self.allowed_vlan}
  {self.state}
!
"""


class RoutedPort:
    def __init__(self, **kwargs):
        self.intf = kwargs.get("intf") or None
        self.ip = kwargs.get("ip") or None
        self.mask = kwargs.get("mask") or None
        self.subnet = kwargs.get("subnet") or None
        self.description = kwargs.get("description") or None
        self.vrf = kwargs.get("vrf") or None
        self.helper = kwargs.get("helper") or None
        self.state = kwargs.get("state") or None
        self.sec_ip = kwargs.get("sec_ip") or None
        self.sec_mask = kwargs.get("sec_mask") or None
        self.sec_subnet = kwargs.get("sec_subnet") or None
        self.vip = kwargs.get("vip") or None


    def __str__(self):
        return f"RoutedPort Class - {self.intf}"

