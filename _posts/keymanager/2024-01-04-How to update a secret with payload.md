---
layout: page
tags: [Keymanager]
page_title: How to update a secret with payload
---

# How to update a secret with payload

You cannot change the payload of a secret (other than deleting the secret), but if you created a secret without specifying a payload, you then can later add a payload to it by using the following command.

Get the “Href” URI from the secret you want to update.

```bash
openstack secret update (your secret href) (secret name)
```

(Leave out brackets)


After doing this, you view the secret by using.

``` bash
Downloads % Openstack secret list
```

In the list you will see that the content type has changed.
