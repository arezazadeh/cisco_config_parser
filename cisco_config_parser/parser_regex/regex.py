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
SPLIT_ON_BANG_MULTILINE = re.compile(r"^!", flags=re.MULTILINE)
SPLIT_ON_SECOND_BANG_MULTILINE = re.compile(r"\s!$", flags=re.MULTILINE)
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
IP_ADDRESS_CIDR_REGEX = re.compile(r"ip\saddress\s(\d+\.\d+\.\d+\.\d+/\d+)")
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

# Routing Protocol
RTP_REGEX = re.compile(r"^router\s(.*)", flags=re.MULTILINE)
RTP_ISIS_REGEX = re.compile(r"^router isis", flags=re.MULTILINE)
RTP_RIP_REGEX = re.compile(r"^router rip", flags=re.MULTILINE)

# Static Route IOS
RTP_IOS_STATIC_REGEX = re.compile(r"^ip route", flags=re.MULTILINE)
RTP_IOS_STATIC_AD_REGEX = re.compile(r"^ip\sroute\s\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+\s(\d+)", flags=re.MULTILINE)
RTP_IOS_STATIC_NAME_REGEX = re.compile(r"^ip\sroute\s.*name(.*)", flags=re.MULTILINE)
RTP_IOS_STATIC_VRF_REGEX = re.compile(r"^ip\sroute\svrf\s(\S+)", flags=re.MULTILINE)


# DETERMINE PLATFORM
IOS_PLATFORM_REGEX_1 = re.compile(r"^Current\sconfiguration\s:\s\d+\sbytes", flags=re.MULTILINE)
NXOS_PLATFORM_REGEX_1 = re.compile(r"^!Command:\sshow\srunning-config", flags=re.MULTILINE)
NXOS_PLATFORM_REGEX_2 = re.compile(r"^feature\s.*", flags=re.MULTILINE)
XR_PLATFORM_REGEX_1 = re.compile(r"^!!\sIOS\sXR\sConfiguration.*", flags=re.MULTILINE)
XR_PLATFORM_REGEX_2 = re.compile(r"^prefix-set.*", flags=re.MULTILINE)
XR_PLATFORM_REGEX_3 = re.compile(r"^route-policy.*", flags=re.MULTILINE)


# IOS ROUTING PROTOCOL - OSPF
RTP_IOS_OSPF_REGEX = re.compile(r"^router\sospf\s(.*)", flags=re.MULTILINE)
RTP_IOS_OSPF_ROUTER_ID_REGEX = re.compile(r"\s+router-id\s(\d+\.\d+\.\d+\.\d+)", flags=re.MULTILINE)
RTP_IOS_OSPF_NETWORK_REGEX = re.compile(r"\s+network\s(\d+\.\d+\.\d+\.\d+)\s(\d+\.\d+\.\d+\.\d+)\sarea\s(\S+)", flags=re.MULTILINE)
RTP_IOS_OSPF_NO_PASSIVE_INTERFACE_REGEX = re.compile(r"\s+no\spassive-interface\s(.*)", flags=re.MULTILINE)
RTP_IOS_OSPF_PASSIVE_INTERFACE_REGEX = re.compile(r"\s+passive-interface\s(.*)", flags=re.MULTILINE)
RTP_IOS_OSPF_AUTO_COST_REGEX = re.compile(r"\s+auto-cost\sreference-bandwidth\s(\d+)", flags=re.MULTILINE)
RTP_IOS_OSPF_INTERFACES_REGEX = re.compile(r"\s+ip\sospf\s\d+\s+area\s.*", flags=re.MULTILINE)
RTP_IOS_OSPF_INTERFACES_AREA_REGEX = re.compile(r"\s+ip\sospf\s\d+\s+area\s(\S+)", flags=re.MULTILINE)
RTP_IOS_OSPF_INTERFACES_PROCESS_ID_REGEX = re.compile(r"\s+ip\sospf\s(\d+)\s+area\s.*", flags=re.MULTILINE)


