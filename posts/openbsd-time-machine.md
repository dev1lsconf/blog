---
title: OpenBSD Time Machine 
publish_date:  2022-12-20
summary: 'Muchos sistemas de backups.. yo mismo uso borg y restic muy comun mente.. pero para mi laptop en OpenBSD tengo esta pieza de arte que encontre en la web de un genio fuente: https://xosc.org/timemachine.html '
---


Time Machine like Backups on OpenBSD
$Id: timemachine.md,v 1.1 2022/05/28 11:00:00 cvs Exp $

Time Machine is a backup software by Apple, part of macOS allowing easy and foolproof backups. In a nutshell, it creates incremental backups on a storage medium of your choice and you can access the data either with a graphical client or directly via file system tools. I especially like that you only have to plug in an external USB drive which is immediately recognized, the backup starts and the drive is unmounted as soon as the backup is done. Since Time Machine is Apple only and I use OpenBSD on all my personal machines, I decided to write my own Time Machine like solution.

Goals of my Solution
Automatic, incremental backups as soon as an external USB device is connected
Automatic unmounting as soon as the backup is finished
All data is fully encrypted
No proprietary backup format, just plain files on disk
Turns out, I can solve the goals easily with mostly base software and one program from ports.

Prepare the external Storage
At first, we need to manually format the disk and create an encrypted file system on top. Plug in the disk and find the correct device name by looking at the dmesg output:


```
umass0 at uhub0 port 2 configuration 1 interface 0 "Kingston DataTraveler 2.0" rev 2.00/1.00 addr 2
umass0: using SCSI over Bulk-Only
scsibus4 at umass0: 2 targets, initiator 0
sd2 at scsibus4 targ 1 lun 0: <Kingston, DataTraveler 2.0, PMAP> removable serial.09511607BA7195A60256
sd2: 7640MB, 512 bytes/sector, 15646720 sectors
```
In this example it’s sd2. Now we need to format the disk and create an encrypted file system on top of it.


```
# fdisk -iy sd2
Writing MBR at offset 0.
```

```
# disklabel -E sd2
Label editor (enter '?' for help at any prompt)
sd2> a a
offset: [64] 
size: [15631181] 
FS type: [4.2BSD] RAID
sd2*> w
sd2> q
```

Upon completion you should see a correct disklabel on the disk.

```
# disklabel sd2
# /dev/rsd2c:
type: SCSI
disk: SCSI disk
label: DataTraveler 2.0
duid: f5a87db156d32c6f
flags:
bytes/sector: 512
sectors/track: 63
tracks/cylinder: 255
sectors/cylinder: 16065
cylinders: 973
total sectors: 15646720
boundstart: 64
boundend: 15631245
drivedata: 0 

16 partitions:
#                size           offset  fstype [fsize bsize   cpg]
  a:         15631181               64    RAID
  c:         15646720                0  unused
```
Since the disk is later controlled by a script we cannot use a passphrase here, we need to store the decryption password in a file. Use the tool of your choice to generate a strong password and store it in a file. To match the passphrase and the disk, name the file after the disks duid (can been seen in disklabel’s output above). As last step, set the file’s permission to 600 so that only the owner can access it. Otherwise, bioctl complains about wrong permissions.

Make sure that you save the file in a secure location on your machine. In my case it’s stored in /root and owned by the root user. Further, write the generated password somewhere down in case you need to access your backup disk without (!) having access to your machine! You could print it on a piece of paper and store it somewhere safe.


```
# pwgen 60 | head -1 > f5a87db156d32c6f.pw
```

```
# cat f5a87db156d32c6f.pw
cI5LddxeQDqJ1kYsh2jFy7lXIldh2ifURYrYKfeDCOwCaZ6U6xw4HNgDx6v7
```

```
# chmod 600 f5a87db156d32c6f.pw
```
Now we need to create an encrypted diskabel within the previous one using the file’s content as passphrase:

