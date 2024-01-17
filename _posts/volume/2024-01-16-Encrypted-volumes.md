---
layout: page
tags: [Volume]
page_title: Creating an encrypted volume
---

# Requirements to create an encrypted volume

In order to create an encrypted volume, the user needs to have the creater or admin barbican role on the project.

It may happen that you do not have volume types, if this is the case you can create them in the following way.

```bash
%  openstack volume type create
    [--description <description>]
    [--public | --private]
    [--property <key=value> [...] ]
    [--project <project>]
    [--project-domain <project-domain>]
    <name>
```
--description <description>: Optional. You can provide a description for the new volume type.

--public or --private: This is optional. Specifies whether the volume type should be public or private. You can use either 
--public to make it public or --private to make it private, depending in your preferences.

--property (key=value) [...]: This is optional. You can set extra key-value properties for the volume type. Replace <key=value> with the specific properties you want to set.

--project <project>: Optional. Specifies the project (tenant) to which the volume type belongs.

--project-domain <project-domain>: Optional. Specifies the domain of the project.

(name): Must give a name. The name of the new volume type.

In practise, this would look like:

```
openstack volume type create --description "My Volume Type" --public --property key1=value1 --property key2=value2 MyVolumeType
```

