from cisco_config_parser import ConfigParser

parser = ConfigParser(method="file", content="/Users/s0107094/devFolder/config.txt")

int_obj = parser.ios_get_switchport(mode="access")
for i in int_obj:
    print(i.port)
    print(i.child)
    print("!")