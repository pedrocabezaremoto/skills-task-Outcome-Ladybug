Attempter Check 1

UPDATE: Removed setup patch from this process to get rid of some contamination. We are applying and removing the setup patch before using this prompt.



Before running this check:
Do not upload the test patch or golden patch. This will leak the resolutions to the agent.
Ensure you are working with an untampered version of the codebase. No patches applied at all. Then apply the setup patch, commit the changes and remove the setup patch file.
Understand that the prompt below will ask the agent to generate a golden patch on its own only using the problem statement, requirements and interfaces.
Then, you need to run the test_patch on your own or using Reviewer Check 1 and figure out which tests were passed, adjust blockers as necessary and retry.


Prompt:
Examine the problem statement, requirements, and interfaces. Consider these sources as the main user request to create a solution patch .diff file that can be applied to the codebase to satisfy the request. 



Your job is to modify the codebase to generate a solution_patch.diff file of the changes needed to resolve this request. You are not allowed to ask any questions to the user about any ambiguities. If any implementation details are unclear, please assume parameters, values or requirements to use using your best judgement and understanding of the codebase. Do not leave any placeholder values or placeholder implementations. Implement everything fully within the patch as if it was the final product and create a patch of the changes called agent_patch.diff.



Important: The agent patch should not modify any test files. It should only modify source files. Eg. No modifications to anything in a /test directory or any tests in the codebase.



Inputs:

Problem Statement:

{{PROBLEM_STATEMENT_MODIFIED}}



Requirements:

{{REQUIREMENTS_MODIFIED}}



Public Interface:

{{INTERFACES_MODIFIED}}





Output:

agent_patch.diff