---
title: How I learned and started hating the term RAG
date: 2026-09-03
tags:
  - llms
  - rag
  - agents
  - claude
  - experiments
excerpt: A control environment, five eval runs, and a lot of bugs on the way to figuring out why a RAG pipeline can't find the first document.
---

I've been working with a RAG service that had abysmal first-document retrieval out of the box, and I wanted to dig further by using a very generic example to see what I could come up with blind, not knowing the domain of the documents I was trying to retrieve. Instead of guessing at knobs to turn, I wanted to run experiments one by one to see what changing a certain technique would cause. I wanted to do this without fetching encodings from a RAG service directly and see what we could do with better plaintext indices and maybe better prompts. The better prompting was something that I was very apprehensive about. I hate solving LLM patterns with prompts and was hoping to see how much the different instructions helped. 

## The control environment

Picked [denoland/docs](https://github.com/denoland/docs) as the target which has 457 markdown files in a public github repo. Nothing I own so no bias in how it's structured. Then two subagents were used to keep their contexts separate.

1. One roleplays a spread of Deno users (Node migrant, beginner, someone debugging permissions, someone pasting an error) and writes 45 queries. Importantly, *without* reading the corpus, so that questions do not get affected by any information that could be found in the documentation.
2. A second agent explores the corpus and links each query to its ground-truth answer doc, or marks it `coverage: none` if nothing in the corpus actually answers it.

I ended up with 38 direct hits, 2 partial, and 5 unanswerable queries in the ground truth. I ended up using gpt-5.1-nano for this as I am of the opinion that making something the best it can be with the worst tools available will make it much easier to adopt the better tools and get even better results, and it saves some money.

## Round 1: the graph loop I originally imagined

My first instinct (and the thing I actually came in wanting to build) was a graph-based agent on [google/adk-go](https://github.com/google/adk-go) — `search → judge → loop back or finalize`, bounded at 4 rounds.

Baseline: **51.1% exact hits, 62.2% acceptable, ~22s/query.**

## Round 2: reading a reference architecture instead of guessing

Before iterating further I went and read a reference architecture of an exploration tool. It differs that it has no judge, no loop at all. One agent turn, instructed to fire tool calls in parallel and search thoroughly before committing, then report once. So I built a second method to test with the same eval set, same tools, no looping to compare it against the original graph idea I had.

**55.6% exact, 62.2% acceptable, ~6s/query.** Faster by 4x and slightly more accurate. The loop wasn't earning its cost on this corpus; sometimes it recovered a wrong first guess, more often it just spent extra rounds converging on the same answer or a worse one.

## Round 3: matching the actual toolset

Kept digging into that same reference architecture's tools instead of assuming. Its glob tool does real `**` glob matching. We swapped in [doublestar](https://github.com/bmatcuk/doublestar). Its grep tool supports ripgrep-style `-A/-B/-C` context lines and added that too. It **made things worse** (51.1% / 57.8%), which was a useful negative result: more context per grep call meant fewer, more "satisfied" parallel calls, trading search breadth for depth it didn't need. I then ported a ranking heuristic that is used to find the right tool among hundreds of deferred ones. It seemed like a similar shape of a problem as finding the right doc among hundreds of files into a `rank_docs` tool that scores every doc by weighted term overlap (path > title > body) and returns a ranked shortlist instead of an unordered grep dump. A note for future self is to do a cost comparison between marginal improvements.

**55.6% exact, 66.7% acceptable** a new best, and it recovered the context-lines regression.

## Round 4: the big one

During these experiments the agent would confidently name a wrong document for queries the corpus doesn't cover, instead of recusing itself. I wanted to try a few more ideas tested together that weren't necessarily aiming at solving that problem, but I wanted to see how useful it was.

1. **A corpus catalog**. Built out-of-band (a separate one-time command, not inside the eval loop), the LLM summarizes every doc in the corpus into single-sentence summaries and some small metadata, batched, then the whole 457-entry catalog gets inlined directly into the agent's system prompt. The idea: the model was deciding "nothing covers this" from an *incomplete* search. Let it see the whole corpus's shape at once instead.
2. **A calibration instruction**. Require the model to quote the actual passage supporting its answer, and tell it explicitly that "not covered" is a common, correct, expected outcome, not a failure to avoid. I hate having to resort to a prompt here, but it did help.

**57.8% exact, 73.3% acceptable** — biggest single jump of the night, and one of the five original unanswerable queries flipped from confidently-wrong to correctly-abstaining for the first time all evening.

## Then I went down a rabbit hole

Towards the end of the experiment I started asking why any of this beats the RAG service that gave me those bad experiences in the first place, and ended up talking myself in a circle about it.

Here are the things that stuck out to me:

**What we built has no vectors in it.** No embedding, vector, or similarity search. The catalog is inlined text the model reads directly, no retrieval step at all. That works because the corpus is small enough to fit in context (457 docs, ~15K tokens for the whole catalog). This solution does not scale. The moment the corpus doesn't fit reasonably into context, you start to incur significant token increase. This is the reason vector retrieval exists: embeddings aren't much better, they're just the best we have for solving these types of problems at the moment at scale.

Also finally got why "RAG" as a label bugs me: it names a paradigm ("retrieve then generate"), and people use it as if it names a technique. Under that one umbrella you'll find naive top-k cosine similarity, hybrid search with reranking, GraphRAG, RAPTOR (hierarchical LLM-summarized trees, our single flat file being related to this), agentic search, and long-context stuffing. These all get called "RAG" depending on who you talk to despite being different mechanisms with different quality ceilings. When a vendor says "we have RAG," it tells you nothing about how they are doing things, you will need to dig in deeper to see if they are doing something novel.

Ended the night generating myself [an explainer on cosine similarity](https://claude.ai/code/artifact/13f6d86e-9e9f-4a69-84d6-290a58999dfe) because I wanted the geometric intuition for why direction-not-distance is the thing being compared, using our own flip-flopping `permissions.md` vs `security.md` result as the running example. My brain hurt by the end. Good night.

## The numbers, all together

| method | exact hits | acceptable hits | avg time/query |
|---|---|---|---|
| graph (search↔judge loop) | 51.1% | 62.2% | 21.6s |
| single-shot, no glob | 55.6% | 62.2% | 5.7s |
| single-shot, +glob | 53.3% | 62.2% | 6.2s |
| single-shot, +glob+context | 51.1% | 57.8% | 5.8s |
| single-shot, +glob+context+rank | 55.6% | 66.7% | 6.2s |
| single-shot, +catalog+calibration | **57.8%** | **73.3%** | 14.0s |

The repo is at [github.com/edwinavalos/rag-research](https://github.com/edwinavalos/rag-research). There's still 2 of the 5 unanswerable queries coming back confidently wrong, so maybe an adventure for another night.
