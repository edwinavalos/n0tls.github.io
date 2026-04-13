---
title: reader is open for early signups
date: 2026-04-12
tag:
  - reader
  - projects
  - side-project
  - audio
excerpt: I built a thing that turns articles into podcast episodes. You can try it now.
---

## What is reader?

I built [reader](https://reader.n0tls.com) because I kept accumulating articles I wanted to read but never got around to. Since becoming a dad, a lot of my media consumption has been in the audio format, I read a lot of books this way ontop of a bunch of podcasts I like. I wanted those articles in my ears, sitting in my podcast app like any other episode.

The idea is simple: paste a URL, and within a couple of minutes you get a podcast episode in your private RSS feed. Open it in whatever podcast app you use (Overcast, Pocket Casts, doesn't matter) and your article is just there waiting. You don't have to install anything new to listen, you just use what you already have.

## How it works

1. Submit a URL through the webapp, the Firefox extension, or the Android share sheet.
2. reader fetches the article, strips out the ads and navigation clutter, and runs the text through a TTS engine.
3. The audio gets added to your private RSS feed automatically.
4. Your podcast app picks it up on the next refresh.

The Firefox extension makes this pretty painless, one click while you're reading and the article queues up in your feed. The Android share sheet integration means any browser on your phone can send URLs to reader directly.

## Why I'm opening it up

I've been running this for personal use for a while and it's become something I actually rely on. My reading queue has genuinely shrunk because I can chip away at it while doing other things. Felt worth sharing.

Right now I'm opening it to a limited number of people. This is a hobby project running on a single server, so I want to grow it slowly and make sure the quality stays acceptable before opening it wider.

## What to expect

This is a best-effort service. It runs on my own hardware, it could break or go away. Audio quality is decent, I'm using a local TTS model to keep costs down, so it sounds like a good automated voice, not a professional narrator.

Current limits per user: 5 submissions per day, 30-day retention on audio files. That might change as I figure out the real costs at scale. If you want to use a lot more than 5 submissions a day let me know and I will raise your limit, it's a safety thing for now.

The code will be open-sourced once it's cleaned up enough that I'm not embarrassed by it, with full self-hosting support.

## Try it

If you want in, head to [reader.n0tls.com](https://reader.n0tls.com). If there are invite slots available you'll see an "Open for limited signups" button, sign in with Google and you're in.

There's also a [Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/readerpodcast/) on AMO if you want the one-click workflow.