```
# bioctl -c C -r auto -p f5a87db156d32c6f.pw -l /dev/sd2a softraid0 
softraid0: CRYPTO volume attached as sd3

# disklabel -E sd3
Label editor (enter '?' for help at any prompt)
sd3> a i
offset: [0]
size: [15630653]
FS type: [4.2BSD]
sd3*> w
sd3> q
No label changes.

# disklabel sd3
# /dev/rsd3c:
type: SCSI
disk: SCSI disk
label: SR CRYPTO
duid: 4be3be137f4ba195
flags:
bytes/sector: 512
sectors/track: 63
tracks/cylinder: 255
sectors/cylinder: 16065
cylinders: 972
total sectors: 15630653
boundstart: 0
boundend: 15630653
drivedata: 0

16 partitions:
#                size           offset  fstype [fsize bsize   cpg]
  c:         15630653                0  unused
  i:         15630624                0  4.2BSD   2048 16384 12960
```
To double test that everything works as designed, detach and re-attach the disk:


```
# bioctl -d sd3
# bioctl -c C -p f5a87db156d32c6f.pw -l /dev/sd2a softraid0
```
softraid0: CRYPTO volume attached as sd3
Now we create a file system where the backups will be stored. Using the -O 2 option we can force newfs to create a FFS2 file system.


```
# newfs -O 2 /dev/rsd3i
/dev/rsd3i: 7632.1MB in 15630624 sectors of 512 bytes
38 cylinder groups of 202.50MB, 12960 blocks, 25920 inodes each
super-block backups (for fsck -b #) at:
 160, 414880, 829600, [...]
# mount /dev/sd3i /mnt/
# ls -l /mnt/
```

The external disk is now ready to be used.

Recognize the disk upon Connection
Now, we make sure that the disk is recognized by the system as soon as it’s connected. This can be easily done with hotplugd. To identify the disk we look at the disklabel of each attached disk and run a script as soon as it’s connected.

```
# cat /etc/hotplug/attach
#!/bin/sh

DEVCLASS=$1
DEVNAME=$2

case $DEVCLASS in
    2)
    # disk devices
    duid=`/sbin/disklabel $DEVNAME 2>&1 | sed -n '/^duid: /s/^duid: //p'`
    case $duid in
        f5a87db156d32c6f)
        # Example USB stick
        logger -i "Example USB stick attached"
        sh /root/openbsd-timemachine-backup.sh f5a87db156d32c6f 4be3be137f4ba195 /root/f5a87db156d32c6f.pw
        ;;
    esac
esac
```

So what does the script above? It is called by hotplugd every time a device is attached. It checks if a disk is attached (DEVCLASS is 2) and then get the disk’s duid from disklabel. If the duid matches the on from the backup disk (f5a87db156d32c6f in our case), it starts a script called /root/openbsd-timemachine-backup.sh. The script gets three parameters:

The duid of the USB disk
The duid of the encrypted disklabel within the first one
Full path to the file with the passphrase
It also logs some information to syslog to make you aware that a backup disk is connected.

Install and configure rsnapshot
rsnapshot is used for backing up the data. According to the website “rsnapshot is a file system snapshot utility based on rsync. rsnapshot makes it easy to make periodic snapshots of local machines, and remote machines over ssh. The code makes extensive use of hard links whenever possible, to greatly reduce the disk space required.” So, exactly what we’re looking after.

Install it from ports:


```
# pkg_add rsnapshot
```

The simplest way to configure it, is to copy the example config from /usr/local/share/examples/rsnapshot/rsnapshot.conf.default to /etc/rsnapshot.conf and adapt it as needed. The things you need to configure to make it work with the script below are as follows:


```
# All snapshots will be stored under this root directory.
#
-snapshot_root  /.snapshots/
+snapshot_root  /backup/

# LOCALHOST
-#backup    /home/  localhost/
+backup     /       localhost/
```
Keep the Greek letter names (alpha, beta, …) for the backup levels. Depending on your available backup disk size you might want to tune the number of snapshots to be retained. To make sure that rsnapshot works as expected mount your backup drive to /backup and run it once. Check for errors and resolve them, if needed.


```
# rsnapshot -c /etc/rsnapshot.conf alpha
```
If rsnapshot works as expected we can now configure the script that runs it automatically.

The backup script
The script is quite simple and just decrypts the disk, mounts it and runs rsnapshot to create an incremental backup. You should not need to change something, however, double check the following points:

