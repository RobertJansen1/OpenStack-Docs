---
layout: page
tags: [Keymanager]
page_title: How to create a secret with payload
---

# How to create a secret with payload.

To create a secret, run the openstack secret store --name) command and specify the name of the secret and optionally the payload for the secret. 
```bash
% secret store --name (name) --payload (name)
```

(Leave out brackets)

Example:
```bash
% secret store --name openstack secret store --name test --payload Testpayload
```
