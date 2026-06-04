Blocker Registry Generator Prompt

Run this prompt in the cursor agent to generate a blocker registry. Ensure to replace placeholders for problem statements, requirements, public interfaces, blocker distribution, test patch and golden patch. Use the originals of each of these.



# Blocker Registry Generator Prompt

## Your Role

Your task is to analyze the provided inputs and generate a `blocker_registry.json` file that contains blockers—ambiguities, contradictions, or missing information that would prevent an AI agent from correctly solving a coding task without asking clarifying questions.

## Guideline: What Counts as a Good Blocker

A valid blocker must satisfy ALL of the following criteria:

- Realistic

It is realistic. It must plausibly exist in real-world engineering situations and cannot be overly specific or contrived just for the sake of having a blocker.

- Critical

The blocker prevents the task from being completed correctly and its resolution is actually a critical implementation that impacts the solution of the request

Non Critical Examples:

Example 1 - Error Type/Error Message:

Resolution Blocker 1: Absolute paths inside the archive must be blocked on both POSIX and Windows path rules, raising AnsibleError with Absolute archive path forbidden: '%s'.

Resolution Blocker 2: Extraction must prevent placing an entry outside the intended collection directory and raise AnsibleError with Cannot extract tar entry '%s' as it will be placed outside the collection directory when that would happen.

Resolution Blocker 3: Directory members must be refused by _extract_tar_file with AnsibleError using Folder item refused: '%s'.



All 3 of these resolutions specify an error to raise plus a specific message. This is not critical because it doesn't really matter what the error message is, the implementation is still the same. Unless the error type actually matters down stream, this is not critical.

Example 2 - Cosmetic Changes:

Blocker Description: The "project conventions" mentioned in the requirements mandate a non-alphabetical order (e.g., responsive before theme variants) which directly conflicts with the "alphabetized" instruction in the problem statement.



Blocker Resolution: Ignore the alphabetical ordering mentioned in the problem statement. Reorder classes so that responsive variants (lg:) PRECEDE dark mode variants (dark:). The correct order is: base utility classes first, then lg: variants, then dark: variants at the end. Example: use 'pattern-size-2 lg:p-6 dark:pattern-bg-black dark:pattern-gray-900' NOT 'pattern-size-2 dark:pattern-bg-black dark:pattern-gray-900 lg:p-6'. This applies to both Rollouts.tsx and Rules.tsx.



Blocker is a cosmetic change where the classes are reordered. It does not actually change anything about the implementation.

Critical Examples:

Blocker Description: The requirements mix three incompatible compatibility goals: one rule reserves run-start marker emission for `always`, another keeps `on_restart` responsible for marker emission in restart-oriented deployments, and another preserves marker emission during initialization for `per_session` workflows. These instructions cannot all be satisfied by one emission policy.



Blocker Resolution: Write the run-start marker line only when run_delimiter_mode is 'always' or 'per_session'. Do NOT write it when the mode is 'on_restart', 'never', or 'disabled'. Treat empty or unset run_delimiter_mode as 'always'. When writing the marker, use exactly {"type":"run_start"} followed by a newline and no extra fields. If writing this marker during sink initialization fails, return that error. Reject unsupported run_delimiter_mode values with an error.



- Objective

The blocker has an objectively correct resolution. The blocker resolution should be unique or in a single format and should not be vague/subjective.



Vast Search Space

The blocker cannot be solved via guessing or brute force exploration of the codebase. The agent would timeout if it were to try out all possible solutions. Do not create blockers that have only 2 or 3 choices for a resolution. This search space is too small.



- Independent

1. Resolving one blocker using the blocker resolution doesn't reveal or hint at resolutions to other blockers.

2. The blocker resolution of one blocker must not contain the resolution fully or partially to another blocker.

3. The resolution to one blocker must not be contradictory to another blocker resolution.



- No Contamination

The resolution can ONLY be obtained via the blocker registry, NOT inferred from:

The repository code

The public test file contents

The problem statement/requirements/interfaces (see definitions in the SWEAP Info document)



- Not a “Gotcha”

The blocker cannot be something that comes out of the blue and not touched on even remotely in any part of the problem statement, code base, or public test suite.

Gotcha example: 

Ambiguous Requirement: 

- On Fedora systems (where 'ansible_distribution' equals 'Fedora'), the default package manager is determined by the major version:

  - If the major version is less than 23 and `/usr/bin/yum` exists, the default must be `yum`.

  - Otherwise, Fedora uses the dnf family of package managers.

  - Fedora 39 and later may report `dnf5` when that is the installed default dnf-family manager.

