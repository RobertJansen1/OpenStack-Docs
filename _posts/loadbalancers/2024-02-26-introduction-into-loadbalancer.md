---
layout: page
tags: [Loadbalancers]
page_title: Introduction into loadbalancer 
---

In this article, the basic concept of OpenStack Octavia loadbalancers are explained. this includes
the uses, options, benefits and how to create a loadbalancer.

## Introduction
Loadbalancers can be an essential part of a cloud infrastructure. Loadbalancers can be used to
distribute the incoming traffic to multiple servers. This can in turn increase the availability of
the servers and the applications. OpenStack Octavia is a loadbalancer service that provides
loadbalancing services to the OpenStack cloud. Octavia is a on-demand and reliable
loadbalancer service. Octavia is a replacement for the older Neutron LBaaS service.

---

## Types of loadbalancers
There are two types of Loadbalancers in OpenStack Octavia which can be used to create your
Loadbalancer setup.

### Single Loadbalancer
A single loadbalancer setup is a simple setup where a single loadbalancer is used to distribute the
incoming traffic to the backend servers/applications. This setup is suitable for non-critical
applications because if the loadbalancer fails, the whole setup will be down.

### Active/Standby Loadbalancer (High Availability)
The Active/Standby Loadbalancer setup is a more reliable setup where the standy loadbalancer will
take over the traffic if the active loadbalancer fails. This setup is highly recommended and
essential for critical applications. This setup can be used to make sure the availability of the
servers and applications can be assured.

### Flavors
Loadbalancer flavors are used to chose between the Single and Active/Standby Loadbalancer
setups. Most of the time, the Active/Standby Loadbalancer setup is used because of its reliability
and availability. Loadbalancer flavors are also used to define the performance of the loadbalancer.
The flavors can be used to define the performance of the loadbalancer like the number of
connections, the number of requests, the bandwidth, vice versa. Based on your requirements, you can
choose the flavor that suits your needs. Most providers indicate the performance of the loadbalancer
in the flavor description.

---

## Listeners
Listeners are used to define the incoming traffic to the loadbalancer. The listeners are used to
define the protocol, port, and the [backend pool](#pools) to which the traffic should be forwarded.

---

## Pools
Pools are a group of backend servers or applications to which the traffic should
be forwarded. The pools are used to define the protocol, the algorithm, and the backend servers for
the specific [Listener](#listeners).

### Loadbalancer Algorithms
Pool algorithms are used to define the way the traffic should be distributed to the backend servers.
- **Round Robin**: is used to distribute the traffic to the backend servers in a circular order.   
- **Least Connections**: is used to distribute the traffic to the backend servers based on the
number of connections towards the backend servers.  
- **Source IP**: is used to distribute the traffic to the backend servers based on the source IP of
the incoming traffic.  

### Session Persistence
Session persistence is used to make sure that the traffic from the same client is always forwarded
to the same backend server. This is used to make sure that the session data is always available on
the same server. This is essential for applications that require session data to be available on the
same server. OpenStack Octavia currently supports the following Session persistence methods:
- **HTTP_COOKIE**: is used to make sure that the traffic from the same client is always forwarded to
the same backend server based on the HTTP cookie.  
- **APP_COOKIE**: is used to make sure that the traffic from the same client is always forwarded to
the same backend server based on the application cookie.  
- **SOURCE_IP**: is used to make sure that the traffic from the same client is always forwarded to
the same backend server based on the source IP of the incoming traffic.  

---

## Monitors
Monitors are used to define the health of the backend servers. The monitors are used to define the
protocol, the interval, the timeout, the retries, and the status of the backend servers. Whenever a
backend server or application is down, the monitor will mark the server as down and the traffic will
not be forwarded to that server anymore. This way you can make sure that the traffic is only
forwarded to the healthy servers to avoid downtime for the users.

---

## SSL Termination (HTTPS)
SSL Termination is used to decrypt the incoming traffic and forward it to the backend servers. This
is used to offload the SSL encryption from the backend servers. This way the backend servers can
focus on the application and the loadbalancer can focus on the SSL encryption. The storage of the
SSL certificates is be done with OpenStack Barbican (Secret Manager) and can be added to the
loadbalancers on creation or at a later point. It is required to use the `TERMINATED_HTTPS` listener 
protocol to enable SSL Termination at the Loadbalancer.

---

## Where to place your loadbalancer
Chosing the best location for you loadbalancer can be an essential part of the setup. We recommend
checking the geographical location of the backend servers to make sure the loadbalancer is placed in
the desired region/availability zone (AZ).

Loadbalancers can be used to forward external traffic to the backend servers but they may also be
used to forward internal traffic within your private network. This is something to keep in mind when
 desiging your cloud infrastructure.

---

## Recommendations
When creating a loadbalancer setup, it is recommended to use the Active/Standby Loadbalancer setup.
This is because of the reliability and availability of the setup. The Active/Standby Loadbalancer
are setup to make sure the availability of the servers and applications can be assured whenever one
of the loadbalancers fails.

When you create a loadbalancer we recommend to use an Floating IP address for the loadbalancer.
This way we can always swap the IP between loadbalancers in case you want to upgrade or replace the
loadbalancer.

---

## Conclusion
Loadbalancers can be an essential part of a cloud infrastructure. Loadbalancers can be used to
distribute the incoming traffic to multiple servers. This can in turn increase the availability of
the servers and the applications. OpenStack Octavia provides a on-demand and reliable
loadbalancer service which is easy to use and manage for your cloud infrastructure.
