---
categories: SysAdmin
description: Getting awesome GPG signatures on git commits!
layout: post
featured_image: covers/verified.png
author: Anders
tags: ['security', 'crypto', 'gpg']
finished: true
date: "2019-02-27"
title: Welcome to the VIP
---

## Being Verified

Computer security in essence boils down to two things:

- Authentication : How can we prove who you are?
- Authorization : What access do you have?

Implementing secure systems often comes down to good habits. This
is one topic where the broken window theory tends to show its symptomps.
Meaning small hacks, lazinesses and lowering of standards tend to propagate and
eventually cause the whole system to become and unmaintainable mess.

I absolutely recommend reading the pragmatic programmer for more on this.

Good crypto habits is a good thing. If you are to be trusted as an
administrator of a system, then you should have good habits on crypto, and take
computer security seriously.

### Signing commits with GPG

Gnu Privacy Guard or GPG is the underlying open source clockwork behind a lot
of crypto in the UNIX ecosystem. So lets use it to sign our commits.  Heres the
breakdown.

**First lets create the key pair**

```bash
gpg --gen-key
gpg --list-secret-keys --keyid-format LONG # find the <key>
gpg --armor --export <key> # Public key for github
```

**And configure git and git(Hub/Lab)**

```bash
git config --global user.signinkey <key>
git config --global commit.gpgsign true
```

The public key provided in the line of the first stage should be put in your
account on github/gitlab/whatever

Congrats, you should now be verified!
