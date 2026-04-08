---
title: "experiments.n0tls.com"
date: 2026-04-07
tags: [meta, experiments]
excerpt: "A new home for small tools and projects — starting with voice model evals."
---

I spun up [experiments.n0tls.com](https://experiments.n0tls.com) as a place to host small tools and one-off projects that don't quite fit as blog posts. Think interactive things, weird ideas, half-finished prototypes that actually work.

The first experiment is a **voice evals tool** — a way to compare output quality across open-weight TTS models by pulling levers on the underlying parameters.
It went from a vague conversation to a working tool in one sitting. The transcripts are up if you want to see how that unfolded:

- [Voice Evals — Ideation](/transcripts/voice-evals-ideation.html): the pivot from another project, rebuilding the scope from scratch in conversation
- [Voice Evals — Implementation](/transcripts/voice-evals-implementation.html): a fresh session reads the CLAUDE.md written in ideation and builds the whole thing

The second experiment is a **batch piper comparison** — the same article synthesized two ways: one piper process per chunk (model reloads each time) vs. one process for all chunks (model loads once). A 29% speedup, and you can hear both to judge whether there's any quality difference.

- [Batch Piper Comparison](https://reader.n0tls.com/experiments/batch-comparison): listen and compare
