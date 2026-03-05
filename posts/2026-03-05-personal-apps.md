---
title: personal apps
date: 2026-03-05
tags:
  - llms
  - clawdlikes
  - education
  - linux
excerpt: squishware of the future
---

# Squishware

I was thinking about hardware engineering in contrast to software engineering the other day and wondered if whatever vibe coding becomes in the future should be called squishware.

My brain thinks of it as software that isn't perfect, but gets the job done most of the time, and is highly malleable.

One of the squishwares I made today was the mechanism for this blog to publish itself on GitHub Pages by simply creating a markdown file in a specific folder on my home system. I had Claude create something off a simple blog structure I had asked for in previous sessions:

```bash
❯ Please write a systemd daemon that when a blog post file is added to
  this site it makes a git commit and pushes the change to auto publish.
  It should be a file system watch
```

It wrote something that was almost correct, I had 2 more edge cases, one was triggering when I moved a file in the same folder, and how I wanted it to track changes if I specifically was using vim as my editor. Easy fixes. It now lets me publish this very post by just creating a file.

These are the fun little apps that help me out, I'll try and document them as I think them up. There was another service that I had that costs a bit of money if you want better voice quality that I'll post about when I have more time.

