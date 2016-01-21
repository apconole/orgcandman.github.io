---
layout: post
title: Writing presentations in emacs with Beamer
category: presentations
tags: emacs presentations beamer
year: 2016
month: 01
day: 20
published: true
summary: Writing presentations without latex using beamer
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
       <h2>Because Presenting Yourself Well Counts!</h2>
       <p>Recently, I attended the <a href="http://www.emacsboston.org">Emacs Boston</a> meetup group. The talk for the night bore the title "Publishing with Emacs." I got myself pumped for a great discussion about advanced publishing techniques involving <b>org-mode</b>, <b>ebooks</b>, and all the fancy kinds of emacs-isms that one could expect from using <a href="http://www.gnu.org/software/emacs">emacs</a>.</p>
       <p>For some context, I have very little time to hack away on interesting things, these days. I have two children, with another on the way. I'm much more likely to spend an hour trip into Boston for going to eat, seeing the parks, and other historic sites. I can find better ways to spend my time than messing with emacs.</p>
       <p>This talk piqued my interest for several reasons, but by far the big reason to attend presented itself with my wife. She's been very into <a href="http://www.genealogy.com">genealogy</a> lately. By using the absolutely astonishing <a href="http://orgmode.org">org-mode</a> extension, her organization of notes and references continues to astonish me. Within a few months, her proficiency with macros, keybind adjustments, and navigation has payed off in spades. She spends almost no time fighting with the <i>text</i>, and all her time fighting to find <i>data</i>. Her eventual goal is to publish her compiled works on the various family trees she has collected.</p>
       <p>So, we were excited, and a bit self-deprecating as we joked about attending an emacs meetup on our only date-night of the month.</p>
       <p>Imagine our disappointment when the talk centered on <a href="https://en.wikipedia.org/wiki/LaTeX">LaTeX</a>. I hold a deep seated loathing of the desktop publishing language invented by Knuth. It's not that I think LaTeX is <u>bad</u>, mind you. I happen to think that LaTeX is _great_ as the <a href="https://en.wikipedia.org/wiki/Post-production">post</a> of the document writing world. But spending your entire doc-writing experience in LaTeX sounds only mildly more interesting than being stung by a horde of bullet ants. Actually, as I write that sentence, I realised something - being stung by bullet ants at least gives an amusing anecdote.</p>
       <p>So, I set off to find out first and foremost, whether I could write a presentation in org-mode and export it, taking full advantage of the emacs environment. I'll let my friend here tell you the answer:</p>
       <img src="http://orig10.deviantart.net/45d1/f/2014/130/9/8/bob_the_builder_by_foxinshadow-d7htd3v.jpg" />
       <p>For this, you'll need an environment which is ready for LaTeX (WHAT?! Didn't I just spend a paragraph saying no to that monstrosity? You'll barely know you used LaTeX). I'll recommend going ahead and installing <b>texlive-full</b> on <a href="http://www.ubuntu.com">ubuntu</a>, and <b>texlive-scheme-full</b> for Fedora (I didn't do this on my fedora machine, so if it doesn't work let me know!). You'll also need the 'pdflatex' binary, which should be installed by those packages. Finally, grab <b>python-pygments</b>. And obviously, <b>emacs</b>, with <b>org-mode</b> version <i>8.0+</i></p>
       <p>First, some required customization is needed in your emacs initialization. I promise, it's very light.</p>
       <pre class="prettyprint">
(require 'ox-beamer)
(require 'ox-latex)
(setq org-export-allow-bind-keywords t)
(setq org-latex-listings 'minted)
(add-to-list 'org-latex-packages-alist '("" "minted"))
(setq org-latex-pdf-process
      '("pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
        "pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
        "pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"))
       </pre>
       <p>The above will insert the <b><a href="http://orgmode.org/worg/exporters/beamer/ox-beamer.html">ox-beamer</a></b> export hook into your org-latex-export environment. The <i>org-export-allow-bind-keywords</i> variable controls whether or not we can rebind variables in our .org files, which is only required to adjust variables like: <i>org-latex-title-command</i> (needed for some custom themes). Additionally, the other gobbledy-gook with pdf-process, and minted allow for exporting <code>#+begin_src/#+end_src</code> blocks with syntax highlighting.</p>
       <p>Once that is added to your <code>$HOME/.emacs.d/init.el</code> (or wherever your emacs init code is), your emacs will be 90% of the way towards <b>ox-beamer</b> presentation domination. Open a new file somwhere called <code>mypresentation.org</code>.</p>
       <p>This org file requires a bit of boiler plate to make it suitable for export as a presentation. Below is a minimum:</p>
       <pre class="prettyprint">
#+TITLE: MY TITLE FOR THIS PRESENTATION
#+AUTHOR: MY NAME
#+DATE: January 20, 2016
#+DESCRIPTION: Some kind of description (why not?)
#+KEYWORDS: anything you want... or blank - I leave this blank too.
#+LANGUAGE:  en
#+OPTIONS:   H:2 num:nil ^:{} toc:nil 
#+LaTeX_CLASS_OPTIONS: [presentation]
#+BEAMER_THEME: AnnArbor
#+EXCLUDE_TAGS: noexport
#+PROPERTY:  header-args :eval no
       </pre>
       <p>That is all you need. Now each top-level bullet will be a page, and the second-tier bullet will be your page title. Within that, add as many sub-sections and bullets as you desire (until you break your page layouts). Here's a sample:</p>
       <pre>
* Secret page                                 :noexport:

** This is where todos and notes can go!

it isn't exported because of the EXCLUDE_TAGS above

*** TODO work how dogs > cats into the PRESENTATION

*** DONE write a quick blog post

* Introduction

** This is an intro page

Org mode is neat, and org-exports are neat, TOO.

- There are lots of keybinds to make things easy

- There are menus and tons of blogs all over

- Plus, did no one mention the LISP?!

* Page two

** Because a second page always helps

*** Idea block one

- don't you want more posts?

*** Idea block two

#+begin_src :python
from ideas import new_ideas

def fun(idea):
   new_ideas.append(idea)
#+end_src
       </pre>
       <p>Just save that into your org file, and now run the super secret <code>M-x org-export-dispatch</code> (as an aside, the default keybind for this action is <i>C-c C-e</i>). In that menu, notice the LaTeX header (should be [l]). Selecting that (by pressing [l]), opens the submenu which has <b>Export to LaTeX (Beamer)</b>, and other associated options. Go ahead, press the key for Export and Open PDF. You should see a sweet first presentation.</p>
       <p>From this point, you can customize lots of things. Want to change the theme to <i>Antibes</i>? Go right ahead. Just change that variable, and re-export. Want to mess with the color scheme? Just add <code>#+BEAMER_COLOR_THEME: spruce</code> (or crane) to the header block. There are a ton of additional options, and you can mess around with how you want the look and feel to be, even on a per-page basis.</p>
       <p>Okay, okay. You want more themes, right? After all, this stuff is amazingly good - and getting extra themes for more choices seems like a no brainer. Okay, here's the last trick up my sleeve. Grab yourself the simple soothing Fedora theme from the <a href="https://fedoraproject.org/wiki/Templates_for_Presentations">Fedora wiki</a>, and grab the <a href="http://melmorabity.fedorapeople.org/latex/beamer/beamer-laughlin/beamer-laughlin.zip">Laughlin</a> theme. Unzip those contents to the <b>~/texmf</b> directory, and run <code>mktexlsr ~/texmf/</code>. Presto - instant new template! Just update your BEAMER header.</p>
       <p>Hopefully, this post helps you write amazing presentations without disrupting your precious date nights.</p>
   </div>
</div>

