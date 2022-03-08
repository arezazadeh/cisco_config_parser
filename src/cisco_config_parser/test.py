
from cisco_config_parser import ConfigParser
file = "/Users/ahmad/running_config.txt"

parser = ConfigParser(file=file)

obj = parser.get_switchport()
for i in obj:
    print(i.port)