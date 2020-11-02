---
title: "WPA2 Enterprise Login"
date: 2020-09-05
description: Micropost on WPA2 Enterprise wifi login
titleWrap: wrap
enableSidebar: false
enableToc: false
tags: ['linux', 'utility', 'micropost']
---

## Wifi

Linux gives gives you more access to the operating system on a lower level, and is very nice in tailoring your software environments the way you want it to be. The downside however is that sometimes seemingly simple things can be troublesome in Linux - for example logging on the corpy wifi. Linux has NetworkManager with the nmcli utility however, which is a big rescue.

Below are the commands I used to log into the manpowergroup wifi:

```shell

nmcli con add type wifi ifname INTERFACE con-name CONNECTION_NAME ssid SSID

nmcli con edit id CONNECTION_NAME

nmcli> set ipv4.method auto

nmcli> set 802-1x.eap peap

nmcli> set 802-1x.phase2-auth mschapv2

nmcli> set 802-1x.identity USERNAME

nmcli> set 802-1x.password PASSWORD

nmcli> set wifi-sec.key-mgmt wpa-eap

nmcli> save

nmcli> activate

```

Taken from [this reddit post](https://www.reddit.com/r/linuxquestions/comments/b1b8jo/psa_for_people_struggling_with_wifi_on_linux_on/)
