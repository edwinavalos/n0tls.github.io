---
title: Things I can automate now
date: 2026-05-24
tags:
  - automation
  - llms
  - claude
excerpt: The things that have become easier
---

There's a quote attributed to Bill Gates: “I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it.”

I'm that lazy person. One of the nice things of being able to do large amounts of 'research' work at $DAYJOB has been finding the places where I can reduce signficant amounts of Toil that slows down a lot of new development activies. I very often had moments in previous development work before coding agents where I would need to stop spending that extra effort to make something 100% automated, or something that had good ergonomics for future maintenance and operations. But since the advent of Claude Code being inserted into my workflow I am able to task the LLMs with those small quality of life tasks.

Things that I have enjoyed automating:

- *Commits*: I generally just let these be journal notes for the LLM, I often have it reference git commit history for notes it left itself.
- *PRs*: If I'm working on something persona, I generally don't PR when vibing, but at work I have it follow a PR template, it generally fills these out pretty well. I like to have a few well defined pieces of evidence required in the PR.
- *Taking screenshots and videos of new features* working to be attached to PRs
- *Watching deployments for failures* and looping until issues are fixed and builds pass. This is a very very lazy way of using these things, but in essence most of the feature work is complete by the time I start this submission loop to CICD, things that get caught in CICD eventually need to be automated/linted/checked for before we get to CI, But I heavily think that should be dictated by some positive feedback loop in the future. This is the one that has saved me the most time to be honest. We have all the automation for every PR to be submitted to CICD on a push, then if those pass a merge to main will push to our dev environment, and a cut of tag can be used release to production. This is a very straightforward process for our group, but baby sitting and making sure nothing odd happens during the deployment is one of those things that I can't fully disconnect from if I am doing it manually. When I started a new project with the use of Claude Code, I still preferred to do the deployment of the software by hand to see what it looked like without complete automation. It would take me upwards of any hour of baby sitting the automation through to production. Longer if I found an issue and needed to write a patch and get that through dev once more. Things like that are easily 'codified' into prompts for the monitoring loop, but in the end a lot of this should end up ina rigid framework down the line. It's good to rapidly protoype the automation. I will go more into these loops when I have a better working example on my personal projects, most of this is at $DAYJOB.
- *Initial project research* A lot of the time I just want to get a survey before I start a big project, finding prior art and thinking about if I am adding anything to the project or if I want expand on an idea. Being able to get run a consistent analysis for indicators of whether or not a project is worth my time shortens this research from hours to a few minutes.


In general I very rarely have to interact with an IDE anymore, I keep Goland open to copy in a scratch file for some formatting most of the time, but the vim mode in Claude Code mostly replaces that. Claude is the main interface to 95% of my computing, its nice to live in the terminal like this. I've only really caught myself running linux commands manually a few times in the last year, mostly when typing the English for what I want to do is slower than just doing `ls -al | grep word`.

I don't know why I wrote this other than to just get my ideas going again, but always curious to see what people are automating.


