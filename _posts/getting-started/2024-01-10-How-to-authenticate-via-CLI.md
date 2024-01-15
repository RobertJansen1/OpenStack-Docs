---
layout: page
tags: [getting-started]
page_title: How to authenticate with your OpenStack via the CLI
---

# How to authenticate with your OpenStack via the CLI

Depending on the location you have saved or placed the source file, you will need to select that directory to authenticate.

You can do this by using the command cd "name of directory". This will start your command line from that directory.
As an example, that would be cd downloads for me as the file is in my downloads folder.

```bash
% cd downloads
```

Once this is done, you can authenticate with your source file. In my case this would be:

```bash
% source AMS2\ -\ username-openrc.sh
```

Once you have entered this, you will be prompted to enter your password for your OpenStack environment.
If the password is correct, the command line will resume without any additional message.

If the password is incorrect, you will receive the following message when you try to perform a command that requires authentication as seen in the screenshot below.


```bash
% openstack server list
```

