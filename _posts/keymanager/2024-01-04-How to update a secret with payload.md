---
layout: page
tags: [Keymanager]
page_title: How to update a secret with payload
---

# How to update a secret with payload

You cannot change the payload of a secret (other than deleting the secret), but if you created a secret without specifying a payload, you then can later add a payload to it by using the following command.

Get the “Href” URI from the secret you want to update.

```bash
openstack secret update (your secret href) (payload name)
```
openstack secret update https://keymanager.ams2.teamblue.cloud/v1/secrets/efab91f4-9104-4274-8574-b61f82008846 twotwotwo-updated


(Leave out brackets)



After doing this, you can view the secret by using.

``` bash
Downloads % Openstack secret list
```

In the list you will see that the content type has changed.
