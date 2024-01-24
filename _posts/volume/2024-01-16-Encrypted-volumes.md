---
layout: page
tags: [Volume]
page_title: Volume types & encrypted volumes
---

# Requirements to create an encrypted volume

In order to create an encrypted template, volume type & volume type, make sure you have the required permissions and configurations set up to execute this command successfully in your OpenStack environment.


If you do not have any volume templates, you will have to create a volume template.

Before starting to create a volume type, a volume template needs to be in place that can you refer to.

## Creating a volume template that uses encryption

Let us create a volume template that uses encryption. Whenever you create new volumes, you can refer to this volume template.
We will be using the LuksEncryptor-Template-256 template as a default. You can replace this with the name you wish to use for your template.

```--encryption-provider:``` Specifies the encryption provider, in this case, nova.volume.encryptors.luks.LuksEncryptor.

```--encryption-cipher:``` Sets the encryption cipher to aes-xts-plain64.

```--encryption-key-size:``` Specifies the encryption key size as 256.

```--encryption-control-location:``` Defines the encryption control location as front-end.

```LuksEncryptor-Template-256:``` The name of the new volume type you are creating..

To read more about these points, you can use the command "openstack volume type create --help"

The commando for creating a volume template with encryption would look like:

```bash
% openstack volume type create --encryption-provider nova.volume.encryptors.luks.LuksEncryptor --encryption-cipher aes-xts-plain64 --encryption-key-size 256 --encryption-control-location front-end LuksEncryptor-Template-256
```

## Creating a volume type

With the commando below, you can create a volume type that specifies the volume setting "luksEncryptor-Template-256" we created above. 

```bash
% openstack volume create --size 1 --type LuksEncryptor-Template-256 Encrypted-Test-Volume
```

## Viewing the volume types

View the result by using the command:

```bash
% openstack volume type list
```

This will give a list of available volume types. It will show the "ID", "Name"  and whether the volume type is public or private.

## Viewing a specific volume

To view the details of a specific volume type, use the command:

```bash
% openstack volume type show (Name of ID)
```

Example:

```bash
% openstack volume type show LuksEncryptor-Template-256
```
Replace the type with the name of your own created template.

## Deleting volume type

In order to delete a volume type, you can use the following command, followed up by the ID or name of the volume type.

```bash
% openstack volume type delete (ID or name)
```
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