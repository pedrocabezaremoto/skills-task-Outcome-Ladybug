Blocker Guessability Prompt

Blocker Guessability Check

Use this prompt to test whether a blocker can be correctly inferred from its description alone. Run the prompt once per blocker.
Ensure the setup patch is applied and that no golden patch or test patch code is present
Agent task

Describe (not implement) the best approach to resolve the blocker.
Expected outcome

The agent’s described approach should NOT match the blocker resolution.
❌ If it does match, the blocker is guessable and should be redesigned.



PROMPT:

You are helping with a software task. Assume you are a competent engineer who is unfamiliar with this repository.



## Problem Statement

{{Problem Statement}}



## Requirements

{{Requirements}}



## Public Interfaces

{{Public Interfaces}}



## My Confusion

I have the following confusion about this problem:

{{blocker_description}}



## Your Task

Describe in detail the best possible or most likely thing I should do to resolve this confusion.



Explore the codebase thoroughly and use your knowledge of best engineering practices for a repository like this before answering.



Do NOT implement anything. Do NOT write code or patches. Just describe what you would most likely do and why.