---
layout: page
tags: [Volume]
page_title: Creating an encrypted volume
---

# Requirements to create an encrypted volume

In order to create an encrypted volume, the user needs to have the creator or admin barbican role on the project.

It may be that you do not possess any volume types, if this is the case you have to create a volume type.

### Creating a volume type

```bash
% openstack volume type create
    [--description <description>]
    [--public | --private]
    [--property <key=value> [...] ]
    [--project <project>]
    [--project-domain <project-domain>]
    <name>
```
--description (Test Volume Type): Optional. You can provide a description for the new volume type.

--public or --private: This is optional. Specifies whether the volume type should be public or private. You can use either 
--public to make it public or --private to make it private, depending on your preferences.

--property (key1=value1) [...]: This is optional. You can set extra key-value properties for the volume type. Replace <key=value> with the specific properties you want to set.

--project <project>: Optional. Specifies the project (tenant) to which the volume type belongs.

--project-domain <project-domain>: Optional. Specifies the domain of the project.

(name): Must give a name. The name of the new volume type.

In practise, this would look like:

```bash
openstack volume type create --description "Test Volume Type" --public --property key1=value1 --property key2=value2 Volumetypetest
```

### Viewing the volume types
View the result by using the command:

```bash
% openstack volume type list
```

This will give a list of available volune types. It sill show the "ID", "Name"  and whether the volume type is public or private.

### Viewing a specific volume

To view the details of a specific volume type, use the command:

```bash
% openstack volume type show (Name of ID)
```

Example:

```bash
% openstack volume type show (Volumetypetest)
```

### Deleting volume types

In order to delete a volume type, you can use the following command, followed up by the ID or name of the volume type.

```bash
% openstack volume type delete (ID or name)
```
As we named our volume type "Volumetypetest" earlier, we place it at the end of the command. The ID is visible after you used the (% openstack volume type list) command.

```bash
% openstack volume type delete Volumetypetest
```

