---
layout: post
title: Parallel Phased Processing
category: Life
tags: parallel algorithm state machine
year: 2012
month: 06
day: 29
published: true
summary: Describe a method for doing parallel work
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>On a parallel state machine</h2>
      <p>Today, I managed to get a working implementation of a parallel state machine integrated at work. What the heck does that mean? How is this different than regular multi-threaded programming? Why do I even need it? Let's dive in!</p>
      <p>First, at work we're doing a fairly secret project. It's still a channel emulator (see <a href="http://www.azimuthsystems.com">Azimuth's</a> website for information), but it's next generation and gives us a much better development and test platform. As part of the hardware design, we have a 'packetized' interface to our hardware. That needs to get packets every 100 microseconds. This isn't very high speed (think about it - that's only 10k fps); the catch is for each frame we do about 300,000 math operations on <u>std::complex</u> data types.</p>
      <p>A bit of profiling showed that we just could not do this work from a single task. It took around 180 microseconds in the worst case to do the entirety of the work, which means we blew up our timing budget. Luckily, the work we're doing is prone to being parallelized - we have 'paths' in the system, composed of 'taps'. Each path/tap combination is somewhat independent (that's all I can say - they are inter-dependent at some point).</p>
      <p>Since the results of these operations are per-path/tap, and go into a packet which has discreet locations in memory, we can divide the work up such that we have 3 threads running on different cores of our 4-core machine, and leave the 4th core for the management tasks (network, control io), etc.</p>
      <p>So, for the first part, it's pretty easy - make an API like so:</p>
      <code>int32_t runParallelWork(work_item_t &wi);</code>
      <p>Each thread looks like a loop with code that looks like the following:</p>
      <pre>
void threadEntry(*arg)
{
    while(arg->work_ready)
    {
        work_item_t wi = getworkitem(arg);
        runParallelWork(wi);
    }
}
      </pre>
      <p>Cool, looks okay, but the problem is this - threads will just run without regard to whether or not memory is ready to read. What do I mean by this? Let's assume the existence of a chunk of packet memory <i>P</i>. This memory represents a descriptor where the output to the hardware would go. Let's assume something about this memory: it is shared with the hardware.</p>
      <p>What does that mean? <i>P</i> is a chunk of memory which is partitioned as a 'packet,' which has a single bit flag that indicates whether the memory is ready for reading by the hardware (think of it as a hardware ring buffer). How can I know whether all the threads are complete and this particular packet of memory is available?</p>
      <p>It turns out the synchronization required here is very tricky. If I just use a counting semaphore and a system call, I introduce indeterminate behavior into the system. One or more threads could spend more time getting switched in/out than we have available. But - synchronization <b>MUST</b> occur. Without at least one synchronization point the threads will clobber each other, and we can't guarantee that we know memory is available.</p>
      <p>There are a few ways to fix this issue, but the one I chose is to use batching with synchronization points governing the system.</p>
      <p>Let's start with the batching explanation because it's the simplest. It turns out that there is a bit of time we'll need to wait. Because the hardware consumes packets at 100uS in this system, and I'm looking at no more than 50uS per frame - I'll clearly run out of packets before the system is ready to continue. Rather than letting the system free-spin, it would be a good use of resources to wait until some number of packets (let's pick 20) become available. Since we want to wait for that condition, and we have a time guarantee around it, we can introduce a sleep for some number of time (I chose 450uS), wake and poll for the number of batched packets. While there are enough packets to make up a batch, we process a batch.</p>
      <p>This means we amortize the cost of our 450uS across the number of batches available. We still pay for the time, but the per-packet cost is very low, since it's spread over a group.</p>
      <p>Great! We've figured out how to give time back to the system to do other processing - but we still have to figure out how to indicate that the work is done.</p>
      <p>Here's where the sync points come in: I devised a formula to mathematically prove to each thread where the others were in the synchronization.</p>
      <p>Let <b>N</b> equal the number of actors in the parallel system (in our case 3), and let <b>S</b> be the number of parallel work sync-points where the threads need to serialize, and finally let <b>C</b> be the number of single-worker sync points. To determine whether or not an individual thread needs to progress beyond the current phase, it will:</p>
      <ol>
          <li>First, perform the actions required during this phase</li>
          <li>Second, increment the phase counter to indicate it has completed the phase</li>
          <li>Third, wait until the counter value is equal to <b>S</b> <b>times</b> <b>N</b> <b>+</b> <b>C</b>.</li>
      </ol>
      <p>So, the loop would look something like:</p>
      <pre>
{
    phase1();
    atomic_inc_phase_counter();
    while(barrier_read(phase_counter) < ((NUM_THREADS * 1) + C)) yield();
    phase2();
    atomic_inc_phase_counter();
    while(barrier_read(phase_counter) < ((NUM_THREADS * 2) + C)) yield();
    // ...
}
      </pre>
      <p>This means that, for instance, when the threads have progressed to phase 2, they will all do so at once. Since the phases are generally multiplicative they won't collide mathematically with another phase. The yields are wait points (meaning we are not <i>Wait-Free</i>, but I'd figure that would be obvious since threads do need to wait for others to catch up).</p>
      <p>While the non-special points might be understandable, what the heck is <b>C</b>?</p>
      <p>There may be actions that only a single thread can undertake. This requires an operation called <u>atomic_barrier_cmpxchg</u>, which will allow a single thread to obtain the critical section 'lock', and let the other threads skip the work required. That means something like:</p>
      <pre>
{
    if(X+1 == atomic_barrier_cmpxchg(phase_counter, X, X+1))
    {
        phase_X();
        atomic_inc_phase_counter();
    }
    atomic_inc_phase_counter();
    while(barrier_read(phase_counter) < ((NUM_THREADS * X) + 1)) yield();
    //...
}
      </pre>
      <p>Phase_X() in this case might be (for instance) "Grab 20 packets from the queue"</p>
      <p>There's one final piece to the puzzle: <i>Resetting the phase counter</i></p>
      <p>This is a delicate operation. The biggest issue is what happens when the main thread resets the phase counter to 0, but then immediately starts executing on the next batch. In that case, the while loop <code>while(barrier_read(phase_counter) < ((NUM_THREADS * X) + 1)) yield();</code> will continue to execute. So, we make a special exception for when the phase counter has looped around: <code>while(barrier_read(phase_counter) > (NUM_THREADS * (X-1)+1) && barrier_read(phase_counter) < ((NUM_THREADS * X) + 1)) yield();</code></p>
      <p>I've had the above psuedo code running for two weeks straight - the checksums have proved out that the code, as implemented on the chip we use, has not raced yet. Hopefully, this would be useful for others to think about in the future.</p>
   </div>
</div>
