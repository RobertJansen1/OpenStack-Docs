---
layout: page
tags: [Loadbalancers]
page_title: Create a loadbalancer with webservers
---

This tutorial guides you through the process of creating a load balancer with webservers functioning as backend servers.  
If you have already configured a network, a router, and webservers, you have the option to skip ahead to the `Creating the loadbalancer` section.  
However, for a comprehensive understanding, we recommend reading through the entire tutorial.

---

## Setting up an OpenStack network
Before diving into the creation of a load balancer, it's essential to configure an internal OpenStack network.  
This involves creating an internal network, an internal subnet, and an OpenStack router. If your network is  
already set up, you can skip this initial configuration and proceed directly to the `Creating the webservers` section.

### Creating an internal network
First we need to create an internal network. For this tutorial we will name it `webserver-network`.  
However, feel free to assign a name of your choice to the network. 
We will connect the network to a router and connect the router to the floating IP network.

In the article below you can find a step by step guide on how to create an internal network: please
replace the name of the network with `webserver-network` and the name of the subnet with `webserver-subnet`.  

[Create an internal network]({{ '/articles/create-an-internal-network' | relative_url }})

---

## Creating the webservers
For this tutorial, we'll set up three webservers. Feel free to adjust the number of webservers according  
to your needs, or you can skip this section entirely if you already have webservers operational.  

For this tutorial assumes three instances are created. you can use the following tutorial combined with the specs below:

[Create instances]({{ '/articles/create-instances' | relative_url }})


On the **Details** tab:  
* **Instance Name**: webserver
* **Description**: Webserver for my cool website
* **Availability Zone**: Leave empty or choose an availability zone to your liking
* **Instance Count**: 3

On the **Source** tab:  
* **Select Boot Source**: Image
* **Create New Volume**: No
* **Image Name**: Ubuntu 22.04 LTS

On the **Flavor** tab:  
* **Flavor**: Standard 1GB

On the **Networks** tab:  
* **Network**: webserver-network

On the **Security Groups** tab:  
* **Security Group**: allow-web

On the **Configuration** tab:  
* Paste the following code into the `Customization Script` field to update packages and install Apache2 on the webservers:  

```cloud-config
#cloud-config
package_upgrade: true
packages:
  - apache2
  - php
  - libapache2-mod-php
write_files:
  - path: /var/www/html/index.php
    content: |
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Loadbalancer Tutorial</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
      </head>
      <body>
          <div class="container mt-5">
              <div class="card">
                  <div class="card-header">
                      Hostname Information
                  </div>
                  <div class="card-body">
                      <h5 class="card-title">Server Hostname</h5>
                      <p class="card-text"><?php echo gethostname(); ?></p>
                  </div>
              </div>
          </div>
      </body>
      </html>
runcmd:
  - systemctl restart apache2

```


---

## Creating the loadbalancer
Now we can create the loadbalancer. We will create a loadbalancer with a listener, a pool and a healthmonitor.

**Step 1**: Navigate to the `Network` tab and select `Load Balancers`.  
**Step 2**: Initiate the process by clicking on the `Create Load Balancer` button.  
**Step 3**: Enter details in the following fields:  
* **Name**: webserver-loadbalancer
* **IP Address**: Leave empty for now
* **Description**: Loadbalancer for our webservers
* **Availability Zone**: Leave empty or choose an availability zone to your liking
* **Flavor**: Choose a flavor to your liking for this tutorial we use the Medium flavor
* **Subnet**: webserver-subnet

**Step 4**: Proceed to the `Listener` tab by clicking on `Next`.  
**Step 5**: Complete the following fields:  
* **Name**: webserver-listener-http
* **Description**: HTTP Listener for our webservers
* **Protocol**: HTTP
* **Protocol Port**: 80
* **Admin State Up**: Yes
Leave all others options as they are for now.

**Step 6**: Proceed to the `Pool Details` tab by clicking on `Next`.  
**Step 7**: Enter information in the following fields:  
* **Name**: webserver-pool-http
* **Description**: HTTP Pool for our webservers
* **Algorithm**: Least connections
* **Session Persistence**: Leave None
* **TLS Enabled** No
* **Admin State Up**: Yes

**Step 8**: Proceed to the `Pool Members` tab by clicking on `Next`.  
**Step 9**: Identify the instances you wish to include and click on `Add` for each.  
**Step 10**: Enter the designated port for the host (80) and set the weight (1). Repeat this step for all webserver hosts you're adding.  

**Step 11**: Navigate to the `Health Monitor` tab by clicking on `Next`.  
**Step 12**: Complete the following fields:  
* **Name**: webserver-healthmonitor-http
* **Type**: HTTP
* **Max Retries Down**: 3
* **Delay**: 5
* **Max Retries**: 3
* **Timeout**: 5
* **HTTP Method**: GET
* **Excepted Codes**: 200
* **URL Path**: /
* **Admin State Up**: Yes

**Step 13**: Initiate the creation of your load balancer by clicking on `Create Load Balancer`.  
**Step 14**: Locate the load balancer you've just set up and click the small arrow beside it. From the dropdown menu, select `Associate Floating IP`.  
**Step 15**: Select an available floating IP or choose the net-float pool, then confirm your choice by clicking on `Associate`.  
**Step 16**: Await the update of the load balancer's Operating Status to ONLINE. Once this status is achieved, navigate to `http://<floating-ip>` in your web browser to witness your load balancer functioning.  

If you want to customize your Loadbalancer even further we highly recommend you to read the [OpenStack Octavia Loadbalancer documentation](https://docs.openstack.org/octavia/latest/user/index.html)