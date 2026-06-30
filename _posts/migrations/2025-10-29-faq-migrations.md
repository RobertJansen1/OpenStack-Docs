---
layout: page
tags: ["Migrations"]
page_title: Migrations FAQ
---

# Migrations FAQ


Below you will find answers to the most frequently asked questions.


## How can I prepare my instances for this migration?

  * Shutdown your instance, and start it up again prior to the migration to see if the instance starts up gracefully without interruption or error messages (a reboot won't be sufficient).
  * Make sure that cloud(base)-init is disabled before you start the migration.
  * Perform a file-system check of all file-systems prior to migration.
  * Please make sure your system has no pending updates, so that there won’t be any interruption of installing patches during the migration (as this might be prematurely interrupted).


## TL;DR, can you give me a short summary?

  * Your instance will be migrated to a new region.
  * If you have a floating IP we will migrate it.
  * We will enable your project on the new platform.
  * If you use custom images or a snapshot to boot your instance from, we will migrate those glance images as well.
  * If you have connected your instance to an internal network, we will extend that network into the new region.
  * If you have a router for internet access on your network the public IP will change.
  * If you have volumes attached to your instance, we will copy them to the new platform.
  * If you have any snapshots on those volumes, those will be lost.
  * If you do not disable cloud-init your SSH host key will change when migrating towards the new region.
  * On Windows guests the admin password will be changed if cloudbase-init was not disabled.
  * Windows instances might require reactivation of the license as the hardware of the VM is replaced
  * We will use ICMP ping to determine if your instance is up and running, please prepare your instance accordingly.
  * We will check commonly used ports (like port 22, 80, 443, etc).
  * If you have a HA setup, there are some caveats.
  * Load balancers will be migrated once all instances have been migrated and will have some minutes of downtime.
  * For HEAT stacks, we will only migrate resources, not the stacks. 
  * The region and availability zones will change name, updates to configuration files is needed.
  

## Not all my instances have the migration metadata, what’s the reason?

We're finalizing the last steps to enable the migration of all instances to the new region

  * HA / vrrp setups will be migrated at a later stage.
  * internal networks with custom routers will be migrated at a later stage.
  * Other configurations of your instance or the platform can limit the migration. those limitations will be resolved at a later phase.


## Will our SSH keys be migrated?

Yes they will, your SSH keys will be copied to the new region but only for the instance (it will not be migrated to your user).


## My instance is not running as expected after migration, can I perform a roll-back?

Yes, once the migration has been successfully completed, you can perform a rollback by setting the metadata key `rollback-now` on your instance within the legacy Horizon dashboard.

If you do perform a rollback, please let us know the reason. We're keen to understand what went wrong so we can improve the process and avoid similar situations in the future.

> **Note**: Any changes made on the new instance will not be carried back and should be considered lost. A rollback is only available within the first 5 days after the migration.


## If I already have instances named equally in the new region, will they be overwritten?

No, we will not overwrite anything in the new region.


## What will be the expected downtime during the migration?

  * We've seen instances with downtime of less than a minute, but for safety reasons you should consider up to 15 minutes (The migration depends on the amount of time to boot up the instance and start all services)
  * Our tests indicate that downtime could be as little as 40 seconds during minimal load on your instance. A graceful shutdown will be initiated using the OpenStack APIs. A new instance is then spawned and created in the new region, with a copy of the disk. The process will monitor the startup time and if it exceeds 10 minutes, we will automatically initiate a rollback.
  * If the instance is attached to an internal network its connection will be lost for up to 10 minutes. This connection is needed to synchronize the internal network between the legacy region and the new region.
  * When the migration is finished and your instance is booted up successfully within the new region please include an additional 10 minutes for the internal network to become ready.
  * If the internal network doesn't respond within 20 minutes after the migration has been finished please contact support and initiate a rollback of your instance.
  * Load balancers will have up to 5 minutes of downtime, as the load balancer needs to be recreated in the new region.


## Will migration of an instance affect my other operational instances?

Unless you have created a dependency on that instance, your other instances will not be affected.

## What will happen with Load Balancers during migration?
All load balancers will be migrated once all instances have been migrated. During the migration of the load balancer there will be some minutes of downtime, as the load balancer needs to be recreated in the new region. The migration of the load balancer will start automatically once all instances have been migrated and will be on the same day as the last instance migration of your project. Load balancers will be converted to Octava load balancers during migration and will have the flavor 'Small' assigned. We expect the performance to be similar to or better than the current load balancer performance.

## What will happen with HEAT stacks during migration?
To prevent errors and unexpected behaviour, all instances in a HEAT stack will be migrated to the new platform as seperate resources. HEAT configurations will be removed from the old platform after the migration is finished. If you want to keep using HEAT on the destination region, we ask you to create a new heat stack with instances and migrate your data and configurations yourself.


## How can I initiate the migration myself?

When your instance is flagged for migration, additional metadata is added to your instance named `o2o-scheduled-YYYY-MM-DDTHH:MM:SS`. You can schedule the migration by changing the date / time (times are in the europe/amsterdam timezone!) to your preference. A date / time in the past will start a migration as soon as a migration slot is available (normally within a minute).
Alternatively you can set metadata `o2o-migrate-now` on the metadata key `migrate_flag`.  

To set or change the metadata of your instance, go to the Horizon interface Project > Compute > Instances. Click the more options triangle next to the instance and choose `Update Metadata`. 

<img class="rounded border border-dark" src="{{ '/assets/images/2025-10-29-faq-migrations/instance_update_metadata.png' | relative_url }}" width="auto" height="600" />

Open `Provider platform options` > `Migration` and Click `+` on `Scheduling options`. Update the date/timestamp to your liking and click `Save`  

<img class="rounded border border-dark" src="{{ '/assets/images/2025-10-29-faq-migrations/add_metadata.png' | relative_url }}" width="auto" height="400" />


## What will happen when I don’t start or schedule the migration myself?

Your instance will be migrated during office hours (9:00-17:00 Europe/Amsterdam timezone) on the date we communicated by e-mail, and set in the metadata.


## Can I migrate outside office hours?

Yes, by scheduling the migration using the provided metadata (see [How can I initiate the migration myself](#how-can-i-initiate-the-migration-myself))


## What will happen if the migration fails?

If the migration fails, your instance will be started again on the current OpenStack platform. We will investigate the cause of the failure and inform you about a new migration date.


## How can I see if the migration was successful?

If the migration was successful, the instance will reach a 'SHUTOFF' state. This can be verified via either the OpenStack Legacy API or in the Horizon dashboard. The instance will be locked. The progress of the migration can be monitored through metadata key `_export_progress`


## Where can I manage my migrated instance?

Your migrated instance can be managed through the new Horizon dashboard, accessible through the Control Panel.


## My instance is connected through an internal network to my other instances, does this still work after migration?

Yes, your internal network will be expanded into the new region.

## I don’t have any projects in new region, do I have to create a new one?

No, if you don’t have any projects created in our new region, we will enable your project in the new region.

## I have multiple projects in the new region, can you migrate my current resources to my existing project?

Yes, please contact support with the project mapping(s) you'd want us to use, so that we can configure it accordingly.

## What happens with snapshots attached to my volumes?

Those will be lost, as we are unable to duplicate snapshots from the legacy to the new platform. When you want to save a snapshot of your volume, create a new volume with the snapshot as source. This can be done in Horizon: Volumes \> New Volume \> Clone an existing volume, here you select the volume where you want to clone the snapshot from and you can select the snapshot itself.

## Are glance images (snapshots/custom images) also imported into the new region?

Yes, but only if the image is still available (not deleted).

## Do I keep my current IP addresses?

Yes, all of your public (floating) and internal IP addresses will be migrated.

## What will happen when I have a floating IP address without a router?

Unfortunattely, the AMS region no longer supports the creation of a floating IP without a router. We will create a router for every network where floating IPs are created without a router, and connect it to the floating network. An additional Public IPv4 address will be added to your new bill.

## I have OpenStack cmd tools / terraform / other tools configured, what do i need to do?
When using API tools, you need to add or change the region to your configuration files. You can find a manual on ho wto configure CLI tools at: [Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

## I would like to migrate all my resources ASAP, is that possible?

We are continuously working on resolving impediments that might block some migrations. You can contact support to validate if your instances can already be migrated.

## Will I still be billed for my migrated resources in the old platform?

We will stop billing for migrated resources as soon as the instance is shut down on the old platform. Instances on the new platform will be billed as soon as they are created. 

## What will happen with my Windows license?

When your virtual machine is migrated, a new virtual machine is created on our destination platform. Windows will detect this new hardware automatically and configure the operating system appropriately. After the migration, it is possible your virtual machine needs to re-activate its license. To verify if your license is properly activated, please go to Windows System settings -> Activation -> Troubleshoot or Activate to verify activation or re-activate your license.

## Will my SSH host key change if cloud-init is enabled?

Yes, the migration from the legacy platform to the new region will result in a new UUID and name for your instance. Due to the way cloud-init works by default, this will result in cloud-init to re-initialise your system as if it was newly spawned. This will also cause your SSH host key to be renewed. If you don't want this, please disable cloud-init before the migration to the new region starts.

## What flavor will my new instance get?

The flavors between the old region and the new one are the same.

-----

