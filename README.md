# Cisco Configuration Parser

## Overview
The **Cisco Configuration Parser** is a Python library designed for network automation tasks, specifically focusing on parsing configuration files from Cisco routers and switches. It supports Cisco IOS, IOS-XE, IOS-XR, and NXOS platforms. This library allows you to convert running configuration files into structured Python objects or JSON/dictionary formats for easier analysis, modification, or automation.

## Key Features

### Platform Detection
This library is designed to be **platform agnostic**, meaning it can automatically determine the Cisco platform based on the syntax of the configuration file. In cases where the platform cannot be determined automatically, you can manually specify the platform by passing `platform="IOS/XR/NXOS"` to the parser.

### Flexible Data Handling
The parser can convert configuration data into either Python objects or JSON/dictionary formats. You can control the format by passing the `return_json=True` flag to the relevant method. This flexibility allows you to integrate with a wide range of automation workflows and tools.

### Configuration Hierarchy Recognition
Cisco configurations often feature a mix of parent-child relationships and standalone entries. This library is adept at recognizing and parsing these patterns to capture both common and critical configuration attributes. For instance:

- **Standalone Configuration Example:**
```bash
hostname switch01.net
``` 

- **Parent-Child Configuration Example:**

```bash
Vlan 100                <<<< Parent
  name DATA_VLAN        <<<< Child
```

This library tries to captures the important and common attributes of the configurations for different sections and convert them to python objects or json/dict format. 

Some of those configs are as follow:

```python
- Hostname,
- AAA, 
- Interface,
- VLAN, 
- Interface (Layer2 and Layer3),
- Access-list, 
- Prefix-list, 
- Prefix-set (IOS-XR)
- Route-map, 
- Route-policy (IOS-XR),
- Static Routes,
- Dynamic Routes
    - RIP
    - EIGRP
    - OSPF
    - IS-IS
    - BGP

- Line-vty 
- Line-con
- Banner
```
Above configuration sections are captured along with the most common attributes/children. and the rest of them are captured inside method `obj.children`. 

### Parent/Child Regex Parsing Capabilities
In addition to above default behavior or the library, you also have the option to pass your own regex to the `ConfigParser` as either `parent_regex=r"<custom_regex>", child_regex=r"<custom_regex>"` or only `parent_regex=r"<custom_regex>"`. 

**Note:** If you pass both `parent_regex` and `child_regex`, the library attempt to search for the parent and the only child that you have searched for. If you would like to get all the children, then just pass the `parent_regex` to the class. I will have some example at the bottom this document. 


## Install the package
This package is available on `pypi.org` you can install the package via `pip`.

https://pypi.org/project/cisco-config-parser/

```bash
pip install cisco-config-parser
```


## Current Classes in this library

```python
IOSStaticRouteConfig
IOSOSPFConfig
IOSEIGRPConfig
IOSBGPConfig
IOSBGPConfig
L3InterfaceParser
L2InterfaceParser
ParentChildParser
```

There more Classes are being built, and will be released in the upcoming versions. 

## Get Example usage:
A short documentation is embeded in the code base. you can view those example by importing `helper` and calling the class

```python
from cisco_config_parser.helper import helper 

helper = helper.IOSStaticRouteConfig()

print(helper)
```

**Output**:
```

Example Usage:
====================================================================================================

with open("show_run.txt", "r") as file_output:
    content = file_output.read()


obj = ConfigParser(content)

obj.get_static_routes() << Returns a list of objects
obj.get_static_routes(return_json=True) << Returns a list of dictionaries 

```
## Examples:

### Loading the Running-Config File 

```python
>>> ios_file = "/Users/fileFolder/devFolder/config.txt"
>>> with open(ios_file, "r") as f:
        running_config = f.read()

>>> from cisco_config_parser import ConfigParser
>>> 
>>> parser = ConfigParser(running_config)
```


### Layer3 Interface

In layer-3 interface, the class attempts to capture all the important attributes of the interface, such as:

