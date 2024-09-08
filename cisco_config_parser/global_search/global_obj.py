from dataclasses import dataclass





@dataclass
class BannerObj:
    banner: list = None

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
class VLANObj:
    vlan: list = None
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

