---
layout: post
title: Building a Better Framework
category: Development
tags: blog 
year: 2015
month: 8
day: 8
published: true
summary: Describing a better RPC interface in C++
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
      <h2>Towards better RPC abstractions</h2>
      <p>Once upon a time I worked with a Command Line Interface (CLI) framework that plainly sucked. You see, someone thought about how they might design their pet feature (recursive structure references) into a giant command line maibutsu monstrosity which was both impossible to debug <i>AND</i> impossible to extend. It turns out having to put each token of a command string into its own table element (complete with either a function call, OR reference to the next structure table) makes programmers not want to add commands. That means few commands with thousands of screen pages of output. In a word: suck.</p>
      <p>When I got to Azimuth (2011), they had a similar style CLI. Here's a bonafide example of a struct (note: I've changed the code and omitted extraneous fields):</p>
      <pre class="prettyprint">
struct parse_token_struct {
    char *token;
    char *helptxt;
    int (*hndlr)(struct cli_sess *, char *, struct parse_token_struct *);
    struct parse_token_struct *nxt;
...
};
      </pre>
      <p>The above is the interface definition. The issue it has isn't that it doesn't provide enough information to extend. The issue is in how the problem was decomposed vs. the human element of actually using the interface. When I think of writing a CLI command, I love the ability to provide help and have pre-tokenized data. It makes writing functionality better. However, this framework gets in the way because it broke the problem down to the most basic unit (token: good!) and then failed to contemplate whether that unit was more useful for a human versus a machine.</p>
      <p>Think about it like this, would you rather pass your <code>hndlr</code> function in the above, and the help text, along with all the tokens? Or would you rather spend hours writing and inserting into static structures like so:</p>
      <pre class="prettyprint">
struct parse_token_struct secondTable[] = {
    {"command", "this is the first command", firstCommand, NULL},
    {"int", "integer", takeInteger, NULL}
};

struct parse_token_struct otherSecondTable[] = {
    {"command", "this is the other first command", otherFirstCommand, NULL},
    {"again", "This goes to another table", NULL, &someOtherTable}
};

struct parse_token_struct rootTable[] = {
    {"first", "this is the first token", NULL, &secondTable},
    {"otherFirst", "this is another first token", NULL, &otherSecondTable}
};
      </pre>
      <p>When you could just write:</p>
      <pre class="prettyprint">
registerCommand("first command", {"this is the first token", "this is the first command"}, firstCommand);
registerCommand("otherFirst command", {"this is another firs token", "this is the other first command"}, otherFirstCommand);
/*...*/
      </pre>
      <p>I prefer the second, myself. Reading through the first requires taking lots of time to mentally build a syntax table, walk it, and understand any special tokens along the way. With the second method, it's much easier to see what the commands are: <code>first command</code>, and <code>otherFirst command</code>.</p> 
      <p>Notice that when I go to add a command it's very easy: write my function, determine the 'syntax' to invoke it, and register it. Because it's so easy to write CLIs, I'm more inclined to do so. After all, if dumping a bit of extra debug data involves a function call and writing the function to dump the data, that's a bit better than trying to figure out where and how I should be inserting each individual token.</p>
      <p>There is a dark side to this approach as well. Because it is so easy to add an arbitrary 'syntax path' to a command, developers can be tempted to add things willy nilly so that there can be multiple sets of commands that look similar but do wildly different things. That can lead to confusion. As an example, imagine:<ul><li>'system show current temperatures'</li><li>'show system running tasks'</li></ul></p>
      <p>Tab completion becomes a nightmare. Contextual help gets confusing. CLI users no longer know what to start typing. That results from inconsistency inherent with multiple developers. There are ways of trying to mitigate that - after all we could fix the roots of all commands, or have the framework scan for tokens appearing in inconsistent places. However, I prefer using code review and the human element for that particular problem. After all, it's a framework <u>for</u> humans, right?</p>
   </div>
</div>

<div class="row">	
	<div class="span9 column">
			<p class="pull-right">{% if page.previous.url %} <a href="{{page.previous.url}}" title="Previous Post: {{page.previous.title}}"><i class="icon-chevron-left"></i></a> 	{% endif %}   {% if page.next.url %} 	<a href="{{page.next.url}}" title="Next Post: {{page.next.title}}"><i class="icon-chevron-right"></i></a> 	{% endif %} </p>  
	</div>
</div>


