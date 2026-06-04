Attempter Check 2

UPDATE: Removed setup patch from this process to get rid of some contamination. We are applying and removing the setup patch before using this prompt.



Before running this prompt:

Ensure you are working with an untampered version of the codebase.
Apply the setup_patch and commit these changes to create a new base commit. Do not apply the golden or test patches. Then remove the setup, golden patch, test patch and relevant test list.
Understand that the prompt below will ask the agent to generate a golden patch on its own using the problem statement, requirements, interfaces, and blocker resolutions. 


After running the prompt:

Upload the test patch and golden patch and test list and then run Reviewer Check 2. 
Replace the Agent Patch of Reviewer Check 2 with the patch that the agent generates in this step above.


Prompt:
Examine the problem statement, requirements, interfaces and blocker resolutions. Consider these sources as the main user request to create a solution patch .diff file that can be applied to the codebase to satisfy the request. 



Your job is to modify the codebase to generate a solution_patch.diff file of the changes needed to resolve this request. You are not allowed to ask any questions to the user about any ambiguities. If any implementation details are unclear, please assume parameters, values or requirements to use using your best judgement and understanding of the codebase. Do not leave any placeholder values or placeholder implementations. Implement everything fully within the patch as if it was the final product and then create an agent_patch.diff of the changes.



Important: The agent patch should not modify any test files. It should only modify source files. Eg. No modifications to anything in a /test directory or any tests in the codebase.



Inputs:

Problem Statement:

{{PROBLEM_STATEMENT_MODIFIED}}



Requirements:

{{REQUIREMENTS_MODIFIED}}



Public Interface:

{{INTERFACES_MODIFIED}}



Blocker Descriptions and Resolutions:

Eg. 

`name_of-blocker description": "description"

`name_of-blocker resolution`: "resolution"



`name_of-blocker description": "description"

`name_of-blocker resolution`: "resolution"

etc.



Output:

agent_patch.diff