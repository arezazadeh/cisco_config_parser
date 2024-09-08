# Description: L2Interface class to store the l3 interface information
from dataclasses import dataclass



@dataclass
class L2AccessInterface:
    """
    L2AccessInterface class to store the l2 Access Interface information
    """
    name: str = None
    description: str = None
    data_vlan: int = None
    voice_vlan: str = None
    state: str = None
    spanning_tree: str = None
    native_vlan: str = None
    children: list = None

    def _add_custom_field(self, custom_name: str, value):
        """
        Dynamically add a custom attribute to the instance
        """
        setattr(self, custom_name, value)

    def __getattr__(self, item):
        """
        If the attribute is not found, return None
        """
        return None


@dataclass
class L2TrunkInterface:
    """
    L3Interface class to store the l3 interface information
    """
    name: str = None
    description: str = None
    allowed_vlans: list = None
    dhcp_snooping: str = None
    dhcp_relay: str = None
    voice_vlan: str = None
    state: str = None
    spanning_tree: str = None
    native_vlan: str = None
    children: list = None

    def _add_custom_field(self, custom_name: str, value):
        """
        Dynamically add a custom attribute to the instance
        """
        setattr(self, custom_name, value)

    def __getattr__(self, item):
        """
        If the attribute is not found, return None
        """
        return None