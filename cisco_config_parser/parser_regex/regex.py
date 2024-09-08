import re

BGP_EVPN_REGEX = re.compile(r"vni [0-9]{7} l2")
BGP_EVPN_PARENT_REGEX = re.compile(r"\s{2}vni [0-9]{7} l2")

BGP_NEIGHBOR_REGEX = re.compile(r"^(\s{4}neighbor\s\d+.\d+.\d+.\d+)")

NVE_MEMBER_VNI_PARENT_REGEX = re.compile(r"^\s{2}member vni [0-9]{7}$")
NVE_MEMBER_VNI_CHILDREN_REGEX = re.compile(r"\s{3}.*")

PARENT_LINE_REGEX = re.compile(r"^(\w+.*)")
CHILDREN_LINE_REGEX = re.compile(r"^\s(.*)$")
CHILDREN_WITH_1_SPACE_REGEX = re.compile(r"\s.*")
CHILDREN_WITH_2_SPACE_REGEX = re.compile(r"\s{2}.*")
CHILDREN_WITH_3_SPACE_REGEX = re.compile(r"\s{3}.*")
CHILDREN_WITH_4_SPACE_REGEX = re.compile(r"\s{4}.*")
CHILDREN_WITH_5_SPACE_REGEX = re.compile(r"\s{5}.*")
ROUTER_BGP_PARENT_REGEX = re.compile(r"^router bgp(.*)")
ROUTER_BGP_VRF_REGEX = re.compile(r"^\s{2}vrf\s(.*)")
SPLIT_ON_BANG_MULTILINE = re.compile(r"!", flags=re.MULTILINE)
SPLIT_ON_FIRST_BANG_MULTILINE = re.compile(r"^!$", flags=re.MULTILINE)
SPLIT_ON_LINE = re.compile(r"\n")
SPLIT_ON_LINE_MULTILINE = re.compile(r"\n", flags=re.MULTILINE)
VLAN_CONFIG_REGEX = re.compile(r"^(vlan\s[0-9]+)")
EXCLUDED_VLAN_CONFIG_REGEX = re.compile(r"^vlan\s[0-9]+,.*")
ROUTER_BGP_VRF_CONFIG_REGEX = re.compile(r"^vrf\s(.*)")
VLAN_SVI_INTERFACE_MULTILINE_REGEX = re.compile(r"^interface Vlan(.*)", flags=re.MULTILINE)
INTERFACE_MULTILINE_REGEX = re.compile(r"^interface\s+(.*)", flags=re.MULTILINE)
TRUNK_ALLOWED_VLAN_REGEX = re.compile(r"allowed\svlan\s(.*)")
TRUNK_NATIVE_VLAN_REGEX = re.compile(r"switchport\strunk\snative\svlan\s(.*)")


# Interface
INTERFACE_REGEX = re.compile(r"interface\s(.*)", flags=re.MULTILINE)


# L3 Interface
DESCRIPTION_REGEX = re.compile(r"description\s(.*)", flags=re.MULTILINE)
IP_ADDRESS_REGEX = re.compile(r"ip\saddress\s(\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+)|ip\saddress\s(\d+\.\d+\.\d+\.\d+/\d+)")
HELPER_ADDRESS_REGEX = re.compile(r"ip\shelper-address\s(.*)")
SECONDARY_IP_ADDRESS_REGEX = re.compile(r"ip\saddress\s(.*)secondary")
VRF_REGEX = re.compile(r"ip\svrf\sforwarding\s(.*)|vrf\smember\s(.*)")


# L2 Interface
SWITCHPORT_REGEX = re.compile(r"switchport\s(.*)", flags=re.MULTILINE)
SWITCHPORT_ACCESS_REGEX = re.compile(r"switchport\smode\saccess", flags=re.MULTILINE)
SWITCHPORT_TRUNK_REGEX = re.compile(r"switchport\smode\strunk", flags=re.MULTILINE)
SWITCHPORT_ACCESS_VLAN_REGEX = re.compile(r"switchport\saccess\svlan\s(.*)", flags=re.MULTILINE)
SWITCHPORT_VOICE_VLAN_REGEX = re.compile(r"switchport\svoice\svlan\s(.*)", flags=re.MULTILINE)
SWITCHPORT_TRUNK_ALLOWED_VLAN_REGEX = re.compile(r"switchport\strunk\sallowed\svlan\s(.*)", flags=re.MULTILINE)
SWITCHPORT_TRUNK_NATIVE_VLAN_REGEX = re.compile(r"switchport\strunk\snative\svlan\s(.*)", flags=re.MULTILINE)
SWITCHPORT_TRUNK_DHCP_RELAY_REGEX = re.compile(r"ip\sdhcp\srelay\s(.*)", flags=re.MULTILINE)
SWITCHPORT_TRUNK_SNOOPING_REGEX = re.compile(r"ip\ssnooping\s(.*)", flags=re.MULTILINE)

# VLAN
VLAN_REGEX = re.compile(r"^vlan\s([0-9]+)", flags=re.MULTILINE)

def find_vrf_section(vrf, item):
    return re.search(f"^(vrf {vrf.upper()}.*)", item.strip())
