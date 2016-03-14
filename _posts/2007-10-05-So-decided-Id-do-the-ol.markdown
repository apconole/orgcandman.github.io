---
layout: post
title: So, decided I'd do the 'ol blog thing
category: Blogging
tags: blog blogging asm memory
year: 2007
month: 10
day: 05
published: true
summary: My first ever blog post
image: none.jpg
---

First Internet Entry
--------------------

So, decided I'd do the 'ol blog thing. I'm gonna try to update this at
least once a week with random thoughts, comments, and opinions (many
of which will be wrong) on software development, and engineering.

As I write this first entry, I reflect on the many firsts upon which I
am currently embarking. I'm leaving my job at Airvana, Inc. to accept a
position at another Chelmsford, MA based company. I'm finishing up my
first heap management package (not open sourced...I'd like to keep a 
few things up my sleeve for later) and I'm trying a $5 bottle of Fiji
water (free at the company as a sampler).

The water isn't bad; the package at the new job isn't bad, and certainly
a constant time heap isn't bad. All in all, lots of good that I hope continue.

A bit of code, and some coolness
--------------------------------

A while ago, I was interested in attaining the backtrace of a particular 
stack address. I could use the gnu backtrace() routine, but that carries 
with it, a few issues:

* It does an internal malloc (not so good when you want a backtrace after
  running out of memory)
* Because it then touches the memory it allocates, it'll potentially cause 
  a pagefault (suspeds the entire process, including all threads)
* isn't supported on all platforms anyway

So, I decided I'd use a little trick to get the frames prior. This isn't
exactly portable, but it should work on linux for most architectures. You 
may have to play with the math a bit to get the correct previous frame addr.
Also, some architectures (notable mips and alpha) just won't work.

First, we can tell where we currently are by getting a stack variable 
address. This means that if we have a function: 
<code>int foo(int someVar)</code>. Inside that function, we add: 
<code>unsigned char *stackAddr = (unsigned char *)&someVar;</code>

*stackAddr* will contain the address of that variable within the frame. This is
great for knowing where in the frame we are, but we really care about the return
address which sits at the bottom (or top depending on your nomenclature) of the
frame. Since stacks grow upwards, we know that the return pointer exists 
somewhere before our current location. We'll be subtracting from the address.

