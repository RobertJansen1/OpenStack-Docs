---
layout: page
tags: ["Migrations"]
page_title: FaQ Migrations
---

# FaQ Migrations



Below you will find answers to the most frequently asked questions.

-----

## How can I prepare my instances for this migration?

  * Shutdown your instance, and start it up again prior to the migration to see if the instance starts up gracefully without interruption or error messages (a reboot won't be sufficient).
  * Make sure that cloud(base)-init is disabled before you start the migration.
  * Perform a file-system check of all file-systems prior to migration.
  * Please make sure your system has no pending updates, so that there won’t be any interruption of installing patches during the migration (as this might be prematurely interrupted).

-----

## TL;DR, can you give me a short summary?

  * Your instance will be migrated to a boot-from-volume instance.
  * If you have a floating IP we will migrate it.
  * We have created a new project for you on the new platform.
  * If you use custom images or a snapshot to boot your instance from, we will migrate those glance images as well.
  * If you have connected your instance to an internal network, we will extend that network into ams2.
  * If you have a router for internet access on your network the public IP will change.
  * If you have volumes attached to your instance, we will copy them to the new platform.
  * If you have any snapshots on those volumes, those will be lost.
  * If you do not disable cloud-init your SSH host key will change when migrating towards ams2.
  * On Windows guests the admin password will be changed if cloudbase-init was not disabled.
  * We will use ICMP ping to determine if your instance is up and running, please prepare your instance accordingly.
  * If you have a HA setup, there are some caveats

-----

## Not all my instances have the migration metadata, what’s the reason?

There are some impedements we are still resolving before we can migrate all instances to our new region

  * If your instance uses volumes larger or equal then 1024GByte, this instance needs to be migrated on a thight schedule to minimize the impact of the migration.
  * If your instance makes use of load balancing, we currently cannot automatically migrate your instance. 
  * If your instances are in a large internal network, we will migrate your instances later
  * HA / vrrp setups are not migrated yet
  * internal networks with custom routers are not migrated yet

-----

## Will our SSH keys be migrated?

Yes they will, your SSH keys wil be copied to the ams2 platform.

-----

## My instance is not running as expected after migration, can I perform a roll-back?

Yes, when the migration was a successfull, you can perform a rollback by setting metadata rollback-now on your instance within the legacy Horizon dashboard. Please let us know why you performed a rollback, as we'd like to improve our process to prevent this roll-back in the future.
Note: all changes made on the new instance will not be migrated back and should be considered lost. A roll-back is available in the first 5 days after the migration.

-----

## If I already have instances named equally in the ams2 platform, will they be overwritten?

No, we will not overwrite anything in ams2.

-----

## What will be the expected downtime during the migration?

  * We've seen instances with downtime of less then a minute, but for safety reasons you should consider up to 15 minutes (The migration depends on the amount of time to boot up the instance and start of all services)
  * Our tests indicate that downtime could be as less as 40 seconds during minimal load on your instance. A gracefull shutdown will be initiated using the OpenStack API's. A new instance is then spawned and created on ams2, with a copy of the disk. The process will monitor the startup time and if it exceeds 10 minutes, we will automatically initiate a rollback.
  * If the instance is attached to an internal network it's connection will be lost for 5 minutes. This connection is needed to synchronize the internal network between the legacy platform and ams2.
  * When the migration is finished and your instance is booted up succesfully within ams2 please include an additional 10 minutes for the internal network to become ready.
  * If the internal network doesnt respond within 20 minutes after the migration has been finished please contact support and initiate a rollback of your instance.

-----

## Will migration of an instance affect my other operational instances?

Unless you have created a dependency on that instance, your other instances will not be affected.

-----

## How can I initiate the migration myself?

When your instance is flagged for migration, additional metadata is added to your instance named migrate-scheduled-YYYY-MM-DDTHH:MM:SS. You can schedule the migration by changing the date / time (times are in UTC!) to your preference. A date / time in the past will start a migration as soon as a migration slot is available (mostly within a minute).
Alternatively you can set metadata migrate-now.

-----

## What will happen when I don’t start or schedule the migration myself?

Your instance will be migrated during office hours (9:00-16:00 CET) on the date we communicated by e-mail, and set in the metadata.

-----

## Can I migrate outside office hours?

Yes, by scheduling the migration using the provided metadata (see [How can i initiate the migration myself](#how-can-i-initiate-the-migration-myself))

-----

## What will happen if the migration fails?

If the migration fails, your instance will be started again on the current OpenStack platform. We will investigate the cause of the failure and get in contact to schedule a retry.

-----

## How can i see if the migration was successful?

If the migration was successful, the instance will reach a 'MIGRATED' state. This can be verified via either the OpenStack Legacy API or in the Horizon dashboard.

-----

## Where can i manage my migrated instance?

Your migrated instance can be managed through our Horizon dashboard, accessible through the Control Panel.

-----


## My instance is connected through an internal network to my other instances, does this still work after migration?

Yes, your internal network will be expanded into the ams2 region.

-----

## I don’t have any projects in ams2, do I have to create a new one?

No, if you don’t have any projects created in our ams2 region, we have already created a project for your convenience.

-----

## I have multiple projects in ams2, can you migrate my current resources to my existing project?

Yes, please contact support with the project mapping(s) you'd want us to use, so that we can configure it accordingly.

-----

## What happens with snapshots attached to my volumes?

Those will be lost, as we are unable to duplicate snapshots from the legacy to the new platform. When you want to save a snapshot of your volume, create a new volume with the snapshot as source. This can be done in Horizon: Volumes \> New Volume \> Clone an exisiting volume, here you select the volume where you want to clone the snapshot from and you can select the snapshot itself.

-----

## Are glance images (snapshots/custom images) also imported into ams2?

Yes, but only if the image is still available (not deleted).

-----

## Do I keep my current IP addresses?

Yes, all of your public and internal IP addresses will be migrated. IP numbers ending with 1 or 2 can’t be used cause the IP numbers are reserved for internal use. If your instance uses one of those ip addresses, they will be changed during the move. The mac address will remain the same, so please configure network device to use DHCP.

-----

## I would like to migrate all my resources ASAP, is that possible?

We are continously working on resolving impedements that might block some migrations, you can contact support to validate if your instances can already be migrated.

-----

## Will i still be billed for my migrated resources in the old platform?

When the first migration is started we will bill your current resources untill we migrated all of your project's resources. When all resources in your project are migrated, we will start billing your resources from ams2 and stop billing from the legacy platform.

-----

## Will my SSH host key change if cloud-init is enabled?

Yes, the migration from the legacy platform to ams2 will result in a new UUID and name for your instance. Due to the way cloud-init works by default, this will result in cloud-init to re-initialise your system as if it was newly spawned. This will also cause your SSH kost key to be renewed. If you dont want this, please disable cloud-init before the migration to the ams2 region starts.

-----

## What flavor will my new instance get?

We have carefully selected ams2 flavors that match the specifications and price of your OpenStack Legacy flavor as closely as possible. See the following table how flavors are matched.

| Openstack Legacy | ams2 |
| --- | --- |
| m1.tiny           | Small HD 2GB |
| m1.small          | Standard 4GB |
| m1.medium         | Small HD 8GB |
| m1.xlarge         | Small HD 32GB |
| m1.large          | Small HD 16GB |
| m1.tiny.windows   | Standard 1GB |
| m1.small.windows  | Standard 4GB |
| m1.medium.windows | Small HD 8GB |
| m1.large.windows  | Small HD 16GB |
| m1.xlarge.windows | Small HD 32GB |
| vps.1             | Standard 1GB |
| vps.2             | Standard 4GB |
| vps.3             | Medium HD 8GB |

-----

