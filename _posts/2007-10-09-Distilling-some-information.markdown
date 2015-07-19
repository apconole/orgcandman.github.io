---
layout: post
title: Distilling some information
category: Programming
tags: algorithms alcohol rcopy strings
year: 2007
month: 10
day: 09
published: true
summary: Distilling some information
image: none.jpg
---

<div class="row">
    <div class="span9 columns">
        <h2>Distilling some information</h2>
        <p>Did you know that in the US, it is illegal to <b>distill</b> alcohol. According to the US definition, distillation is the process by which we apply a thermal change (either colder or hotter) to separate fluids with different boiling/freezing points from a solution.</p>
        <p>In fact, in the US, it's illegal to ferment alcohol unless one happens to be 21. This means that if you, perchance, drop some yeast into a bucket of sugar water then walk away and it ferments out you _might_ have broken the law (if you're 3 years old). More realistically, what about the 13 year old kid who buys unpasteurized cider, and accidentally leaves it in his or her basement for a month. It will most likely ferment out into hard cider, and said 13 year old will forever be on a quest to learn more about the process.</p>
        <p>Even worse, if he decides "Oh, I don't want to get in trouble for having this" and leaves it with his trash, on a cold winter day, it will distill out into applejack, which is a felony. Seems to me the country has some 'splaining to do, Lucy.</p>
        <hr>
        <p>As far as an interesting topic for computer science goes, it's interesting to me that so many people don't look beyond the first five lines of code before they believe they understand everything about the function. A good example is the following:</p>
        <pre>
void *rcopy(void *dst, const void *src, size_t size)
{
   void *ret = dst;
   src+=size;

   while(size--)
   {
     (char*)*(dst++) = (char*)*(src--);
   }
   return ret;
}
        </pre>
        <p>and the following algorithm by <u>Paul Lovvik</u> (as published in the <i>Sun Developer's Network, June 2004</i>)</p>
        <pre>

void *
rcopy(void *dest, const void *src, size_t size) {
  int srcIndex = size - 1;
  int destIndex = 0;

  while (srcIndex >= 0) {
   ((char *)(dest))[destIndex++] =
       ((char *)(src))[srcIndex--];
  }
  return (dest);
}
        </pre>
        <p>When comparing the two, most pick algorithm 1 as the faster algorithm. On the surface, sure, it does look faster. But Algorithm 2 has two important differences:</p>
        <ol>
            <li>It is much more readable</li>
            <li>It has 1 less mathematic operator. This means in the long run it is faster by at least 1 instruction</li>
        </ol>
        <p>Ultimately, we need to take some time to just analyze the costs associated with anything in our lives. Whether it be taking the law into our own hands to enjoy some fresh distilled apple jack at 13, or whether it's the obscure cost of an extra comparison within our code, we need to carefully weigh each nugget of information and compare it with who we are and who we want to be. </p>
    </div>
</div>
