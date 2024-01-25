---
layout: page
tags: [Network]
page_title: Rent an IP range
---

# Rent an IPv4 range team.blue

Within some of the team.blue / TransIP / Combell OpenStack regions, it is possible to rent a dedicated IPv4 public IP range. 
As a dedicated IPv4 range is an expensive resource, they need to share the network with your project first. 


## Create the network
**Step 1**: Ask support to share the BYoIP subnetpool to your project (provide them with your project ID)
**Step 2**: Log in to the OpenStack dashboard and proceed to the `Network` tab.  
**Step 3**: Select `Networks` and then click on the `Create Network` button.  
**Step 4**: Enter the required details in the following fields:  
* **Network Name**: customer-public
* **Enable Admin State**: Should be marked
* **Create Subnet**: Should be marked
* **Availability Zone Hints**: Leave empty for now
* **MTU**: Leave empty for now

**Step 4**: Click on `Subnet` and fill in the following fields:  
* **Subnet Name**: customer-public-subnet
* **Network Address Source**: "Allocate Network Address from a pool"
* **Address Pool**: select `byoip-ipv4` or `byoip-ipv6` depending on the IP version you want to use
* **Network Mask** select an appropriate subnet, be aware, the larger the network, the more expensive it will be (IPv6 is free).

**Step 5**: Navigate to `Subnet Details` and fill in the following information:  
* **DHCP Enabled**: Ensure this option is marked.  
* **DNS Name Servers**: Configure DNS servers for DHCP to hand out.
* Leave all other fields blank, then click on `Create`.  

**Step 6**
* In the background, the network will be fine-tuned and configured. This should be done within 5 minutes, if not, you should contact support.

### Dual-Stack IPv4 and IPv6
- When both an IPv4 and IPv6 address pool are added, an IPv4 and an IPv6 address will be allocated for each port created.


## Delete the network
**Step 1**: To delete the network, the network gateway needs to be disconnected first
* Delete all ports connected to the network
* This can be done by removing ports from instances, or by removing instances  

**Step 2** Within Horizon, go to networks > network > "Your rented network" > subnets  
**Step 3** Edit every subnet and select "Disable Gateway" (Within several seconds, but at most 5 minutes, your subnet will be disconnected)   
**Step 4** Delete the subnets  
