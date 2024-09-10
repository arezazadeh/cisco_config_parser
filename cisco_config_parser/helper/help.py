

RTP_IOS_STATIC_HELP = """

Example Usage For Static Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)
obj.get_static_routes()
obj.get_static_routes(return_json=True)
"""


RTP_IOS_OSPF_HELP = """
Example Usage For OSPF Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)
ospf = obj.get_ospf_config(return_json=True)
ospf = obj.get_ospf_config()
for i in ospf:
    print(i.children)
    print(i.network)
    print(i.no_passive_interface)

"""
RTP_IOS_EIGRP_HELP = """
Example Usage For EIGRP Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)
eigrp = obj.get_eigrp_config(return_json=True)
eigrp = obj.get_eigrp_config()
for i in eigrp:
    print(i.children)
    print(i.network)
    print(i.vrf_children) << returns a list of EIGRPVrfChildren objects
    vrf_children = i.vrf_children
    for vrf in vrf_children:
        print(vrf.network)
        print(vrf.children)
"""


RTP_IOS_BGP_HELP = """
Example Usage For Static Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)

bgp = obj.get_bgp_config(return_json=True)
bgp = obj.get_bgp_config()
for i in bgp:
    print(i.children)
    print(i.network)
    print(i.vrf_children) << returns a list of BGPVrfChildren objects
    vrf_children = i.vrf_children
    for vrf in vrf_children:
        print(vrf.network)
        print(vrf.children)
"""

PARENT_CHILD_HELP = """
Example Usage:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()

obj = ConfigParser(content)

parent_child = obj.get_parent_child(custom_regex="(^snmp.*)|(^aaa.*)")

for i in parent_child:
    print(i.parent)
    print(i.children)

"""
LAYER3_INTERFACE_HELP = """
Example Usage:
====================================================================================================
with open("show_run.txt", "r") as file_output:
    content = file_output.read()

obj = ConfigParser(content)

# returns dictionary of layer3 interfaces
l3_intfs = obj.get_l3_interface_details()

l3_intfs = obj.get_l3_interface()

for intf in l3_intfs:
    print(intf.name)
    print(intf.ip_address)
    print(intf.children)


# you can also search for specific entry under layer3 interface with custom regex
l3_intfs = obj.get_l3_interface(ip_pim="(ip\spim\s.*)", load_interval="(load\sinterval.*)")


for intf in l3_intfs:
    print(intf.name)
    print(intf.ip_address)
    print(intf.ip_pim) <<< dynamically creates an attribute based on the custom regex
    print(intf.load_interval) <<< dynamically creates an attribute based on the custom regex

"""
LAYER2_INTERFACE_HELP = """
Example Usage:
====================================================================================================
with open("show_run.txt", "r") as file_output:
    content = file_output.read()

obj = ConfigParser(content)

# returns dictionary of layer2 interfaces
l2_intfs = obj.get_l2_interface_details()

l2_intfs = obj.get_l2_interface()

for intf in l2_intfs:
    print(intf.name)
    print(intf.children)

"""