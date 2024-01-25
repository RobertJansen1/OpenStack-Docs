---
layout: page
tags: [Network]
page_title: Create an internal network
---

This tutorial guides you through the process of creating an internal network on. 
An internal network can be used to connect instances together without internet connectivity. 
If needed, an OpenStack router can be created to allow for internet connectivity and allow for associating floating IPs

---


## Creating an internal network
First we need to create an internal network. For this tutorial we will name it `internal-network`.  
However, feel free to assign a name of your choice to the network.

**Step 1**: Log in to the OpenStack dashboard and proceed to the `Network` tab.  
**Step 2**: Select `Networks` and then click on the `Create Network` button.  
**Step 3**: Enter the required details in the following fields:  
* **Network Name**: internal-network
* **Enable Admin State**: Should be marked
* **Create Subnet**: Should be marked
* **Availability Zone Hists**: Leave empty for now
* **MTU**: Leave empty for now

**Step 4**: Click on subnet and fill in the following fields:  
* **Subnet Name**: internal-subnet
* **Network Address Source**: Enter Network Address manually
* **Network Address**: 10.0.0.0/24
* **IP Version**: IPv4
* **Gateway IP**: 10.0.0.1
* **Disable Gateway**: Should be unmarked

**Step 5**: Navigate to Subnet Details and fill in the following information:  
* **DHCP Enabled**: Ensure this option is marked.  

Leave all other fields blank, then click on `Create`.  

## Creating a router
We'll proceed to create an OpenStack router. In this tutorial, we'll name it `internal-network-router`,  
indicating its connection to the `internal-network` network. However, feel free to name the router as per your preference.

**Step 1**: Navigate to the `Network` tab and select `Routers`.  
**Step 2**: Initiate the router creation process by clicking on the `Create Router` button.  
**Step 3**: Enter details in the following fields:  
* **Router Name**: internal-network-router
* **Admin State**: Should be marked
* **External Network**: Not required but recommended to set to floating IP network (Provides all instances in the network with internet connectivity)
* **Availability Zone Hists**: Leave empty for now
Press **Create Router**.

**Step 4**: Locate the router you've just created and click on the small arrow next to it. From the dropdown menu, select `Set Gateway`.  
**Step 5**: Opt for the net-float pool and confirm by clicking on `Set Gateway`.  
**Step 6**: Select the router you created and navigate to the `Interfaces` tab.  
**Step 7**: Begin adding an interface by clicking on `Add Interface`. Enter the required information in the following fields:  
* **Subnet**: internal-network (internal-subnet)
* **IP Address**: Leave empty for now

**Step 8**: Click on **Add Interface** to add the interface.  
