---
categories: Linux
subtitle: Saving lost penguins
description: Saving lost penguins
featured_image: covers/tux-1.png
author: Anders
title: Stuck at Terminal Island
finished: true
date: "2018-07-29"
layout: post
tags: ['linux', 'terminal', 'networking']
---
## Terminals are great

Being good on the terminal gives you fine grained control over a system.  It is
the hallmark skill and language of the system administrator, and even if you're not
a professional sysadmin, you still have manage a system of some sort and it would help you to be
able to manage it efficiently.  If you're into IT and technology in any way
it should be obvious that obtaining linux skills is pretty much always a good investment.

So once in a while I am stuck at a terminal island for some reason. What is terminal island? Well all you have is a terminal, but you also have no network connection.  There are no cables available, and it would be so very nice to connect to wifi... from the terminal. This can happen if for example youre booting into a linux system on a usb stick on a laptop and you have no cabeled network, or you're at a public place and your wifi GUI app is malfunctioning (both have happened to me). This is a horrible situation, because you will have to google your way to wifi from your phone, and if you're not an expert on wifi, networking and linux system administration from before, then you're gonne have a bad time. 

![Bad time picture](/assets/img/blog/bad_time_wifi.jpg)

The web is flooded with high verbosity on this subject, which is expected because there are a handful of different wifi security standards (and your first search result will for some reason be on WEP, which is insecure and hardly used). Networking is a big subject, and can be quite hard to understand unless you have experience with both networking and the specific networking technology (like good luck with understanding the bluetooth stack in a resonable amount of time). And you don't care.. you just want to connect to the WiFi!

I thought that knowing wifi connection from the terminal would be a useful feather in my SysAdmin hat, so at some point I decided to create a TL;DR guide on this in my notes (didn't find anything sufficient simple online), and I noticed it would be a decent blogpost, so I thought I'd share it!

## TL;DR

#### Prerequisite
These tools usually come standard with most linux distros
- wpa_supplicant
- net-tools

#### Getting Status
- Interface status : 

```$ ifconfig / ip addr show```
- WLAN status : 

```$ iw <wlan inerface> info```

#### Enable wlan interface
- Up : 

```$ ifconfig <interface> up```

#### Find networks
- Scan : 

```$ iwlist <interface> scan```

#### Connect
- WEP : 

```
$ iwconfig <interface> essid <network name> key s:<password>
```

But if you/sysadmin have any sense, you're probably using some flavor of wpa
- WPA : Couple of steps
   * Connection config creation : 

```
$ wpa_passphrase <ssid> > <configfile>.conf
```

-> Next you will be prompted for network password
   * Connect to network : 

```
$ wpa_supplicant -B -i<interface> -c<config (from above cmd)> -D<type (wext or nl80211 usually works)>
```
   * Release DHCP leases : 

```$ dhclient -r```
   * Get new DHCP lease : 

```$ dhclient <interface>```

#### Common issues / FAQ
- After running wpa_supplicant, ioctl might throw an error saying "Invalid argument".  This can be ignored
- When running wpa_supplicant, a process will be started.  If you have multiple processes running, then you will not be able to connect to network because of conflicts.  Therefore make sure you killall wpa_supplicants before running a new one :
          ```$ killall wpa_supplicant```
- I prepended all commands with $, however many of them might have to be run as root (#), so do that when that is needed.
