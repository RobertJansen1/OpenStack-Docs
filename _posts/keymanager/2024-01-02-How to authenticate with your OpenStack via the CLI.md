---
layout: page
tags: [Keymanager]
page_title: How to authenticate with your OpenStack via the CLI
---

# How to authenticate with your OpenStack via the CLI

Depending on the location you have placed it in after downloading the OpenStack RC File, you will need to select that directory in the CLI.

You can do this by using the command CD <name of directory>. This will start your command line from that directory.
As an example, that would be CD downloads for me as the file is in my downloads folder.

![Source Download]({{ '/assets/images/keymanager/cd downloads.jpeg' | relative_url }})

Once this is done, you can authenticate with your source file.
In my case this would be:

“Source AMS2\ -\ ebagac-openrc.sh”
(You can also do Source AMS2 and then use the tab button to auto fill the rest of the file name)

![Source Download]({{ '/assets/images/keymanager/source connect.jpeg' | relative_url }})

Once you have entered this, you will be prompted to enter your password for your OpenStack environment.
If the password is correct, the command line will resume without any additional message.

![Source Download]({{ '/assets/images/keymanager/pw succes.jpeg' | relative_url }})

If the password is incorrect, you will receive the following message when you try to perform a command that requires authentication as seem in the screenshot below.

![Source Download]({{ '/assets/images/keymanager/download-source-file.png' | relative_url }})
