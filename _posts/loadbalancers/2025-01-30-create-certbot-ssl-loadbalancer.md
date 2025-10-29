---
layout: page
tags: [Loadbalancers]
page_title: Add Let's Encrypt to your SSL loadbalancer
---

This tutorial guides you through the process of adding an automated certificate renewal for 
your existing load balancer with HTTPS_OFFLOADING. Using command line tools, certbot, DNSaaS, 
cron, Barbican and a custom script 

---

## Requirements
Before adding Let's Encrypt certificates to your load balancer, we first need to create a load 
balancer with HTTPS_OFFLOADING, like described in [Create a ssl loadbalancer]({{ '/articles/create-a-ssl-loadbalancer' | relative_url }}) 
 
We need a linux machine with the OpenStack command line tools [Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

For this guide we assume you have already created a DNS Zone, if you haven't
done this yet please read the following article:
[Create a DNS Zone]({{ '/articles/create-a-dns-zone' | relative_url }})
 
We will be storing the Let's Encrypt SSL certificates in OpenStack. We are using 
Keymanager to do so. To read more about Keymanaer, refer to the article 
[Introduction to Keymanager]({{ '/articles/introduction-to-keymanager' | relative_url }}).



### Preparing the linux server

For the script to work, we need a couple applications and scripts. 



**Step 1**  
Install tools with your prefered linux package manager. 
```bash
# For Debian-based systems
sudo apt install python3 python3-pip certbot

# For Redhat-based systems
sudo yum install python3 python3-pip certbot
```
**Step 2**  
Install the python packages with pip. 
```bash
sudo pip install openstacksdk cryptography certbot git+https://opendev.org/x/certbot-dns-openstack.git
```

**Step 3**  
Download the script from cloudtutorials. We recommend you reading the script before executing, this is always good practice.
```bash
sudo wget -O /root/renew_certificates.py https://raw.githubusercontent.com/CloudTutorials/OpenStack-Docs/refs/heads/main/assets/scripts/2025-01-30-create-certbot-ssl-loadbalancer/renew_certificates.py
```
 
**Step 4** 
Gather the loadbalancer listener id(s) from the OpenStack project to verify which listeners 
you want to add the certificates to. 
```bash
openstack --os-cloud ams2 loadbalancer listener list
```

### Running the script and schedule it  

**Step 1** 
Run the script once to evaluate check if everything works
```bash
sudo python3 /root/renew_certificates.py --os-cloud <cloud> --domain *.test.example.com --renew \
 --create-barbican-secret --octavia-listener <UUID>
```  
We expect the script to request a certificate through certbot. Certbot on its turn will use a 
plugin to create a DNS record in OpenStack Designate to validate the domain. 
The option --create-barbican-secret will gather the certificates from certbot's live directories 
and upload the certificate to OpenStack Barbican. 
The option --octavia-listener <UUID> will configure all listeners supplied with the uploaded 
certificate. 

**Step 2**
When the script is running succesfully, we can create a cron to schedule the creation. 
```bash
sudo cat > /etc/cron.d/renew_certs << EOF
# /etc/cron.d/renew_certs: crontab entries for the automated OpenStack
# Certificate renewal
#
# Upstream certbot recommends attempting renewal twice a day
#
# Eventually, this will be an opportunity to validate certificates
# haven't been revoked, etc.  Renewal will only occur if expiration
# is within 30 days.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

0 */12 * * * root test -x /usr/bin/certbot && perl -e 'sleep int(rand(43200))' && python3 /root/renew_certificates.py --os-cloud <cloud> --domain *.test.example.com --renew  --create-barbican-secret --octavia-listener <UUID> >> /var/log/renew_cert.log 2>&1

EOF
```