- IPv4 Address
- Subnet 
- Subnet Mask
- Secondary IPv4 Address
- Secondary Subnet 
- Secondary Subnet Mask 
- HSRP or VRRP Config
    - VIP 

#### Subnet list and their Usages 

One of the great feature in this library is it captures all the subnets that are being used in your Network Device along with their usage. 
Also it tells you how many of each subnet masks are being used as well. I personaly use this feature when i need to automate DHCP/IPAM documentaion cleanup. 

**Example below illustriates this feature:**

```python
>>> subnet_usage = parser.get_subnet_and_usage(include_subnet_count=True)
>>> print(json.dumps(subnet_usage, indent=4))

{
    "Loopback100": "10.241.17.8/32",
    "Loopback200": "10.252.248.1/32",
    "Vlan200": "10.252.182.0/23",
    "Vlan300": "10.244.16.160/27",
    "Vlan310": "10.241.101.80/28",
    "Vlan400": "10.39.10.32/27",
    "Vlan700": "172.31.81.0/25",
    "Vlan1100": "10.242.12.0/26",
    "Vlan1125": "10.241.8.0/27",
    "Vlan1126": "10.241.8.32/27",
    "Vlan1127": "10.241.8.64/27",
    "subnet_count": {
        "/32": 2,
        "/23": 1,
        "/27": 5,
        "/28": 1,
        "/25": 1,
        "/26": 1,
    }
}
```

#### Layer3 Interfaces - List of Objects

```python
>>> l3_interfaces = parser.get_l3_interfaces()
>>>for l3 in l3_interfaces:
        print(l3.name)
        print(l3.ip_address, l3.subnet)
        print("!")

Loopback100
10.241.17.8 10.241.17.8/32
!
Loopback200
10.252.248.1 10.252.248.1/32
!
Loopback202
10.245.0.199 10.245.0.199/32
```
#### Layer3 Interfaces - Json/Dict Format

```python
>>> l3_interfaces = parser.get_l3_interfaces(return_json=True)
>>> print(json.dumps(l3_interfaces, indent=4))
[
    {
        "name": "Loopback100",
        "description": "SWITCH01-SA01 Loopback IP",
        "ip_address": "10.241.17.8",
        "mask": "255.255.255.255",
        "subnet": "10.241.17.8/32",
        "helpers": null,
        "sec_ip_address": null,
        "sec_mask": null,
        "sec_subnet": null,
        "vrf": "mgt100",
        "state": null,
        "vip": null,
        "children": [
            "description SWITCH01-SA01 Loopback IP",
            "ip vrf forwarding mgt100",
            "ip address 10.241.17.8 255.255.255.255",
            "ip pim sparse-mode",
            "ip ospf 100 area 0"
        ]
    },
]
```

#### Layer3 Interfaces - Custom Key/Value and Regex

```python
>>> l3_interfaces = parser.get_l3_interfaces(ip_pim="ip pim.*")
>>> for i in l3_interfaces:
        print(i.name)
        print(i.ip_pim)
        print("!")

Loopback100
ip pim sparse-mode
!
Loopback200
ip pim sparse-mode
!
```

### Layer2 `Access` and `Trunk` Interface

#### `Access Port` List of Objects 
 
```python
>>> access_ports = parser.get_l2_access_interfaces()
>>> 
>>> for intf in access_ports:
    print(intf.name)
    print(intf.description)
    print(intf.children)
    print("!")
... 
GigabitEthernet1/1
Data Users
['description Data Users', 'switchport access vlan 200', 'switchport mode access', 'switchport voice vlan 700', 'no logging event power-inline-status', 'ip dhcp snooping information option allow-untrusted']
!
GigabitEthernet1/2
Data Users
['description Data Users', 'switchport access vlan 200', 'switchport mode access', 'switchport voice vlan 700', 'no logging event power-inline-status', 'ip dhcp snooping information option allow-untrusted']
!
```

#### `Access Port` the json/dict format:

