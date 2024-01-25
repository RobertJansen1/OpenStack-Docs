---
layout: page
tags: [Volume]
page_title: Identify cinder volumes from within the instance
---

# Identifying disks in the instance

As we all know, volume attachments to a nova instance are sometimes hard to recognise, especially if the volumes are mounted as `/dev/sdb`. Though if there are more volumes attached, the order of disks is sometimes randomized, without a real indication of how it presents itself.

From the nova standpoint, it is passing along the mountpoint to libvirt, and the scsi lun id is incrementing according to the order the volumes have been attached to the instance, but still it does not really work well.
What also happens, is that the disks' serial number is set to the cinder volume id. That is something we can identify from within the vm.

For example, in Ubuntu, this is already exposed under the path `/dev/disk/by-id/`, for example:
```bash
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
```

## Workaround: Add a new symlink with just the cinder uuid
Now this is great and all, but it would be nice to make it shorter, so we could mount the volumes based on the cinder volume id, which is stored in the disk serial number.

**Step 1**: Create a custom udev `.rules` file

In order to do that, we need to first define some custom udev rules in `/etc/udev/rules.d/`. For example: `60-disk-scsi-ids.rules`
```bash
cat > /etc/udev/rules.d/60-disk-scsi-ids.rules << EOF
# Add more links for cinder volumes, based on ID_SCSI_SERIAL
KERNEL=="sd*|sr*|cciss*", ENV{DEVTYPE}=="disk", ENV{ID_SCSI_SERIAL}=="?*", SYMLINK+="disk/by-id/$env{ID_SCSI_SERIAL}"
KERNEL=="sd*|cciss*", ENV{DEVTYPE}=="partition", ENV{ID_SCSI_SERIAL}=="?*", SYMLINK+="disk/by-id/$env{ID_SCSI_SERIAL}-part%n"
EOF
```


**Step 2**: Reload udev (or reboot)
```bash
udevadm control --reload-rules && udevadm trigger
```

And then voila, the symlinks should be present:
```bash
ubuntu@instance:~$ ls -al /dev/disk/by-id
total 0
drwxr-xr-x 2 root root 440 Dec 21 09:52 .
drwxr-xr-x 7 root root 140 Dec 20 10:10 ..
lrwxrwxrwx 1 root root   9 Dec 21 09:52 1831dfbb-951f-4e73-b54d-c493a64a1a32 -> ../../sdb
lrwxrwxrwx 1 root root   9 Dec 21 09:52 51b39d45-a8a5-43d7-b5f7-7dbf195d4014 -> ../../sdd
lrwxrwxrwx 1 root root   9 Dec 21 09:52 85ca773c-a78b-415e-b1cd-2c4f1a1d267f -> ../../sdc
```

**Step 3**: Update your `/etc/fstab`

So now, you can now mount your volume based directly from `/etc/fstab` like this:
```fstab
ID=85ca773c-a78b-415e-b1cd-2c4f1a1d267f /mnt ext4 defaults 0 0
```

When finished editing your fstab file, just mount it using `mount -a`
