---
layout: page
tags: [DNS]
page_title: Create a DNS Zone
---

When creating an Floating IP or an Port with an external network a reverse DNS entry is automatically created.  
The default reverse DNS entry might not be what you want, so you have the ability to change it in the OpenStack Dashboard.

## Create the DNS Zone
---
If you want to change your reverse DNS for a floating IP, you can do this in the OpenStack Dashboard.

**Step 1**: First Login on the OpenStack Dashboard and go to the `DNS` tab.  
**Step 2**: Click on the `Zones` tab.  
**Step 3**: Click on the `Create Zone` button.  
**Step 4**: Enter the zone `Name` for example cloudtutorials.eu. (make sure the domain ends with a dot).  
**Step 5**: Enter the `Description` (not required).  
**Step 6**: Enter an `Email Address` (be aware the email will be shown publicly in the SOA record).  
**Step 7**: Make sure the `Type` is set to `Primary`.  
**Step 8**: Click on the `Create Zone` button after which you zone will be created.

> Note: When creating a new zone in your project it might take a few minutes before it is resolvable from the outside world.

## Retrieve the Nameservers for the DNS Zone
---
**Step 1**: First Login on the OpenStack Dashboard and go to the `DNS` tab.  
**Step 2**: Click on the `Zones` tab.  
**Step 3**: Click on the zone of which you want to retrieve the Nameservers.  
**Step 4**: Click on the `Record Sets` tab.  
**Step 5**: Find the `NS - Name server` type (The `Records` of this entry are the nameservers normally something like `ns1.*` and `ns2.*`).  
**Step 6**: Copy the `Records` of the `NS - Name server` type.  
**Step 7**: Go to your domain registrar and change the nameservers to the ones you copied in the previous step.  
**Step 8**: Wait for the nameserver change to propagate (this can take up to 24 hours).  
