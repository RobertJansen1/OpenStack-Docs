---
layout: page
tags: [Network]
page_title: Use multiple public ip's on one instance
---

This tutorial guides you through using multiple public ip addresses on an instance.
Because in OpenStack there are multiple subnets, it's possible you get 2 ip addresses, in different subnets.
This causes you to have multiple default gateways.

## Introduction
The reason this is a problem is as followed:
Let's say you have 3 interfaces, all with a public ip address. Let's call them A, B and C.

A is the main interface, it's your default gateway. Traffic from interface A will be all fine.
But now, we want to do something with interface B, our second IP address.

As A has the default gateway, interface B will try to send packets over the default gateway of A.
Interface A will then say: "No." and the packet will be dropped. Causing you to not have a connection from your second IP address.

We can fix this using a routing table per interface.


**If you use a floating IP address, the situation describe above is not a problem and it should work without doing this.**
**If you get two IP addresses that are within the same subnet, this should also not become a problem**

---

## First create your ports, for your ip addresses and attach them to your instance
**Step 1**: Log in to the OpenStack dashboard and proceed to the `Network` tab.
**Step 2**: Select `Networks` and then click on the `net-public` network. Verify you are in the `ports` tab.
**Step 3**: Click on `Create Port` and enter the required details in the following fields:
* **Enable Admin State**: Should be marked
* **Device ID**: Leave empty for now
* **Device Owner**: Leave empty for now
* **Specify IP address or subnet**: SUBNET should be selected
* **Subnet**: Select the IPv4 network
* **MAC Address**: Leave empty for now
* Repeat this until you have enough interfaces for your instance.
* Make sure the security group is set as expected. It does need to allow traffic to work for you.

**Step 4**: Proceed to the `Compute` tab, go to your preferred instance and attach your ports that you just created.

## Add the interfaces in the VM

**Before doing this, make sure to give your vm a hard reboot, so all of the interfaces have their rightfull place in the vm**

For example on Ubuntu in /etc/network/interfaces:
Use inet for IPv4 and inet6 for IPv6
If you want you can change the metric per interface, the higher the metric, the lower the priority.
10 is less important than 1.

Make sure to add all interfaces to this configuration.
```
allow-hotplug <interface>
 iface <interface> <inet/inet6> dhcp
 metric 1
```

## Add the routing tabbles

**Step 1**: Open the `/etc/rc.local` file in your vm and add the following lines:
```
ip route add default via <default gateway (visible in subnet overview)> dev <interface> table out-<interface>
ip rule add from <your ipv4 address>/32 lookup out-<interface>
```
**Make sure to add this for all your interfaces**

After a reboot all should work as expected.
