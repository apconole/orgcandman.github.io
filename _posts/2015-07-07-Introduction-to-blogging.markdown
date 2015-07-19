---
layout: post
title: Introduction to github blogging
category: Blogging
tags: blog blogging git github
year: 2015
month: 7
day: 7
published: true
summary: My first attempt at a blog post using github
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>Preface</h2>
      <p>This is my first attempt at using github with jekyll integration. My guess is that the example I followed (from <a href="https://github.com/erjjones/erjjones.github.com/">Eric Jones</a>) is great, and that if anything is broken here it's because I messed it up.</p>
      <p><b>Update</b>: I'm going to back-port all of my older blogspot posts to this format and then start trying to get better at keeping up with this.</p>
   </div>
</div>

<div class="row">	
	<div class="span9 column">
			<p class="pull-right">{% if page.previous.url %} <a href="{{page.previous.url}}" title="Previous Post: {{page.previous.title}}"><i class="icon-chevron-left"></i></a> 	{% endif %}   {% if page.next.url %} 	<a href="{{page.next.url}}" title="Next Post: {{page.next.title}}"><i class="icon-chevron-right"></i></a> 	{% endif %} </p>  
	</div>
</div>
