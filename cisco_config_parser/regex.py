import re

BGP_EVPN_REGEX = re.compile("vni [0-9]{7} l2")
BGP_EVPN_PARENT_REGEX = re.compile("\s{2}vni [0-9]{7} l2")

BGP_NEIGHBOR_REGEX = re.compile("^(\s{4}neighbor\s\d+.\d+.\d+.\d+)")

NVE_MEMBER_VNI_PARENT_REGEX = re.compile("^\s{2}member vni [0-9]{7}$")
NVE_MEMBER_VNI_CHILDREN_REGEX = re.compile("\s{3}.*")

PARENT_LINE_REGEX = re.compile("^(\w+.*)")
CHILDREN_LINE_REGEX = re.compile("^\s+(.*)$")
CHILDREN_WITH_1_SPACE_REGEX = re.compile("\s.*")
CHILDREN_WITH_2_SPACE_REGEX = re.compile("\s{2}.*")
CHILDREN_WITH_3_SPACE_REGEX = re.compile("\s{3}.*")
CHILDREN_WITH_4_SPACE_REGEX = re.compile("\s{4}.*")
CHILDREN_WITH_5_SPACE_REGEX = re.compile("\s{5}.*")
ROUTER_BGP_PARENT_REGEX = re.compile("^router bgp(.*)")
ROUTER_BGP_VRF_REGEX = re.compile("^\s{2}vrf\s(.*)")
SPLIT_ON_BANG_MULTILINE = re.compile("!", flags=re.MULTILINE)
SPLIT_ON_FIRST_BANG_MULTILINE = re.compile("^!$", flags=re.MULTILINE)
SPLIT_ON_LINE = re.compile("\n")
SPLIT_ON_LINE_MULTILINE = re.compile("\n", flags=re.MULTILINE)
VLAN_CONFIG_REGEX = re.compile("^(vlan\s[0-9]+)")
EXCLUDED_VLAN_CONFIG_REGEX = re.compile("^vlan\s[0-9]+,.*")
ROUTER_BGP_VRF_CONFIG_REGEX = re.compile("^vrf\s(.*)")
VLAN_SVI_INTERFACE_MULTILINE_REGEX = re.compile("^interface Vlan(.*)", flags=re.MULTILINE)
INTERFACE_MULTILINE_REGEX = re.compile("^interface\s+(.*)", flags=re.MULTILINE)


def find_vrf_section(vrf, item):
    return re.search(f"^(vrf {vrf.upper()}.*)", item.strip())
