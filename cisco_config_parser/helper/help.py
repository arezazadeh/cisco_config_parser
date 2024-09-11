

RTP_IOS_STATIC_HELP = """

Example Usage For Static Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)

# Return it as a json object
obj.get_static_routes(return_json=True)

# or as a list of StaticRoute objects
obj.get_static_routes()
"""


RTP_IOS_OSPF_HELP = """

Example Usage For OSPF Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)

# Return it as a json object
ospf = obj.get_ospf_config(return_json=True)

# or as a list of OSPFConfig objects
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

# Return it as a json object
eigrp = obj.get_eigrp_config(return_json=True)

# or as a list of EIGRPConfig objects
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

Example Usage For BGP Routes:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)

# Return it as a json object
bgp = obj.get_bgp_config(return_json=True)


# or as a list of BGPConfig objects
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

Example Usage For Parent Child:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()

obj = ConfigParser(content)

# This will only return the parent and its child based on the custom regex
parent_child = obj.get_parent_child(parent_regex="^aaa.*", child_regex="^server.*")

>> output:
    aaa group server tacacs+ TACACS_GROUP
    server-private 1.1.1.1 key 7 1234567890


# This will only return the parent and its child based on the custom regex
parent_child = obj.get_parent_child(parent_regex="(^snmp.*)|(^aaa.*)")

for i in parent_child:
    print(i.parent)
    print(i.children)

"""
LAYER3_INTERFACE_HELP = """

Example Usage For Layer3 Interfaces:
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

Example Usage For Layer2 Interfaces:
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