To avoid nested mounts, the script uses /backup as mount point for the external device. If you prefer another location you have to change the MNTPOIN variable at the beginning of the script and don’t forget to change rsnapshot’s config as well.
As seen above, I created the outer partition as sdXa (note the small letter ‘a’) and the inner partition as sdXi (note the small letter ‘i’). If you chose a different partition in disklabel you have to change the bioctl and mount commands.
If you chose different names for rsnapshot’s backup levels (so others that alpha, beta, …) you have to modify the script accordingly.
Upon the first call, a counter is written to the backup disk. Every 8th run, a rsnapshot gamma backup is done, every 4th run a beta backup, and an alpha backup on all other runs.


```
# cat /root/openbsd-timemachine-backup.sh
!/bin/sh

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

MNTPOIN=/backup
# DUID of the softraid container
OUTER_DUID=$1
# DUID of the disk within the decrypted container
INNER_DUID=$2
# Location to the file containing the passphrase
PASSFILE=$3
# Location to counter file
CNTF=${MNTPOIN}/.counter

# Wrong number of arguments
if [[ -z $OUTER_DUID || -z $INNER_DUID ]]; then
    logger -i -t error "$(basename $0): DUIDs missing. Abort"
    exit 1
fi

if [[ -z $PASSFILE ]]; then
    logger -i -t error "$(basename $0): No path to PASSFILE given. Abort"
    exit 1
else
    if [[ ! -f $PASSFILE ]]; then
        logger -i -t error "$(basename $0): Cannot open $PASSFILE. Abort"
        exit 1
    fi
fi

if [[ -n $(mount | grep ${MNTPOIN}) ]]; then
    logger -i -t error "$(basename $0): Mount point $MNTPOIN is not empty. Abort"
    exit 1
fi

bioctl -c C -p $PASSFILE -l ${OUTER_DUID}.a softraid0 > /dev/null || exit 1
logger "$(basename $0): Backup disk successfully bio-attached"

sync

mount -o softdep,noatime ${INNER_DUID}.i $MNTPOIN || exit 1
logger "$(basename $0): Backup disk mounted successfully to $MNTPOIN"

# First backup of its kind
if [[ ! -f ${CNTF} ]]; then
    echo "1" > $CNTF
fi

i=$(cat $CNTF)
if [ $((i%8)) -eq 0 ]; then
    logger "$(basename $0): Iteration ${i}, doing a gamma backup"
    rsnapshot -q -c /etc/rsnapshot.conf gamma
elif [ $((i%4)) -eq 0 ]; then
    logger "$(basename $0): Iteration ${i}, doing a beta backup"
    rsnapshot -q -c /etc/rsnapshot.conf beta
else
    logger "$(basename $0): Iteration ${i}, doing an alpha backup"
    rsnapshot -q -c /etc/rsnapshot.conf alpha
fi
echo $((i+=1)) > $CNTF

sync

umount $MNTPOIN || exit 1

logger "$(basename $0): $MNTPOIN successfully unmounted"

bioctl -d $INNER_DUID || exit 1

logger "$(basename $0): disk successfully bio-detached"
```

Once you connect the disk you should see a backup job running and similar output to the following in /var/log/messages (timestamps cut):


```
sd2 at scsibus4 targ 1 lun 0: <WD, Elements 25A1, 1018> serial.105825a214463442
sd2: 2861556MB, 512 bytes/sector, 5860466688 sectors
root[28211]: 2TB Backup USB disk attached
openbsd-timemachine-backup.sh: Backup disk successfully bio-attached
sd3 at scsibus3 targ 2 lun 0: <OPENBSD, SR CRYPTO, 006>
sd3: 2097095MB, 512 bytes/sector, 4294852016 sectors
root: openbsd-timemachine-backup.sh: Backup disk mounted successfully to /backup
root: openbsd-timemachine-backup.sh: Iteration 54, doing an alpha backup
rsnapshot[6708]: WARNING: /usr/local/bin/rsnapshot -q -c /etc/rsnapshot.conf alpha: completed, but with some warnings
root: openbsd-timemachine-backup.sh: /backup successfully unmounted
sd3 detached
root: openbsd-timemachine-backup.sh: disk successfully bio-detached
```
