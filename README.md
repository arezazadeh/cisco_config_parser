# ConfigParser
## This Package will parse the Cisco running-configuration File in a parent/child style

## Install the package 

`pip install ConfigParser-arezazadeh`

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

* Finding Routing Protocol
```ruby
    from ConfigParser import *
    
    
    my_file = "switch01_running_config.txt"
    parse = ConfigParser(my_file)
    
    
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
    from ConfigParser import *


    my_file = "switch01_running_config.txt"
    parse = ConfigParser(my_file)
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
