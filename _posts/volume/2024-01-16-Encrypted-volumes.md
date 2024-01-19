---
layout: page
tags: [Volume]
page_title: Volume types & encrypted volumes
---

# Requirements to create an encrypted volume

In order to create an encrypted template, volume type & volume type, make sure you have the required permissions and configurations set up to execute this command successfully in your OpenStack environment.


It may be that you do not possess any volume types, if this is the case you have to create a volume type.

Before starting of a volume type, a volume template needs to be in place.

## Creating a volume template that uses encryption

Let us create a volume template that uses encryption. Whenever you create new volumes, you can refer to this volume template.
We will be using the LuksEncryptor-Template-256 template as a default. You can replace this with the name you wish to use.

--encryption-provider: Specifies the encryption provider, in this case, nova.volume.encryptors.luks.LuksEncryptor.

--encryption-cipher: Sets the encryption cipher to aes-xts-plain64.

--encryption-key-size: Specifies the encryption key size as 256.

--encryption-control-location: Defines the encryption control location as front-end.

LuksEncryptor-Template-256: The name of the new volume type you are creating..

To read more about these points, you can use the command "openstack volume type create --help"

The commando creating a volume template with encryption would look like:

```bash
% openstack volume type create --encryption-provider nova.volume.encryptors.luks.LuksEncryptor --encryption-cipher aes-xts-plain64 --encryption-key-size 256 --encryption-control-location front-end LuksEncryptor-Template-256
```

## Creating a volume type

With the commando below, you can create a volume type.

```bash
% openstack volume create --size 1 --type LuksEncryptor-Template-256 'Encrypted-Test-Volume'
```
--description: Optional. You can provide a description for the new volume type.

--public or --private: This is optional. Specifies whether the volume type should be public or private. You can use either 
--public to make it public or --private to make it private, depending on your preferences.

--property (key1=value1) [...]: This is optional. You can set extra key-value properties for the volume type. Add, update, or remove properties (extra specifications) associated with the volume type.

--project <project>: Optional. Specifies the project (tenant) to which the volume type belongs.

--project-domain <project-domain>: Optional. Specifies the domain of the project.

(name): Give the volume a name. Remove the brackets

```bash
% openstack volume type create --description "Description of the new volume type" --public --property key1=value1 --property key2=value2 NewVolumeType
```

## Viewing the volume types

View the result by using the command:

```bash
% openstack volume type list
```

This will give a list of available volune types. It will show the "ID", "Name"  and whether the volume type is public or private.

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
As we named our volume type "Volumetypetest" earlier, we place it at the end of the command. The ID is visible after you used the (% openstack volume type list) command.

```bash
% openstack volume type delete LuksEncryptor-Template-256
```

## Creating an encrypted volume

Above we have created a volume template and type. Now we can create an encrypted volume based on that.

We know how we create a regular volume, with the commando:

```bash
% openstack volume create --size 10 EncryptedVolume
```
By adding a type to this volume, we can make it encrypted as a template was created.

```bash
% openstack volume create --size 10 --type LuksEncryptor-Template-256 EncryptedVolume
```
An encrypted volume now created with 10 GB of size and using the LuksEncryptor-Template-256 template with the name EncryptedVolume.