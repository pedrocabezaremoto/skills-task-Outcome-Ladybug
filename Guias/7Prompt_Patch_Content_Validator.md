Patch Content Validator Prompt

Before running this check:
Replace the placeholders with the actual contents. Please use the modified versions of the problem statement, requirements and interfaces.
Provide the Blocker resolutions in a list:
Resolution 1: content
Resolution 2: content
Resolution 3: content
etc.


Prompt:
Your job is to determine the following:

whether you can find the tests from the relevant test list within the test patch.

whether you can find a relevant test for each blocker resolution. Note that we need to test if each resolution in the blocker registry was correctly implemented, so there should be a test that checks that the solution followed each resolution properly.

whether the golden patch implements the problem statement plus the requirements plus public interface (if any) plus the blocker resolutions within the blocker registry. The problem statement, requirements and public interface may contain ambiguities. These ambiguities or blockers are described within the blocker registry. Read the blocker description to understand the blocker and implement the blocker resolution as the solution to overcome that blocker.

Whether there is separation in the contents of the setup, golden and test patches.

Inputs:

Problem Statement:

{{PROBLEM_STATEMENT_MODIFIED}}

Requirements:

{{REQUIREMENTS_MODIFIED}}

Public Interface:

{{INTERFACES_MODIFIED}}

Blocker Resolutions:

{{Blocker Resolutions}})

Relevant tests:

{{RELEVANT_TESTS_MODIFIED}}

Golden Patch:

{{GOLDEN_PATCH_MODIFIED}}

Setup Patch:

{{SETUP_PATCH_MODIFIED}}

Test Patch:

{{TEST_PATCH_MODIFIED}}

Workflow:

If you cannot find one or more relevant tests within the test patch, return FALSE.

If there are one or more requirements missing from the problem statement, requirements, public interfaces or blocker resolutions within the golden patch, return FALSE.

If there is one or more missing test that should address one of the blocker resolutions or problem statement, or requirements or interfaces, return FALSE

If you find a test for each specified resolution but one or more tests do not properly check if the resolution was applied, return FALSE

If there is overlap in any of the setup, test or golden patches, return FALSE

If the golden patch modifies files in the test folder, return FALSE.

If the test patch modifies files outside of the test folder, return FALSE.

If you find none of the above issues, return TRUE

Output:

<TRUE/FALSE - if FALSE, explain why>

Example:

FALSE - could not find test/units/plugins/connection/test_winrm.py::TestWinRMKerbAuth::test_kinit_success_pexpect[options3-expected3] within the test patch.

Only output plaintext and no markdown. Use the blocker title when referencing a blocker.