# IOS ROUTING PROTOCOL - EIGRP
RTP_EIGRP_REGEX = re.compile(r"^router eigrp", flags=re.MULTILINE)
RTP_IOS_EIGRP_VRF_REGEX = re.compile(r"\s+address-family\sipv4\svrf\s(\S+)", flags=re.MULTILINE)
RTP_IOS_EIGRP_NETWORK_REGEX = re.compile(r"\s+network\s(\d+\.\d+\.\d+\.\d+)\s(\d+\.\d+\.\d+\.\d+)", flags=re.MULTILINE)

# IOS ROUTING PROTOCOL - BGP
RTP_BGP_REGEX = re.compile(r"^router bgp", flags=re.MULTILINE)
RTP_BGP_ROUTER_ID_REGEX = re.compile(r"\s+bgp\srouter-id\s(\d+\.\d+\.\d+\.\d+)", flags=re.MULTILINE)
RTP_IOS_BGP_VRF_REGEX = re.compile(r"\s+address-family\sipv4\svrf\s(\S+)", flags=re.MULTILINE)
RTP_IOS_BGP_NETWORK_REGEX = re.compile(r"\s+network\s(\d+\.\d+\.\d+\.\d+)\smask\s(\d+\.\d+\.\d+\.\d+)", flags=re.MULTILINE)
RTP_IOS_BGP_NEIGHBOR_IP_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\s(.*)", flags=re.MULTILINE)
RTP_IOS_BGP_NEIGHBOR_REMOTE_AS_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\sremote-as\s(\d+)", flags=re.MULTILINE)
RTP_IOS_BGP_NEIGHBOR_DESCR_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\sdescription\s(.*)", flags=re.MULTILINE)
RTP_IOS_BGP_NEIGHBOR_UPDATE_SRC_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\supdate-source\s(.*)", flags=re.MULTILINE)
RTP_IOS_BGP_NEIGHBOR_RM_INBOUND_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\sroute-map\s(.*)\sin", flags=re.MULTILINE)
RTP_IOS_BGP_NEIGHBOR_RM_OUTBOUND_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\sroute-map\s(.*)\sout", flags=re.MULTILINE)

RTP_IOS_BGP_PEER_GROUP_REGEX = re.compile(r"\s+neighbor\s(\S+)\speer-group$", flags=re.MULTILINE)
RTP_IOS_BGP_PG_REMOTE_AS_REGEX = re.compile(r"\s+neighbor\s(.*)\sremote-as\s(\S+)", flags=re.MULTILINE)
RTP_IOS_BGP_PG_UPDATE_SRC_REGEX = re.compile(r"\s+neighbor\s(.*)\supdate-source\s(\S+)", flags=re.MULTILINE)
RTP_IOS_BGP_PG_RM_IN_REGEX = re.compile(r"\s+neighbor\s(.*)\sroute-map\s(\S+)\sin", flags=re.MULTILINE)
RTP_IOS_BGP_PG_RM_OUT_REGEX = re.compile(r"\s+neighbor\s(.*)\sroute-map\s(\S+)\sout", flags=re.MULTILINE)
RTP_IOS_BGP_PG_NEIGHBOR_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\speer-group(.*)", flags=re.MULTILINE)
RTP_IOS_BGP_PG_NEIGHBOR_DESCR_REGEX = re.compile(r"\s+neighbor\s(\d+\.\d+\.\d+\.\d+)\sdescription(.*)", flags=re.MULTILINE)
RTP_IOS_BGP_GLOBAL_IPV4_REGEX = re.compile(r"\s+address-family\sipv4$", flags=re.MULTILINE)

RTP_IOS_BGP_REDISTRIBUTE_REGEX = re.compile(r"\s+(redistribute\s.*)", flags=re.MULTILINE)
RTP_IOS_BGP_REDISTRIBUTE_W_RM_REGEX = re.compile(r"redistribute\s(\S+\s\S+|\S+)\s+route-map(.*)", flags=re.MULTILINE)
RTP_IOS_BGP_REDISTRIBUTE_WO_RM_REGEX = re.compile(r"redistribute\s(\S+\s\S+|\S+)$", flags=re.MULTILINE)



def find_vrf_section(vrf, item):
    return re.search(f"^(vrf {vrf.upper()}.*)", item.strip())
