---
layout: page
tags: [Volume]
page_title: Restore a volume backup
---

# Restore a volume backup

Backups are an essential part of any infrastructure and system. Within the 
OpenStack Environment you can use the `cinder` service to create backups of
volumes. These can be used to restore a volume in case of data loss or
corruption.

This article will guide you through the process of restoring a backup of a
volume using the OpenStack Dashboard and the OpenStack CLI. If you do not yet
have a backup which you want to restore then please refer to the
[Create a volume backup]({{ '/articles/create-volume-backup' | relative_url }})
article.

## Using the OpenStack Dashboard

**Step 1**  
Log in to the OpenStack Dashboard.

**Step 2**  
Navigate to the `VOLUMES` section and click on `Backups`.

**Step 3**
Click on `RESTORE BACKUP` next to the backup you want to restore.

**Step 4a (Restoring to an new volume)**  
If you want to restore the backup to a new volume then select the
`CREATE A NEW VOLUME` option and click on `Restore Backup`. This options will
use the default volume type SSD. should you want to use a different volume type
you will have to proceed to step 4b and skip this step (step 4a).

> Note: If you are trying to restore an encrypted backup we recommend first
> creating a new volume with the `encrypted` volume type and then restoring
> the backup to the new volume. (See step 4b)

**Step 4b (Restoring to an existing volume)**  
Select the volume you want to restore the backup to and click on `Restore
Backup`.

> Note: If you are trying to restore an encrypted backup make sure to use the
> same volume type as the original volume when restoring the backup. This is
> to make sure the data can be read from the volume after restoring the backup.

---

## Using the OpenStack CLI
To restore a backup using the OpenStack CLI you can use the following command:

To restore a backup to a new volume please proceed to the
[Restore backup to a new volume](#restore-backup-to-a-new-volume) section.

To restore a backup to an existing volume please proceed to the
[Restore backup to an existing volume](#restore-backup-to-an-existing-volume)
section.

### Restore backup to a new volume
Restoring a backup to a new volume can be really useful if you want to keep
to original volume for comparison or for investigation on what went wrong. 
To restore a backup to a new volume you can use the following steps.

If you want to restore a backup to an existing volume please proceed to the
[Restore backup to an existing volume](#restore-backup-to-an-existing-volume)
section.

**Step 1**  
First make sure you have setup the OpenStack CLI and that you are able to
execute commands using the `openstack` command. For more information please
refer to the
[Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

**Step 2**  
Now we list all backups to get the ID and to the size of the backup we want to
restore.
```bash
openstack volume backup list
```

**Step 3**  
Now we can create a new volume. Replace `<backup_id>` with the ID of the
backup and `<volume_name>` with the name of the new volume. Replace
`<size>` with the size of the volume which should be equal to or bigger then
the size of the backup.
```bash
openstack volume create --os-volume-api-version 3.47 --size 10 --backup <backup_id> <volume_name>
```

A new volume will now be created with the data from the backup.

> Note: If you are restoring an backup of an encrypted volume make sure
> to use the same encrypted volume type like `<type>-encrypted` when restoring
> the backup. You can do this by adding the  `--type <volume-type>` argument.

> Note: In older versions of the OpenStack the `--os-volume-api-version 3.47`
option might not work, in this case you need to create a new volume and then
restore the backup to the new volume using the instructions in the
[Restore backup to an existing volume](#restore-backup-to-an-existing-volume)
section.

> Note: If you want to restore the backup to an other availability zone, you
can add `--availability-zone <availability-zone>` argument to the command
above.

> Note: If you want to restore the backup to a specific volume type
you can add `--type <volume-type>` argument to the command above. For example
`--type ssd` to restore the backup to a volume with the `ssd` volume type.

### Restore backup to an existing volume

**Step 1**  
First make sure you have setup the OpenStack CLI and that you are able to
execute commands using the `openstack` command. For more information please
refer to the
[Using the OpenStack CLI article](
    {{ '/articles/using-the-cli-linux' | relative_url }}
).

**Step 2**  
List all volumes to get the ID of the volume you want to backup.
```bash
openstack volume list
```

**Step 3**  
Now we list all backups to get the ID of the backup we want to restore.
```bash
openstack volume backup list
```

**Step 4**  
Now that we have the ID of the backup and the volume where we want to restore
the backup to we can execute the following command to restore the backup.
```bash
openstack volume backup restore <backup_id> <volume_id> --force
```

> Warning: The `--force` option will overwrite the data on the volume with the
> data from the backup. Make sure you have a backup of the data on the volume
> before restoring the backup incase you made a mistake and overwrite
> something important.

> Note: If you are trying to restore an encrypted backup make sure to use the
> same volume type as the original volume when restoring the backup. This is
> to make sure the data can be read from the volume after restoring the backup.
---

You have now restored your backup! We hope this article was helpful and that
you have successfully recovered your data using your volume backup!
