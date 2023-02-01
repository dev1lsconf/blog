---
title:  Hardened Archlinux
publish_date:  2022-12-24
summary: 'This guide provides a walkthrough of how to turn on many of these features during installation, as well as reasoning for why certain features help improve security.' 
---


# Building a Secure Arch Linux Device

Locking down a linux machine is getting easier by the day. Recent advancements in systemd-boot have enabled a host of features to help users ensure that their machines have not been tampered with. This guide provides a walkthrough of how to turn on many of these features during installation, as well as reasoning for why certain features help improve security. 

The steps laid out below draw on a wide variety of existing resources, and in places I'll point to them rather than attempt to regurgitate full explanations of the various security components. The most significant one, which I highly encourage everyone to read, is Rod Smith's [site about secure boot](https://www.rodsbooks.com/efi-bootloaders/secureboot.html), which is the most comprehensive and cogent explanation of UEFI, boot managers and boot loaders, and secure boot. Another incredibly useful resources is [Safeboot](https://safeboot.dev), which encapsulates many of the setup steps below in a Debian application. Finally, the Arch Wiki pages for [Secure Boot](https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface/Secure_Boot), [disk encryption](https://wiki.archlinux.org/title/Dm-crypt/Encrypting_an_entire_system), and [systemd-boot](https://wiki.archlinux.org/title/Systemd-boot). Many of the decisions to use certain technologies were inspired by Matthew Garret's [Producing a trustworthy x86-based Linux appliance](https://mjg59.dreamwidth.org/57199.html).

## How best to use this guide

Using Linux is designed to be an empowering and enriching experience. Therefore, I'd like to issue a word of caution about blindly following this gude (no judgment though, I do it too). At many points in this guide there will be a series of steps with fairly complex commands, but I urge you to pause and think about each one. It may be slow and painful, and it will definitely require some googling, but if you don't proceed with intent it's possible to end up with a system that has and does a bunch of stuff that you don't understand. As this is a guide about security, that's, like, bad. Not that you should know how every intricate detail of Arch Linux, UEFI, TPMs, etc. work; I'm pretty sure no one does. But you should at least know how to find out if you come across something that is causing you trouble. It's a hard-earned skill, but you can get almost all of the way there by just paying close attention. I'll try to tip you off to when you should pay closer attention where I can, but neither of us is perfect, so make your best effort and I'll make mine.

I'm getting off the high horse now and getting on with the show. 

### Table of Contents
1. [Getting Started](#Getting-Started)
3. [Setting up Secure Boot](#Setting-up-Secure-Boot)
4. [Using TPM2-TOTP](#Using-TPM2-TOTP)
5. [Using systemd-cryptenroll](#Using-systemd-cryptsetup)
6. [Working with dm-verity](#Working-with-dm-verity)
7. [Swapping `doas` for `sudo`](#Swapping-doas-for-sudo)

## Getting Started

The first step is to install Arch normally, following the [installation guide](https://wiki.archlinux.org/title/Installation_guide). You will likely have to disable Secure Boot in your device's firmware before you can boot the archiso USB stick, which is good practice for later on. I would strongly recomend relying on the `archinstall` script to do the install, making sure to turn on disk encryption.

## Setting up Secure Boot

Now we are ready to implement Secure Boot. I want to stress again that I highly recommend Rod Smith's [super comprehensive explanation](https://www.rodsbooks.com/efi-bootloaders) of what UEFI and Secure Boot are and how they work. I will provide a breif recap here and dive into setting up Scure Boot.

Secure Boot is a feature of the Unified Extensible Firmware Interface (UEFI), which we've already been interacting with on the down low. UEFI is basically a standard set of features that device firmware can implement (including a first-stage bootloader), and Secure Boot is one of its features. UEFI firmware has a notion of EFI executables that can be run after the firmware gets initialized (if you've ever mashed F12 repeatedly after pushing the power button to launch a live USB, the menu that comes up to let you select the live image is a list of EFI executables that the firmware has found. 

Systemd-boot is a specific kind of EFI executable called a *boot manager* (also referred to as a second-stage boot loader), that in turn has a more sophistacted set of features for deciding what programs get control on boot. In principle, with the Linux kernel's EFISTUB implementation, you could just launch the kernel directly from UEFI, but this offers less flexibility (you can only boot one thing, whereas with a boot manager you can set multiple options, i.e. a regular image, a recovery image, rebooting into the firmware, etc). Additionally, using a boot manager gives us the ability to use software at boot time to do things like decrypting the hard disk, interacting with the TPM, and measuring the firmware, boot manager, and kernel to make sure nothing has changed unexpectedly. 

### Generating keys

Secure boot works by generating a set of signing keys which are used to cryptographically sign EFI executables so that only signed executables can be run via a UEFI implementation with Secure Boot turned on. Secure Boot relies on two different keys, a Platform Key (PK) and a Key Exchange Key (KEK). I'm not going to go into depth here, again check out Rod Smith's site, but briefly the PK is associated with your platform (usually the TPM on the motherboard), the KEK is used to sign a trusted list of signatures and keys (referred to as the database or db), and also to sign a ban list of signatures and keys not trusted by the machine owner (dbx). There are also pther auxiliary keys like Machine Owner Keys (MOKs) that came about as a way for one signing authority to delegate others, but again that's not really important to our discussion here. 

To generate the keys and signatures we need to get Secure Boot working, I recommend just pulling down Rod Smith's script, described [here](https://www.rodsbooks.com/efi-bootloaders/controlling-sb.html#creatingkeys) and wget'able [here](https://www.rodsbooks.com/efi-bootloaders/mkkeys.sh). You also need the `efitools` package. 

```
sudo pacman -S efitools
sudo mkdir /etc/efi-keys
cd !$
sudo wget https://www.rodsbooks.com/efi-bootloaders/mkkeys.sh
sudo chmod +x mkkeys.sh
sudo ./mkkeys.sh
```

The script will ask you to enter a Common Name, part of the X509 certificate standard. You can just put in whatever you'd like. 

### Generating and signing a unified EFI image

Now that we have signing keys, it's time to sign. I really like the [`sbupdate` tool](https://github.com/andreyv/sbupdate#sbupdate), which makes it seamless to generate a unified kernel and bootloader image as well as sign it. Installing `sbupdate` also installs pacman hooks which automatically remake and sign the unified image whenever the system is updated, so you don't have to do it manually every time. Of course, the usual caveats about choosing which software to include in your trusted arsenal apply, but fortunately it's a quite small package that consists of a bash script and some hooks, so it's fairly easy to verify by eye.
```
yay -S sbupdate
```

`sbupdate` does require some configuration, as once it is installed it is the program responsible for setting the kernel command line, splash screen, and other things. 

```
KEY_DIR="/etc/efi-keys"
ESP_DIR="/boot"
OUT_DIR="EFI/Linux"
#SPLASH="/usr/share/systemd/bootctl/splash-arch.bmp"
#BACKUP=1
EXTRA_SIGN=('/boot/EFI/BOOT/BOOTX64.EFI' '/boot/EFI/systemd/systemd-bootx64.efi')
CMDLINE_DEFAULT="cryptdevice=UUID={UUID}:luksdev root=/dev/mapper/luksdev quiet splash rw"
```

Note that the `CMDLINE_DEFAULT` variable contains the same thing as the `options` variable from our systemd-boot file above, so make sure `{UUID}` is replaced correctly as in that file. Alternatively, you can just `cat /proc/cmdline >> /etc/sbupdate.conf` from a root shell and adjust as needed. The `EXTRA_SIGN` variable tells `sbupdate` to also sign and include systemd-boot and the basic Linux EFI stub into the unified image. 

Now, run the tool:
`sbupdate`

There should now be a file `linux-signed.efi` in `/boot/EFI/Linux` that corresponds to our signed unified image. Systemd-Boot should pick this up automatically if there are no entries present in `/boot/loader/entries`. If you've found this is not the case, you can add a systemd-boot entry to use the signed image only. Open the `/boot/loader/entries/arch.conf` file in your editor of choice and change it to this:

```
title Arch Linux Signed
efi   /EFI/Linux/linux-signed.efi
```

Make sure to run `sudo bootctl update` to tell systemd-boot that there's a new boot image to load. 

### Configuring Secure Boot in firmware

At this point we have now generated keys and a unified kernel image, and signed it, but the firmware still doesn't know what keys to trust, so we have to tell it. Reboot into the firmware interface. If you'd like to avoid having to mash the F2 key on reboot every time, you can use bootctl to reboot into the firmware interface: 

```
sudo bootctl set-oneshot auto-reboot-to-firmware-setup
sudo reboot
```

On reboot, if you haven't already, the first thing you should do is set an administrator password on your firmware interface. It's not much good configuring Secure Boot if someone can just go in and turn it off! As with your disk encryption password, do not forget this password! But also pick a good one that's unique and memorable. If you absolutely must, stash the password in a password manager that you trust. 

After that, it's time to enroll the keys you generated earlier into the firmware. On some devices, like the Framework laptop, you can do this directly from the firmware interface. On the Secure Boot page, there are options for locating the PK, KEK, db, and dbx files on the boot partition. 

If you aren't so lucky as to have an awesome firmware interface that can enroll keys, you'll have to use `sbkeysync` or `KeyTools`, instructions for which you can find on the [Arch wiki](https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface/Secure_Boot#Enrolling_keys_in_firmware). I've never had much luck with `sbkeysync`, but hopefully you will. Remember to set your firmware interface to `Setup Mode` before trying to use either. 

If you're using KeyTool, make sure to copy your keys over to `/boot` so that it can find them. 

**IMPORTANT:** Make sure you make backups of the existing keys. Depending on your device, turning on Secure Boot and trying to use new keys may make existing option ROMs unusable by the firmware, **effectively bricking your device.** This is especially an issue with CPUs that don't have internal graphics available; see the discussion [here](https://github.com/osresearch/safeboot/issues/84). If you think your device may need to use opROMs to boot, proceed with *extreme* caution. There are usually ways to restore the factory boot keys, e.g. by setting jumpers on the board. I don't believe this will be an issue with most newer consumer devices, but be warned. Always make sure to back up the existing keys. There may also [be ways to sign opROMs](https://github.com/osresearch/safeboot/issues/84#issuecomment-815402662) or to [add their hashes to `db`](https://github.com/Foxboron/sbctl/issues/85#issuecomment-886539689), but this is not a beginner friendly operation. 

After the keys are enrolled, make sure to regenerate the initramfs and the unified kernel, and resign it. 

```
sudo mkinitcpio -P
sudo sbupdate
```

Finally, turn on Secure Boot in the firmware interface and reboot. If you get into the OS, congratulations, you've successfully setup Secure Boot with keys only known to you! After this step, make sure to remove the keys from your `/boot` partition, as that partition isn't encrypted and will leak the keys to an attacker, which kind of defeats the point. 

## Using TPM2-TOTP

We now have Secure Boot setup! Wonderful! However, there is still potential for someone to tamper with the system undetected. An attacker can attach a microcontroller to the motherboard of the device and flash a new database of signed EFI executables, and then boot whatever they want. While we can't stop this attack, we can make it easier to detect using the Trusted Platform Module (TPM) that is resident on pretty much every x86 system produced in the last ten years (and even some non-x86 ones).

As part of the Secure Boot process, boot "measurements" are made and stored in the TPM, which provides secure registers that are difficult (though not impossible) to read without proper authorization. The registers are called platform configuration registers (PCRs), and each register contains certain data specified by the TPM standard. For example, PCR0 contains a hash of information about the device, including the firmware binary as well as a unique token stored in the TPM on the device. This means that PCR0 values are unique and cryptographically hard to fake. PCR values are also chained, so that the value in PCR1 contains a hash of new data (the specifics of which are not relevant here) *plus* the hash stored in PCR0. So on and so forth for the other PCRs. PCR7 contains a hash of the Secure Boot policy, including a hash of the databse of trusted keys, along with the hash chain, meaning that if we can have a reliable way to check its value we can make sure that our trusted databases have not been tampered with. 

This is where TPM2-TOTP comes in. It's a utility that takes advantage of the TPM's ability to generate time-based one-time passwords (TOTPs) just like the ones used by multifactor authentication apps. The TPM generates a secret based on the current values of the PCRs and some other data and shares that data with the user via a QR code. The QR code can be used with any MFA app (I like Aegis).

On boot, the TOTP is displayed at the screen where the user enters the disk encryption password, offering an opportunity to verify the state of the system before entering in a password that could potentially be sniffed by malicious software. If the TOTP doesn't match the one on the user's verification app, something has gone wrong and the system should not be trusted. 

TPM2-TOTP can be found in the official repositories, as well as a `git` tracked version in the AUR and [here](https://github.com/tpm2-software/tpm2-totp). The official repo should work, but if it doesn't downloading the source and compiling it may be necessary to correctly configure the hooks needed by systemd-boot to display the codes. Most of the depencies should already be installed, though you will need to grab the `autoconf-archive` package. 

Install from official sources:
```
sudo pacman -S tpm2-totp
```

Install and build from source: 
```
sudo pacman -S autoconf-archive tpm2-tss qrencode
git clone https://github.com/tpm2-software/tpm2-totp
cd tpm2-totp
./bootstrap
./configure --sysconfdir=/etc
make
sudo make install
```
Note: the commands in the git repo are different than in the Arch repo, so I encourage you to look at the help message to figure out which set of commands you need to use. 

Now generate a new secret:
```
sudo tpm2-totp --pcrs=0,7 generate
```

Scan the QR code with your preferred authentication app, and then check that it worked:
```
sudo tpm2-totp calculate
```

Make sure `tpm2-totp` appears in the `HOOKS` section of `/etc/mkinitcpio.conf` *before* `encrypt`, then regenerate the initramfs, resign, and reboot.
```
sudo mkinitcpio -P
sudo sbupdate
sudo reboot
```

If the value you see is the one on your other device, things should be working. Regenerate the initramfs and resign, then reboot. At the password prompt, you should see the code, which you can verify. 


### Installing with Plymouth


If you would like a better looking version of this, install plymouth before installing TPM2-TOTP. The `./configure` step should automatically detect that plymouth is installed and do the right thing. Note that you will have to add `systemd sd-encrypt sd-plymouth sd-plymouth-tpm2-totp` to your `/etc/mkinitcpio.conf` file's `HOOKS` section. 
```
sudo mkinitcpio -P
sudo sbupdate
sudo reboot
```

I've managed to get this working on my Framework laptop, but not on the Lenovo I'm using to write this guide. It's a little finicky, and it might be easiest just to stick with the default.

## Using systemd-cryptenroll [WIP]

If you don't want to have to type in a password at boot every time, you can enroll your LUKS key into the TPM using `systemd-cryptenroll`. Doing this will ensure that your disk is only decrypted if the system state (as measured by Secure Boot) matches a known-good configuration. Using the following configuration will ensure that the disk is unlocked only if everything up to and including the kernel match expected values (replace `/dev/tpmrm0` with the path to your tpm2 device, or use `auto`): 
 
```
systemd-cryptenroll --tpm2-device=/dev/tpmrm0 --tpm2-pcrs=0+2+4+5+7 /dev/nvme0n1p2
```
It will prompt you to enter a password, and if successful should unlock your disk on the next boot up. **Note:** you must re-enroll your key every time your kernel changes (every time sbupdate gets run), otherwise your disk will no longer decrypt automatically. 

You also must replace the `encrypt` hook with `sd-encrypt`, `plymouth` with `sd-plymouth` (if you're using plymouth), and add the `systemd` hook in your mkinitcpio.conf:

```
HOOKS=(systemd base udev sd-plymouth autodetect keyboard keymap modconf block plymouth-tpm2-totp sd-encrypt filesystems fsck)
```

**WARNING:** enabling automatic decryption may make you more vulnerable to evil maid attacks, as you will not have the same opportunity to verify the state of the system before the disk decryption key is unsealed. Do this only if you know what you are doing!

## Working with dm-verity

[TODO]

## Swapping `doas` for `sudo`

`doas` is OpenBSD's replacement for `sudo`, featuring a much more elegant codebase that has a smaller attack surface in comparison with sudo. This makes it more likely that systems relying on `doas` for privilege escalation are less likely to be impacted by bugs [like this one](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3156). On Arch, it is super easy to replace `sudo` with `doas`:

```
yay -S opendoas
```

This installs `doas`, which I configure as follows in `/etc/doas.conf:

```
permit persist :wheel
```

This allows any member of the `wheel` group to get root privileges. `persist` allows the authentication to be retained for up to five minutes, so you don't have to keep typing in your password. 

It's important that we remove `sudo` as well, otherwise we'll still be susceptible to flaws in it that permit privilege escalation attacks. Doing so is really easy:

```
yay -S opendoas-sudo
```

This will symlink `sudo` to `doas`, as well as uninstalling sudo if you enter `y` at the prompt. 
