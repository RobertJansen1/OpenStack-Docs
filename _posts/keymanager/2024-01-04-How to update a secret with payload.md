---
layout: page
tags: [Keymanager]
page_title: How to update a secret with payload
---

# How to update a secret with payload

You cannot change the payload of a secret (other than deleting the secret), but if you created a secret without specifying a payload, you then can later add a payload to it by using the “openstack secret update” command.

Get the “Href” URI from the secret you want to update.

openstack secret update (your secret href) (secret name)
(Leave out brackets)

![Source Download]({{ '/assets/images/keymanager/secret update 2.jpeg' | relative_url }})

In the screenshot above, you can see that the content types has changed for the secret.
