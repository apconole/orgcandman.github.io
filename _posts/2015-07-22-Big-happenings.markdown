---
layout: post
title: Big Happenings
category: Life
tags: ovs redhat job life
year: 2015
month: 7
day: 22
published: true
summary: Reflections on what is going on
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>Life Happenings</h2>
      <p>So, I've just sent in my acceptance letter for Red Hat. That's right, in a few short weeks, I'll be a Shadowman follower. I'm pretty excited about it - I've wanted something like this for a long time. I've used open source software since the 1990s, and even made some money supporting Redhat 6.1 (the one which used kernel 2.2.12-20). It's why I ended up getting a job at BL Software, Airvana, Sycamore, and Azimuth. Getting to give back would be great.</p>
      <p>Speaking of which, I started doing some work on <a href="http://github.com/openvswitch/ovs">Open vSwitch</a>. It's a multi-layer virtual switch which provides SDN "as a service" (I think). I started out by running CPPCHECK against the sources, and then ran ``make distcheck`` - which promptly failed. At that point, I found my raison d'etre for my first contribution. After experimenting with my own local fork, I finally got a patch set that was deemed acceptable by the OVS moderate, Ben Pfaff. He's been awesome to work with for the 5 minutes I've worked with him. Anyway, so now the ``distcheck`` target is successful under OVS and more progress can be made (hopefully, without breaking the build again). Shared libraries are still not working, but there's a patch currently under review which should resolve that. Then the travis build off master should run completely.</p>
   </div>
</div>

<div class="row">	
	<div class="span9 column">
			<p class="pull-right">{% if page.previous.url %} <a href="{{page.previous.url}}" title="Previous Post: {{page.previous.title}}"><i class="icon-chevron-left"></i></a> 	{% endif %}   {% if page.next.url %} 	<a href="{{page.next.url}}" title="Next Post: {{page.next.title}}"><i class="icon-chevron-right"></i></a> 	{% endif %} </p>  
	</div>
</div>


