---
layout: page
tags: [Template]
page_title: Template page
---

This tutorial guides you through the process of creating a template page. 
This section is used to give a brief explanation of what is achieved with the tutorial.
---


### Fist header (declares one of the larger steps in the tutorial)
When you need more headers, you are probably better of creating different articles, and link the articles under each header untill you reach the main part of your tutorial.
After the header, a brief description of what is build in the chapter is given. 

For this tutorial, we need an internal network with a router, edit the following URL to use in the tutorial
[Create an internal network]({{ '/articles/create-an-internal-network' | relative_url }})



### Second header
**Step 1**: Describe the first step
**Step 2**: second step
* Additional information for step 2
* **some more bold information**: more info
**Step 3**: Step with code block (this is prefered over images, as it can be copy-pasted)  

For example, in Ubuntu, this is already exposed under the path `/dev/disk/by-id/`, for example:
~~~~~~~~ bash
ubuntu@instance:~$ ls -al /dev/disk/by-id
total 0
drwxr-xr-x 2 root root 360 Dec 21 10:08 .
drwxr-xr-x 7 root root 140 Dec 20 10:10 ..
...
lrwxrwxrwx 1 root root   9 Dec 21 10:08 scsi-0QEMU_QEMU_HARDDISK_1831dfbb-951f-4e73-b -> ../../sdb
lrwxrwxrwx 1 root root   9 Dec 21 10:08 scsi-0QEMU_QEMU_HARDDISK_51b39d45-a8a5-43d7-b -> ../../sdd
lrwxrwxrwx 1 root root   9 Dec 21 10:08 scsi-0QEMU_QEMU_HARDDISK_85ca773c-a78b-415e-b -> ../../sdc
...
lrwxrwxrwx 1 root root   9 Dec 21 10:08 scsi-SQEMU_QEMU_HARDDISK_1831dfbb-951f-4e73-b54d-c493a64a1a32 -> ../../sdb
lrwxrwxrwx 1 root root   9 Dec 21 10:08 scsi-SQEMU_QEMU_HARDDISK_51b39d45-a8a5-43d7-b5f7-7dbf195d4014 -> ../../sdd
lrwxrwxrwx 1 root root   9 Dec 21 10:08 scsi-SQEMU_QEMU_HARDDISK_85ca773c-a78b-415e-b1cd-2c4f1a1d267f -> ../../sdc
...
~~~~~~~~  

**Step 4**: Step with images
![<Image description>](/assets/images/<article name>/<image name>)

### Before publishing:

Don't forget to read the readme for more guidelines

