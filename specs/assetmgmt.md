
# new objects

## itenvironment

- name
- description 
- location (as markdown)
- state (NEW, INSTALLING, OK, ERROR, PAUSE)
- owners (can be more than 1) (*)
- tasks
- links
- comments
- messages
- devices

linked to
- contacts (*)
- companies (*)
- projects (*)

## device

- name
- description 
- techid (str, is to describe some technical identification)
- category
- cost
- currency
- vendor (is link to a company, optional)
- location (as markdown)
- state (NEW, INSTALLING, OK, ERROR, PAUSE)
- tasks
- links
- comments
- messages
- components (list)
- istemplate (boolean)
- ports (list)
- connections (list)

## port
- name
- description
- type (ethernet, bridge, vxlanbridge, serial)
- connections (list)
- netaddresses (list)

## component

- name
- description 
- category
- cost
- currency
- techid (str, is to describe some technical identification)
- vendor (is link to a company)
- location (as markdown)
- state (NEW, INSTALLING, OK, ERROR)
- tasks
- links
- comments
- istemplate (boolean)

## netaddress

- description (normally empty)
- type (OOB, MGMT, PUB, OVERLAY): auto filled in when network range selected
- techid (str, is to describe some technical identification)
- state (NEW, OK, DOWN)
- ipaddr (ipv4 or 6 addr)
- networkrange (link and only 1)

## networkrange

- description
- type (OOB, MGMT, PUB, OVERLAY)
- techid (str, is to describe some technical identification)
- state (NEW, OK, DOWN)
- ipv6 (boolean)
- range e.g. 192.168.10.0/24
- gateway e.g. 192.168.10.254

## connection

- name
- description
- type (zerotier, vlan, lan, vxlan, serial, power,ethernet)
- techid (str, is to describe some technical identification)
- devices (list): devices connected to this connection (if no port)
- ports (list): ports connected to this connection
- networkranges  (list)
- state (NEW, OK, DOWN)




# remarks

## how to link objects

the more than 1 fields (see *) are done as in
![image](https://user-images.githubusercontent.com/6021844/30523815-854335da-9be8-11e7-833d-6d148adbd479.png)


