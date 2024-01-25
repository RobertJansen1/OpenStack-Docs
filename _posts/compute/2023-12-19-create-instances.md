---
layout: page
tags: [Compute]
page_title: Create an instance
---

This tutorial guides you through the process of creating a set of web servers on an existing internal network.
The instancess will run an apache2 server and host a basic webpage with the instance hostname.


---

## Prerequisites

  This tutorial assumes an internal network is created that is connected to a router with an external gateway.
You can create a network like this with the [Create an internal network]({{ 'articles/create-an-internal-network' | relative_url }}) tutorial.

  At least one public key is added to your project for ssh authentication

---

## Creating instances
For this tutorial, we'll set up three instances in a single availability zone. Feel free to adjust the number of instances according to your needs.

**Step 1**: Access the `Compute` tab and select `Instances`.  
**Step 2**: Initiate instance creation by clicking on the `Launch Instance` button.  
**Step 3**: Provide the required information in the following fields:  
* **Instance Name**: webserver
* **Description**: Webserver for my cool website
* **Availability Zone**: Leave empty or choose an availability zone to your liking
* **Instance Count**: 3

**Step 4**: Navigate to the `Source` tab and enter the necessary information in the following fields:  
* **Select Boot Source**: Image
* **Create New Volume**: No
* **Image Name**: Ubuntu 22.04 LTS

**Step 5**: Choose a suitable flavor by clicking on the `Flavor` tab. For this tutorial, select the Standard 1 GB flavor.  
**Step 6**: Select your network by clicking on the `Networks` tab. For this tutorial, we select net-public  
**Step 7**: Add necessary security by clicking on the `Security Groups` tab and selecting the `allow-remote-access` security group.  
**Step 8**: Assign a key pair by clicking on the `Key Pair` tab. Select a key pair of your preference, or create or upload one here if you don't have one.  
**Step 9**: Configure your setup by clicking on the `Configuration` tab. Custom cloud-init scripts can be put in to spawn a preconfigured instance. We will cover this in a later tutorial

> We recommend spreading your instances across multiple availability zones to ensure high availability.