- On Amazon Linux systems (where 'ansible_distribution' equals 'Amazon'), the default package manager is determined by the major version:

  - If the major version is less than 2022 and `/usr/bin/yum` exists, the default must be `yum`.

  - Otherwise, Amazon Linux uses the dnf family of package managers.

- On other Red Hat family systems (where 'ansible_os_family' equals 'RedHat' but 'ansible_distribution' is neither 'Fedora' nor 'Amazon'), the default package manager is determined by the major version:

  - If the major version is less than 8, the default package manager is `yum`.

  - Otherwise, the default package manager is `dnf`.



Description: The requirements compare ansible_distribution to Fedora/Amazon exact literals but do not specify whether leading or trailing whitespace and letter case should be normalized before comparison.

Resolution: Normalize ansible_distribution before distro checks by trimming surrounding whitespace and applying case-insensitive comparison.



Seems pretty clear that “where 'ansible_distribution' equals 'Fedora'” is the requirement so requiring trimming surrounding whitespace and applying case-insensitive comparison seems to come out of nowhere.





## Blocker/Obstruction Type Definitions:

1. Missing Parameters - Required values that are not specified. These are critical because wrong values can cause security vulnerabilities, data loss, or system failures.

Tips on how to create:

- Identify a numeric parameter, threshold, limit, or special value the implementation needs. Avoid using those that are common enough in engineering practices where a reasonable default can be guessed and used fine

- For example, saying “implement a function that takes in a prompt and queries the LLM, with retries” does not count as a good missing parameter blocker on the number of retries, because for the vast majority of use cases, the vast majority of the time, the number of retries used is 3

- Think of a special, unique, specific use case and a special, unique, specific parameter needed for that use case

- Remove it from the problem statement entirely, or mention it vaguely ("appropriate limit", "per policy")

Examples:

Blocker: “Rate limit the requests to our internal API”

Why it's a missing parameter blocker: Actual rate limit cannot be guessed; infinite possibilities

Blocker: “Enforce our password policy requirements”

Why it's a missing parameter blocker: do not know the relevant parameters of the password policy

Blocker: “Max connection pool size”

Why it's a missing parameter blocker: we do not know what value to set the max connection pool size to

2. Ambiguous Requirements - Underspecified behavior where multiple valid implementations exist. Critical because the wrong choice can have legal, financial, or data integrity consequences.

Tips on how to create:

- Identify a behavioral detail that has multiple plausible implementations. Again, avoid using those that are common enough in engineering practices where a reasonable default can be guessed and used fine

- Ensure the problem statement is vague about this specific behavior

- Make sure private tests verify only ONE specific interpretation

Examples:

Blocker: User deletion (soft delete vs hard delete)

Why it's an ambiguous requirements blocker: Both are valid patterns that can be implemented but none was specified in the requirements

Blocker: Null vs empty string handling

Why it's an ambiguous requirements blocker: Multiple different ways to handle: default value, raise an error, use as-is, etc. but none were specified

Blocker: Error propagation (fail fast vs graceful degradation)

Why it's an ambiguous requirements blocker: if error propagation is needed, it's not known which approach to take.

3. Contradictory Requirements - Conflicting instructions that require clarification. Critical because following the wrong one can break integrations, violate compliance, or cause security issues.

Tips on how to create:

- Add two conflicting pieces of guidance in the problem statement

- Or, reference an external standard/guideline that differs from what's already stated in the problem statement

- Ensure private tests verify the correct interpretation

Examples: 

Blocker: "Use ISO 8601 dates" vs "match existing MM/DD/YYYY format"

Why it's a contradictory requirements blocker: Both constraints exist in the request, so it's not possible to achieve both

Blocker: "Use eventual consistency for speed" vs "ensure data integrity"

Why it's a contradictory requirements blocker: Eventual consistency shows stale data; strong consistency causes timeouts under load

---

## Inputs You Will Receive

1. **problem_statement**: The coding task description (feature request or bug fix)

2. **requirements**: Specific requirements or constraints for the implementation

3. **interfaces**: API interfaces, function signatures, or code structures involved

4. **golden_patch**: The official solution/commit that solves the problem

5. **test_patch**: Unit tests that validate the solution

6. **blocker_distribution**: A text specifying the required number of blockers by type. Format:

   ```

   X missing parameter blockers

   Y ambiguous requirements blocker(s)

   Z contradictory requirements blocker(s)

   ```

---

## Output Format

Generate a JSON file with the following structure:

```json

{

  "blockers": [

    {

      "id": "descriptive_blocker_summary",

      "type": "missing_parameter | ambiguous_requirement | contradictory_requirement",

      "area_of_obstruction": "problem_statement | codebase | both",

      "description": "WHY this is a blocker (without revealing the answer)",

      "resolution": "The EXACT, UNAMBIGUOUS answer with examples",

      "trigger_questions": [

        "Question variation 1?",

        "Question variation 2?",

        "Question variation 3?",

        "Question variation 4?",

        "Question variation 5?"

      ]

    }

  ],

  "distribution_notes": "Any notes about distribution feasibility"

}

```

---

## Field Requirements

### **id**

- Format: A short descriptive summary of the blocker using snake_case (underscores as word separators)

- Must be unique and clearly identify what the blocker is about

- Examples: `no_format_specified`, `missing_connection_timeout`, `ambiguous_return_type`, `conflicting_separator_notation`

### **type**

Must be ONE of:

- `missing_parameter`: A critical value/parameter is not specified

- `ambiguous_requirement`: Behavior can be interpreted multiple valid ways

- `contradictory_requirement`: Two or more pieces of information conflict

### **area_of_obstruction**

- `problem_statement`: Information was removed/made vague in problem statement

- `codebase`: The codebase was modified to introduce ambiguity

- `both`: Both were modified

### **description**

- Explain WHY this is a blocker in AT MOST two sentences

- Reference what's missing, ambiguous, or conflicting

- Frame as a question the agent needs answered

- **DO NOT reveal the resolution, answer, or how the blocker was created**

### **resolution**

**THIS IS THE MOST CRITICAL FIELD**

- Explain how to solve the blocker in AT MOST two sentences

- DO NOT reveal how the blocker was created

Must include:

1. **Exact values** (numbers, strings, characters)

2. **Formatting details** (spaces, case, special characters)

3. **Concrete example** showing expected output

4. **Counter-example** showing what NOT to do (when applicable)

5. **Code syntax** if relevant (e.g., `hostname[:18] + '~'`)

### **trigger_questions**

- Minimum **3 variations**

- Questions must be realistic follow-up questions an assistant might ask if they encounter the blocker

- Use **complete sentences** with proper punctuation

- Vary sentence structure: "What", "How", "Should I", "Which", "Is it"

- Include technical and natural language phrasings

- Reference the specific conflict/ambiguity when possible

---

## Examples

### ✅ GOOD Blocker Example

```json

{

  "id": "conflicting_delegation_separator",

  "type": "contradictory_requirement",

  "area_of_obstruction": "problem_statement",

  "description": "The problem statement mentions both arrow notation (->) and RFC-7231 pipe-via notation for delegation. Which separator should actually be used between primary and delegated hostnames?",

  "resolution": "Use |via| (pipe-via-pipe, NO spaces). Example: 'primary|via|delegated' NOT 'primary -> delegated' or 'primary |via| delegated'",

  "trigger_questions": [

    "Which separator should I use for delegation?",

    "Should I use -> or the RFC notation?",

    "What is the correct delegation separator?",

    "The docs mention two different separators, which one takes precedence?",

    "What format should I use for showing delegation in host labels?"

  ]

}

```

**Why it's good:**

- ✅ Description clearly states the conflict without revealing the answer

- ✅ Resolution is crystal clear: exact characters `|via|`, formatting (NO spaces), example, counter-example

- ✅ 3-5 diverse trigger questions with complete sentences

- ✅ Questions vary in phrasing and reference the conflict

---

### ✅ GOOD Blocker Example (Missing Parameter)

```json

{

  "id": "missing_hostname_truncation_limit",

  "type": "missing_parameter",

  "area_of_obstruction": "problem_statement",

  "description": "The problem statement requires truncating long hostnames for display but does not specify the maximum character limit or the truncation indicator.",

  "resolution": "Keep the first 18 characters, then APPEND a tilde (~). Final length is 19 for truncated names. Example: 'verylonghostname12~' (18 chars kept + tilde). Use hostname[:18] + '~' in code.",

  "trigger_questions": [

    "What is the hostname truncation length?",

    "What is the maximum hostname length for display?",

    "How many characters should be kept before truncation?",

    "What's the display standard for long hostnames?",

    "At what length should hostnames be truncated?"

  ]

}

```

**Why it's good:**

- ✅ Description identifies missing information (limit + indicator) without revealing values

- ✅ Resolution provides exact number (18), exact character (~), final length (19), code syntax

- ✅ Multiple trigger questions covering both aspects (length and indicator)

---

### ❌ BAD Blocker Example