In order to correctly align the pointer for the linux stack, we need to know how
the linux stack frame looks. According to [http://math-atlas.sourceforge.net/devel/atlas_contrib/node93.html](math-atlas), the frame on my system is laid out such
that:

| offset  | Description of the offset           |
|   0     | The ptr to the callee address frame |
|   4     | The link register save location     |
|   8     | The parameter area                  |

This means that in our example above, we're currently pointing to offset 8. 
Going back 8 bytes then should get us to the ptr to the callee address frame.

So, lets write a quick 'n dirty test function, and use gdb to check on the
results.

<pre class="prettyprint">
int backtrace_test(int nFrameParameterOffset)
{
unsigned char *pStackPtr = (unsigned char *)&nFrameParameterOffset;
unsigned int *pCalleePtr = 0;

pStackPtr -= 8; //this will back us up to the callee ptr
pCalleePtr = (unsigned int *)pStackPtr;

printf("address of callee [%p] points to [%x]\n", pCalleePtr, *pCalleePtr);
return 0;
}

int main()
{
return backtrace_test(1234);
}
</pre>

Compile with: *gcc -g -o backtrace_test backtrace_test.c*

Running this produces the following:
<pre>
aconole@linuxws220 /localhome/aconole/bt-test
$./backtrace_test
address of callee [0xbffff618] points to [bffff648]
</pre>

Under gdb, if we look at these values, we'll notice that at *0xbffff64c* 
(4 bytes ahead of the frame to which we are pointed) we see (*0x080483ee*). 
Attempting to disassemble this address (_disas 0x080483ee_) puts us at the
return address after the call to _init. Looks like we're getting a clue as to
the stack workings. Let's put in another frame and see what we get. We'll add
the following to our code:

<pre class="pretttprint">
int foo(int bar)
{
return backtrace_test(bar);
}
</pre>

And we'll change main to call foo. The new result is:

<pre>
aconole@linuxws220 /localhome/aconole/bt-test
$./backtrace_test
address of callee [0xbffff5f8] points to [bffff618]</pre>

Notice, instead of *0xbffff618* pointing to *0xbffff648*, we have *0xbffff5f8*
pointing to *0xbffff618*. The extra frame is at *0xbffff5f8*! Lets follow the
rest of the frames in gdb:

<pre>
(gdb) p/x *0xbffff618
$2 = 0xbffff638
(gdb) p/x *0xbffff638
$3 = 0xbffff668
(gdb) p/x *0xbffff668
$4 = 0xbffff6c8
(gdb) p/x *0xbffff6c8
$5 = 0x0
</pre>

We can see that all the frames link back until we hit 0. If we look at
*0xbffff61c* now (4 bytes after the callee ptr), we see *0x80483b7*. gdb 
gives us more information:

<pre>
(gdb) disassemble 0x80483b7
Dump of assembler code for function foo:
0x080483a6 : push %ebp
0x080483a7 : mov %esp,%ebp
0x080483a9 : sub $0x8,%esp
0x080483ac : sub $0xc,%esp
0x080483af : pushl 0x8(%ebp)
0x080483b2 : call 0x8048368
*0x080483b7 : add $0x10,%esp*
0x080483ba : leave
0x080483bb : ret
End of assembler dump.
(gdb)
</pre>

Success! *0x80483b7* is the bolded line. It's the return address inside foo!

We know two things now: Following the return register back will give us all the frames (until we hit frame 0), and 4 bytes after the callee ptr, the link register gives us the program counter for the frame. Let's write a stack dumper function which will give us a simple stack trace:

<pre class="prettyprint">
unsigned int *dumpAllFrames(unsigned int nFramesMax)
{
unsigned char *pStackAddrPtr = (unsigned char *)&nFramesMax;
unsigned int *pFramePointer = 0;

pStackAddrPtr -= 8;

pFramePointer = (unsigned int *)pStackAddrPtr; //at this point we have the stack list

while(pFramePointer && nFramesMax)
{
printf("Current Frame=<%p>, Next Frame=<0x%x>, PC=<0x%x>\n",
pFramePointer, *pFramePointer, *(pFramePointer+1));
pFramePointer = (unsigned int *)*pFramePointer;
nFramesMax--;
}

return pFramePointer;
}
</pre>

and call that from within backtrace_test. The results:
<pre>
$./backtrace_test
Current Frame=<0xbffff5d8>, Next Frame=<0xbffff5f8>, PC=<0x80483d2>
Current Frame=<0xbffff5f8>, Next Frame=<0xbffff618>, PC=<0x80483ed>
Current Frame=<0xbffff618>, Next Frame=<0xbffff648>, PC=<0x804841b>
Current Frame=<0xbffff648>, Next Frame=<0xbffff6a8>, PC=<0x418de3>
Current Frame=<0xbffff6a8>, Next Frame=<0x0>, PC=<0x80482e1>
</pre>

And using gdb:

<pre>
(gdb) disas 0x80483d2
Dump of assembler code for function backtrace_test:
0x080483c2 : push %ebp
0x080483c3 : mov %esp,%ebp
0x080483c5 : sub $0x8,%esp
0x080483c8 : sub $0xc,%esp
0x080483cb : push $0xa
0x080483cd : call 0x8048368
0x080483d2 : add $0x10,%esp
0x080483d5 : mov $0x0,%eax
0x080483da : leave
0x080483db : ret
End of assembler dump.
(gdb) disas 0x80483ed
Dump of assembler code for function foo:
0x080483dc : push %ebp
0x080483dd : mov %esp,%ebp
0x080483df : sub $0x8,%esp
0x080483e2 : sub $0xc,%esp
0x080483e5 : pushl 0x8(%ebp)
0x080483e8 : call 0x80483c2
0x080483ed : add $0x10,%esp
0x080483f0 : leave
0x080483f1 : ret
End of assembler dump.
(gdb) disas 0x804841b
Dump of assembler code for function main:
0x080483f2 : push %ebp
0x080483f3 : mov %esp,%ebp
0x080483f5 : sub $0x8,%esp
0x080483f8 : and $0xfffffff0,%esp
0x080483fb : mov $0x0,%eax
0x08048400 : add $0xf,%eax
0x08048403 : add $0xf,%eax
0x08048406 : shr $0x4,%eax
0x08048409 : shl $0x4,%eax
0x0804840c : sub %eax,%esp
0x0804840e : sub $0xc,%esp
0x08048411 : push $0x4d2
0x08048416 : call 0x80483dc
0x0804841b : add $0x10,%esp
0x0804841e : leave
0x0804841f : ret
End of assembler dump.
(gdb) disas 0x80482e1
Dump of assembler code for function _start:
0x080482c0 <_start+0>: xor %ebp,%ebp
0x080482c2 <_start+2>: pop %esi
0x080482c3 <_start+3>: mov %esp,%ecx
0x080482c5 <_start+5>: and $0xfffffff0,%esp
0x080482c8 <_start+8>: push %eax
0x080482c9 <_start+9>: push %esp
0x080482ca <_start+10>: push %edx
0x080482cb <_start+11>: push $0x8048474
0x080482d0 <_start+16>: push $0x8048420
0x080482d5 <_start+21>: push %ecx
0x080482d6 <_start+22>: push %esi
0x080482d7 <_start+23>: push $0x80483f2
0x080482dc <_start+28>: call 0x80482a0
0x080482e1 <_start+33>: hlt
0x080482e2 <_start+34>: nop
0x080482e3 <_start+35>: nop
End of assembler dump.
</pre>

As you can see, we don't have the frame before main(). I didn't include that 
because it is most likely part of some runtime generated code, and therefore 
we can't actually get it. However, we do see that every other frame is
accounted for. We can see exactly where in memory we are, and we should be 
able to use this information to dump a stack wherever we choose, without the 
issues with gnu backtrace().

A word of caution: This has only been tested on cygwin, powerpc and x86 
(32-bit) linux. This will be broken on 64-bit systems, and MIPS / AXP
systems (which don't always put addresses in stack space).


