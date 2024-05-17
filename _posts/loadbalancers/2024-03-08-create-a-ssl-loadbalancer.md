---
layout: page
tags: [Loadbalancers]
page_title: Create a SSL loadbalancer
---

This tutorial guides you through the process of creating a load balancer with SSL encryption. 
The article assumes there is an internal network present with working http web servers listening on 
port 80. When you still need to create webservers and an internal network, please use the first part 
of article [Create a loadbalancer with webservers]({{ '/articles/create-a-loadbalancer-with-webservers' | relative_url }})


---

## SSL certificate
Before creating the load balancer, we need to store our SSL certificaten in OpenStack. We are using 
Keymanager to do so. To read more about Keymanaer, refer to the article 
[Introduction to Keymanager]({{ '/articles/introduction-to-keymanager' | relative_url }}).
Currently it is not possible to upload the certificate through Horizon so we will be using the CLI.
There are multiple options to upload the certificate to barbican. Our advise would be to use the
container approach 
([Uploading the SSL certificate to keymanager in a container](#uploading-the-ssl-certificate-to-keymanager-in-a-container))
. The easier option is the combined, although slightly less secure, approach
which has the benefit of being selectable in horizon after storing 
([Uploading the SSL certificate to keymanager as single file](#uploading-the-ssl-certificate-to-keymanager-as-single-file))
.

### Uploading the SSL certificate to keymanager in a container

The prefered way of storing a certificate in barbican for Octavia is to use seperate secrets to
store the server certificate, private key, intermediate certificates and the passhprase. After
storing the secrets, we can combine them using a certificate container. The downside of this
approach however is secret containers are not yet supported in Horizon to use for Octavia.

**Prerequisites**
 - All certificates files are stored on the OpenStack CLI server. We need the following files:
   - certificate.pem (the certificate file for the load balancer)
   - private.key (the private key for the load balancer, password protected)
   - intermediate.pem (intermediate certificates in proper order of your SSL supplier)
 - Passphrase to decrypt the private key
 - openssl tooling installed on the OpenStack CLI server


**Step 1**  
First make sure you have setup the OpenStack CLI and that you are able to
execute commands using the `openstack` command. For more information please
refer to the
[Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

**Step 2**  
Store the certificate in barbican
```bash
# Store variables
certificate=certificate.pem
domain="$(openssl x509 -noout -subject -in "$certificate"|cut -d= -f 3| tr -d ' ')"
name="${domain}_certificate"

# Store the secret in keymanager
openstack secret store --name="${name}" -t 'application/octet-stream' -e 'base64' \
--payload="$(base64 < "$certificate")" --expiration $(date --date="$(openssl x509 -enddate -noout \
-in "$certificate"|cut -d= -f 2)" --iso-8601)
```
Make sure to save the returned secret_href as variable, we need that later
```bash
certificate_url="https://keymanager.domain.tld:/v1/secrets/uuid"
```

**Step 3**  
Store the passhprase for the private key in barbican.

```bash
# Store variables
name="${domain}_passphrase"

# Store the secret in keymanager
openstack secret store --secret-type passphrase --name ${name} \
--payload $(read -sp "Password: ";echo ${REPLY})
```
Answer the password question and press enter

Make sure to save the returned secret_href as variable, we need that later
```bash
passphrase_url="https://keymanager.domain.tld:/v1/secrets/uuid"
```

**Step 4**  
Store the private key in barbican

```bash
# Store variables
name="${domain}_private_key"
certificate=private.key

# Store the secret in keymanager
openstack secret store --name="${name}" -t 'application/octet-stream' -e 'base64' \
--payload="$(base64 < "$certificate")"
```
Make sure to save the returned secret_href as variable, we need that later
```bash
private_key_url="https://keymanager.domain.tld:/v1/secrets/uuid"
```

**Step 5**  
Store all intermediate certificates in barbican

```bash
# Store variables
certificate=intermediate.pem
name="${domain}_intermediates"

# Store the secret in keymanager
openstack secret store --name="${name}" -t 'application/octet-stream' -e 'base64' \
--payload="$(base64 < "$certificate")" --expiration $(date --date="$(openssl x509 -enddate -noout \
-in "$certificate"|cut -d= -f 2)" --iso-8601)
```
Make sure to save the returned secret_href as variable, we need that later
```bash
intermediates_url="https://keymanager.domain.tld:/v1/secrets/uuid"
```

**Step 6**  
Create a certificate container containing the certificate, all intermediates
the passphrase and the private key.

```bash
# Store variables
name="${domain}_container"

# Store the secret in keymanager
openstack secret container create --name "${name}" --type certificate \
-s "certificate=${certificate_url}" -s "intermediates=${intermediates_url}" \
-s "private_key=${private_key_url}" -s "private_key_passphrase=${passphrase_url}"

```
Make sure to save the returned secret_href as variable, we need that later
```bash
octavia_certificate_url="https://keymanager.domain.tld:/v1/containers/uuid"
```

### Uploading the SSL certificate to keymanager as single file
The alternative way to store a certificate to use with an Octavia loadbalancer is to create a single
pkcs12 file with all certificates without password protection.
The downside of this approach is we need to temporarily store the unencrypted private key for the
load balancer on the OpenStack CLI server. The benefit is we can select the certificate in Horizon.


**Prerequisites**
 - The server certificate, intermediate certificates and private key are stored in the proper order in
a single file on the OpenStack CLI server named 'certificate.pem'
 - OpenSSL tooling installed on the OpenStack CLI server

**Step 1**  
First make sure you have setup the OpenStack CLI and that you are able to
execute commands using the `openstack` command. For more information please
refer to the
[Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

**Step 2**  
Convert the certificates to a pkcs12 certificate (skip this if you already have a pkcs12 encoded
file with all required certificates):
```bash
openssl pkcs12 -export -inkey private.key -in certificate.pem -certfile intermediate.pem \
-passout pass: -out complete.p12
```

**Step 3**  
Store the certificate in barbican
```bash
certificate=complete.p12
domain="$(openssl pkcs12 -in "$certificate" -nokeys -passin pass: | openssl x509 -noout \
-subject | cut -d= -f 3| tr -d ' ')"
name="${domain}_complete_certificate"
expiration_date="$(date --date="$(openssl pkcs12 -in "$certificate" -nokeys -passin pass: | \
openssl x509 -enddate -noout | cut -d= -f 2)" --iso-8601)"
openstack secret store --name="${name}" -t 'application/octet-stream' -e 'base64' \
--payload="$(base64 < "$certificate")" --expiration "${expiration_date}"
```
Make sure to save the returned secret_href as variable, we need that later
```bash
octavia_certificate_url="https://keymanager.domain.tld:/v1/secrets/uuid"
```

---

## Creating the loadbalancer

## Creating the loadbalancer using the OpenStack Dashboard
> Note: When you decided to store your certificate through a container, it is not easy to create the
load balancer through the OpenStack Dashboard. Follow the step 
([Creating the loadbalancer using the OpenStack CLI](#creating-the-loadbalancer-using-the-openstack-cli))

Now we can create the loadbalancer. We will create a loadbalancer with a listener, a pool and a
healthmonitor.

**Step 1**  
Navigate to the `Network` tab and select `Load Balancers`.  
**Step 2**  
Initiate the process by clicking on the `Create Load Balancer` button.  
**Step 3**  
Enter details in the following fields:  
* **Name**: webserver-loadbalancer
* **IP Address**: Leave empty for now
* **Description**: Loadbalancer for our webservers
* **Availability Zone**: Leave empty or choose an availability zone to your liking.
* **Flavor**: Choose a flavor to your liking for this tutorial we use the Medium flavor.
* **Subnet**: webserver-subnet

**Step 4**  
Proceed to the `Listener Details` tab by clicking on `Next`.  
**Step 5**  
Complete the following fields:  
* **Name**: webserver-listener-https
* **Description**: HTTPS Listener for our webservers
* **Protocol**: TERMINATED HTTPS
* **Protocol Port**: 443
* **Admin State Up**: Yes
Leave all others options as they are for now.

**Step 6**  
Proceed to the `Pool Details` tab by clicking on `Next`.  
**Step 7**  
Enter information in the following fields:  
* **Create Pool**: Yes
* **Name**: webserver-pool-http
* **Description**: HTTP Pool for our webservers
* **Algorithm**: Least connections
* **Session Persistence**: Leave None
* **TLS Enabled** No
* **Admin State Up**: Yes
> Note: Find out more about the `Algorithm` and `Session Persistence` fields in the article
[Introduction into loadbalancer](
{{ '/articles/introduction-into-loadbalancer' | relative_url }})



**Step 8**  
Proceed to the `Pool Members` tab by clicking on `Next`.  
**Step 9**  
Identify the instances you wish to include and click on `Add` for each.  
**Step 10**  
Enter the designated port for the host (80) and set the weight (1). Repeat this step
for all webserver hosts you're adding.  
> Note: In this tutorial, the connection from the load balancer to the webservers is not encrypted.
The SSL encryption is hereby offloaded to the load balancer. If it is required to have an encrypted
connection to the webservers, the webservers itself need an ssl certificate as well. This is outside
of the scope for this tutorial. 

**Step 11**  
Navigate to the `Health Monitor` tab by clicking on `Next`.  
**Step 12**  
Complete the following fields:  
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

**Step 13**  
Proceed to the `SSL Certificates` tab by clicking on `Next`.  
**Step 14**  
Add the appropriate certificate from the available certificates. It will be named
`DomainName_complete_certificate`
> Note: It is possible to add multiple certificates. The load balancer will use SNI to select the
appropriate certificate


**Step 15**  
Initiate the creation of your load balancer by clicking on `Create Load Balancer`.  
**Step 16**  
Locate the load balancer you've just set up and click the small arrow beside it. From
the dropdown menu, select `Associate Floating IP`.  
**Step 17**  
Select an available floating IP or choose the net-float pool, then confirm your choice
by clicking on `Associate`.  

**Step 18**  
Finalize the deployment and start testing
([Testing the loadbalancer](#testing-the-loadbalancer))

## Creating the loadbalancer using the OpenStack CLI
Now we can create the loadbalancer. We will create a loadbalancer with a listener, a pool and a
healthmonitor. It is only possible to create the loadbalancer through 

**Prerequisites**  
We should already have a bash variable set with the certificate location
```bash
octavia_certificate_url="https://keymanager.domain.tld:/v1/containers/uuid"
```
**Step 1**  
Gather the subnet uuid for the internal network:
```bash
openstack subnet list
vip_subnet_uuid=uuid
```

**Step 2**  
Create the loadbalancer
```bash
openstack loadbalancer create --name "webserver-loadbalancer" \
--description "Loadbalancer for our webservers" --flavor Medium --vip-subnet-id "${vip_subnet_uuid}"
```
Make sure to save the returned `id` as variable, we need that later
```bash
lb_uuid=uuid
```

**Step 3**  
Create the listener
```bash
openstack loadbalancer listener create "${lb_uuid}" --name "webserver-listener-https" \
--description "HTTPS Listener for our webservers" --protocol TERMINATED_HTTPS --protocol-port 443 \
--default-tls-container-ref "${octavia_certificate_url}" 
```

Make sure to save the returned `id` as variable, we need that later
```bash
listener_uuid=uuid
```

**Step 4**  
Create the pool

```bash
openstack loadbalancer pool create --name "webserver-pool-http" \
--description "HTTP Pool for our webservers" --protocol HTTP --lb-algorithm LEAST_CONNECTIONS \
--listener "${listener_uuid}"
```
Make sure to save the returned `id` as variable, we need that later
```bash
pool_uuid=uuid
```


**Step 5**  
Create the health monitor

```bash
openstack loadbalancer healthmonitor create "${pool_uuid}" --name "webserver-healthmonitor-http" \
--type HTTP --delay 5 --timeout 5 --max-retries 3
```

**Step 6**  
Create the members

repeat the following command for all webservers you want to add to the pool

```bash
openstack loadbalancer member create "${pool_uuid}" --protocol-port 80 --name "<server_name>" \
--address "<server_address>"
```

**Step 7**  
Finalize the deployment and start testing
([Testing the loadbalancer](#testing-the-loadbalancer))


---

## Testing the loadbalancer.  
Now that the load balancer is created, we can test it

**Step 1**  
Create an A record in DNS for the domain to point to the floating IP address
[managing DNS records](
{{ '/articles/managing-dns-records' | relative_url }})


**Step 2**  
Await the update of the load balancer's Operating Status to ONLINE and the DNS to
propagate. Once this status is achieved, navigate to `https://DomainName` in your web browser to 
witness your load balancer functioning.  

**Step 3**  
Verify the SSL of the load balancer to have your URL checked with the   
[SSL Labs SSL Server Test](https://www.ssllabs.com/ssltest/analyze.html)

If you want to customize your Loadbalancer even further we highly recommend you to read the 
[OpenStack Octavia Loadbalancer documentation](https://docs.openstack.org/octavia/latest/user/index.html)