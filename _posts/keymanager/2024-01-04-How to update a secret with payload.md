---
layout: page
tags: [Keymanager]
page_title: How to update a secret with payload
---

# How to update a secret with payload

You cannot change the payload of a secret (other than deleting the secret), but if you have created a secret without specifying a payload, you then later can add a payload to it by using the following command.

Get the “secret Href” URL from the secret you want to update.

```bash
% openstack secret update (your secret href) (payload name)
```


Below an example how it would look, by adding an optional name to the secret.

```bash
% openstack secret update https://keymanager.ams2.teamblue.cloud/v1/secrets/efab91f4-9104-4274-8574-b61f82008846 test-updated
```

After doing this, you can view the secret by using "Openstack secret list"  command.

``` bash
% openstack secret list
```

The original secret will have the content type {'default': 'application/octet-stream'}.
The updated secret will have the content type {'default': 'text/plain'}, which will overwrite the original secret.

In the list you will see that the content type has changed of the corresponding secret.
