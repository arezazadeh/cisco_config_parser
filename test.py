import json

from cisco_config_parser import ConfigParser
from cisco_config_parser import ConfigParserOld
from netmiko import ConnectHandler


"""
1. routing protocol
 - ios 
    Global:
        ip route 10.0.0.0 255.255.255.0 10.20.20.1 name test
    VRF:
        ip route vrf grn200 10.0.0.0 255.255.255.0 10.20.20.1 name test
 - nxos
    Global:
     ip route 10.0.0.0 255.255.255.0 10.20.20.1 name test
    VRF:
        vrf context grn200
        ip route 10.0.0.0 255.255.255.0 10.20.20.1 name test
 - xr:
    Global:
        router static
          address-family ipv4 unicast
           0.0.0.0/0 10.240.129.3 description MC-RS01
    VRF:
        router static
          vrf grn200
            address-family ipv4 unicast
             10.252.53.141/32 10.245.14.254 description MILESTONE_SERVERS_300P_SOC

2- route-map
    - ios
    - nxos
    - xr
3- prefix-list
    - ios
    - nxos
    - xr
4- access-list
    - ios
    - nxos
    - xr


"""
def get_running_config(host):
    router = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': 'netsmart',
        'password': '@lph@B0+',
        'fast_cli': False
    }

    net_connect = ConnectHandler(**router)
    output = net_connect.send_command("show run", cmd_verify=False, read_timeout=120)
    net_connect.disconnect()

    with open("/Users/s0107094/devFolder/ios_pe_config.txt", "w") as f:
        f.write(output)



nxos_file = "/Users/s0107094/devFolder/nxos_config.txt"
ios_file = "/Users/s0107094/devFolder/config.txt"
ios_pe_file = "/Users/s0107094/devFolder/ios_pe_config.txt"

with open(ios_pe_file, "r") as f:
    res = f.read()



obj = ConfigParser(res)

#
# parent_child = obj.get_parent_child(custom_regex="(^snmp.*)|(^aaa.*)")
#
#
# for i in parent_child:
#     print(i.parent)


from cisco_config_parser.helper import helper

print(helper.IOSRouteParser())





