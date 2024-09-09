# Description: L3Interface class to store the l3 interface information
from dataclasses import dataclass



@dataclass
class L3Interface:
    """
    L3Interface class to store the l3 interface information
    """
    name: str = None
    description: str = None
    ip_address: str = None
    mask: str = None
    subnet: str = None
    helpers: list = None
    sec_ip_address: str = None
    sec_mask: str = None
    sec_subnet: str = None
    vrf: str = None
    state: str = None
    vip: str = None
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

