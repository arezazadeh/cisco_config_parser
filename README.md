# ConfigParser
## This Package will parse the Cisco running-configuration File in a parent/child style

## Install the package 

`pip install ConfigParser-arezazadeh`

## Examples:

* Finding Routing Protocol
```
    from ConfigParser import *
    
    
    my_file = "switch01_running_config.txt"
    parse = ConfigParser(my_file)
    
    
    obj_list = parse.find_parent_child("^router")
    for i in obj_list:
        print(i.parent)
        for child_obj in i.child:
            print(child_obj)
 
 ```
 * Finding Interface and Helper address Example 
```

    from ConfigParser import *


    my_file = "switch01_running_config.txt"
    parse = ConfigParser(my_file)
    

    for i in obj_list:
        vlan_200 = re.search("Vlan200", i.parent)
        if vlan_200:
            print(i.parent)
            for c_obj in i.child:
                if str(c_obj).startswith("\s+ip helper"):
                    print(str(c_obj))
```
