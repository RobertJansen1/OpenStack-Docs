---
layout: page
tags: [DNS]
page_title: Managing DNS Records
---

Recordsets are used to define the DNS records for a zone. A recordset is a collection of records that
share the same name and type. For example, a recordset named `www.example.com` can contain records for
the `A` and `AAAA` record types. A recordset named `mail.example.com` can contain records for the `MX` record type.

For this guide we assume you have already created a DNS Zone, if you haven't done this yet please follow the the following tutorial: [Create a DNS Zone]({{ '/articles/create-a-dns-zone' | relative_url }})

## Create a Record Set
---
Creating a recordset in the OpenStack Dashboard is very easy, just follow the steps below.

**Step 1**: First Login on the OpenStack Dashboard and go to the `DNS` tab.  
**Step 2**: Click on the `Zones` tab.  
**Step 3**: Click on `Create Record Set` behind the zone you want to create a recordset in.  
**Step 4**: Select the type of record you want to create for this tutorials we create an A record.  
**Step 5**: Enter the `Name` for example `www.example.com.` (make sure you enter the full FQDN and that the record ends with a dot).  
**Step 6**: Enter the `Description` (not required).  
**Step 7**: Enter the `TTL` which stands for Time To Live, we recommend to set this to 3600 (one hour).  
**Step 8**: Enter a `Record` under `Records` for example 127.0.0.1. (You can create multiple with the `Add Record` button).  
**Step 9**: Click on the `Submit` button after which you recordset will be created.  

## Editing a Record Set
---
**Step 1**: First Login on the OpenStack Dashboard and go to the `DNS` tab.  
**Step 2**: Click on the `Zones` tab.  
**Step 3**: Click on the zone of which you want to edit the recordset.  
**Step 4**: Click on the `Record Sets` tab.  
**Step 5**: Click on the `Update` button behind the recordset you want to edit.  
**Step 6**: Edit the fields you want to edit (`Name`, `Description`, `TTL` or `Records`).  
**Step 7**: Click on the `Submit` button after which you recordset will be updated.

## Deleting a Record Set
---
**Step 1**: First Login on the OpenStack Dashboard and go to the `DNS` tab.  
**Step 2**: Click on the `Zones` tab.  
**Step 3**: Click on the zone of which you want to delete the recordset.  
**Step 4**: Click on the `Record Sets` tab.  
**Step 5**: Click on the small arrow button behind the recordset you want to delete.  
**Step 6**: Click on `Delete` after which you recordset will be deleted.  