```python
>>> access_ports = parser.get_l2_access_interfaces(return_json=True)

>>> print(json.dumps(access_ports, indent=4))

[
    {
        "name": "GigabitEthernet1/1",
        "description": "DATA Users",
        "data_vlan": "200",
        "voice_vlan": "700",
        "state": null,
        "spanning_tree": null,
        "native_vlan": null,
        "children": [
            "description DATA Users",
            "switchport access vlan 200",
            "switchport mode access",
            "switchport voice vlan 700",
            "no logging event power-inline-status",
            "ip dhcp snooping information option allow-untrusted"
        ]
    },
]
```
#### `Access Port` Custom Key/method search

You can use your own custom regex with your own key, this key then become a dynamic method of the class where you can either call it or recieve it as json format. 


```python
>>> access_ports = parser.get_l2_access_interfaces(logging="no loggin.*", return_json=True)

>>> print(json.dumps(access_ports, indent=4))

[
    {
        "name": "GigabitEthernet1/1",
        "description": "SHC-Users",
        "data_vlan": "200",
        "voice_vlan": "700",
        "state": null,
        "spanning_tree": null,
        "native_vlan": null,
        "children": [
            "description SHC-Users",
            "switchport access vlan 200",
            "switchport mode access",
            "switchport voice vlan 700",
            "no logging event power-inline-status",
            "ip dhcp snooping information option allow-untrusted"
        ],
        "logging": "no logging event power-inline-status"                       <<<<< custom Key to find logging command
    },
]
```

#### `Trunk Port` List of Objects

```python
>>> trunk_interfaces = parser.get_l2_trunk_interfaces()

>>> for intf in trunk_interfaces:
        print(intf.name)
        print(intf.description)
        print("!")

TenGigabitEthernet5/1
(MP)SWITCH-SD03:Twe1/0/6
!
TenGigabitEthernet5/2
Link to SWITCH-SA01 Te6/2 Decomm
!
TenGigabitEthernet6/1
(MP)SWITCH-SD04:Te1/1
!
```

#### `Trunk Port` Json/Dict format

```python
>>> trunk_interfaces = parser.get_l2_trunk_interfaces(return_json=True)
>>> print(json.dumps(trunk_interfaces, indent=4))

[
    {
        "name": "TenGigabitEthernet5/1",
        "description": "(MP)SWITCH-SD03:Twe1/0/6",
        "allowed_vlans": null,
        "dhcp_snooping": null,
        "dhcp_relay": null,
        "voice_vlan": null,
        "state": null,
        "spanning_tree": null,
        "native_vlan": "256",
        "children": [
            "description (MP)SWITCH-SD03:Twe1/0/6",
            "switchport trunk native vlan 256",
            "switchport trunk allowed vlan 182,256,504,1100,3101,3201,3301,3311,3321,3331",
            "switchport trunk allowed vlan add 3351,3401,3411,3911",
            "switchport mode trunk",
            "load-interval 30",
            "udld port aggressive",
            "service-policy output egress_queueing",
            "ip dhcp snooping trust"
        ],
        "allowed_vlan": "182,256,504,1100,3101,3201,3301,3311,3321,3331"
    },
]
```
#### `Trunk Port` Custom Key/method search

```python
>>> access_ports = parser.parser.get_l2_trunk_interfaces(load="load.*", return_json=True)

>>> print(json.dumps(access_ports, indent=4))

    {
        "name": "TenGigabitEthernet5/1",
        "description": "(MP)SWITCH-SD03:Twe1/0/6",
        "allowed_vlans": null,
        "dhcp_snooping": null,
        "dhcp_relay": null,
        "voice_vlan": null,
        "state": null,
        "spanning_tree": null,
        "native_vlan": "256",
        "children": [
            "description (MP)STNMED-LPCH-SD03:Twe1/0/6",
            "switchport trunk native vlan 256",
            "switchport trunk allowed vlan 182,256,504,1100,3101,3201,3301,3311,3321,3331",
            "switchport trunk allowed vlan add 3351,3401,3411,3911",
            "switchport mode trunk",
            "load-interval 30",
            "udld port aggressive",
            "service-policy output egress_queueing",
            "ip dhcp snooping trust"
        ],
        "allowed_vlan": "182,256,504,1100,3101,3201,3301,3311,3321,3331",
        "load": "load-interval 30"                                      <<<<< Custom Key and Value
    },
```


