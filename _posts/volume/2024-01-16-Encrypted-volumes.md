---
layout: page
tags: [Volume]
page_title: Creating an encrypted volume.
---


As we named our volume type "LuksEncryptor-Template-256" earlier, we place it at the end of the command. The ID is visible after you have used the ```% openstack volume type list``` command.

```bash
% openstack volume type delete LuksEncryptor-Template-256
```

## Creating an encrypted volume

Above we have created a volume template and type. Now we can create an encrypted volume based on that.

We know how we create a regular volume, with the commando:

```bash
% openstack volume create --size 10 EncryptedVolume
```
By adding a type to this volume, we can make it encrypted as a template was created in the earlier steps.

```bash
% openstack volume create --size 10 --type LuksEncryptor-Template-256 EncryptedVolume
```
An encrypted volume is now created with 10 GB of size and using the LuksEncryptor-Template-256 template with the name EncryptedVolume.

## Deleting a volume type

In order to delete a volume type, you can use the following command, followed up by the ID or name of the volume type.

```bash
% openstack volume type delete (ID or name)
```