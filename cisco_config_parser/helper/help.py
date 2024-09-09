

RTP_IOS_HELP = """

Example Usage:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)


#
##
###
#### Static Routes Example:
###
##
#
obj.get_static_routes()
obj.get_static_routes(return_json=True)


#
##
###
#### OSPF Example:
###
##
#
ospf = obj.get_ospf_config(return_json=True)
ospf = obj.get_ospf_config()
for i in ospf:
    print(i.children)
    print(i.network)
    print(i.no_passive_interface)

#
##
###
#### EIGRP Example:
###
##
#
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
