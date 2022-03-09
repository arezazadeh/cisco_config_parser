class ParentObj:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child


class IntObj:
    def __init__(self, intf, ip_add, description, vrf, helper, state):
        self.intf = intf
        self.ip_add = ip_add
        self.description = description
        self.vrf = vrf
        self.helper = helper
        self.state = state

    def __str__(self):
        return f"IntObj Class - {self.intf}"



class SwitchPortAccess:
    def __init__(self, port, **kwargs):
        self.port = port
        self.vlan = kwargs.get("vlan") or None
        self.voice = kwargs.get("voice") or None
        self.description = kwargs.get("description") or None
        self.state = kwargs.get("state") or None

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
    def __init__(self, port, **kwargs):
        self.port = port
        self.description = kwargs.get("description") or None
        self.allowed_vlan = kwargs.get("allowed_vlan") or None
        self.state = kwargs.get("state")

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
    def __init__(self, intf, **kwargs):
        self.intf = intf
        self.ip_add = kwargs.get("ip_add") or None
        self.mask = kwargs.get("mask") or None
        self.subnet = kwargs.get("subnet") or None
        self.description = kwargs.get("description") or None
        self.vrf = kwargs.get("vrf") or None
        self.helper = kwargs.get("helper") or None
        self.state = kwargs.get("state") or None

    def __str__(self):
        return f"RoutedPort Class - {self.intf}"

