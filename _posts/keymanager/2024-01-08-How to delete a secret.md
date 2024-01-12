---
layout: page
tags: [Keymanager]
page_title: How to delete a secret
---

# How to delete a secret

You can delete your secret by using the following command:
```bash 
% openstack secret delete (secret HREF)
```
Place the HREF link that you can see via use the "Openstack secret list" command.

Example below:

```bash
% openstack secret delete https://keymanager.ams2.teamblue.cloud/v1/secrets/efab91f4-9104-4274-8574-b61f82008846 
```

You can look up if the deletion is done correctly by checking by using  “Openstack secret list” the command.

In the screenshot below you can see that the secret has been deleted.

