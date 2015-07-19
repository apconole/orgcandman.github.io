---
layout: post
title: Broken down
category: Hardware
tags: hardware htpc hacking
year: 2007
month: 11
day: 5
published: true
summary: Working with open source and HTPC
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>Progress with HTPC</h2>
      <p>Got my DVR equipment, and decided to start in on it right away. Since I didn't have the PVR-250 with me, I used an old WinTV GO! that I had in my desktop machine.</p>
      <p>Some reviews:</p>
      <p>Firstly, putting the system together was a non-issue. It took almost no time and everything just fit. I think the total process there took about 2 hours, and included monkeying with the WinTV GO card to get rid of the faceplate.</p>
      <p>Second off, I figured that all the raves about the amazingness of KnoppMyth meant that I would be up and watching TV in a few hours. Wrong. I _still_ can't get TV coming through the system. DVD playback is terrible. Worst of all though, the system took me forever to configure. Why? The good folks at KnoppMyth did not include a correct version of the Via CLE266 driver. As a result X-windows didn't work. Since there's no option to boot the system in non-X mode, I had to go back through the install disc to get a shell, and convert the output driver to vesa. That's not the end of my troubles though. The ethernet setup scripts don't automatically assume DHCP. You have to go through a setup window as the 'mythtv' user. And if you screw up a configuration or want to change something? Forget about it. The system doesn't give you an intuitive command to run to reconfigure.</p>
      <p>As far as MythTV goes? It's awful. It doesn't always respond when you make a keystroke, so you have to restart it. The backend and frontend design is good for a distributed terminal approach, but what about the single box approach? Also, the fact that when I stick the card into the box it doesn't automatically just create Inputs and whatnot makes the configuration process confusing and useless. I understand that it allows for more configuration options, but you can have both. You can have the system build up a default input mapping, which the user can then _choose_ to ignore.</p>
      <p>I'm rather disappointed with the whole "Build your own DVR using OpenSource Software" experience. I've spent only 1 weekend with it, and already I'm hoping that I can find a cheap copy of Windows XP MCE. </p>
   </div>
</div>
