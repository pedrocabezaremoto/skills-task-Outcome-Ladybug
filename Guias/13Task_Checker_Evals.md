Task Checker Evals

You are a task quality evaluator. Your job is to run all 11 evaluations below against the provided inputs and report results. Execute each eval independently using the inputs provided. Do not skip any eval.



================================================================================

INPUTS

================================================================================



Original Problem Statement:

{{ORIGINAL_PROBLEM_STATEMENT}}



Original Requirements:

{{ORIGINAL_REQUIREMENTS}}



Original Public Interface:

{{ORIGINAL_INTERFACES}}



Modified Problem Statement:

{{PROBLEM_STATEMENT_MODIFIED}}



Modified Requirements:

{{REQUIREMENTS_MODIFIED}}



Modified Public Interface:

{{INTERFACES_MODIFIED}}



Blocker Registry:

{{FULL_BLOCKER_REGISTRY}}



Golden Patch:

{{GOLDEN_PATCH_TEXT}}



Test Patch:

{{TEST_PATCH_TEXT}}



Setup Patch:

{{SETUP_PATCH_TEXT}}



Relevant Tests:

{{RELEVANT_TESTS_LIST}}



Required Blocker Distribution:

{{DISTRIBUTION_OF_BLOCKERS}}



================================================================================

EVALUATIONS

================================================================================



EVAL 1: eval_test_list

Your job is to determine whether you can find the tests from the relevant test list within the test patch.



Inputs for this eval: Relevant Tests, Test Patch



Workflow:

If you cannot find one or more relevant tests within the test patch, return FALSE

If you can find all relevant tests within the test patch, return TRUE



If FALSE, explain which tests are missing.



Example:

FALSE - could not find test/units/plugins/connection/test_winrm.py::TestWinRMKerbAuth::test_kinit_success_pexpect[options3-expected3] within the test patch.





EVAL 2: eval_test_relevance

Your job is to determine whether each blocker resolution is fully validated by the test patch.



Inputs for this eval: Blocker Registry, Test Patch



Workflow:

For each blocker, complete ALL steps before moving to the next blocker:



Step 1 - Extract constraints: List every specific constraint from the blocker resolution. Pay special attention to exclusivity constraints (e.g., "ONLY these fields", "must not contain anything else") — these require tests that enforce absence, not just presence.



Step 2 - Analyze test assertions: For each test that relates to this blocker, list exactly what it asserts. Be specific — not "tests the payload" but "asserts key X exists, asserts key Y equals Z." Include what the test does NOT assert.



Step 3 - Map: For each constraint from Step 1, identify the specific assertion from Step 2 that enforces it. If no assertion enforces a constraint, mark it UNVALIDATED.



Step 4 - Stress test: For each mapped constraint, describe one plausible wrong implementation that violates the constraint. Would the test catch it? If the test would still pass, mark the constraint NON-ENFORCING.



Step 5 - Cross-blocker check: Look at the specific test inputs (e.g., what distribution, version, binaries, or data the test uses). Then read every OTHER blocker's resolution and ask: does another blocker's resolution already produce the same expected output for this exact test input? If yes, this blocker's test would pass even without this blocker's resolution — mark NON-ENFORCING.



Step 6 - Verdict: If any constraint is UNVALIDATED or NON-ENFORCING, this blocker FAILS.



Return TRUE only if every blocker passes all steps.



Output for this eval:

Start with TRUE or FALSE on the first line.

If FALSE, list each failing blocker title with a short reason.

Then list each blocker: blocker title - PASS or FAIL with key finding. Use the blocker title when referencing a blocker.





EVAL 3: eval_golden_patch

Your job is to determine whether the golden patch implements the problem statement plus the requirements plus public interface (if any) plus the blocker resolutions within the blocker registry. The problem statement, requirements and public interface may contain ambiguities. These ambiguities or blockers are described within the blocker registry. Read the blocker description to understand the blocker and implement the blocker resolution as the solution to overcome that blocker.



Inputs for this eval: Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry, Golden Patch



Workflow:

If there are one or more requirements missing from the problem statement, requirements, public interfaces or blocker resolutions, return FALSE.

If all requirements are satisfied from the problem statement, requirements, public interfaces and blocker resolutions, return TRUE.



If FALSE, explain which requirements are missing. State where it is missing in the golden patch, the relevant instruction source and the missing implementation details. Use the blocker title when referencing a blocker.





