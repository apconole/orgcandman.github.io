---
layout: post
title: Emacs and Magit Git Blame
category: Development
tags: blog 
year: 2015
month: 8
day: 9
published: true
summary: A quick productivity tip for gnu-emacs
image: none.jpg
---

<div class="row">
   <div class="span9 columns">
   <h2>Blame Everyone!</h2>
   <p>Once upon a time (y2k I think), I worked for a small Java-based CRM company in Haverhill, MA called <a href="http://www.sematree.com">SemaTree</a>. Actually, they were ComponenTree first, but renamed after they merged with ECS, an ERP/CRM component vendor. Anyway, that aside, I noticed that my productivity in Forte/NetBeans was nowhere near the level of one of my coworkers using X-Emacs. So being the good little hacker I was, I got home that night, fired up my linux system, opened GNU emacs, and haven't looked back since. The first weekend, I had read through the manpages, tutorial, and started setting up jde/j2ee mode. By the time I moved on to Airvana, I was fulltime in GNU Emacs, and writing rudimentary elisp well enough to get myself going anywhere.</p>
   <p>I recently decided to start putting my emacs environment up in 'the internet' at <a href="http://github.com/orgcandman/emacs-plugins">Orgcandman's Emacs Plugins Repository</a>. One of the things I recently pushed there is something I realized other folks might have use for so I patched it up and have pushed the new function <code>magit-blame-other-window</code> bound to <b>C-x g b</b> to invoke <code>magit-blame-mode</code> in an indirect buffer tied to the file backing the current buffer.</p>
   <p>Some quick background - what is <code>git blame</code> and why should you care?</p>
   <p>Occasionally, while developing, it's common to encounter bugs (GASP!), and when they crop up, it's likely that code in question will need to change. However, it's always good to understand <i>what</i> the code was actually intended to fix, rather than just killing it outright.</p>
   <p>Enter <code>git blame</code>, which shows who last worked on the line in question and allows picking out the exact commit which introduced the problem. Getting to that commit can be very insightful and allows asking the original authors whether a particular change has other implications which aren't immediately obvious. As such, I use magit-blame-mode quite frequently, and have made the above described emacs lisp function to facilitate easier viewing.</p>
   <p>The code itself is small, so I'll republish it here in case you don't want to use my .emacs stuff:</p>
   <pre class="prettyprint lang-scm">
;; Magit-blame in other window of current buffer
(defun magit-blame-other-window ()
  "Opens a new window from the current buffer filename and runs magit-blame on 
   it"
  (interactive)

  (setq buffer-name (generate-new-buffer-name "*Magit Blame Mode*"))
  (setq previous-buffer-file-name (buffer-file-name))
  (pop-to-buffer (make-indirect-buffer (current-buffer) buffer-name))
  (setq buffer-file-name previous-buffer-file-name)
  (magit-blame-mode 1)
  (goto-char (point-min)))

(global-set-key (kbd "C-x g b") 'magit-blame-other-window)
   </pre>
   <p>I'll be the first to admit, there's probably a better way of doing this, but it gets the job done. I'm also not sure if there's any side effect with the bug described at <a href="https://github.com/magit/magit/issues/1731">Issue #1731</a> for the <a href="https://github.com/magit/magit">Magit</a> project.</p>
   </div>
</div>
