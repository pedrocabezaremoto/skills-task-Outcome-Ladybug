# Blocker Registry — Complete Reference Guide

> **Audience:** LLM agents and QA task builders working on the Outlier platform.
> **Purpose:** Full operational reference for creating, reading, and using the Blocker Registry JSON file.
> **Scope:** Structure, field rules, resolution standards, trigger question requirements, flow mechanics, and common mistakes.

---

## What is the Blocker Registry?

The Blocker Registry is a **hidden** JSON registry that acts as the **answer key** for a task. It functions as a smart FAQ system that:

1. Stores all the missing information (blockers) hidden from the agent.
2. Maps agent questions to their resolutions.
3. Powers the `ask_human()` tool that agents use to request clarification.

> **Key Point:** The agent NEVER sees this file — it is completely hidden from the agent at all times.

---

## Structure Breakdown

```json
{
  "blockers": [
    {
      "id": "name_for_blocker_1",
      "type": "contradictory_requirement",
      "description": "WHY this is a blocker",
      "resolution": "The EXACT answer",
      "trigger_questions": [
        "Question variation 1?",
        "Question variation 2?",
        "Question variation 3?",
        "Question variation 4?",
        "Question variation 5+"
      ]
    },
    {
      "id": "name_for_blocker_2",
      "type": "missing_parameter",
      "description": "...",
      "resolution": "...",
      "trigger_questions": ["..."]
    }
  ]
}
```

---

## Field-by-Field Explanation

### 1. `id` (string)

- **Purpose:** Unique name for this blocker.
- **Format:** Must be **lowercase** and **underscored**.
- **Example:**
```json
"id": "encoding_choice"
```

---

### 2. `type` (string)

- **Purpose:** Categorize the blocker type.
- **Valid Values:**

| Value | Meaning |
|---|---|
| `"missing_parameter"` | A required value is not specified. |
| `"ambiguous_requirement"` | Underspecified behavior with multiple valid options. |
| `"contradictory_requirement"` | Conflicting instructions exist in the problem statement. |

- **Example:**
```json
"type": "contradictory_requirement"
```

---

### 3. `description` (string)

- **Purpose:** Explain **WHY** this is a blocker — without revealing the answer.

#### What to INCLUDE:
- What information is missing or unclear.
- Why it creates ambiguity.
- What conflict exists (for `contradictory_requirement` type).

#### What NOT to INCLUDE:
- The actual resolution or answer.
- Specific values or implementation details.
- References to how the blocker was created (e.g., "I removed a parameter from…").

#### ✅ Good Examples:
```json
"description": "The problem statement mentions both arrow notation (->) and RFC-7231 pipe-via notation. Which separator should actually be used between primary and delegated hostnames?"
```
```json
"description": "It is unclear what is the maximum number of ports allowed in destination_ports per the organization's security policy."
```
```json
"description": "How should port ranges be counted toward the limit - each range entry as 1, or expanded (e.g., does '80:90' count as 1 or 11?)"
```

#### ❌ Bad Examples:
```json
// Reveals the answer
"description": "The separator should be |via| not ->"

// Too vague
"description": "There's a problem with the format"

// Self-referential (references the blocker creation process)
"description": "The specific error type was removed from the problem statement"
```

---

### 4. `resolution` (string)

- **Purpose:** Provide the **EXACT, UNAMBIGUOUS** answer to the blocker.

> ⚠️ **THIS IS THE MOST CRITICAL FIELD.** A vague or incomplete resolution will cause the agent to fail or produce incorrect output.

#### Resolution Requirements — Must Include:
1. Exact values (numbers, strings, characters).
2. Formatting details (spaces, case, special characters).
3. A concrete example showing the expected output.
4. Edge cases or exceptions (if applicable).

#### ✅ Good Resolutions:

```json
"resolution": "Use |via| (pipe-via-pipe, NO spaces). Example: 'primary|via|delegated' NOT 'primary -> delegated'"
```
**Why this is good:**
- Exact characters: `|via|`
- Formatting rule: NO spaces
- Positive example: `primary|via|delegated`
- Counter-example: NOT `primary -> delegated`

---

```json
"resolution": "Use exactly [UNRESOLVED] (with square brackets, uppercase). Example: 'primary|via|[UNRESOLVED]'"
```
**Why this is good:**
- Exact string: `[UNRESOLVED]`
- Formatting: square brackets, uppercase
- Example shown in context.

---

```json
"resolution": "12"
```
**Why this is good (for simple numeric values):**
- Exact number.
- Completely unambiguous.

---

```json
"resolution": "Each list element counts as 1 regardless of ranges (e.g., '80:90' = 1, not 11). So ['80', '443', '8080:8090'] counts as 3 ports toward the limit."
```
**Why this is good:**
- Clear rule stated upfront.
- Multiple examples provided.
- Counter-example included (not 11).
- Complete example showing the full calculation.

#### ❌ Bad Resolutions:

```json
// Too vague — no format detail
"resolution": "Use a placeholder for unresolved hosts"

// Missing format detail — which pipe? spaces?
"resolution": "Use the pipe separator"

// Ambiguous — "appropriately" is not a rule
"resolution": "Truncate long names appropriately"

// No example — what error? what format?
"resolution": "Return an error for invalid values"

// Self-referential — references the editing process
"resolution": "Raise a ValueError. This solves the problem statement edit"
```

---

### 5. `trigger_questions` (array of strings)

- **Purpose:** List the various ways an agent might ask about this blocker.

#### Requirements:
- Write **3–5 variations minimum**.
- Use **complete sentences** with proper grammar and punctuation.
- **Vary** sentence structure and phrasing.
- Cover both **direct** and **indirect** ways of asking.
- Include both **technical** and **natural language** phrasings.
- Each question must be **self-contained** — readable as a standalone question in response to the problem statement.
- Questions must **NOT be self-referential** to the blocker mechanism or editing process.

