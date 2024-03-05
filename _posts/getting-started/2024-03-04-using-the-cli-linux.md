---
layout: page
tags: ["Getting-Started"]
page_title: Using the OpenStack CLI (Linux)
---

# Using the OpenStack CLI (Linux)

For Windows installations please see
[Using the OpenStack CLI (Windows)]({{ '/articles/using-the-cli-windows' | relative_url }}).

The OpenStack Command Line Interface (CLI) is a powerful tool for managing
OpenStack resources. This guide will show you how to install the OpenStack CLI,
log in to the OpenStack CLI, and use the OpenStack CLI to manage OpenStack
resources.

This guide makes use of the `clouds.yaml` file to store OpenStack credentials.
You can also use environment variables to store your credentials using the
`openrc` file. The `clouds.yaml` file is the recommended way to store your
OpenStack credentials, as it is easier to manage and add multiple clouds
(projects, regions etc.).

---

## Install the OpenStack CLI
The installation of the OpenStack CLI is different for each Operating System 
and distrubution. Below you will find the installation instructions for the
most common Linux distributions.

For Windows installations please see
[Using the OpenStack CLI (Windows)]({{ '/articles/using-the-cli-windows' | relative_url }}).


### Debian (10, 11, 12) | Ubuntu (20.04 | 22.04)
To install the OpenStack CLI, run the following commands:

**Step 1**  
Update our package list to make sure we install the latest version of the
OpenStack CLI.
```bash
sudo apt update
```

**Step 2**  
Install the OpenStack CLI
```bash
sudo apt install python3-openstackclient
```

After the installation has finished proceed to
[Preparing your OpenStack Credentials](#preparing-your-openstack-credentials).

### CentOS Stream (8, 9) | RHEL (8, 9) | Rocky Linux (8, 9) | AlmaLinux (8, 9)

To install the OpenStack CLI, run the following commands:

**Step 1**  
Install python3 and pip3 
```bash
sudo dnf install python3 python3-pip
```

**Step 2**  
We will now update pip3 to make sure we use the latest version of pip3
```bash
sudo pip3 install --upgrade pip
```

**Step 3**  
Now we can install the OpenStack CLI
```bash
sudo pip3 install python-openstackclient
```

After the installation has finished proceed to
[Preparing your OpenStack Credentials](#preparing-your-openstack-credentials).

---

### Preparing Your OpenStack Credentials
After installing the OpenStack CLI, we need to prepare our credentials to make
sure we are able to login using the OpenStack CLI.

**Step 1**  
First we will create a file to store our OpenStack credentials. In this
tutorial we will use the `clouds.yaml` file to store our credentials. You
can also use environment variables to store your credentials using the
`openrc` file.

Create the directory in which the clouds.yaml file will be stored.
```bash
mkdir -p ~/.config/openstack
```

**Step 2**  
We will now create the clouds.yaml file, the next step will describe how to
populate the file with the necessary information.

```bash
nano ~/.config/openstack/clouds.yaml
```

**Step 3**  
In the clouds.yaml file add the following content to it. Replace: `region`,
`<cloud_name>`, `<auth_url>`, `<username>`, `<password>`, `<project_name>`, `<project_id>`,
`<user_domain_name>`, and `<project_domain_name>` with your OpenStack
credentials.

```yaml
clouds:
  <cloud_name>:
    auth:
      auth_url: <auth_url>
      username: "<username>"
      project_id: <project_id>
      project_name: "<project_name>"
      user_domain_name: "<user_domain_name>"
      password: "<password>"
    region_name: "<region>"
    interface: "public"
    identity_api_version: 3
```

> Note: The cloud_name can be any name you want to give to your cloud. We
recommend using the region name as the cloud name.

> Note: If you do not know all information, you can download the clouds.yaml
file from the OpenStack dashboard. Go to the OpenStack dashboard, click on
`Project` and then `API Access`. Click on `DOWNLOAD OPENSTACK RC FILE` and
click on `OPENSTACK CLOUDS.YAML FILE`. This will download the clouds.yaml file
with all the necessary information.

> Note: For security reasons you may want to remove the `password` line from 
the clouds.yaml file, when you enter a command in the OpenStack CLI your
password will be asked for.

**Step 4**  
Now save the file and exit the text editor. by pressing `CTRL + X` and then `Y`
and `Enter`.

After you have configured your credentials you can procceed to
[Using the OpenStack CLI](#using-the-openstack-cli) to test if
the OpenStack CLI works.

---

## Using the OpenStack CLI
Now that we have installed the OpenStack CLI, we can use the OpenStack CLI to
manage our OpenStack resources.

First we we need to specify the cloud (project/region) we want to use. make
sure to replace `<cloud_name>` with the name you used in the `clouds.yaml`
file.

```bash
export OS_CLOUD=<cloud_name>
```

Now we can use the OpenStack CLI to manage our OpenStack resources.
For example, to list all the available images, run the following command:

```bash
openstack image list
```

To list all openstack instances (servers), run the following command:

```bash
openstack flavor list
```

Your are now ready to use the OpenStack CLI to manage your OpenStack resources.
The OpenStack CLI has many more commands and options, so be sure to check the
[OpenStack CLI documentation](https://docs.openstack.org/python-openstackclient/latest/cli/index.html)

> Note: Instead of setting the `OS_CLOUD` environment variable you can also
specify the cloud using the `--os-cloud` option in the OpenStack CLI commands.