import json

from cisco_config_parser import ConfigParser
from netmiko import ConnectHandler

# router = {
#     'device_type': 'cisco_ios',
#     'host': 'STNRNV-C10R26-BL01',
#     'username': 'netsmart',
#     'password': '@lph@B0+',
#     'fast_cli': False
# }
#
# net_connect = ConnectHandler(**router)
# output = net_connect.send_command("show run", cmd_verify=False, read_timeout=120)
# net_connect.disconnect()

nxos_file = "/Users/s0107094/devFolder/nxos_config.txt"
ios_file = "/Users/s0107094/devFolder/config.txt"

with open(nxos_file, "r") as f:
    res = f.read()


l2_intf = ConfigParser(res)
# print(l2_intf)

parent_child = l2_intf.get_vlan_info()

for i in parent_child:
    print(i.vlan)
    print(i.children)





