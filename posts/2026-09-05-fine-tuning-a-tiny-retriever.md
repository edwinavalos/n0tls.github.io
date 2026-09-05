---
title: RAG research continued - fine tuning three bi-encoders
date: 2026-09-05
tags:
  - llms
  - rag
  - embeddings
  - experiments
excerpt: Learning more about training and finetuning for text retrieval
---

Previously we built an [agent](/posts/2026-09-03-i-think-i-reinvented-rag-with-grep.html) that was the result of working through a set of evals based on an unknown corpus of markdown documents. It worked OK because the index of 457 markdown documents comfortably fits into a context window. We found an easy-ish solution that did some calculations upfront (creating the index) and used that to drive better results. But bi-encoders and vector search exist, and in particular help us scale solutions where we are indexing many thousand or millions of documents. I wanted to learn how those technologies work and how we can use them to improve our results.

I also had a hardware itch to scratch. I've got a desktop on the network with an RTX 3080 (surprisingly lets me do a lot with it), and I wanted to know if I could finetune bi-encoders to do a better job if they know more about documents, and how they are used.

## The pipeline

Three scripts:

1. Generate synthetic `(query, doc)` training pairs by batching the corpus through an LLM and asking for a few realistic user questions per doc. 457 docs became 1,373 pairs, minus one dropped for looking too close to a real eval query, checked by word overlap between the two.
   - **The risk being guarded against:** the eval and the synthetic training set both come from questions about the same corpus, so they can coincidentally converge on near-identical phrasing. If a real eval query asks "how do I set environment variables for a deno script" and a training pair happened to generate "how do I set env variables in a deno script," fine-tuning on that pair would let the model memorize the exam question instead of learning to retrieve it, which would inflate the eval score without meaning anything.
2. Fine-tune a small bi-encoder on those pairs with **`MultipleNegativesRankingLoss`**, the loss that treats every other example in the batch as a free negative, so a batch of 32 gives you 31 negatives per query for nothing. Ran this against three different starting points: `all-MiniLM-L6-v2`, `bge-small-en-v1.5`, and `e5-small-v2`. Each one trained in under a minute on the 3080. Not a hardware-bound problem at this corpus size, which leaves room for more experimentation as we test against corpora an order of magnitude or two bigger. Fine-tuning is a one-time upfront compute cost; if it holds up at that scale, paying it once ahead of time beats paying heavier compute costs over and over later.
3. Score it: encode every doc and every query, cosine similarity via a single matrix multiply, rank, compare to ground truth using the exact same scoring rules as the agent evals so the numbers are actually comparable.

I also tried retrieve-then-rerank: let the bi-encoder shortlist the top 10, then have an off-the-shelf cross-encoder reorder just those 10. To achieve this we used sentence transformers as the bi-encoder embeds the query and each document separately, so doc vectors get computed once, ahead of time, and search is just a similarity check against vectors already sitting there. A cross-encoder takes the query and one document together as a single input and outputs a relevance score for that pair; it can't precompute anything and can't search a corpus on its own, only re-score a short list some other process already retrieved.

## Experiment results

| model | exact hit@1 | acceptable@1 |
|---|---|---|
| all-MiniLM-L6-v2, base | 26.7% | 37.8% |
| **all-MiniLM-L6-v2, fine-tuned** | **40.0%** | **48.9%** |
| bge-small-en-v1.5, base | 44.4% | 55.6% |
| bge-small-en-v1.5, fine-tuned | 35.6% | 44.4% |
| e5-small-v2, base | 31.1% | 44.4% |
| e5-small-v2, fine-tuned | 33.3% | 44.4% |

(exact hit@1: the model's top-ranked doc is the actual ground-truth answer; acceptable@1: the top-ranked doc is the ground-truth answer or one of a small set of marked acceptable alternates)

Fine-tuning helped on every single metric I tracked for the MiniLM models, including a jump from 75% to 92.5% on recall@5.

Then we worked against bge-small. It was the strongest model before we ran it through our pipeline. It was better out of the box than either of the other two, better than either of them fine-tuned, and my fine-tuning run made it worse across the board. Finally e5-small landed in between: basically flat on hit@1, better on recall.

I don't have a solid explanation for the bge-small regression. My best guess is that 1,372 pairs from a single LLM pass, with no hard negatives and no hyperparameter search, is a thin recipe, thin enough that it happened to suit whatever MiniLM was weak at and disagreed with whatever bge-small was already good at. I didn't chase it further this round. Scaling up the pair count or mining actual hard negatives are the next levers, which might become a follow-up post.

## The reranker made things worse

I fully expected retrieve-then-rerank to be a free accuracy bump. It's the standard second stage in 'real' retrieval pipelines. Instead:

| pipeline | hit@1 before | hit@1 after |
|---|---|---|
| finetuned-minilm -> cross-encoder rerank | 40.0% | 37.8% |
| bge-small (base) -> cross-encoder rerank | 44.4% | 35.6% |

(hit@1, same definition as above: how often the model's top-ranked doc after reranking is the correct one)

Both got worse. The cross-encoder I used is trained on MS-MARCO, general web search relevance. Because of that "relevant" on web search queries and "relevant" on Deno CLI documentation aren't the same shape of judgment. It confidently re-ordered a correct top-1 guess into second place often enough to drag both pipelines down. A domain-matched cross-encoder, or a fine-tuned one, is a different experiment.

## What matters

None of these beat the single-shot LLM agent from last time, which got 57.8% exact / 73.3% acceptable just by reading a catalog and grepping around with some calibration instructions. On a corpus this small, an LLM that can see the whole thing and reason about intent still wins over pure nearest-neighbor lookup with no ability to say "none of these documents answer this."

A bi-encoder's whole value proposition is sublinear lookup over a corpus too big to fit in a prompt, and 457 docs are not enough to fill most contexts nowadays. I built and scored a retriever whose actual advantage never got exercised. The real next experiment is running all of this, agent methods included, against corpora one or two orders of magnitude bigger, where shoving it into context is not a valid solution and I'd expect the fine-tuned retriever to start performing better.

Along the way I also built myself a few explainers: [a walkthrough of the bi-encoder/cross-encoder architecture](https://claude.ai/code/artifact/c9bd557a-17a4-442f-8f65-a7c7d010a64b), [a line-by-line map from that theory to the actual code in this repo](https://claude.ai/code/artifact/8ac1ece9-cf0c-4245-9110-81da60d2c4fc), and, because I realized I didn't actually understand what was happening inside these models below the sentence-transformers API, [a walkthrough of the transformer internals themselves](https://claude.ai/code/artifact/a5d9564f-1617-4026-bc70-6db7bccdf7f2): tokenization, attention, pooling, and why training one of these from scratch on a corpus this small almost certainly wouldn't work (pretraining sees billions of sentence pairs; this corpus is a few hundred thousand words).

Full writeup with all the numbers, the process notes, and what's deferred is in the repo at [`docs/finetuning-investigation.md`](https://github.com/edwinavalos/rag-research/blob/main/docs/finetuning-investigation.md). Repo's at [github.com/edwinavalos/rag-research](https://github.com/edwinavalos/rag-research).
