from cisco_config_parser import ConfigParser
# from netmiko import ConnectHandler
#
# router = {
#     "device_type": "cisco_ios",
#     "host": "10.250.80.1",
#     "username": "netsmart",
#     "password": "@lph@B0+",
#     "fast_cli": False,
# }
#
# ssh = ConnectHandler(**router)
# ssh.send_command("terminal length 0")
# res = ssh.send_command("show run", cmd_verify=False, read_timeout=900)


with open("/Users/s0107094/devFolder/config.txt", "r") as f:
    res = f.read()
parser = ConfigParser(method="ext_ssh", content=res)

int_obj = parser.ios_get_switchport(mode="all")
print(int_obj)
