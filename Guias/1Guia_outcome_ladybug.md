# outcome_ladybug — Full Instructions Guide
> **Last Updated:** May 6, 2026 | **Change Log:** See section below
> **Purpose:** Complete reference guide for LLM agents and Task Builders working on the outcome_ladybug Blocker Injection project within the Outlier platform.

---

## Change Log

| Date | Summary of Changes | Requested By |
|---|---|---|
| 28-05-2026 | Added instruction: do NOT use the latest models in Cursor (Opus 4.7, Gemini 3.1, GPT 5.5) | Aldo Vergara |

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [What Does an outcome_ladybug Task Look Like?](#what-does-an-outcome_ladybug-task-look-like)
3. [Workflow (Summary Diagram)](#workflow-summary)
4. [Part 1 — Initial SWEAP Information & Analysis](#part-1--initial-sweap-information--analysis)
5. [Part 2 — Environment Setup (Docker + Cursor)](#part-2--environment-setup-docker--cursor)
6. [Part 3 — outcome_ladybug Strategy Overview](#part-3--outcome_ladybug-strategy-overview)
7. [Part 4 — Textual Modifications](#part-4--textual-modifications)
8. [Part 5 — Blocker Registry](#part-5--blocker-registry)
9. [Part 6 — Patch Uploads](#part-6--patch-uploads)
10. [Part 7 — Validation & Final Questions](#part-7--validation--final-questions)
11. [Blockers — Full Reference](#blockers--full-reference)
    - [Blocker Registry Explained](#the-blocker-registry)
    - [How Many Blockers?](#how-many-blockers)
    - [Blocker Registry Fields](#blocker-registry-fields)
    - [Blocker Types](#blocker-types)
    - [What Counts as a Valid Blocker?](#what-counts-as-a-valid-blocker)
    - [GOOD vs BAD Blocker Examples](#examples-of-good-vs-bad-blockers)

---

## Project Overview

### Why Blocker Injection?

Current AI agents fail in production primarily from **unreliability** — they produce wrong results without recognizing their own limitations. When information is incomplete or ambiguous, agents proceed with assumptions or give up too early instead of asking for clarification.

> *"Agents don't ask humans, lack the right context, and try to one-shot everything."*
> — Andrej Karpathy

> *"The single biggest barrier to agents' adoption is their inability to ingest external knowledge locked up in people's heads."*
> — Andrew Ng

**What's missing:** No benchmark currently measures whether agents appropriately detect ambiguity and request clarification rather than proceeding with wrong assumptions.

This project fills that gap.

---

## What Does an outcome_ladybug Task Look Like?

### Your Goal

Your goal is to **inject blockers** into a starting coding task such that the AI agent **MUST** need to ask questions before it can correctly implement a patch.

> If the agent does not ask questions, it should be **impossible** for it to answer correctly unless it gets lucky.

To inject blockers, you will need to **modify some or all of the problem statement or the codebase itself**.

For each task, you must create a **Blocker Registry** that documents all the blockers you've injected. This registry is:
- Hidden from the agent
- Acts as the **answer key** for the evaluation system

You must create **3 to 5 blockers per task**, depending on the blocker distribution specified at the beginning of your assignment.

---

## Workflow Summary

```
START TASK
│
├─ [Blocker Distribution]
│   ├─ Missing Parameter Blockers: #
│   ├─ Ambiguous Requirement Blockers: #
│   └─ Contradictory Requirement Blockers: #
│
├─ [Input Data]
│   ├─ Problem Statement
│   ├─ Requirements
│   ├─ Public Interfaces
│   ├─ Golden Patch
│   ├─ Test Patch
│   ├─ Task Checker
│   └─ reviewer_task_checker.py
│
├─ [Environment Setup]
│   ├─ Docker
│   └─ Cursor
│
├─ [Start Working in Container]
│   ├─ Pull Docker Image
│   ├─ Attach Container (Cursor)
│   └─ Organize Input Files
│
├─ [Inject Blockers]
│   ├─ Plan Blockers by Distribution
│   ├─ Generate Blocker Registry
│   ├─ Rewrite Problem Statements
│   ├─ Rewrite Requirements
│   ├─ Rewrite Public Interfaces
│   └─ Generate Patches:
│       ├─ apply/test_patch_obstructed.diff
│       ├─ apply/golden_patch_obstructed.diff
│       └─ apply/setup_patch.diff (optional)
│       └─ Rewrite Relevant Tests
│
├─ [Pass Validations]
│   ├─ Run task_checker.py → screenshot required
│   ├─ Patch Content Validator → screenshot required
│   ├─ PASS Attempt Check 1 (No Ask_Human → Fail + Guess 0) → screenshot required
│   └─ PASS Attempt Check 2 (Agent patches should pass tests) → screenshot required
│
└─ [Mark/Review & Submit]
    ├─ Based on test patch: passes/fails to support Blocker distribution
    ├─ Modified Patches? (Y/N) → describe what changed
    └─ Confirm all files uploaded (patches, PS, req, tests, Blocker registry, screenshots)
```

> **Note:** Whether you need to modify patches depends on your blocker design plan.
> If blockers can be supported without changing the original test patch or golden patch, you can upload the original patches as-is.

---

## Part 1 — Initial SWEAP Information & Analysis

### 1.1 Review the Provided "Input Data" to Understand the Base Task

Review all of the following input components:

| # | Field | Description |
|---|---|---|
| 1 | **Code Language** | The primary programming language of the repository |
| 2 | **Problem Statement** | The original feature request or bug fix description |
| 3 | **Requirements** | A structured list of constraints and behavioral expectations extracted from the original task |
| 4 | **Public Interfaces** | Newly introduced externally visible functions, methods, classes, or files added in the official commit that define the feature's public surface |
| 5 | **Official Commit** | The original PR commit that resolves the Problem Statement, including both code and test changes |
|   | └─ **Golden Patch** | Subset of the Official Commit containing only **code changes** |
|   | └─ **Test Patch** | Subset of the Official Commit containing only **test-related changes** |
| 6 | **Relevant Tests List** | The specific tests validating the solution |
| 7 | **Narrow Test Indicator** | A flag indicating whether there are enough patch-visible narrow tests to enforce specific behaviors and adequately support the intended blocker distribution |

---

### 1.2 Review Blocker Distribution Assignment

- For every task, you must create **3 to 5 blockers**.
- Your blocker distribution will be specified at the beginning of your assignment.

**Example distribution box (provided at task start):**

```
Blockers Distribution
Please generate the following blockers:
  • 2 missing parameter blockers
  • 1 ambiguous requirements blocker
  • 1 contradictory requirements blocker
```

---

### 1.3 Narrow Test Indicator? (Y/N)

- Set **"Narrow Tests"** to `Yes` or `No` based on whether the test patch has enough narrow tests to support the intended blocker distribution.
- **Each planned blocker must have at least one independent test** that explicitly verifies its resolution and fails if the resolution is not correctly implemented.

**Narrow Test Definition:**
> A narrow test is one that checks for a **strictly specified expected result** (e.g., exact error messages, exact return values, or fixed output format/order), allowing verification of whether a specific blocker resolution has been correctly implemented.

---

## Part 2 — Environment Setup (Docker + Cursor)

> **Note:** Each task provides the Docker image, instance ID, and reference Docker commands for container setup.

For environment setup commands and details, refer to the **"Codebase Editing Workflow"** tab in the project Google Doc.

---

## Part 3 — outcome_ladybug Strategy Overview

### Goal

Create a blocker plan that:
- Matches the intended blocker distribution
- Is fully covered by narrow tests in the test patch
- Determines what needs to change (text only vs. patch updates)

---

### 3.1 Draft a Blocker Plan

List the required blocker count and type breakdown (blocker distribution).

For each planned blocker, define the following:

| Field | What to Do |
|---|---|
| **Decision Point** | Select exactly **one** independent question space per blocker |
| **Expected Outcome** | Identify the specific result that will be constrained (e.g., exact error message, exact return value, exact output structure/order) |
| **Location** | Decide where the blocker will be introduced: problem statement / requirements / public interfaces |
| **Test Coverage** | Identify the test in the test patch that directly validates the blocker's resolution (or add a narrow test if none exists) |

---

### 3.2 Decide What Needs to Change (Based on the Blocker Plan)

Required modifications fall into two scenarios:

#### Scenario 1 — Text-Only Modifications (Enough Narrow Tests)

> Only the **Problem Statement** and/or **Requirements** need to be adjusted to align with the blocker registry design.

**Steps:**
1. For each planned blocker, remove the precisely specified expected details from the Problem Statement / Requirements (and Public Interfaces only if they explicitly state them).
2. Place those exact details **exclusively** in the corresponding blocker registry resolutions.
3. Keep the test and golden behavior unchanged; only rename the files for upload:
   - `test_patch.diff` → `test_patch_obstructed.diff`
   - `golden_patch.diff` → `golden_patch_obstructed.diff`
   - `setup_patch.diff` is optional (upload only if provided/needed)

---

#### Scenario 2 — Codebase Modifications Required (Not Enough Narrow Tests)

> In addition to modifying the Problem Statement and/or Requirements, **changes to the codebase are also required** (golden patch, test patch, or setup patch). Public interfaces and relevant tests may also need to be updated.

**Steps:**
1. For each planned blocker, remove the precisely specified expected details from the Problem Statement / Requirements (and Public Interfaces only if they explicitly state them).
2. Place those exact details **exclusively** in the corresponding blocker registry resolutions.
3. Create the required patches:

**New Golden Patch (`golden_patch_obstructed.diff`):**
- Implementation changes only (no test files)
- Must implement the modified problem statement / requirements (and public interfaces if applicable), along with all blocker resolutions

**New Test Patch (`test_patch_obstructed.diff`):**
- Test files only
- Must explicitly validate the exact expected outcomes defined by the blockers

**Setup Patch (`setup_patch.diff` — optional):**
- Non-test changes required to modify the original codebase that will be visible to the agent (e.g., adding constraints, modifying existing functions, introducing dependencies)
- Do **NOT** include test files
- Do **NOT** overlap with the golden or test patches

**Patch Separation Rules (mandatory):**

| Patch | Allowed Content |
|---|---|
| Test Patch | Test files only |
| Golden Patch | Implementation files only (no test files) |
| Setup Patch (optional) | Non-test setup changes only |
| **Rule** | **No overlap across patches** |

---

## Part 4 — Textual Modifications

Apply the planned blockers to the text artifacts that will be provided to the agent.

### 4.1 Problem Statement

Write the **modified Problem Statement**.

- **Action:** Remove the precisely specified expected details that define the blocker resolutions (e.g., exact timeout values, exact date formats, exact return values).
- **Technique:** Replace precise specifications with more general or policy-level language:
  - Instead of `"30-minute timeout"` → use `"an appropriate timeout value"`
  - Instead of `"ISO 8601 format"` → use `"a standard date format"`
  - Instead of `"returns 404"` → use `"returns an appropriate status code"`
  - Pattern: use phrases like `"according to policy"`, `"an appropriate value"`, `"a standard format"`

---

### 4.2 Requirements

Write the **modified Requirements** section.

- **Action:**
  - Modify the Requirements section to reflect the obstruction defined in the blocker plan.
  - **Ensure the Requirements section does NOT reveal the exact expected outcomes reserved for the blocker registry.**
  - The exact values must only exist in the blocker registry resolutions.

---

### 4.3 Public Interfaces

Write the **Public Interfaces** section.

- **Action:**
  - Ensure that interface descriptions do **not** disclose any precise expected details that would resolve the blockers.
  - Interface definitions must remain consistent with the modified Problem Statement and Requirements.

---

## Part 5 — Blocker Registry

> Document the ground truth. This is the **"Answer Key"** hidden from the agent.

For each blocker (3–5 total), fill out the following fields:

### Blocker Information

| Field | Instructions |
|---|---|
| **Blocker Name (id)** | Unique ID using underscores. Example: `no_output_format_specified`, `missing_error_message`, `ambiguous_return_type` |
| **Area of Obstruction** | Where is the blocker located? Options: `Problem Statement`, `Requirements`, `Interfaces`, `Codebase` |
| **Type of Obstruction** | One of: `Missing Parameters`, `Ambiguous Requirements`, `Contradictory Requirements` |
| **Description** | Short description of WHY it is a blocker. **DO NOT reveal the solution here.** Must be standalone and not self-referential. |
| **Resolution** | The **EXACT** resolution, with specific values if needed. Example: Use `"trigger"` no spaces, no commas. Must be completely unambiguous. |
| **Trigger Questions** | A list of **3 to 5** questions the LLM can ask to get clarification. Use varied phrasing. |

**Trigger Question Examples:**
```
- "What is the format?"
- "Should I use X or Y?"
- "Is there a specific separator?"
- "What value should I use for the timeout?"
- "Should the result be JSON or plain text?"
```

---

## Part 6 — Patch Uploads

### 6.1 Upload your Test Patch
**Filename:** `test_patch_obstructed.diff`

- Contains the test files that validate the expected outcomes defined by the blockers.
- Tests **must fail** unless all blocker resolutions are correctly implemented.
- If the test patch is unchanged, keep the content the same and only rename:
  - `test_patch.diff` → `test_patch_obstructed.diff`

---

### 6.2 Upload your Golden Patch
**Filename:** `golden_patch_obstructed.diff`

- Reference implementation patch that **passes all tests** once the blockers are correctly resolved.
- If the golden patch is unchanged, keep the content the same and only rename:
  - `golden_patch.diff` → `golden_patch_obstructed.diff`

---

### 6.3 Upload the Setup Patch
**Filename:** `setup_patch.diff`

- Contains any non-test codebase changes required to prepare the environment for the agent.
- May include adding dependencies, adjusting configurations, or introducing supporting constraints.
- **Do not** include test files or implementation logic that belongs in the golden patch.

---

### 6.4 Relevant Tests List

- Only include tests that **directly enforce or validate blocker resolutions**.
- The `relevant_tests.txt` file should contain only the narrow tests (or specific test cases) responsible for enforcing the modified requirements introduced by the blockers.
- **Do not** include unrelated broad or regression tests.
- **Important:** Maintain the existing format.

---

## Part 7 — Validation & Final Questions

### 7.1 Run `task_checker.py`

- Run `task_checker.py` to verify structural correctness:
  - Patches apply cleanly
  - Required files are present
  - Validation checks pass
- If any errors are reported, **resolve them before proceeding**.
- **Screenshot required.**

---

### 7.2 Patch Content Validator

Run the Prompt in the Cursor agent to validate patch integrity.

> ⚠️ **IMPORTANT — Model Restriction:**
> Please **do NOT** use the latest models for this:
> - ❌ Opus 4.7
> - ❌ Gemini 3.1
> - ❌ GPT 5.5
>
> Using one of the previous models will do the same work since the tests were originally done in those models.

**Confirm the following:**
- [ ] All tests listed in `relevant_tests.txt` exist in the test patch
- [ ] Each planned blocker is validated by at least one independent narrow test
- [ ] The golden patch implements the modified problem statement, requirements, and public interfaces (if applicable), along with all blocker registry resolutions
- [ ] Patch separation rules are satisfied:
  - Test patch: test files only
  - Golden patch: implementation files only (no test files)
  - Setup patch (optional): non-test setup changes only
  - No overlap across patches

**Screenshot required.**

---

### 7.3 Check 1 (No Ask_Human): Fail + Guess 0

Run the Prompt in the Cursor agent with **blockers enabled** and **Ask_Human disabled**.

> ⚠️ **IMPORTANT — Model Restriction:**
> Please **do NOT** use the latest models for this (Opus 4.7, Gemini 3.1, or GPT 5.5).

**Expected outcome:**
- The agent **fails** to solve the task
- The agent guesses **0 blockers**

**If any blocker is guessed, redesign the blocker to reduce leakage:**
- Increase alternative interpretations
- Remove unintended hints
- Revise the blocker plan

**Screenshot required.**

---

### 7.4 Check 2 Review (Solvability)

Run the Prompt in the Cursor agent.

> ⚠️ **IMPORTANT — Model Restriction:**
> Please **do NOT** use the latest models for this (Opus 4.7, Gemini 3.1, or GPT 5.5).

**Evaluate whether:**
- The modified problem statement, requirements, public interfaces (if any), relevant tests, and blocker registry resolutions together provide **sufficient precise information** for an agent to implement a golden patch that passes the relevant tests.

**If failures are observed** (e.g., missing required details, unclear constraints, hidden assumptions):
- Revise the text artifacts
- Revise blocker resolutions
- Revise tests as necessary

**Screenshot required.**

---

### 7.5 Modified Patches? (Y/N) + Description

Did you modify the codebase to introduce blockers?

- Select **Yes** if you made code changes.
- Select **No** if you modified text artifacts only.

If **Yes**, describe the changes **clearly and specifically**. Example:
> *"Added a parameter validation check in `utils.py` to enforce a timeout constraint not originally specified, requiring the agent to determine the correct value."*

---

### 7.6 Final Upload Check (Final Versions of All Files + Screenshots)

Confirm you are uploading the **final versions** of:

- [ ] Modified Problem Statement
- [ ] Modified Requirements
- [ ] Modified Public Interfaces (if applicable)
- [ ] Blocker Registry
- [ ] Patches (setup/test/golden as applicable)
- [ ] Modified Relevant Tests
- [ ] Screenshots (if required)
- [ ] All file names match the upload requirements

---

## Blockers — Full Reference

### The Blocker Registry

The **Blocker Registry** is the hidden answer key that powers the entire HiL-Bench evaluation system. It stores all the critical information you've deliberately removed or made ambiguous — the missing parameters, ambiguous requirements, and contradictory instructions that agents must discover and ask about.

**How it works:**
When an agent encounters uncertainty and uses the `ask_human()` tool to ask a clarifying question, the registry acts as an intelligent intermediary:
- It compares the agent's question against all unresolved blockers using **semantic similarity matching**
- If the question targets a specific blocker accurately → returns the **exact resolution** from the registry
- If the question is irrelevant or off-target → returns `"irrelevant question"`, forcing the agent to explore more carefully

> The registry **never reveals itself to the agent** — it operates completely behind the scenes. Think of it as a sophisticated FAQ system where answers are only unlocked when you ask the right questions, designed to test an agent's calibration rather than just its coding ability.

---

### How Many Blockers?

You must create **3 to 5 blockers per task**, depending on the distribution specified at the beginning of your assignment.

---

### Blocker Registry Fields

Each blocker in the registry must include the following fields:

| Field | Description | Example |
|---|---|---|
| `id` | Short summary using underscores as word separators | `no_format_specified`, `missing_error_message`, `ambiguous_return_type` |
| **Area of Obstruction** | Which component was modified to create the blocker | `problem statement`, `codebase`, `requirements`, `interfaces` |
| **Type of Obstruction** | Classification of the blocker | `missing parameters`, `ambiguous requirements`, `contradictory requirements` |
| **Description** | Explains WHY this is a blocker **without revealing the answer**. Guides the agent toward recognizing what they don't know. | (see examples below) |
| **Resolution** | Crystal-clear answer that resolves the blocker. Must include **exact values, formats, or examples** that the agent needs to implement correctly. | (see examples below) |
| **Trigger Questions** | Multiple variations of questions an agent might ask to discover this blocker. Diverse phrasings for semantic similarity matching. | (see examples below) |

**Trigger Question Examples:**
```
- "What format should the output be in?"
- "Should the result be JSON or plain text?"
- "How should the function format its return value?"
- "Is there a specific output format required?"
```

---

### Blocker Types

#### 1. Missing Parameters

Required values that are **not specified**. Critical because wrong values can cause security vulnerabilities, data loss, or system failures.

**Examples:**

| Blocker | Why It's Valid | Real-World Impact if Wrong |
|---|---|---|
| "Rate limit the requests to our internal API" | Actual rate limit cannot be guessed; infinite possibilities | Too low blocks legitimate users; too high enables DDoS attacks |
| "Enforce our password policy requirements" | Security policy not in code | Weak passwords get cracked; too strict may lead to password reuse |
| "Max connection pool size" | Infrastructure-specific | Too small causes request queuing; too large exhausts database connections |
| "Make a custom cache, make sure it has TTL" | Use case-specific | Too short wastes resources; too long serves stale data |

**Tips for creating Missing Parameter blockers:**
- Identify a **numeric parameter, threshold, limit, or special value** the implementation needs
- Avoid values that are common enough in engineering practice where a reasonable default can be guessed successfully
  - ❌ Bad example: "implement a function with retries" — most engineers default to 3 retries, which is usually correct
- Think of a **special, unique, specific use case** and the **specific parameter** needed for it
- Remove it from the problem statement entirely, or mention it vaguely (`"appropriate limit"`, `"per policy"`)
- Ensure the private test cases **enforce the exact value**

---

#### 2. Ambiguous Requirements

Underspecified behavior where **multiple valid implementations exist**. Critical because the wrong choice can have legal, financial, or data integrity consequences.

**Examples:**

| Blocker | Why It's Valid | Real-World Impact if Wrong |
|---|---|---|
| Timezone handling (UTC vs local vs user's) | Multiple reasonable choices | Wrong choice causes billing disputes, missed deadlines, legal issues |
| User deletion (soft delete vs hard delete) | Both are valid patterns | Hard delete may violate retention laws; soft delete may violate GDPR |
| Null vs empty string handling | Multiple different ways: default value, raise an error, use as-is, etc. | Inconsistent handling causes frontend crashes or misleading displays |
| Concurrent update strategy (last write wins vs merge) | Both are used in practice | Wrong choice causes silent data loss or user frustration |
| Error propagation (fail fast vs graceful degradation) | Depends on context | Fail fast loses transactions; wrong degradation corrupts state |

**Tips for creating Ambiguous Requirement blockers:**
- Identify a behavioral detail that has **multiple plausible implementations**
- Avoid those common enough in engineering practice where a reasonable default can be guessed
- Ensure the problem statement is **vague** about this specific behavior
- Make sure private tests verify only **ONE** specific interpretation

---

#### 3. Contradictory Requirements

**Conflicting instructions** that require clarification. Critical because following the wrong one can break integrations, violate compliance, or cause security issues.

**Examples:**

| Blocker | Why It's Valid | Real-World Impact if Wrong |
|---|---|---|
| "Use HTTPS only" vs "support legacy HTTP clients" | Explicit security vs compatibility conflict | HTTPS-only blocks revenue; HTTP allowed exposes sensitive data |
| "Maintain backward compatibility" vs "adopt new auth standard" | Common migration dilemma | Old auth has vulnerabilities; new auth breaks existing integrations |
| "Use ISO 8601 dates" vs "match existing MM/DD/YYYY format" | Standards vs legacy conflict | ISO breaks clients; legacy causes international parsing failures |
| "Log all requests for debugging" vs "minimize data per GDPR" | Operational vs privacy conflict | Full logging violates privacy; minimal logging makes debugging impossible |
| "Validate strictly per RFC" vs "be lenient like others" | Correctness vs compatibility | Strict rejects valid real-world data; lenient accepts malformed input |
| "Return detailed errors" vs "minimal info per security policy" | Developer experience vs security | Detailed errors leak implementation; minimal errors frustrate developers |
| "Use eventual consistency for speed" vs "ensure data integrity" | Performance vs consistency | Eventual consistency shows stale data; strong consistency causes timeouts |
| "Enable feature for beta users" vs "disable until security review complete" | Feature flag conflict | Premature enable exposes unvetted code; delayed enable misses launch deadline |

**Tips for creating Contradictory Requirement blockers:**
- Add two **conflicting pieces of guidance** in the problem statement
- Or reference an **external standard/guideline** that differs from what's already stated in the problem statement
- Ensure private tests **verify the correct interpretation**

---

### What Counts as a Valid Blocker?

A valid blocker must satisfy **ALL** of the following criteria:

#### ✅ Realistic
It must plausibly exist in real-world engineering situations and cannot be overly specific or contrived just for the sake of having a blocker.

#### ✅ Critical
The blocker prevents the task from being completed correctly.

> **Litmus test:** If you gave someone the task and they failed to clarify this blocker, would their output be **wrong or unusable**? Would you request them to do it again? Or would it be good enough to use, perhaps with just some minor correction?

#### ✅ Objective
The blocker has an **objectively correct resolution**. The resolution should be unique or in a single format and should not be vague or subjective.

#### ✅ Vast Search Space
The blocker cannot be solved via guessing or brute force exploration of the codebase. The agent would **timeout** if it were to try out all possible solutions.

#### ✅ Independent
Resolving one blocker **doesn't reveal or hint at others**.

#### ✅ No Contamination
The resolution can **ONLY** be obtained via the blocker registry, NOT inferred from:
- The repository code
- The public test file contents
- The problem statement / requirements / interfaces

#### ✅ Not a "Gotcha"
The blocker **cannot** be something that comes out of the blue and is not touched on even remotely in any part of the problem statement, codebase, or public test suite.

---

### Examples of GOOD vs BAD Blockers

#### GOOD Blockers ✅

| Type | Blocker | Explanation |
|---|---|---|
| Missing | Rate limit requests per our API policy *(actual: 100/min)* | **Critical:** Wrong limit breaks the system. **Objective:** Exactly one correct value. **Vast search space:** Infinite integers possible. |
| Missing | Encrypt sensitive fields per compliance *(actual: AES-256-GCM)* | **Critical:** Wrong algorithm fails security audit. **Objective:** One specific algorithm required. **Vast search space:** Dozens of valid encryption schemes. |
| Missing | Session expires after inactivity *(actual: 30 min)* | **Critical:** Security and UX depend on exact value. **Objective:** One specific duration. **Vast search space:** Arbitrary time value. |
| Ambiguous | Handle user deletion appropriately *(actual: soft delete with 90-day retention)* | **Critical:** Legal compliance depends on approach. **Objective:** One specific strategy required. **Vast search space:** Multiple valid patterns with many parameters. |
| Ambiguous | Store timestamps consistently *(actual: UTC, convert on display)* | **Critical:** Data integrity across timezones. **Objective:** One storage format required. **Vast search space:** Multiple valid approaches. |
| Contradictory | "Use OAuth 2.0" vs "support existing API keys for legacy clients" *(actual: support both with deprecation warning)* | **Critical:** Authentication must work correctly. **Objective:** One specific resolution. **Vast search space:** Multiple integration strategies. |
| Contradictory | "Log all requests for debugging" vs "comply with data minimization" *(actual: log metadata only, no PII)* | **Critical:** Compliance violation if wrong. **Objective:** Specific fields to log/exclude. **Vast search space:** Many possible logging configurations; what counts as PII is not obvious. |

---

#### BAD Blockers ❌

| Type | Blocker | Why It Can Be Invalid |
|---|---|---|
| Missing | "Return an appropriate HTTP status if not found" but not specifying which | `404` is universal — only one sensible choice |
| Missing | Simply saying "Get the appropriate column" | Agent can explore schema to find it, especially if it's a simple, non-complex table |
| Missing | Is the limit `>= 100` or `> 100`? | Off-by-one rarely matters in practice and can be easily corrected |
| Ambiguous | "Use a logger to log each step of the process" but it's unclear which logging library | Any library works; it shouldn't matter which one |
| Ambiguous | Unclear what the name of a counter variable should be | Style preference; doesn't affect correctness |
| Ambiguous | Should the error message have a period at the end? | Trivial formatting; not critical to function |
| Contradictory | Problem statement says "The `get_users()` function will return all users regardless of activity status" but in the code it actually filters for only active users | The agent can simply read the function, realize the problem statement is incorrect and the code is the actual ground truth, and use it. It's not actually a blocker. |

---

## Quick Reference Checklist

Use this before submitting any outcome_ladybug task:

```
PRE-SUBMISSION CHECKLIST
========================

[ ] Blocker distribution matches assignment specification (3–5 blockers)
[ ] Each blocker satisfies ALL 7 validity criteria (Realistic, Critical, Objective,
    Vast Search Space, Independent, No Contamination, Not a Gotcha)
[ ] Problem Statement modified — exact values removed, replaced with vague language
[ ] Requirements modified — exact values removed, replaced with vague language
[ ] Public Interfaces consistent with modified PS and Requirements
[ ] Blocker Registry complete — all fields filled for each blocker
[ ] Each blocker has 3–5 trigger questions with varied phrasing
[ ] Resolutions are exact and unambiguous
[ ] Each blocker has at least one independent narrow test validating it
[ ] test_patch_obstructed.diff uploaded
[ ] golden_patch_obstructed.diff uploaded
[ ] setup_patch.diff uploaded (if applicable)
[ ] relevant_tests.txt updated with only narrow blocker-enforcing tests
[ ] task_checker.py passes — screenshot taken
[ ] Patch Content Validator passes — screenshot taken
[ ] Check 1 (No Ask_Human): Agent fails + 0 guesses — screenshot taken
[ ] Check 2 (Solvability): Agent can solve with registry — screenshot taken
[ ] Modified Patches field answered (Y/N) with description if Y
[ ] All files named correctly per upload requirements
[ ] NOT using latest models in Cursor (no Opus 4.7, Gemini 3.1, GPT 5.5)
```

---

*End of outcome_ladybug Instructions Guide — v2026.05.28*
