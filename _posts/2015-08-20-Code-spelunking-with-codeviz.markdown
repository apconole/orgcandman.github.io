---
layout: post
title: Code Spelunking with llvm/clang and Codeviz on Ubuntu 14.04LTS
category: Development
tags: blog 
year: 2015
month: 8
day: 20
published: true
summary: How to build and run codeviz on Ubuntu 14.04LTS along with llvm tricks
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>Code Spelunking with llvm/clang and Codeviz on Ubuntu 14.04LTS</h2>
      <p>This post is inspired by reading the ACM Queue Article <a href="http://queue.acm.org/detail.cfm?id=1483108">Code Spelunking Redux</a> by <i>George v. Neville-Neil</i>. The article is quite good, going over a number of tools to use to start to understand a new codebase of incredible complexity (such as <a href="http://github.com/openvswitch/ovs">Open vSwitch</a>). This post will cover how to install and run the codeviz suite.</p>
      <p>It's important to note that at the time of this writing, gcc 4.6.2 is the latest supported GCC version for codeviz. I'm currently working on a minor patch to add 5.2.0 support, and will update this when it's done.</p>
      <p>First step will be to visit the <a href="http://www.csn.ul.ie/~mel/projects/codeviz/">CodeViz Project Page</a> and <a href="http://www.csn.ul.ie/~mel/projects/codeviz/codeviz-1.0.12.tar.gz">Download</a> the latest release. Save this in <code>~/Downloads/codeviz-1.0.12.tar.gz</code>.</p>
      <p>Next, ensure that the requisite development dependencies are installed by running <code>sudo apt-get install libgmp-dev libmfp-dev libmfc-dev build-essential gcc-multilib graphviz imagemagik global doxygen autoconf libtool clang</code>. When the installation completes you should have everything needed to build CodeViz, as well as do some additional source analysis.</p>
      <p>On Ubuntu 14.04LTS, I found that building would fail when using tex/latex on the file <em>compilers/gcc-graph/gcc-4.6.2/gcc/doc/cppopts.texi</em> due to line 772's <u>@itemx --help</u> value. I suggest editing line 33 of <em>compilers/install_gcc-4.6.2.sh</em> to insert <code>sed -rei 's/@itemx --help/@item --help/g' gcc-graph/gcc-4.6.2/gcc/doc/cppopts.texi</code> which should get past the compile error. Also note - due to Ubuntu's use of the newer 4.8/4.9 GCC, there are many errors generated regarding reserved C++11 keywords. Hopefully, this doesn't cause you too much headache.</p>
      <p>More To come... Just want to sleep...</p>
      <h2>And one more trick for the road</h2>
      <p>So, that's a pretty complicated set of hoops to jump through in order to get the codeviz project building. There's a faster (albeit, less detail-giving) mechanism for getting first order code graphs. This is made possible thanks to the <code>-S -emit-llvm</code> and <code>opt</code> portions of the LLVM/Clang project.</p>
      <p>As an example, let's presume I have a source file, <em>foo.c</em> which contains some C code, with calls, etc. I can run <code>clang -S -emit-llvm foo.c -o - | opt -analyze -dot-callgraph && dot -Tpng -ofoo.png callgraph.dot</code> and get a neat little png file which contains some detailed call flow information.</p>
      <p>Okay, you might ask, but how do I get that for a large project (such as, say Open vSwitch). Provided the project is using the GNU Autotools package, the following snippet should be included in your Makefile.am (or any Makefile.am that you wish to work with):</p>
      <pre class="prettyprint">
get_cs_flags = $(foreach target,$(subst .,_,$(subst -,_,$($(2)))),$($(target)_$(1)FLAGS))
get_cs_all_flags = $(foreach type,$(2),$(call get_cs_flags,$(1),$(type)))
get_cs_compile = $(if $(subst C,,$(1)),$($(1)COMPILE),$(COMPILE))
get_cs_cmdline = $(call get_cs_compile,$(1)) $(call get_cs_all_flags,$(1),check_PROGRAMS bin_PROGRAMS lib_LTLIBRARIES) -fsyntax-only

get_bc_cmdline = $(call get_cs_compile,$(1)) $(call get_cs_all_flags,$(1),check_PROGRAMS bin_PROGRAMS lib_LTLIBRARIES) -S -emit-llvm

check-syntax:
	s=$(suffix $(CHK_SOURCES));\
	if   [ "$$s" = ".c"   ]; then $(call get_cs_cmdline,C)	 $(CHK_SOURCES);\
	elif [ "$$s" = ".cpp" ]; then $(call get_cs_cmdline,CXX) $(CHK_SOURCES);\
	else exit 1; fi

build-calls:
	s=$(suffix $(CHK_SOURCES));\
	if   [ "$$s" = ".c"   ]; then $(call get_bc_cmdline,C)   $(CHK_SOURCES) -o - | opt -analyze -dot-callgraph; dot -Tpng -o$(CHK_SOURCES:.c=.png) callgraph.dot; \
	elif [ "$$s" = ".cpp" ]; then $(call get_bc_cmdline,CXX) $(CHK_SOURCES) -o - | opt -analyze -dot-callgraph; dot -Tpng -o$(CHK_SOURCES:.c=.png) callgraph.dot; \
	else exit 1; fi

.PHONY: check-syntax build-calls
      </pre>
      <p>The first target, <b>check-syntax</b> is merely a way for flymake to auto-check files. The second is where the magic happens. Re-running the autotools and doing a configure with CC and CXX set to clang and clang++, respectively, generates a Makefile that lets us do something more akin to: <code>make CHK_SOURCES=lib/table.c build-calls</code> and get out a lib/table.png that describes the flow pretty well to start working. Even better would be to integrate the combination of approaches here, and top it off with <b>Doxygen</b> to gain insight very quickly.</p>
   </div>
</div>
