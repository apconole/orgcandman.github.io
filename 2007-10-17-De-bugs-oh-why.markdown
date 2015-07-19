---
layout: post
title: De bugs...oh why?
category: Programming
tags: bugs assembler posix
year: 2007
month: 10
day: 17
published: true
summary: De bugs...oh why?
image: none.jpg
---

<div class="row">
    <div class="span9 columns">
        <h2>Do you trust your posix implementation?</h2>
        <p>So, I believe I found an issue with the pthread_create routine. Why do I believe this? <b>Update:</b> Important note here: the issue I observed was actually a bug in the glibc code. It was resolved in a later commit; I'm going to track it down and link it here. Vindication is sweet</p>
        <p>During the course of writing my own userspace heap, I noticed that during multi-threaded test execution I had 1 block being leaked. The block was obviously more than 64b, but less than 128b. I wrote a backtrace routine (described in earlier posts) to try and quickly figure out where the leak was taking place. And here is what I found:</p>
        <pre>
0x4000dcc4 : call 0x4000076c
0x4000dcc9 : test %eax,%eax</pre>
        <p>The above is where the leak occurs.</p>
        <p>The following is the backtrace:</p>
        <pre>
#0 0x4000dc9b in allocate_dtv () from /lib/ld-linux.so.2
#1 0x4000df3c in _dl_allocate_tls () from /lib/ld-linux.so.2
#2 0x441a78e5 in pthread_create@@GLIBC_2.1 () from /lib/tls/libpthread.so.0
#3 0x0804885a in main () at test.c:59
        </pre>
        <p>Valgrind reports a similar issue, so I can't be wrong here, I think. <b>Update:</b> I wasn't wrong. You'll find current (as of 2011 or so) versions of glibc does not display this behavior - even with my custom heap</p>
        <p>I write up a bug, detailing this. Response is something along the lines of "nptl has no memory leaks, and valgrind isn't always right. Also, you're using an old version. Please upgrade and rerun test."</p>
        <p>BULL! It's not just valgrind reporting this. I see the same issue in my own heap implementation. It is an overlay of the malloc() and free() routines (malloc, free, calloc and realloc to be precise). Open source community, want to know why you have such a bad rep? You believe that because you wrote an ethernet driver, or a RAID array controller, somehow you're untouchable. WRONG. I've written drivers, heaps, userspace apps, cell tower apps, and a whole plethora of things. I don't spout off nonsense to try and get a big e-rection. I actually try and solve problems. <b>Update:</b> I'm leaving this rant here for posterity and honesty, but it was written in a moment of passion, and I don't actually feel that the open source community has a bad rep.</p>
    </div>
</div>
        