## Static Route Config

**Features**
- Parse Static Routes: Extract and parse static routing commands (ip route entries) from Cisco running configurations.
- Convert to Python Objects: Represent these routes as structured Python objects, enabling programmatic manipulation and easy integration with Python-based tools.
- Export to JSON/Dict: Convert static routing information into JSON or dictionary format, making it straightforward to use in web applications, APIs, or data storage solutions.

#### Example

**Python Object:**
```python

>>> static = parser.get_static_config()
>>> for i in static:
        print(i.subnet, i.name, i.nexthop_ip)

0.0.0.0/0 MC-RS01 10.240.129.3
0.0.0.0/0 NC-RS01 10.240.129.11
10.243.98.32/28 P2P_Subnet 10.243.99.186
```

**Json/Dict:**
```python
static = parser.get_static_config()
[
    {
        "network": "0.0.0.0",
        "mask": "0.0.0.0",
        "nexthop_ip": "10.240.129.3",
        "subnet": "0.0.0.0/0",
        "vrf": "default",
        "name": "MC-RS01",
        "admin_distance": null
    },
]
```


## Dynamic Route Config

### EIGRP 

`eigrp_configs = parser.get_eigrp_config(return_json=True)`

```json
[
    {
        "as_number": 300,
        "network": [
            {
                "network": "10.242.96.240",
                "subnet_mask": "255.255.255.252",
                "wildcard_mask": "0.0.0.3"
            },
            {
                "network": "10.242.97.244",
                "subnet_mask": "255.255.255.252",
                "wildcard_mask": "0.0.0.3"
            },
            {
                "network": "10.242.98.248",
                "subnet_mask": "255.255.255.252",
                "wildcard_mask": "0.0.0.3"
            },
            {
                "network": "10.242.99.252",
                "subnet_mask": "255.255.255.252",
                "wildcard_mask": "0.0.0.3"
            }
        ],
        "vrf": "Global",
        "wild_card_mask": null,
        "subnet": null,
        "has_vrf": true,
        "vrf_count": 8,
        "passive_interface": null,
        "no_passive_interface": null,
        "auto_cost": null,
        "interfaces": null,
        "children": [
            "network 10.242.96.240 0.0.0.3",
            "network 10.242.97.244 0.0.0.3",
            "network 10.242.98.248 0.0.0.3",
            "network 10.242.99.252 0.0.0.3",
            "no passive-interface GigabitEthernet1/9",
            "no passive-interface GigabitEthernet1/10",
            "passive-interface default",
            "no auto-summary"
        ],
        "vrf_children": [
            {
                "vrf": "mgt100",
                "network": [
                    {
                        "network": "10.242.96.240",
                        "subnet_mask": "255.255.255.252",
                        "wildcard_mask": "0.0.0.3"
                    }
                ],
                "wild_card_mask": null,
                "subnet": null,
                "passive_interface": null,
                "no_passive_interface": null,
                "auto_cost": null,
                "interfaces": null,
                "children": [
                    "redistribute bgp 65240 metric 1000 100 255 1 1500 route-map MGT100_EIGRP_REDIST_BGP",
                    "network 10.242.96.240 0.0.0.3",
                    "passive-interface default",
                    "no passive-interface TenGigabitEthernet1/9.3131",
                    "distribute-list route-map route_map_inbound in",
                    "autonomous-system 300",
                    "exit-address-family"
                ]
            },
        ]
    }
    
]
```

### BGP Route Config:

**Example:**
`bgp_configs = parser.get_bgp_config(return_json=True)`