#### ✅ Good Trigger Questions:
```json
"trigger_questions": [
  "Which separator should I use for delegation?",
  "Should I use -> or the RFC notation?",
  "What is the correct delegation separator?",
  "The docs mention two different separators, which one?",
  "What format for showing delegation in host labels?"
]
```
**Why this is good:**
- 5 distinct variations.
- Complete sentences throughout.
- Different phrasings: direct, indirect, and technical.
- References the conflict ("two different separators").

#### ❌ Bad Trigger Questions:
```json
"trigger_questions": [
  "separator",                         // Single word — not a sentence
  "What separator",                    // Incomplete sentence
  "Tell me the separator",             // Repetitive phrasing
  "Tell me separator",                 // Same idea repeated
  "Separator please",                  // Same idea repeated
  "Which one should I use",            // Vague pronoun — not self-contained
  "Why was the problem statement edited so that the separator is unclear?" // Self-referential
]
```

---

## How the Blocker Registry Works — The Flow

```
1. Agent calls ask_human("Which separator should I use?")
         │
         ▼
2. System evaluates the question against ALL unresolved blockers
         │
         ▼
3. System checks trigger_questions for a semantic match
         │
         ├── Match found       → Returns the resolution from that blocker
         ├── No match found    → Returns "irrelevant question"
         └── Already resolved  → Returns the resolution from that blocker again
```

---

## Complete Real Example

**Task:** QH2 — Ansible Callback Host Label

```json
{
  "blockers": [
    {
      "id": "separator_notation",
      "type": "contradictory_requirement",
      "description": "The problem statement mentions both arrow notation (->) and RFC-7231 pipe-via notation. Which separator should actually be used between primary and delegated hostnames?",
      "resolution": "Use |via| (pipe-via-pipe, NO spaces). Example: 'primary|via|delegated' NOT 'primary |via| delegated'",
      "trigger_questions": [
        "Which separator should I use for delegation?",
        "Should I use -> or the RFC notation?",
        "What is the correct delegation separator?",
        "The docs mention two different separators, which one should I use?",
        "What is the right format for showing delegation in host labels?"
      ]
    },
    {
      "id": "template_rendering_string",
      "type": "missing_parameter",
      "description": "What string should be used when _ansible_delegated_vars exists but ansible_host is missing or empty (template rendering failure case)?",
      "resolution": "Use exactly [UNRESOLVED] (with square brackets, uppercase). Example: 'primary|via|[UNRESOLVED]'",
      "trigger_questions": [
        "What to use when ansible_host is missing?",
        "What is the correct fallback for empty delegated host?",
        "How to handle missing ansible_host in delegated_vars?",
        "What string should I use for unresolved delegation?",
        "What to display for failed template delegation?"
      ]
    },
    {
      "id": "maximum_hostname_length",
      "type": "ambiguous_requirement",
      "description": "What is the maximum hostname length for the display standards?",
      "resolution": "Keep the first 18 characters, then APPEND a tilde (~). Final length is 19 for truncated names. Example: 'verylonghostname12~' (18 chars kept + tilde). Use hostname[:18] + '~' in code.",
      "trigger_questions": [
        "What is the hostname truncation length?",
        "What is the maximum hostname length for display?",
        "How many characters do I keep in the hostname before truncation?",
        "What's the display standard for long hostnames?",
        "At what length should hostnames be truncated?"
      ]
    }
  ]
}
```

---

## Best Practices

### For `description`:
1. Frame it as a question the agent needs answered.
2. Reference the ambiguity or conflict present in the problem statement.
3. Be specific about what is unclear.
4. Do **not** reveal the answer.

### For `resolution`:
1. Be **obsessively specific** — imagine explaining to someone who will interpret you literally.
2. Include exact values with proper formatting (spaces, case, special characters).
3. Provide **concrete examples** showing correct usage.
4. Add **counter-examples** showing what NOT to do.
5. For code, include exact syntax (e.g., `hostname[:18] + '~'`).
6. **Never** use vague phrases like "appropriately" or "as needed".

### For `trigger_questions`:
1. Write **3–5 variations minimum**.
2. Think like an agent: technical, direct, exploratory questions.
3. Include questions that reference the conflict or ambiguity.
4. Use complete sentences with proper punctuation.
5. Vary between `"What"`, `"How"`, `"Should I"`, `"Which"`, `"Is it"` formats.
6. Do not repeat the same question with only minor word changes.

---

## Common Mistakes — Quick Reference

| Mistake | Bad Example | Correct Fix |
|---|---|---|
| Vague resolution | `"Use appropriate separator"` | `"Use \|via\| (pipe-via-pipe, NO spaces)"` |
| Missing format details | `"Use the pipe separator"` | Specify exact characters, spacing, and casing. |
| Ambiguous resolution | `"Truncate long names appropriately"` | `"Keep first 18 chars, append '~'. Use hostname[:18] + '~'"` |
| No example in resolution | `"Return an error for invalid values"` | Include the exact error type, format, and a code example. |
| Self-referential resolution | `"Raise a ValueError. This solves the problem statement edit"` | Remove all references to the editing process. |
| Incomplete trigger question | `"What separator"` | `"What separator should I use between primary and delegated hosts?"` |
| Single-word trigger | `"separator"` | Write a full, self-contained sentence. |
| Vague pronoun in trigger | `"Which one should I use"` | `"Which separator format is correct for host delegation?"` |
| Self-referential trigger | `"Why was the problem statement edited?"` | Ask about the ambiguity itself, not how it was introduced. |

---

*End of Blocker Registry Reference Guide.*