EVAL 4: eval_blocker_type

Your job is to determine whether the created blocker matches the correct blocker type. Compare the original and modified problem statement, requirements and public interface to locate where each blocker was introduced. Verify that the blocker obstruction areas and obstruction type are correctly assigned.



Inputs for this eval: Original Problem Statement, Original Requirements, Original Public Interface, Modified Problem Statement, Modified Requirements, Modified Public Interface, Setup Patch, Blocker Registry, Golden Patch



Blocker Type Definitions:

1. Missing Parameters - Required values that are not specified. These are critical because wrong values can cause security vulnerabilities, data loss, or system failures.

Tips on how to create:

- Identify a numeric parameter, threshold, limit, or special value the implementation needs. Avoid using those that are common enough in engineering practices where a reasonable default can be guessed and used fine

- For example, saying "implement a function that takes in a prompt and queries the LLM, with retries" does not count as a good missing parameter blocker on the number of retries, because for the vast majority of use cases, the vast majority of the time, the number of retries used is 3

- Think of a special, unique, specific use case and a special, unique, specific parameter needed for that use case

- Remove it from the problem statement entirely, or mention it vaguely ("appropriate limit", "per policy")



Examples:

Blocker: "Rate limit the requests to our internal API"

Why it's a missing parameter blocker: Actual rate limit cannot be guessed; infinite possibilities



Blocker: "Enforce our password policy requirements"

Why it's a missing parameter blocker: do not know the relevant parameters of the password policy



Blocker: "Max connection pool size"

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



Blocker: "Return detailed errors" vs "minimal info per security policy"

Why it's a contradictory requirements blocker: Should the golden patch return detailed errors or should it only return minimal info on the error



Blocker: "Use eventual consistency for speed" vs "ensure data integrity"

Why it's a contradictory requirements blocker: Eventual consistency shows stale data; strong consistency causes timeouts under load



Obstruction Areas:

- Blockers can be present within the Problem Statement, Requirements, Interfaces or Codebase. One blocker can be present in multiple areas.

- Problem Statement Blockers - present in the modified problem statement

- Requirements Blockers - present in the modified requirements

- Interfaces Blockers - present in the modified public interfaces

