---
layout: page
tags: [Keymanager]
page_title: How to view secrets
---

# How to view secrets

If you are just starting with this, you most likely will not have any secrets available yet.
To view your secrets, type the following command in the CLI.

_Openstack secret list_


![Source Download]({{ '/assets/images/keymanager/cd downloads.jpeg' | relative_url }})

Once this is done, you can authenticate with your source file.
In my case this would be:

“Source AMS2\ -\ <username>-openrc.sh”
(You can also do Source AMS2 and then use the tab button to auto fill the rest of the file name)

![Source Download]({{ '/assets/images/keymanager/source connect.jpeg' | relative_url }})

Once you have entered this, you will be prompted to enter your password for your OpenStack environment.
If the password is correct, the command line will resume without any additional message.

![Source Download]({{ '/assets/images/keymanager/pw succes.jpeg' | relative_url }})

If the password is incorrect, you will receive the following message when you try to perform a command that requires authentication as seem in the screenshot below.

![Source Download]({{ '/assets/images/keymanager/pw incorrect.jpeg' | relative_url }})
