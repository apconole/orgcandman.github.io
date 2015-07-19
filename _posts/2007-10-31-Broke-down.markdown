---
layout: post
title: Broke down...
category: Hardware
tags: hardware htpc hacking
year: 2007
month: 10
day: 31
published: true
summary: My hacking on an htpc
image: none.jpg
---

<div class="row">
    <div class="span9 columns">
        <h2>Home theater PCs are the new hotness</h2>
        <p>I finally broke down and ordered the missing pieces that I'd need to build my DVR machine. I originally started by using a stripped down NetX Embedded board, but was quickly frustrated with the fact that it used an odd case design making my PCI Riser card unusable.</p>
        <p>So, with a lightening of my wallet, I purchased the following (from <a>itxdepot.com</a>)</p>
        <ol>
            <li>EPIA ME 6000G (170mm x 170mm size, 2x ATA133 connectors, onboard MPEG2 playback accelerator, S-Video, LVDS, 1x PCI, 1x Serial, 600MHz C7, 1GB memory, fanless)</li>
            <li>2699R black case</li>
            <li>Slimline DVDRW</li>
            <li>160GB HDD (2.5")</li>
            <li>assorted lengths of wire</li>
        </ol>
        <p><b>TOTAL COST:</b> (Including 2-day shipping) $450</p>
        <p>Why did I choose these things?</p>
        <p>The 6000G is not a powerhouse for computing. However, I don't need anything super duper since it'll just be controlling the Hauppage PVR-250 card. I'm gonna front-end with MythTV (probably just use the KnoppMyth distribution since I'm too busy to spin my own custom linux build). The nice thing about having hardware encoder/decoder for MPEG2 is that my CPU could have all the processing power of a wet turd, and it wouldn't matter. I'm hoping to someday get a wifi connection to the box, but we'll save those hopes and dreams for later.</p>
        <p>My plans for this are semi-big. It'll be my set top box. It'll control everything. Sound, video, pictures, and all manner of other things. I'll hopefully have a full media box in a week or two.</p>
    </div>
    <div class="span9 columns">
        <p>As a link to the past, I've gone back to try and get the awesome code I wrote below for stack tracing working on an alpha.</p>
        <p>What I found was the axp platform does not keep a reference to the previous frame pointer on the stack all nice and neat. Therefore, we have to do some wonky hacking. We basically traverse the stack, one byte at a time mind you, dereferencing it until we locate what _could_ be a frame (by either an lda or subq instruction). Not exactly a good time. <b>Update:</b> MIPS is similar</p>
        <p>But, at least, still possible to do entirely in C, albeit...this time you'll have to know the assembly. </p>
    </div>
</div>
