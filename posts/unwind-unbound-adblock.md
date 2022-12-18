---
title: OpenBSD - unwind + Unbound - Adblock 
publish_date: 2022-10-26
summary: 'Unbound-adblock es una utilidad de firewall de DNS rápida, flexible y fácil de usar. Le permite bloquear contenido en línea no deseado en toda su red.' 
---

unbound-adblock 0.5 OpenBSD Installation Instructions 
Copyright 2018-2021 Jordan Geoghegan <jordan@geoghegan.ca>


## Table of Contents:

1) Unwind Configuration Notes

2) Fresh Install Instructions

3) Post Install Notes

### Notes:

1) This guide assumes you know how to setup unwind. If not, there are plenty of online guides to setting up unwind.

## OpenBSD Unwind Quick Start:

```
rcctl enable unwind
rcctl start unwind
echo 'supersede domain-name-servers 127.0.0.1;' > /etc/dhclient.conf
sh /etc/netstart
```

# Fresh Installation Guide 

2) Download script:


```
$ ftp https://geoghegan.ca/pub/unbound-adblock/0.5/unbound-adblock.sh
```

3) Create a new user (we'll call ours "_adblock"):
 The user should be created with a default shell of "nologin", home folder set to /var/empty/ with no password specified (disables password logins)


```
 useradd -s /sbin/nologin -d /var/empty _adblock
```

4) Install script with appropriate permissions:

```
install -m 755 -o root -g bin unbound-adblock.sh /usr/local/bin/unbound-adblock
```

4.b) OPTIONAL: Install RipGrep and mawk for greatly improved performance:
Note: RipGrep is not available on all CPU architectures, use ggrep if affected.


```
pkg_add ripgrep mawk
```

5) Create required files:


```
install -m 644 -o _adblock -g wheel /dev/null /var/db/unwind-adblock.db
install -d -o root -g wheel -m 755 /var/log/unbound-adblock
install -o _adblock -g wheel -m 640 /dev/null /var/log/unbound-adblock/unbound-adblock.log
install -o _adblock -g wheel -m 640 /dev/null /var/log/unbound-adblock/unbound-adblock.log.0.gz
```

6) Give user '_adblock' strict doas permission for the exact commands the 
script needs run as superuser. NOTE: Unlike 'sudo', _ALL_ users must be explicitly granted permission to use doas, even the root user.

Note: unbound-adblock 0.5 errata 004 changed the doas permissions to be less permissive and more portable 
 
```
$ cat /etc/doas.conf

...
permit root
permit nopass _adblock cmd /usr/sbin/unwindctl args reload
...
```

7) Add blocklist to unwind.conf:


```
vi /etc/unwind.conf
...
block list "/var/db/unwind-adblock.db" log
...

```

8) Run script manually to parse and load the adblock ruleset:

```
doas -u _adblock unbound-adblock -o unwind -O openbsd
unwind(ok)
```

10) Edit _adblock users crontab to run unbound-adblock every night:

```
crontab -u _adblock -e
...
~ 0~1 * * *	-s unbound-adblock -o unwind -O openbsd
...
```
Yay! unbound-adblock is now installed!


### The Real DNS Firewall!


With the nightly cron job, the list will be regularly updated with
the latest known bad hosts.

Please read the man page for information on how to configure unbound-adblock.
The manpage can be found here: https://www.geoghegan.ca/pub/unbound-adblock/0.5/man/man.txt

[Fuente](https://www.geoghegan.ca/unbound-adblock.html)


