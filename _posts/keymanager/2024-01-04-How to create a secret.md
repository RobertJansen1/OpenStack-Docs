---
layout: page
tags: [Keymanager]
page_title: How to create a secret
---

# How to create a secret.

How to create a secret

You can create two types of secrets, with and without payload. The difference will be visible in the “Secret list”. 
Below is a creation of a secret without payload, which is:

```bash
% openstack secret store --name (name)
```
Replace name with the name you want to give your secret.

Example:
```bash
% openstack secret store --name Test
```

In the above overview you can see secret href of the secret and the name that is given to it.