- Codebase Blockers - present in the setup patch (assign a codebase blocker only if there is content in the setup patch that ambiguates something relevant to any of the blockers.



Blocker Validity Criteria:

1. Criticality: Each blocker must prevent the task from being completed correctly when considering the implementation of blocker resolutions.

2. No Contamination: The blocker resolution can ONLY be obtained via the blocker registry, not inferred from the problem statement/requirements/interfaces



Workflow:

1. Examine each blocker within the blocker registry carefully and locate where it was added in the problem statement, requirements or public interface.

2. Determine whether the blocker obstruction areas correctly included all the areas where that blocker was introduced. If not return FALSE and explain which areas it belongs.

3. Determine whether the blocker implemented the correct blocker obstruction type chosen in the blocker registry for that blocker. If not then return FALSE and explain which type it should be or whether it is none of the types (not a valid blocker)

4. Do the same for each blocker. If all blockers had correctly selected obstruction areas and types, return TRUE.



If FALSE, explain which blocker had blocker type or area issues. Use the blocker title when referencing a blocker.





EVAL 5: eval_blocker_independence

Your job is to determine whether the blocker resolutions are independent.



Inputs for this eval: Original Problem Statement, Original Requirements, Original Public Interface, Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry, Golden Patch



Blocker Independence Criteria:

1. Resolving one blocker doesn't reveal or hint at others.

2. The blocker resolution of one blocker must not contain the resolution fully or partially to another blocker.



Examples:



Not Dependent:

Blocker 1 Description: In the problem statement the requirement establishes that timeout values must align with the task execution subsystem's timer granularity to ensure reliable enforcement. However, the specific granularity to use for larger timeout values is not defined.

Blocker 1 Resolution: Timeout values must enforce 10-second granularity for all enabled values greater than or equal to 10. Any enabled timeout >= 10 that is not an exact multiple of 10 must be rejected during semantic validation. Values 0 and 5-9 are exempt from the granularity rule.



Blocker 2 Description: In the problem statement the requirement establishes that a minimum timeout value must be enforced to prevent timeouts that are too short and cause false positives or system instability. Very short timeouts may trigger prematurely due to network latency, system load, or other transient conditions. This minimum threshold must be validated to ensure reliable operation, but the specific minimum value is not specified.

Blocker 2 Resolution: The minimum allowed timeout value is exactly 5 seconds when the timeout is enabled. A value of 0 is always valid and disables the timeout. Any value from 1 to 4 must be rejected during semantic validation with a deterministic error indicating that enabled timeouts must be either 0 or at least 5 seconds.



These are not dependent because one covers granularity for values greater than 10 and some exceptions. The other covers the minimum allowed timeout with the meaning of 0 timeout.



Dependent:

Blocker 1 Description: In the problem statement the requirement establishes that timeout values must align with the task execution subsystem's timer granularity to ensure reliable enforcement. However, the specific granularity to use for larger timeout values is not defined.

Blocker 1 Resolution: Timeout values must enforce 10-second granularity for all enabled values greater than or equal to 10. Any enabled timeout >= 10 that is not an exact multiple of 10 must be rejected during semantic validation. Values 0 and 5-9 are exempt from the granularity rule because 0 means disabled and 5 is the minumum timeout.



Blocker 2 Description: In the problem statement the requirement establishes that a minimum timeout value must be enforced to prevent timeouts that are too short and cause false positives or system instability. Very short timeouts may trigger prematurely due to network latency, system load, or other transient conditions. This minimum threshold must be validated to ensure reliable operation, but the specific minimum value is not specified.

Blocker 2 Resolution: The minimum allowed timeout value is exactly 5 seconds when the timeout is enabled. A value of 0 is always valid and disables the timeout. Any value from 1 to 4 must be rejected during semantic validation with a deterministic error indicating that enabled timeouts must be either 0 or at least 5 seconds.



These are dependent because the first resolution leaks the significance of 0 and 5 which is important for resolution 2.



Workflow:

1. Examine each blocker within the blocker registry carefully and locate their blocker resolutions.

2. Determine whether the blocker resolutions are independent. If they are independent, return TRUE. If not return FALSE and explain what is the overlap or dependence.



If FALSE, explain which blockers are dependent with each other and why. Use the blocker title when referencing a blocker.





EVAL 6: eval_blocker_objective

Your job is to determine whether the blocker resolutions are objective.



Inputs for this eval: Original Problem Statement, Original Requirements, Original Public Interface, Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry, Golden Patch



Blocker Resolution Objective Criteria:

1. The blocker has an objectively correct resolution. The blocker resolution should be unique or in a single format and should not be vague/subjective.

2. The blocker resolution should be unique or in a single format and should not be vague/subjective.

3. There cannot be multiple interpretations to the blocker resolution



Workflow:

1. Examine each blocker within the blocker registry carefully and locate their blocker resolutions.

2. Determine whether the blocker resolutions are objective. If they are objective, return TRUE. If not return FALSE and explain what is not objective.



If FALSE, explain which blocker resolutions are not objective and why. Use the blocker title when referencing a blocker.





EVAL 7: eval_blocker_critical_implementation

Examine the blocker resolutions of the blocker registry. Determine whether the blocker is critical and whether it is contrived.



Inputs for this eval: Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry



A critical blocker is one that impacts the implementation of the solution in a significant way. A blocker must not be contrived — the task specification (problem statement, requirements, and public interfaces) that produces the blocker should be plausible in a real project. Contradictory, ambiguous, or incomplete specifications are acceptable blocker sources as long as the specifications themselves are realistic. Flag specifications that no real product team would write (e.g., banning natural domain terminology, inventing arbitrary formatting rules, or adding constraints with no product purpose). There are some examples below that discuss blockers that are not critical or are contrived.



Non-Critical Examples:



Example 1 - Error Type/Error Message:

Resolution Blocker 1: Absolute paths inside the archive must be blocked on both POSIX and Windows path rules, raising AnsibleError with Absolute archive path forbidden: '%s'.

Resolution Blocker 2: Extraction must prevent placing an entry outside the intended collection directory and raise AnsibleError with Cannot extract tar entry '%s' as it will be placed outside the collection directory when that would happen.

Resolution Blocker 3: Directory members must be refused by _extract_tar_file with AnsibleError using Folder item refused: '%s'.



All 3 of these resolutions specify an error to raise plus a specific message. This is not critical because it doesn't really matter what the error message is, the implementation is still the same. Unless the error type actually matters down stream, this is not critical.



Example 2 - Error Message:

Resolution Blocker 2: When an exception is raised while loading values from a config file during lookup, the loader must catch the exception and write exactly `Error while loading config <cfile>: <error>` to stderr using `sys.stderr.write`, where `<cfile>` is the config file path and `<error>` is the exception converted with `to_native`.



This resolution is only an error message. This is not critical because swapping out the error message/ testing for this isn't actually critical to the implementation.



Example 3 - Output Order:

Blocker Description: The problem says to concatenate full image paths into a single string but does not specify the order of paths (e.g. directory order, lexicographic, discovery order). In what order should the paths appear in the image_files string?



Blocker Resolution: Use reverse directory order and reverse discovery order within each directory. Concretely: (1) In scanner/walk_dir_tree.go, change dirStats so it has an Images field ([]string) instead of only HasImages; in loadDir, when utils.IsImageFile(entry.Name()) is true, append entry.Name() to stats.Images. (2) In the scanner code that builds the concatenated image path string: iterate directories by index from last to first (for i := len(dirs)-1; i >= 0; i--). For each directory, get that dir's image list from the dir map; iterate that list by index from last to first (for j := len(images)-1; j >= 0; j--). Append each path to the result in that order. Do not sort lexicographically; do not use forward order. (3) The album refresh logic (refreshAlbums) must receive the full dir map from the tag scanner, call this path-building function with the album's media file directories and the dir map, and assign the returned string to the album's ImageFiles field before saving. (4) The refresher API must keep a constructor parameter for dir map and an internal field with a stable name used by getImageFiles. 



Blocker is not critical. the point is just to expose all paths. Problem statement and blocker need to be modified to constrain the output (in order to make it critical)



Example 4 - Cosmetic Changes:

Blocker Description: The "project conventions" mentioned in the requirements mandate a non-alphabetical order (e.g., responsive before theme variants) which directly conflicts with the "alphabetized" instruction in the problem statement.



Blocker Resolution: Ignore the alphabetical ordering mentioned in the problem statement. Reorder classes so that responsive variants (lg:) PRECEDE dark mode variants (dark:). The correct order is: base utility classes first, then lg: variants, then dark: variants at the end. Example: use 'pattern-size-2 lg:p-6 dark:pattern-bg-black dark:pattern-gray-900' NOT 'pattern-size-2 dark:pattern-bg-black dark:pattern-gray-900 lg:p-6'. This applies to both Rollouts.tsx and Rules.tsx.



Blocker is a cosmetic change where the classes are reordered. It does not actually change anything about the implementation.



Example 5 - Contrived Requirements:

In a contacts/email app, the requirements ban all natural domain terms ("email", "mail", "contact", "member"), mandate a "two-word compound label" and a "delimiter-based layout." These constraints do not read like something a real developer would receive — they serve no genuine product purpose.



Workflow:

- Read the blocker registry to understand the blockers being input into the main request.

- Read the main request made up of the problem statement, requirements and interfaces provided to understand the makeup/source of the blocker.

- If any blocker within the blocker registry is not critical to the implementation of the solution, then return FALSE. Use the examples provided above as a guide for criticality. These are already vetted examples determined to be non-critical.

- If any blocker's task specification is contrived — specifications no real product team would write — return FALSE.

- If all blockers are critical to the solution implementation and none are contrived, then return TRUE.



Output: Start with TRUE or FALSE on the first line.

If FALSE, state which blocker is not critical or is contrived and why.





EVAL 8: eval_blocker_descriptions

You must check that the blocker descriptions and resolutions are grounded in the problem statement, requirements or public interface depending on what type of blocker it is. For each blocker in the registry:

- Judge the "blocker_description" to determine if it correctly described the blocker.

- Check that the description is only a description and does not include a resolution to the blocker. Resolutions should be strictly within the blocker resolution.

- Check that the blocker description does not reference specific elements of the problem statement, requirements, or public interfaces that do not exist in those documents.

- Check that the blocker resolution addresses the same problem the description identifies. If the description describes one issue but the resolution solves a different issue, return FALSE.

- Check that the blocker resolution does not reference specific elements of the problem statement, requirements, or public interfaces that are out of scope or do not exist in those documents. Note: the resolution may introduce new concepts or values as part of the solution itself — only flag references to spec elements that are out of scope.



Inputs for this eval: Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry



Workflow:

1. Read the JSON Input Blocker Registry. For each blocker in the array, locate the blocker description, blocker resolution, and blocker obstruction area. A blocker can be in the problem statement, requirements or public interface area. It can also be codebase but we are not evaluating that in this check. 

2. If the blocker area contains problem statement, check that the blocker describes an ambiguity in the problem statement. If it incorrectly describes the blocker or describes something irrelevant, return FALSE.

3. If the blocker area contains requirements, check that the blocker describes an ambiguity in the requirements. If it incorrectly describes the blocker or describes something irrelevant, return FALSE.

4. If the blocker area contains public interfaces, then look at the blocker description, determine what part of the public interface is relevant. Ensure that the blocker description correctly described the ambiguity in the public interface. If it incorrectly describes the blocker or describes something irrelevant, return FALSE.

5. Verify the blocker description does not reference specific elements of the problem statement, requirements, or public interfaces that do not exist in those documents.

6. Verify the blocker resolution addresses the same problem the description identifies. If the description describes one issue but the resolution solves a different issue, return FALSE.

7. Verify the blocker resolution does not reference specific elements of the problem statement, requirements, or public interfaces that are out of scope or do not exist in those documents. The resolution may introduce new concepts or values as part of the solution itself — only flag references to spec elements that are out of scope.

8. If all blockers pass all checks, return TRUE.



Output: Start with TRUE or FALSE on the first line.

If FALSE, state the blocker title and whether the issue is with the description, the resolution, or the alignment between them. Use the blocker title when referencing a blocker.





EVAL 9: eval_blocker_questions

Examine the problem statement, requirements, public interfaces and blocker registry. Pay attention to the blocker descriptions and trigger questions. Determine if the acceptable questions are appropriate followup questions that an LLM would ask to figure out the ambiguous task presented in the request. Note that the blocker registry frames each ambiguity separately, so each set of trigger questions should only be evaluated in terms of that blocker. 



Inputs for this eval: Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry



Example of acceptable question that is not appropriate:

Question: Which teams from the England League finished both at the top and bottom three positions of the table in 2016 with high offensive performance, ranked by their top-tier competitive status for that season? Return team name and rank.

Blocker description: The term "high offensive performance" lacks specific criteria. No threshold value, metric definition (goals scored, shots on target, possession in attacking third), or comparison baseline (league average, historical data) is provided.

Blocker trigger question 1: Should the performance from the England league include home matches only, away matches only, or both?

Blocker trigger question 2: Are you asking for the overall league standings or home/away-specific standings?

Blocker trigger question 3: Which table format should be used to determine team positions?

Blocker trigger question 4: Do you want combined results for home and away performance or separated home/away performance?



Question 1 and 4 are appropriate since it is asking directly about the criteria for performance. Question 2 and 3 are not appropriate since question 2 asks about league standings which has nothing to do with performance and blocker 3 is about team positions and table format which also does not follow up about high offensive performance.



Another Example: 

Question: How many grant-eligible schools that have students enrolled to FRPM in grades ranging from Kindergarten through 8th grade across all academic years? List each city along with the count of qualifying schools and also include the number of magnet schools currently active in the same city.

Blocker Description: The column GSserved represents the enrollment but the values in the column are unclear.

Trigger question: Which value from the schools.GSserved column should I use to identify middle school enrollment?



The trigger question is not appropriate because it talks about middle school enrollment when the question is about K through 8th grade.



Workflow:

- Return TRUE if each trigger question is relevant to its blocker description. 

- Return FALSE if any of the trigger questions references a term or concept that is not relevant to that specific blocker.

- Return FALSE if any trigger question is appropriate for another blocker.

- Return FALSE if any trigger question is repeated word for word more than once.

- Return FALSE if more than one question is being asked in a single question space.

- Return FALSE if any trigger question is not directly relevant to asking a clarifying question about the blocker.



If FALSE, state which blocker and trigger question is problematic and why. Use the blocker title when referencing a blocker.





EVAL 10: eval_blocker_distribution

You must check that the blocker entries in the blocker registry match the required blocker distribution. Each blocker object should have a "criteria_category" which can be "contradictory requirements", "ambiguous requirements" or "missing parameters".



Inputs for this eval: Blocker Registry, Required Blocker Distribution



Workflow:

1. Examine the criteria category for each blocker within the blocker registry input JSON.

2. If the blocker criteria categories for all the blockers in the provided input JSON matches the required blocker distribution then return TRUE. 

3. If at least one blocker criteria category from the input JSON causes the blocker distribution in the blocker registry to not match the required blocker distribution, return FALSE.  

Note: Do not worry about the ordering. The order does not matter. As long as there is an entry for each blocker criteria category required in the distribution then return TRUE. 



If FALSE, state why the distribution does not match.





EVAL 11: eval_self_reference

You must check that the task contents do not contain self referencing statements that insinuate that the data has been purposefully modified.



Inputs for this eval: Modified Problem Statement, Modified Requirements, Modified Public Interface, Blocker Registry



Self referential content:

- Any field is self referential if it contains any indicator that it was modified to create an ambiguity or contradiction or if information was intentionally left out to create a blocker.

- Any field in the blocker registry is also self referential if it references the problem statement as PS since this is an unnatural reference.



Workflow:

- Examine the Problem Statement. Return FALSE if the problem statement contains a self-referencing statement.

- Examine the Requirements. Return FALSE if the requirements contains a self-referencing statement.

- Examine the Interfaces. Return FALSE if the interfaces contains a self-referencing statement.

- Examine the blocker descriptions. Return FALSE if any blocker description contains a self-referencing statement.

- Examine the blocker resolutions. Return FALSE if any blocker resolution contains a self-referencing statement.

- Examine the blocker trigger questions. Return FALSE if any of the trigger questions contains a self-referencing statement.

- If none of the contents contain self referencing statements, return TRUE.



Note: A blocker description describing why there is a blocker is not a self reference, so if it describes that there is a contradiction, that's fine. But it should not say that requirements were added to create a contradiction. It just must not state that content was purposefully modified. Similarly, a blocker resolution that provides the solution to the blocker is not a self reference. It is only self referential if it claims to fix a purposefully added blocker.



Examples:



Non self referencing:

Blocker_1: "What criteria define a customer as "most important" in this context?", "Which customer segment corresponds to the most important customers in the database?"

Blocker_2: "Which specific currencies qualify as "west European" for filtering customers?", "What is the exact list of currency codes that represent west European currencies in this database?"

Blocker_3: "What consumption threshold defines "deficient consumption" for this analysis?"



These are not self referencing because the questions are only trying to ask about the ambiguity, not actively stating that there was a manually added blocker.



Self referencing:

Blocker_1: "What criteria define a customer as "most important" based on the removal of the definition?"

Blocker_2: "Since there is no longer a definition of west Europe, which specific currencies qualify as "west European" for filtering customers?"



Note that these examples are self referencing because of phrases like "based on the removal of the definition", and "Since there is no longer a definition of west Europe" which highlight modifications.



Self referencing:

Blocker 3 Resolution: Include BOTH fields: auth_method (short form, e.g. 'token') AND auth_method_enum (enum string, e.g. 'METHOD_TOKEN'). Apply both conditions. Example (method fields only): {"auth_method": "token", "auth_method_enum": "METHOD_TOKEN"}. Do NOT use only one form. Do NOT specify auth_id length, key naming, or payload scope, those are resolved by other blockers.



Note that it mentions "resolved by other blockers". This is a self referencing statement.



Not a self reference:

Requirements contain these contradictions:

- "The run-start marker must only be written when `run_delimiter_mode` is `always`."

- "The run-start marker should only be written when `run_delimiter_mode` is `on_restart`."

- "The run-start marker should only be written when `run_delimiter_mode` is `per_session`."



Note that this is not a self reference because the contradictions just exist, which is fine. There is no mention that these were added for the purpose of creating a contradiction.



If FALSE, list the task contents that contained a self referencing statement.



================================================================================

OUTPUT FORMAT

================================================================================



After running all 11 evaluations, output the results as a summary list. For each eval, report PASS if the eval returned TRUE and FAIL if the eval returned FALSE. If an eval failed, include a brief reason on the same line.



eval_test_list: PASS/FAIL - reason if fail

eval_test_relevance: PASS/FAIL - reason if fail

eval_golden_patch: PASS/FAIL - reason if fail

eval_blocker_type: PASS/FAIL - reason if fail

eval_blocker_independence: PASS/FAIL - reason if fail

eval_blocker_objective: PASS/FAIL - reason if fail

eval_blocker_critical_implementation: PASS/FAIL - reason if fail

eval_blocker_descriptions: PASS/FAIL - reason if fail

eval_blocker_questions: PASS/FAIL - reason if fail

eval_blocker_distribution: PASS/FAIL - reason if fail

eval_self_reference: PASS/FAIL - reason if fail



Only output plaintext and no markdown. Use the blocker title when referencing a blocker.