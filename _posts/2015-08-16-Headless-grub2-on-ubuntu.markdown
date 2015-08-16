---
layout: post
title: Headless Grub2 on Ubuntu
category: Development
tags: blog 
year: 2015
month: 8
day: 16
published: true
summary: Setting up a headless Grub2 Installation
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
   <h2>Headless Grub2 on Ubuntu 12.04LTS (possible 14.04, as well)</h2>
   <p>Once upon a time, I was building an embedded platform which ran an unmodified Ubuntu 12.04LTS base image, onto which our embedded applications ran. A few changes were made to that system. The first, which isn't discussed here, is to build and install Linux 3.6.6, with the realtime patchset applied. The second, which this article will discuss, was to modify the GRUB configuration to eliminate the annoying prompting that happens when the system crashes, reboots unexpectedly, etc.</p>
   <p>As a tangent, when building a 'bench-type,' network accessible product (test equipment, scope, etc.) which ships it's important that at no point in time should the user have to log directly into the box. After all, worst case, they should just expect to reboot the machine and have things work. As a failsafe, I configured the system to reboot when kernel faults occur (using /proc/sys/kernel/panic_on_oops file, and a linux command line option to reboot on panic). This is great for us - we almost never see these panics (and it's typically due to a vendor supplied driver which fails); when they do happen, the box restarts within a minute so the user is ready to continue from where they left off with only a minor interruption. Ideally, this wouldn't happen, but we don't live in an ideal world.</p>
   <p>Unfortunately, when this first would happen, GRUB2 would not start correctly. It would hang waiting for someone to pick the boot option to proceed. This turned from an annoyance into a possible show-stopper. After all, our product didn't have monitor/keyboard exposure to the user. We had to fix it.</p>
   <p>There's a couple of important options we needed to tweak. The first is the <code>GRUB_RECORDFAIL_TIMEOUT</code> option. This option means that when GRUB detects boot or system failure, it will either timeout for the amount of seconds indicated, or it will hang forever (if the value is -1). This needs to be added to <em>/etc/default/grub</em>.</p>
   <p>The second option happened after a power failure while the system was journaling data to the disk. In this case, the system started to boot normally, but detected a need to run <em>/sbin/fsck</em>, and required a root password entry before continuing. The way around this was to change <code>FSCKFIX=no</code> to <code>FSCKFIX=yes</code> in <em>/etc/default/rcS</em>. After these edits, running update-grub is required.</p>
   <p>Of course, doing this manually was not an option; thanks to the power of dpkg's postinst scripting, the code to do this looked something like:</p>
   <pre class="prettyprint">
#!/bin/bash

DO_UPGRADE_GRUB=no

FOUND_GRUB_FAIL_LACKING=$(/bin/grep 'GRUB_RECORDFAIL_TIMEOUT' /etc/default/grub)

if [ "$?" == "1" ]; then
    /bin/echo "GRUB_RECORDFAIL_TIMEOUT=5" >> /etc/default/grub
    DO_UPGRADE_GRUB=yes
else
    FOUND_TIMEOUT_NEGONE=$(/bin/grep 'GRUB_RECORDFAIL_TIMEOUT=-1' /etc/default/grub)
    if [ "$?" == "1" ]; then
        /bin/sed -rei 's@GRUB_RECORDFAIL_TIMEOUT=-1@GRUB_RECORDFAIL_TIMEOUT=5@' /etc/default/grub
        DO_UPGRADE_GRUB=yes
    fi
fi

FOUND_FSCKFIX=$(/bin/grep 'FSCKFIX=' /etc/default/rcS)
if [ "$?" == "1" ]; then
    /bin/sed -rei 's@FSCKFIX=no@FSCKFIX=yes' /etc/default/rcS
else
    /bin/echo 'FSCKFIX=yes' >> /etc/default/rcS
fi

if [ "$DO_UPGRADE_GRUB" == "yes" ]; then
   /usr/sbin/update-grub
fi

   </pre>
   <p>The above script is close to what I've actually put in a postinst file. The <code>sed</code> lines were changed a bit, YMMV as far as their working. However, this is a simple way of making a server run headless; and a way of editing some embedded application <b>.deb </b> postinst control file to enable that.</p>
