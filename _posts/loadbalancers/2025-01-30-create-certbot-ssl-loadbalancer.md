---
layout: page
tags: [Loadbalancers]
page_title: Add LetsEncrypt to your SSL loadbalancer
---

This tutorial guides you through the process of adding an automated certificate renewal for 
your existing load balancer with HTTPS_OFFLOADING. Using command line tools, certbot, DNSaaS, 
cron, Barbican and a custom script 

---

## Requirements
Before adding letsencrypt certificates to your load balancer, we first need to create a load 
balancer with HTTPS_OFFLOADING, like described in [Create a ssl loadbalancer]({{ '/articles/create-a-ssl-loadbalancer' | relative_url }}) 
 
We need a linux machine with the OpenStack command line tools [Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

For this guide we assume you have already created a DNS Zone, if you haven't
done this yet please read the following article:
[Create a DNS Zone]({{ '/articles/create-a-dns-zone' | relative_url }})
 
We will be storing the letsencrypt SSL certificates in OpenStack. We are using 
Keymanager to do so. To read more about Keymanaer, refer to the article 
[Introduction to Keymanager]({{ '/articles/introduction-to-keymanager' | relative_url }}).



### Preparing the linux server

For the script to work, we need a couple applications and scripts. 

**Prerequisites**
 - Python 3 is installed together with pip3
   
 All certificates files are stored on the OpenStack CLI server. We need the following files:
   - certificate.pem (the certificate file for the load balancer)
   - private.key (the private key for the load balancer, password protected)
   - intermediate.pem (intermediate certificates in proper order of your SSL supplier)
 - Passphrase to decrypt the private key
 - openssl tooling installed on the OpenStack CLI server


**Step 1**  
Install tools with linux package manager 
```bash
apt install python3 python3-pip
```
**Step 2**  
Install the python packages with pip 
```bash
cat > requirements_certbot_dns_openstack.txt << EOF
openstacksdk
cryptography
certbot
git+https://opendev.org/x/certbot-dns-openstack.git
EOF
pip3 install -r requirements_certbot_dns_openstack.txt
rm requirements_certbot_dns_openstack.txt
```

**Step 3**  
Download and evaluate the script from cloudtutorials 
```bash
wget -O ~/renew_certificates.py https://github.com/RobertJansen1/OpenStack-Docs/blob/main/assets/scripts/2025-01-30-create-certbot-ssl-loadbalancer/renew_certificates.py
less ~/renew_certificates.py
python3 ~/renew_certificates.py --help
```
 
**Step 4**
