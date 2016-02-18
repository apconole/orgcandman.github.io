---
layout: post
title: Setting up DPDK with vhostuser on RHEL
category: networking
tags: dpdk networking ovs openvswitch vhost vhostuser
year: 2016
month: 02
day: 18
published: false
summary: Setting up virtual machines with dpdk and vhostuser on Red Hat Enterprise Linux
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
       <h2>How hard could it be to not run wires?</h2>
       <p>So, my day job at <a href="https://www.redhat.com/en">Red Hat</a> is to write code to enable datapath. That's fancy speak for &quot;take this packet, and put it there.&quot; For my part, I spend a lot of time with <a href="http://openvswitch.org">Open vSwitch</a> and the <a href="http://dpdk.org">Data Plane Development Kit</a>. Recently, I've been working on making the ramp up using DPDK and OvS to join VMs and networks a bit easier out of the gate. This aims to document some of that work, and how to get up and running using OVS+DPDK and some vhostuser interfaces.</p>
       <p>The first thing you'll need is a couple of VMs that you want to boot. I suggest reading my <a href="/blog/VMs">101 VMs, Open vSwitch, and YOU</a>. This will get you a few VMs to play around with on your system, and will prove out your installation of Open vSwitch.</p>
       <p>If you're using RHEL7.2+ (which I really do recommend), you'll also need to upgrade your qemu-kvm packages to the Tech Preview versions (qemu-kvm 2.3.0). Since you're using RHEL, you have a subscription, and I don't need to document this process.</p>
       <p>If you aren't using RHEL right now, let me first encourage you to think about it. A $300USD developer subscription is a wise investment for testing the waters. But if you're not keen on giving us money (for instance, you prefer Mark Shuttleworth's company), that's cool too - you'll just need to make sure the version of qemu-kvm you use has support for vhostuser baked in. You'll know if it doesn't when it fails loudly trying to install vhostuser entries :)</p>
       <p>Now that the plug is out of the way, time to get Open vSwitch. There's a tech-preview version of OVS 2.4 with DPDK available, but to be honest, we aren't going to use it. The reasons are easy:<ul><li>At the time of this writing, OVS+DPDK 2.5.0 is close to being ready for release anyway</li><li>There is a patch series I'm working on (latest version as of this writing is <a href="http://openvswitch.org/pipermail/dev/2016-February/066085.html">here</a>) that we want to use to improve setup time</li><li>Since I work on it, I prefer building from upstream. The bugs are much more fun :)</li></ul></p>
       <p>So go ahead, and grab DPDK 2.2.0 (I checkout v2.2.0 under git, but you can download) and unzip it. Then configure up a version of openvswitch which uses this version of dpdk (after grabbing the patches)</p>
       <pre class="prettyprint">
#!/bin/bash

setconf()
{
    cf=build/.config
    if grep -q ^$1= $cf; then
        sed -i "s:^$1=.*$:$1=$2:g" $cf
    else
        echo $1=$2 >> $cf
    fi
}

mkdir -p ~/git

pushd ~/git
git clone git://dpdk.org/dpdk
cd dpdk
git checkout v2.2.0

make T=x86_64-native-linuxapp-gcc config

setconf CONFIG_RTE_LIBRTE_VHOST y

setconf CONFIG_RTE_EAL_IGB_UIO n
setconf CONFIG_RTE_LIBRTE_KNI n
setconf CONFIG_RTE_KNI_KMOD n

setconf CONFIG_RTE_NEXT_ABI n
setconf CONFIG_RTE_LIBRTE_CRYPTODEV n
setconf CONFIG_RTE_LIBRTE_MBUF_OFFLOAD n

setconf CONFIG_RTE_BUILD_SHARED_LIB n
setconf CONFIG_RTE_BUILD_COMBINE_LIBS y

make T=x86_64-native-linuxapp-gcc -j8
popd

pushd ~/git
git clone https://github.com/openvswitch/ovs
cd ovs
git checkout 7b383a56a76e2496f630bcfbc8f9b46f82c62081

patches=(582026 582027 582028 582029 582030 582031)
for patch in patches; do
   wget -O patch http://patchwork.ozlabs.org/patch/${PATCH}/mbox
   git am patch
done

./boot.sh
./configure --with-dpdk=${HOME}/git/dpdk/build/ --disable-ssl --prefix=/usr
make -j8
sudo make install
popd
       </pre>
       <p>The above script should build and install a dpdk enabled Open vSwitch for you.</p>
   </div>
</div>
