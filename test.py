import json

from cisco_config_parser import ConfigParser
from cisco_config_parser import ConfigParserOld
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

with open(ios_file, "r") as f:
    res = f.read()


l2_intf = ConfigParserOld(content=res, method="ext_ssh")
# print(l2_intf)


l2 = l2_intf.ios_get_switchport(mode="access")
print(l2)




