Generate Golden Patch And Test Cases

Generate Golden Patch and Test Cases


BEFORE RUNNING PROMPT:
Use this prompt to fully test the implementation of blocker resolutions within your golden patch. The output of this prompt will be test_patch_obstructed.diff and golden_patch_obstructed.diff. which are all the relevant tests needed to check if the agent was able to follow instructions, and the actual solution.



Please apply setup_patch.diff and commit it to the codebase before running this step so that your codebase obstructions are present.



PROMPT:
You are a test case and solution generator agent. Please read the instructions of the problem statement, requirements, public interfaces and blocker resolutions. Also understand the contents of the codebase.





Workflow:

- Implement the solution first within the relevant files. The golden patch should not modify any test files. Ensure that the golden solution addresses all the instructions of the problem statement, requirements, interfaces and blocker resolutions.

- If any portion of the instructions is still ambiguous in terms of implementation details after considering blocker resolutions, then stop execution and output a message: `UNDOCUMENTED BLOCKERS - your instructions contain blockers not documented in the blocker registry` along with the list of ambiguous instructions. Do not assume any implementation details. Any blockers not fully documented should either be documented or be clarified.

- If all instructions are clear, then complete golden solution implementation and create the golden_patch_obstructed.diff file.

- Implement the test cases that fully validate the implementation of the problem statement, requirements, interfaces and blocker resolutions within the solution. Keep a tab of which test cases cover which blocker resolutions. Remember that each test case should fail before the golden_patch is applied and pass after the golden patch is applied. Any passing test before applying the golden patch is an invalid test, same as any test failing after the golden patch is applied.

- After generating relevant tests, create the test_patch_obstructed.diff file.

- Output a list of relevant tests in JSON array format as well that work with the reviewer_task_checker.py script.

- Also output which tests are relevant to which blocker resolution.

- You can run reviewer_task_checker.py to check that all tests fail before applying the golden solution and all tests pass after applying the golden solution.





Inputs:

Problem Statement (with blockers):

{{PROBLEM_STATEMENT_MODIFIED}}





Requirements (with blockers):

{{REQUIREMENTS_MODIFIED}}





Public Interfaces (with blockers):

{{INTERFACES_MODIFIED}}



Blocker Registry:

`name of blocker` description: description 

`name of blocker` resolution: resolution 



`name of blocker` description: description 

`name of blocker` resolution: resolution 



`name of blocker` description: description 

`name of blocker` resolution: resolution 



Task Checker File:

{{reviewer_task_checker.py}}



Outputs:

golden_patch_obstructed.diff

test_patch_obstructed.diff

relevant_tests.txt

tests_to_blockers.txt



Output in Case of undocumented blockers:

`UNDOCUMENTED BLOCKERS - your instructions contain blockers not documented in the blocker registry` 



the list of ambiguous instructions:

ambiguity 1

ambiguity 2

etc



Example outputs:



Example relevant tests:



["src/app/store/_shares/useDefaultShare.test.tsx | useDefaultShare says share is available by default", "src/app/store/_shares/useDefaultShare.test.tsx | useDefaultShare says share is not available if locked", "src/app/store/_shares/useDefaultShare.test.tsx | useDefaultShare says share is not available if soft deleted"]



Example tests to blockers:

`blocker name`: test name 1, test name 2, test name 3, etc.

`blocker name`: test name 1, test name 2, test name 3, etc