```json
[
    {
        "router_id": "10.240.129.45",
        "vrf_list": [
            "blu300",
        ],
        "vrf": "Global",
        "network": [
            "10.245.49.132/32"
        ],
        "peer_group": [
            {
                "peer_group": {
                    "name": "RR",
                    "remote_as": "65234",
                    "update_source": "Loopback1",
                    "route_map": {
                        "in": "PEER_GROUP_RR_INBOUND",
                        "out": "PEER_GROUP_RR_OUTBOUND"
                    },
                    "neighbors": [
                        {
                            "ip": "10.252.248.251",
                            "description": "RR-Router-01"
                        },
                    ]
                }
            },
        ],
        "neighbors": null,
        "redistribute": [
            {
                "vrf": "Global",
                "protocol": "eigrp 100",
                "route_map": ""
            }
        ],
        "vrf_children": [
            {
                "vrf": "blu300",
                "network": [
                    "10.245.17.132/32"
                ],
                "peer_group": null,
                "neighbors": [
                    {
                        "vrf": "blu300",
                        "ip": "10.245.20.30",
                        "remote_as": "65245",
                        "description": "REMOTE_ROUTER-SA01_BLU300",
                        "update_source": "TenGigabitEthernet10/14.3301",
                        "route_map": {
                            "in": "ALLVRF_BGP_RM_INBOUND",
                            "out": "ALLVRF_BGP_RM_OUTBOUND"
                        }
                    }
                ],
                "redistribute": [
                    {
                        "vrf": "blu300",
                        "protocol": "eigrp 252",
                        "route_map": " BLU300_BGP_REDIST_EIGRP"
                    },
                    {
                        "vrf": "blu300",
                        "protocol": "static",
                        "route_map": " BLU300_BGP_REDIST_STATIC"
                    }
                ],
            }
        ]
    }
]
```

### OSPF Route Config

In ospf, ConfigParser attemps to capture any interfaces that are participating in OSPF as well. 

**Example:**

`ospf = parser.get_ospf_config(return_json=True)`

```json
[
    {
        "process_id": "240",
        "router_id": "10.240.129.45",
        "network": [
            {
                "network": "10.3.3.0",
                "subnet_mask": "255.255.255.0",
                "wildcard_mask": "0.0.0.255",
                "area": "0"
            }
        ],
        "wild_card_mask": null,
        "subnet": null,
        "vrf": null,
        "passive_interface": [
            {
                "interface": "default"
            }
        ],
        "no_passive_interface": [
            {
                "interface": "GigabitEthernet1/0"
            }
        ],
        "auto_cost": "10000",
        "interfaces": [
            {
                "interface": "Loopback0",
                "area": "0",
                "process_id": "240"
            }
        ]
    }
]
```

## Custom Parsing

**Example:**
`custom_search = parser.get_parent_child(parent_regex="aaa.*", child_regex="server.*", return_json=True)`

```json

[
    {
        "parent": "aaa group server tacacs+ ISE_TACACS",
        "children": "server tacacs+ ISE_TACACS"
    }
]
```



## Future Enhancements
I am actively working on expanding the capabilities of this library. Upcoming features include:

- **Enhanced support for NXOS**: Additional parsing for NXOS-specific configurations and features.
- **Full support for IOS-XR**: Expanding coverage for IOS-XR configurations to include more advanced routing and service configurations.
- **More configuration sections**: Additional Cisco configuration types and attributes will be parsed in future releases.

Stay tuned for these updates and more in future versions of the library!



## Contribution
Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a feature branch.
3. Make your changes and add tests if applicable.
4. Submit a pull request for review.
5. Feel free to open an issue for any bug reports or feature requests.



## License
This project is licensed under the MIT License.

### Key Improvements:
1. **Title and Overview:** I emphasized the functionality of the library with clear mention of automation, parsing, and supported platforms.
2. **Key Features:** I made the features section clearer and more structured.
3. **Usage Example:** Added a usage example to make it easy for users to get started.
4. **Installation:** Provided simple installation instructions using `pip`.
5. **Contribution and License Sections:** These are standard in open-source projects and help potential contributors know how to get involved.
