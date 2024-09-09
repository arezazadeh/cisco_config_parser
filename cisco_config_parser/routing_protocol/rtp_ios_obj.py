from dataclasses import dataclass




@dataclass
class StaticRoute:
    network: str = None
    mask: str = None
    nexthop_ip: str = None
    subnet: str = None
    vrf: str = None
    name: str = None
    admin_distance: str = None




@dataclass
class OSPFConfig:
    process_id: str = None
    router_id: str = None
    network: str = None
    wild_card_mask: str = None
    subnet: str = None
    vrf: str = None
    passive_interface: list = None
    no_passive_interface: list = None
    auto_cost: str = None
    interfaces: list = None
    children: list = None



@dataclass
class EIGRPVrfChildren:
    vrf: str = None
    network: list = None
    wild_card_mask: str = None
    subnet: str = None
    passive_interface: list = None
    no_passive_interface: list = None
    auto_cost: str = None
    interfaces: list = None
    children: list = None


@dataclass
class EIGRPConfig:
    as_number: str = None
    network: list = None
    vrf: str = "Global"
    wild_card_mask: str = None
    subnet: str = None
    has_vrf: bool = None
    vrf_count: int = None
    passive_interface: list = None
    no_passive_interface: list = None
    auto_cost: str = None
    interfaces: list = None
    children: list = None
    vrf_children: object = None


    def __post_init__(self):
        if self.vrf_children is None:
            self.vrf_children = EIGRPVrfChildren()

