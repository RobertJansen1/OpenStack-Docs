---
layout: page
tags: [Keymanager]
page_title: How to create a secret with payload
---

# How to create a secret with payload.

To create a secret, run the <openstack secret store command> and specify the name of the secret and optionally the payload for the secret. 

secret store --name (name) --payload (name)

(Leave out brackets)

![Source Download]({{ '/assets/images/keymanager/secret with payload.jpeg' | relative_url }})

To see the difference, type the command “Openstack secret list” to see the secrets.

![Source Download]({{ '/assets/images/keymanager/Secret list2.jpeg' | relative_url }})