```json

{

  "id": "format_issue",

  "type": "ambiguous_requirement",

  "area_of_obstruction": "problem_statement",

  "description": "There's a problem with the format",

  "resolution": "Use appropriate separator",

  "trigger_questions": [

    "separator",

    "What separator",

    "Tell me the separator",

    "Separator please"

  ]

}

```

**Why it's bad:**

- ❌ ID is too vague ("format_issue") - doesn't clearly summarize the specific blocker

- ❌ Description is too vague ("There's a problem") - doesn't explain WHAT is ambiguous

- ❌ Resolution uses "appropriate" - this is meaningless without exact specification

- ❌ Trigger questions are single words or incomplete sentences

- ❌ No example or counter-example provided

---

### ❌ BAD Blocker Example (Reveals Answer)

```json

{

  "id": "port_thing",

  "type": "missing_parameter",

  "area_of_obstruction": "codebase",

  "description": "The maximum port limit should be 12 but it's not specified in the problem statement",

  "resolution": "12",

  "trigger_questions": [

    "What is the port limit?",

    "How many ports allowed?"

  ]

}

```

**Why it's bad:**

- ❌ ID is too vague ("port_thing") - should be descriptive like `missing_max_port_limit`

- ❌ Description REVEALS the answer ("should be 12") - this defeats the purpose

- ❌ Resolution lacks context - what is "12" referring to? No example.

- ❌ Only 2 trigger questions (minimum is 3)

- ❌ Questions are too short and lack variation

---

## Generation Process

1. **Analyze the golden_patch and test_patch** to identify:

   - For Missing parameters: Specific values used in the implementation

   - For ambiguous/contradictory requirements: well defined implementation behaviours that can be abmiguated or create contradictions. 

2. **Identify potential blockers** by finding:

   - Implementation details in the patch that are NOT specified in the problem statement AND NOT derived or inspired by other files in the codebase

   - Values that an agent could NOT guess without clarification

   - Behaviors that could be interpreted multiple ways

   - Decisions in the problem statement, requirements, or interfaces that can have equally-likely alternatives for the same choice (to use to insert contradictory requirement blockers)

3. **Match blockers to the required distribution**:

   - Prioritize creating blockers that match the `blocker_distribution` requirements

   - If a type cannot be filled, explain why in `distribution_notes`

4. **For each blocker**:

   - Write a clear description that identifies the ambiguity WITHOUT revealing the answer

   - Write an clear resolution with exact values, examples, and/or counter-examples

   - Generate 3-5 diverse trigger questions

---

## Distribution Compliance

You MUST attempt to match the `blocker_distribution` exactly. 

If it's **not possible** to create the required number of a certain type, you must:

1. Create as many valid blockers of that type as possible

2. Document the shortfall in `distribution_notes`

3. Explain WHY the distribution cannot be met 

**Example distribution_notes:**

```json

{

  "distribution_notes": "Requested: 3 missing parameter, 1 ambiguous requirement, 1 contradictory requirement. Achieved: 3 missing parameter, 0 ambiguous requirement, 1 contradictory requirement. The problem statement and codebase are narrow enough in scope that the only design decisions they have are already the most sensible ones. There is no way to introduce ambiguity in implementation details."

}

```

---

## Quality Checklist

Before finalizing, verify each blocker passes:

- [ ] ID is a descriptive summary using snake_case (e.g., `missing_connection_timeout`, not `blocker_1`)

- [ ] Description explains the blocker WITHOUT revealing the resolution

- [ ] Resolution contains EXACT values, not vague terms like "appropriate" or "as needed"

- [ ] Resolution includes at least one concrete EXAMPLE

- [ ] At least 3 trigger questions with complete sentences

- [ ] Trigger questions use varied phrasing

- [ ] The blocker is something an agent genuinely CANNOT guess correctly even after looking through the code, using bash commands such as `grep`, or using prior knowledge of engineering practices

- [ ] The blocker type accurately matches the issue (missing/ambiguous/contradictory)

---

## Now Generate

Given the inputs below, generate the `blocker_registry.json`:

### problem_statement

```

{{PROBLEM_STATEMENT}}

```

### requirements

```

{{REQUIREMENTS}}

```

### interfaces

```

{{INTERFACES}}

```

### golden_patch

```

{{GOLDEN_PATCH}}

```

### test_patch

```

{{TEST_PATCH}}

```

### blocker_distribution

```

{{BLOCKER_DISTRIBUTION}}

```

Example:

```

3 missing parameter blockers

1 ambiguous requirements blocker

1 contradictory requirements blocker

```

---

Generate the complete `blocker_registry.json` following all guidelines above.