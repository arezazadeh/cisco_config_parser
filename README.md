# Cisco Configuration Parser
## This Package Will Parse Cisco IOS, IOS-XE, IOS-XR, and NXOS Configuration File.

There are two ways to parse the config, 1, SSH which is not recommended, and 2, feeding the running-config file 
* to use file, use `ConfigParser(method="file", content=<your_file>)`. 
* to use SSH:
```ruby
ConfigParser(
    method="int_ssh",
    ssh=True, 
    user="username", 
    password="password", 
    device_type="cisco_ios", 
    host="your_switch_ip"
    )
```
device types that are accepted are:
```ruby
cisco_ios
cisco_xe
cisco_xr
cisco_nxos
```
pass the kwargs then it will login to your device and does the `show running-config` and will parse it. 

## Install the package

https://pypi.org/project/cisco-config-parser/

```ruby
pip install cisco-config-parser
```


## Regex Search Strings:

* to find lines in the configuration starting with "router"
```ruby
parse.find_parent_child("^router")
```


* to parse all confuguration into parent and child format
```ruby
parse.find_parent_child("^.")
```


* to find lines in the configuration that has "Loopback" in them
```ruby
parse.find_parent_child("^.*Loopback")

```


## Examples:

* Parsing NXOS Config For All the Related VLAN Info.


```ruby
>>> nxos_parser = ConfigParser(method="file", content=file1)
>>> vlan_info = nxos_parser.nxos_get_vlan_info()
>>> vlan_info.vlan = "2626"
>>> print(vlan_info.vlan)
:return:
!
vlan 2626
  name GRN200_nonPROD_APP_01
  vn-segment 2002626
!
interface Vlan2626
  description grn200 nonPROD App Servers 01
  no shutdown
  mtu 9216
  vrf member GRN200
  no ip redirects
  ip address 10.147.148.1/24
  no ipv6 redirects
  fabric forwarding mode anycast-gateway
!
int nve1
  member vni 2002626
    suppress-arp
    ingress-replication protocol bgp
!
evpn
  vni 2002626 l2
    rd auto
    route-target import auto
    route-target export aut

```

* Getting Routed Ports

```ruby 

from cisco_config_parser import ConfigParser

my_file = "running-config.txt"

parser = ConfigParser(method="file", content=my_file)

obj = parser.ios_get_routed_port()

for i in obj:
    print(i.intf)
    print(i.ip_add, i.mask)
    print(i.subnet)
    print(i.description)
    print(i.vrf)
    print(i.description)
    print(i.state)
    print("!")

```
output: 

```
interface TenGigE0/3/0/29.3240
10.10.1.1 255.255.255.248
10.10.1.0/29
 description Connected to device_A
 vrf vrf_A
 no shutdown
!
interface TenGigE0/3/0/29.3340
10.244.10.1 255.255.255.252
10.244.10.0/30
 description Connected to device_A
 vrf vrf_B
 no shutdown
```

* Getting Switchport:
there are two different mode on switchport, `access` and `trunk`. you should specify the mode `mode=trunk` or `mode=access`. this way you will be able to access all the access-ports or trunk-ports by accessing the methods (get_access or get_trunk)

```ruby

from cisco_config_parser import ConfigParser

my_file = "switch01_run_config.txt"

parser = ConfigParser(method="file", content=my_file)

obj = parser.ios_get_switchport(mode="access")

for i in obj:
    print(i.port)
    print(i.vlan)
    print(i.voice)
    print(i.description)
    print("!")

for i in obj:
    print(i.get_access)
```

output:

```
  
interface GigabitEthernet10/38
Access Port
Vlan  200
Voice  vlan 700
 description ent-user
!
interface GigabitEthernet10/38
Access Port
Vlan  200
Voice  vlan 700
 description ent-user
```

* Finding Routing Protocol
```ruby
    from cisco_config_parser import ConfigParser
    
    
    my_file = "switch01_running_config.txt"
    parse = ConfigParser(method="file", content=my_file)
    
    
    obj_list = parse.find_parent_child("^router")
    for i in obj_list:
        print(i.parent)
        for child_obj in i.child:
            print(child_obj)
 
 ```
 Output:
 
 ```
 router eigrp 252
 !
 address-family ipv4 vrf vrf_A autonomous-system 252
  network 10.10.10.0 0.0.0.63
  passive-interface default
  no passive-interface Vlan3123
  no passive-interface Vlan3124
  eigrp stub connected summary
 exit-address-family
 !
 address-family ipv4 vrf vrf_B autonomous-system 252
  network 10.20.10.0 0.0.0.3
  network 10.20.11.0 0.0.0.3
  passive-interface default
  no passive-interface Vlan3223
  no passive-interface Vlan3224
  eigrp stub connected summary
 exit-address-family
 !

 ```
 
 * Finding Interface and Helper address Example 

```ruby
    from cisco_config_parser import ConfigParser


    my_file = "switch01_running_config.txt"
    parse = ConfigParser(method="file", content=my_file)
    obj_list = parse.find_parent_child("^interface")

    for i in obj_list:
        vlan_200 = re.search("Vlan200", i.parent)
        if vlan_200:
            print(i.parent)
            for c_obj in i.child:
                if str(c_obj).startswith(" ip helper"):
                    print(str(c_obj))
```
Output: 

```
interface Vlan200
 ip helper-address 192.168.1.10
 ip helper-address 172.31.10.10
```

* Finding SVI in the config with all its child configuration

```ruby 

from cisco_config_parser import ConfigParser



my_file = "switch_01-run_config.txt"
parser = ConfigParser(method="file", content=my_file)

res = parser.ios_get_svi_objects()

for i in res:
    if "lan200" in i.intf:
        print(i.intf)
        print(i.ip_add)
        print(i.description)
        print(i.vrf)
        print(i.state)
        print(i.helper)
        print("!")
```

output:

```
interface Vlan200
 ip address 10.20.80.1 255.255.254.0
 description USER VLAN-
 ip vrf forwarding vrf_A
 no shutdown
[' ip helper-address 10.10.1.10 ', ' ip helper-address 10.20.1.10']
!
```
