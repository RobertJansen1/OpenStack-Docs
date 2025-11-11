---
layout: page
tags: ["Migrations"]
page_title: HA Migrations
---

# HA Migrations

## \<a id="ha-setup"\>\</a\> I have created a HA setup with VRRP / keepalived / CARP, how do i migrate?

With the assumpion that you've created a HA setup, where you'd want as little downtime with this migration as possible, this dedicated section has been created to provide extra insights of how to prepare for this migration.

*Requirements:*

  * A setup with at least 2 instances (from now on referred to as the load balancers).
  * One or more Floating IP(s) assigned to one or more OpenStack network ports (referred as HA IP(s)).
  * The internal IP(s) which are associated with the HA IP(s) are configured as vip through keepalived / VRRP / CARP.
  * Keepalived / VRRP / CARP is healthy, started and is configured to auto start upon boot of your instance.

*Migration steps:*

Migrate your primary load balancer to OpenStack 2.0:

  * Network settings are reproduced and the disk contents will be migrated to the OpenStack 2.0 platform.
  * After the disk storage migration, this primary load balancer in OpenStack 1.0 will be powered off.
  *   - Upon shutdown, the HA IP will be served from the secondary load balancer in OpenStack 1.0.
  * The new loadbalancer in OpenStack 2.0 will be started and validated.
  * After successfull validation, the HA IP(s) will be migrated to OpenStack 2.
  *   - Now, the load balancer setup in OpenStack 1.0 is obsolete, regardless of keepalived state on the secondary load balancer. Both load balancers will appear primary of the HA IP, but from that point on, the OpenStack 2.0 environment will act as the primary environment.

Migrate your secundary keepalived instance to OpenStack 2.0:

  * After the migration process, we will automatically add this instance to the setup and your configuration is highly available again.

*Known caveats:*

  * As the VRRP protocol is blocked between both platforms, it is not possible to roam your HA IP between OpenStack 1.0 and OpenStack 2.0.

*Rollback options:*

  * When you have 2 load balancers, one in OpenStack 1.0 and one in OpenStack 2.0, a rollback of the HA IP can be performed by shutting down the load balancer in OpenStack 2.0. When the instance is shut off again, the HA IP's will be active in OpenStack 1.0.

To read more about creating a HA-IP in the OpenStack 2.0 platform, [please read this article](/knowledgebase/entry/2825).

-----