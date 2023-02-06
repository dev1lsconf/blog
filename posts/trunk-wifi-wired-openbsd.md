---
title: Trunk wired and wifi on OpenBSD
publish_date:  2023-02-06
summary: 'Configure your local network enable Wi-Fi access point in WPA2 mode, DHCP server, and router.'
---
# Connect to Wi-Fi and Ethernet networks from OpenBSD

##by roman zolotarev

Configure your local network (enable Wi-Fi access point in WPA2 mode, DHCP server, and router).

Install OpenBSD on your computer.
Connect to Ethernet network

It should works out of the box.

OpenBSD has em(4) driver for Intel Ethernet network adapter and as in case with many other network drivers em0 network interface should be configured by OpenBSD installer. You can change the configuration anytime.

```bash
echo 'dhcp
up' > /etc/hostname.em0

chown root:wheel /etc/hostname.em0
chmod 0640 /etc/hostname.em0

sh /etc/netstart
em0: no link... got link
em0: bound to 192.168.1.2 from 192.168.1.1 (yy:yy:yy:yy:yy:yy)
```

## Connect to Wi-Fi network

OpenBSD has iwm(4) driver for Intel Wireless network adapter, but it requires firmware files as most of wireless drivers.

OpenBSD runs fw_update(1) to install a prepackaged version of the firmware on the first boot, but you can run fw_update anytime, make sure your Ethernet network is up.

```bash
fw_update
iwm-firmware-0.20170105: ok
```

Write your network configuration (incl. password) to hostname.if(5) and run netstart(8) to start up network.


```bash
echo 'join Home wpakey p@ssw0rd
dhcp
up' > /etc/hostname.iwm0
```


```bash
chown root:wheel /etc/hostname.iwm0
chmod 0640 /etc/hostname.iwm0

sh /etc/netstart

iwm0: no link... got link
iwm0: bound to 192.168.1.2 from 192.168.1.1 (yy:yy:yy:yy:yy:yy)
```

## Connect to another Wi-Fi network

Scan to find Wi-Fi networks near you with ifconfig(8). Update your network configuration and start up network.

```bash
 ifconfig iwm0 up
 ifconfig iwm0 scan
iwm0: flags=8843 mtu 1500
        lladdr xx:xx:xx:xx:xx:xx
        ...
        status: no network
        ieee80211: nwid ""
                nwid Work chan 2 bssid yy:yy:yy:yy:yy:yy 85% HT-MCS23 privacy,short_preamble,short_slottime,radio_measurement,wpa2

 echo 'join Home wpakey p@ssw0rd
join Work wpakey @n0th3r0n3
dhcp
up' > /etc/hostname.iwm0

 sh /etc/netstart
iwm0: no link... got link
iwm0: bound to 10.0.1.2 from 10.0.1.1 (zz:zz:zz:zz:zz:zz)
```

## Roam between wired and wireless

For computers with two or more Ethernet and Wi-Fi network adapters you can configure trunk(4) pseudo-device to create a link failover interface.

With this configuration when Ethernet is connected OpenBSD uses em0 interface, otherwise it tries to connect to one of Wi-Fi networks via iwm0.

```bash
echo 'up' > /etc/hostname.em0

echo 'join Home wpakey p@ssw0rd
join Work wpakey @n0th3r0n3
up' > /etc/hostname.iwm0

echo 'trunkproto failover trunkport em0 trunkport iwm0
dhcp
up' > /etc/hostname.trunk0

chown root:wheel /etc/hostname.*
chmod 0640 /etc/hostname.*

sh /etc/netstart
trunk0: no link... got link
trunk0: bound to 192.168.1.2 from 192.168.1.1 (yy:yy:yy:yy:yy:yy)
```

## Troubleshooting

Shout down all network interfaces: em0, iwm0, and remove trunk0. Reset the routing tables.


```bash
 ifconfig em0 down
 ifconfig iwm0 down
 ifconfig trunk0 destroy
 route -n flush

```

Check your /etc/hostname.* files as described in the previous section.

Then start up the network, check the statuses of all the network interfaces with ifconfig(8), check address resolution protocol (ARP) entries with arp(8), check the routing tables with route(8), and ping(8) your default gateway.

```bash
 sh /etc/netstart
trunk0: no link.... got link
trunk0: bound to 192.168.1.2 from 192.168.1.1 (yy:yy:yy:yy:yy:yy)
```


```bash
 
 ifconfig
...
em0: flags=8b43 mtu 1500
        lladdr xx:xx:xx:xx:xx:xx
        index 2 priority 0 llprio 3
        trunk: trunkdev trunk0
        media: Ethernet autoselect (1000baseT full-duplex,rxpause,txpause)
        status: active
iwm0: flags=8943 mtu 1500
        lladdr xx:xx:xx:xx:xx:xx
        index 1 priority 4 llprio 3
        trunk: trunkdev trunk0
        groups: wlan
        media: IEEE802.11 autoselect (HT-MCS0 mode 11n)
        status: active
        ieee80211: join Home chan 40 bssid zz:zz:zz:zz:zz:zz 67% wpakey wpaprotos wpa2 wpaakms psk wpaciphers ccmp wpagroupcipher ccmp
trunk0: flags=8843 mtu 1500
        lladdr xx:xx:xx:xx:xx:xx
        index 33 priority 0 llprio 3
        trunk: trunkproto failover
                trunkport iwm0
                trunkport em0 master,active
        groups: trunk egress
        media: Ethernet autoselect
        status: active
        inet 192.168.1.2 netmask 0xffff0000 broadcast 192.168.255.255
```

```bash
arp -a
Host                  Ethernet Address    Netif Expire    Flags
192.168.1.1           yy:yy:yy:yy:yy:yy  trunk0 19m59s
192.168.1.2           xx:xx:xx:xx:xx:xx  trunk0 permanent l
```

```bash
route -n show -inet
Routing tables

Internet:
Destination        Gateway            Flags   Refs      Use   Mtu  Prio Iface
default            192.168.1.1        UGS        4        8     -     8 trunk0
...
192.168/16         192.168.1.2        UCn        1   104371     -     4 trunk0
192.168.1.1        yy:yy:yy:yy:yy:yy  UHLch      1   103533     -     3 trunk0
192.168.1.2        xx:xx:xx:xx:xx:xx  UHLl       0      113     -     1 trunk0
192.168.255.255    192.168.1.2        UHb        0       30     -     1 trunk0
```

```bash
ping -c 2 -I 192.168.1.2 192.168.1.1
PING 192.168.1.1 (192.168.1.1): 56 data bytes
64 bytes from 192.168.1.1: icmp_seq=0 ttl=64 time=0.443 ms
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.398 ms

--- 192.168.1.1 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/std-dev = 0.398/0.421/0.443/0.023 ms
```
sources: https://romanzolotarev.com/m/on.html
