---
layout: post
title: Travis and Jenkins for development
category: Programming
tags: travis jenkins continuous integration
year: 2015
month: 7
day: 19
published: true
summary: Integrating two different stacks for better development
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>Travis and Jenkins as a Service</h2>
      <p>So, I've started trying to build a better development mouse-trap to protect myself from my own foolish mistakes. After all, being better is what the game is all about. In that vein, I've started reading up and using <a href="https://travis-ci.org">travis-ci</a>; I'm also very familiar with (and use, constantly) <a href="https://jenkins-ci.org">Jenkins</a>.</p>
      <p>The logical question I ask myself: can I use Jenkins and Travis-CI at the same time? The answer is <b>YES</b>!</p>
      <p>What is the goal?</p>
      <ul>
          <li>Obviously, making sure I don't break the build</li>
          <li>Getting better code coverage numbers</li>
          <li>Performing Static Analysis (to protect against undefined-behavior type bugs)</li>
          <li>Possibly running doxygen to get documentation</li>
      </ul>
      <p>How do we get there? (Travis Side first)</p>
      <p>GitHub and Travis-CI work in conjunction to provide constant builds. Whenever I push to GitHub, it will trigger a travis build (probably via a post-commit hook). Travis-CI and <a href="https://coveralls.io">Coveralls</a> integrate to provide me with rough code coverage numbers</p>
      <p>So, I set up a <i>.travis.yml</i> which will install the required packages, <i>pip install</i> the coveralls uploader, and do a build to include the code coverage profiling data (gcov data).</p>
      <p>The other big thing I'll do is run the code, and spit out an XML file in cppunit 1.12.1 "xUnit" format. This is because such a format is easy to write, can be done from a bash script, and can be imported by any xunit import plugin (see the Jenkins section for more)</p>
      <p>As part of the <u>script:</u> stage, I run a <b>./run_if_travis.sh</b> which checks for the existence of a jenkins environment variable, and if one doesn't exist, runs the coveralls uploader. Since the previous step ran the code and generated an XML, we have gcov <i>.gcno</i> and <i>.gcda</i> files.</p>
      <p>For static anaylsis, coverity is available; I'm still waiting on them to determine that my projects are open source.</p>
      <p>Jenkins Side</p>
      <p>So, now I'll install jenkins locally. Read up on the Jenkins site to get information to install it for your platform. The biggest global configurations I've done are:</p>
      <ul>
          <li>Set it to run on localhost only</li>
          <li>Set it to authenticate against the local 'unix' database (requires shadow group permission)</li>
          <li>Gave it unlimited <i>sudo</i> access (<b>NOTE</b> - this is highly dangerous)</li>
          <li>Installed the <u>travis-yml</u>, <u>cppcheck</u>, <u>git</u>, <u>cobertura</u>, and <u>xUnit</u> plugins (among others)</li>
      </ul>
      <p>Now, I setup a job to use my local git repository as it's build source, and tell my post-commit hook to kick off a build (NOTE: or you could poll...)</p>
      <p>When the job runs, it should generate a results.xml and code_coverage.xml set of XMLs. I'll run <i>gcovr</i> to get coverage data. Additionally, I have it run <i>cppcheck</i> and generate a cppcheck.cxml file to get some static analysis.</p>
      <p>So, when I make a commit, Jenkins does the build and if I'm happy with it, I can push it up and let Travis do the build, too.</p>
      <p>That's basically it. Check out <a href="https://github.com/orgcandman/pam_tfa.git">PAM Two-factor</a> for a set of sample scripts to do this.</p>
   </div>
</div>

<div class="row">	
	<div class="span9 column">
			<p class="pull-right">{% if page.previous.url %} <a href="{{page.previous.url}}" title="Previous Post: {{page.previous.title}}"><i class="icon-chevron-left"></i></a> 	{% endif %}   {% if page.next.url %} 	<a href="{{page.next.url}}" title="Next Post: {{page.next.title}}"><i class="icon-chevron-right"></i></a> 	{% endif %} </p>  
	</div>
</div>
