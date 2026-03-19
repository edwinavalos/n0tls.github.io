---
title: Local Coding Agents Were A Mistake
date: 2026-03-10
tags:
  - llms
  - coding agents
  - claude
  - context
excerpt: Local coding agents introduce too much risk
---

## Intro

I have lived in Claude Code for the better part of 9 months now and have come to love it as a sysadmin and coding tool available to me right in my terminal. I lived in the terminal prior to this as I generally hate using a mouse and having to click around in GUIs to make things work. My experience has been mostly at work and at home in very different contexts.

This isn't going to be the normal "you should be sandboxing all these tools" types of post, as more of just the general observations I have made as coding agents start to proliferate in corporate environments. Because coding agents can be so powerful in automating many engineering tasks from writing code, to managing deployments and the full lifecycle of an application given enough MCP/CLI/MCP access, the blast radius of these tools is potentially catastrophic. Getting in the way of developers going at Mach 10 is never a popular proposition, so then how do we start moving the mush-iness that is LLM produced code to making the process more rigid and prevent the LLMs from diverging as much as possible from doing the right thing.

## Doing the right thing

My general philosophy to user experience when people are expected to use APIs I contribute is "Make it hard to do the wrong thing, make it seamless to do the right thing". I've worked on projects in the past to standardize the deployment process for various deployment technologies at [$DAYJOB](https://tech.target.com/blog/targets-cloud-journey). When we first started on the journey to creating TAP we did a lot of things in very clunky ways as everything was still coming to existence in and around management or cloud resources.

Coding Agents feels the same to me. Individual's coding assistant configurations are all over the place. On the same engineering team you might have 7 different ways of configuring your local coding agent sessions than others on your team. In a lot of cases this is probably fine, as long as what you think should absolutely should be shared is somewhere in the files that the coding agent has access to. Individual coding assistants feels like the *pets vs cattle* phase of cloud deployments back in the day. The industry eventually moved towards immutable infrastructure and the reliability that the paradigm introduced to cloud computing.

As well intentioned a developer might be, the fact that we can get wildly different results from the same prompts has always bothered me deep down inside. We are engineers, we prefer to have rigid processes and algorithms that solve the problem as deterministically as possible, and with that comes the risk of agents doing the absolutely wrong thing in some percentage of a unit of work they have been tasked to do. LLMs lie, cheat, and will do anything to try and solve your problems. We've all been there, you start to see Claude start writing some intense bash one liners and see a directory you did not expect to be read being read. You mash the esc key as fast as you can to abort. It happens a few times a week for me, but I also believe that I use these tools significantly more than the average user.

## My observations

1. LLMs will eventually do something dangerous, so do your engineers.
2. LLMs increase the speed of seasoned engineers in some aspects, for me in particular is local testing, Claude runs all my local integration testing in managing my local test environments in docker and in libvirt.
3. Greenfield is what they are best at, I have pointed coding agents in the summer to existing code bases and they struggled, but since November things have changed dramatically in this aspect, and I think given time these agents will get even better.
4. LLMs do best with a very very small unit of work.
5. LLMs favor those that can hold large architecture contexts in their brains as well.
6. Filling a context window and compacting it kills the effectiveness of agents, subagents with extremely small contexts is my current solution to this

## Things that have influenced me

[Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
[Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04)
[Gas Town Repo](https://github.com/steveyegge/gastown)
[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) -- This was my introduction to subagents in the summer, from this I was able to envision tooling that would break work down into the smallest reliable pieces of work an LLM can do.
[Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams)
[Code Mode: give agents an entire API in 1,000 tokens](https://blog.cloudflare.com/code-mode-mcp/)
[Claude Code Advance Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

# What I think needs to exist

Centralized orchestrators have to exist for large engineering organizations. There are very corporate reasons for some of my arguments, but a lot of them will come down to trying to lower the amount of uncertainty and prevent as many LLM mistakes as possible.

What that looks like in my opinion is something that marries a lot of ideas that I've thrown around but haven't been able to string all the PoCs together but here's the system I envision.

1. A coding agent should act as much as like a thin client to a remote system where the agent is actually operating.
2. For any given task, an agent should be able to check if there's an approved workflow for running through the current ask (task gateway?)
3. Tasks in workflows are so small that they can be evaluated for behavior 1000s of times with 0 or some amount of acceptable failures
4. Self-Verification is our white whale, how do people execute or verify the code that an LLM produced, the same tools we use to QA should be available to the LLMs eventually once people are comfortable with them verifying their own work... I know, I know, I'll talk about this some other time.
5. Most importantly, context should be heavily manipulated within a workflow to only insert the absolutely necessary context to execute the small task as possible, do not waste context in your system prompt that isn't relevant in running a linter. This is where subagents and atomic operations that can be run in large evaluation runs come in...
6. MCP gateways are a must, the agent needs to find the right tool from potentially hundreds/thousands of tools at a large enough company that we need to have methods of injecting only the needed tools for a workflow task to be completed.

But Edwin, why can't most of this just be scripts? Most of it should and will eventually be as automated as possible into deterministic code, but what I've found myself doing many times, is working an LLM to 'manually' execute a procedure, and then I ask it to eventually create a script for the process that we just accomplished and with the knowledge of anything it itself found confusing during the testing and execution of the process.

I have to think this through a little more, but this system partially already exists. Beads, Molecules, Formulas are a start to this paradigm. LLMs need to find and use the right workflow for a given task, and those tasks should be as small as possible.

Given enough autonomy I think you can eventually get the LLMs to improve their own processes by examining their own session behavior and create common tooling for themselves and their own agent swarms, but that is far off.

There's more that I need to think about, but wanted to get my ideas down somewhere.
