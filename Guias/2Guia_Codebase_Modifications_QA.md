# Codebase Editing Workflow
> **Agent Context Document** — Read this file in full at the start of every session to understand the complete workflow for codebase modification tasks on the Outlier platform.

---

## Overview

This document describes the end-to-end process for:
1. Pulling and running a Docker task image
2. Attaching to the container via Cursor or VS Code
3. Verifying the correct parent commit
4. Validating original patches (golden + test)
5. Creating a setup patch (if needed)
6. Injecting blockers into the golden and test patches
7. Generating the final `.diff` output files
8. Uploading the patches back to the task

All steps must be followed in order. Do not skip or reorder them.

---

## Step 1 — Download the Docker Image

### 1.1 Pull the image

```shell
docker pull <image>
```

**Example:**

```shell
docker pull jefzda/sweap-images:ansible.ansible-ansible__ansible-a6e671db2538\
1ed111bbad0ab3e7d97366395d05-v0f01c69f1e2528b935359cfe578530722bca2c59
```

### 1.2 Run the image

```shell
docker run -d --name <your_container_name> <image> -c "while true; do sleep 3600; done"
```

| Placeholder | Description |
|---|---|
| `<your_container_name>` | A unique name you assign to the container |
| `<image>` | The image tag provided in the task |

**Example:**

```shell
docker run -d --name ansible_d05 --platform linux/amd64 \
  jefzda/sweap-images:ansible.ansible-ansible__ansible-a6e671db2538\
  1ed111bbad0ab3e7d97366395d05-v0f01c69f1e2528b935359cfe578530722bca2c59 \
  -c "while true; do sleep 3600; done"
```

---

## Step 2 — Open the Container in Cursor or VS Code

1. Install the **Dev Containers** extension (and the **Docker** extension if not already installed).
2. In VS Code or Cursor:
   - Press `Ctrl/Cmd + Shift + P`
   - Select **Dev Containers: Attach to Running Container**
   - Choose the container name you assigned in Step 1.2

---

## Step 3 — Open the `/app` Folder

1. Click **Open Folder** inside the connected container window.
2. Navigate to `/app` and click **OK**.
3. You should now see all repository files in the explorer panel.

---

## Step 4 — Verify the Parent Commit Before Making Any Changes

> **Critical:** All patches (`setup_patch.diff`, `test_patch_obstructed.diff`, `golden_patch_obstructed.diff`) must be created on top of the **parent commit**. Do not work from any other commit.

### 4.1 Identify the Expected Parent Commit

- Check the **commit link** provided in the task.
- Go to that commit page on GitHub. The **parent commit hash** is displayed on the right side (e.g., `80b48fc`).

### 4.2 Verify the Repository's Current Commit in the Container

```shell
git rev-parse HEAD
```

**Example output:**

```
root@427301ebad23:/app# git rev-parse HEAD
80b48fcbaab5ad307beb69e73b30aabc1b6f033c
```

The first 7 characters (`80b48fc`) must match what you saw on the GitHub commit page.

### Rules

- The **parent commit is the baseline** for this task.
- **Do not create patches from any other commit.**
- All patches must be **generated relative to the parent commit**.

---

## Step 5 — Validate the Original Patches

Confirm that the original golden and test patches apply cleanly and all tests pass before making any modifications.

### 5.1 Obtain the golden patch from the original commit

```shell
git show <commit> > golden_patch.diff
```

**Example:**

```shell
git show a6e671db25381ed111bbad0ab3e7d97366395d05 > golden_patch.diff
```

### 5.2 Apply the golden patch to the codebase

```shell
git apply golden_patch.diff
```

### 5.3 Run the modified tests

Run only the test files referenced in the test patch:

```shell
pytest test/units/module_utils/facts/hardware/test_aix_processor.py
```

### 5.4 Confirm all tests PASS

Expected result: all collected test items show `PASSED`. If any test fails at this stage, **stop and investigate** before proceeding — the baseline is broken.

---

## Step 6 — Modify Base Codebase and Create Setup Patch

> **When required:** If the base codebase contains information (values, comments, functions) that would allow an agent to resolve the blockers trivially without asking questions, you must strip that context first. This produces the `setup_patch.diff`.

### 6.1 Revert the golden patch to return to the parent commit state

```shell
git checkout -- .
```

### 6.2 Make your setup changes to the base codebase

Edit the relevant files to remove values, comments, or functions that would give away the blocker answers.

### 6.3 Generate the setup patch

```shell
git diff > setup_patch.diff
```

### 6.4 Commit the setup changes locally

This makes the modified base the new starting point for golden and test patches.

```shell
git add <setup_files>
git commit -m "Setup changes for blockers"
```

> After this commit, all subsequent diffs (golden and test patches) will be generated against this new base — which already includes the setup changes.

---

## Step 7 — Inject the Blockers

### 7.1 Re-apply the golden patch on top of the setup changes

```shell
git apply golden_patch.diff
```

### 7.2 Identify which files were modified

- Check the **commit URL** provided in the task.
- Open the **Changes** tab in Cursor / VS Code to see modified files.

### 7.3 Make the blocker changes

Edit the modified files to introduce the intended blockers, following the blocker guidelines provided in the task. These changes will be captured as diffs in Step 8.

---

## Step 8 — Generate the Patches

### 8.1 Check Git status

```shell
git status
```

This shows which files are modified (tracked) and which are untracked.

### 8.2 Stage the files

If you have **untracked files** (new files not yet in Git history), stage them first:

```shell
git add <file_1> <file_2>
```

**Example:**

```shell
git add \
  lib/ansible/module_utils/facts/hardware/aix.py \
  changelogs/fragments/78223_aix_fix_processor_facts.yml \
  test/units/module_utils/facts/hardware/aix_data.py \
  test/units/module_utils/facts/hardware/test_aix_processor.py
```

### 8.3 Generate `golden_patch_obstructed.diff`

Contains only the **source code and changelog files** (not test files):

```shell
git diff --cached -- <file_1> <file_2> > golden_patch_obstructed.diff
```

**Example:**

```shell
git diff --cached -- \
  lib/ansible/module_utils/facts/hardware/aix.py \
  changelogs/fragments/78223_aix_fix_processor_facts.yml \
  > golden_patch_obstructed.diff
```

### 8.4 Generate `test_patch_obstructed.diff`

Contains only the **test and test data files**:

```shell
git diff --cached -- <file_1> <file_2> > test_patch_obstructed.diff
```

**Example:**

```shell
git diff --cached -- \
  test/units/module_utils/facts/hardware/aix_data.py \
  test/units/module_utils/facts/hardware/test_aix_processor.py \
  > test_patch_obstructed.diff
```

---

## Step 9 — Upload the Patches to the Task

### 9.1 Download the patch files from the container

In Cursor / VS Code, right-click each `.diff` file in the explorer and select **Download...** to save them to your local machine.

Files to download:
- `setup_patch.diff` *(if created in Step 6)*
- `golden_patch_obstructed.diff`
- `test_patch_obstructed.diff`

### 9.2 Upload to the task

Go back to the task interface and upload the downloaded `.diff` files to the corresponding upload fields.

---

## Summary: Files Produced

| File | When created | Contains |
|---|---|---|
| `setup_patch.diff` | Step 6 (optional) | Base codebase changes that strip context hints |
| `golden_patch_obstructed.diff` | Step 8.3 | Source + changelog diffs with blockers injected |
| `test_patch_obstructed.diff` | Step 8.4 | Test + test data diffs with blockers injected |

---

## Key Rules for the Agent

- Always verify `git rev-parse HEAD` matches the expected parent commit **before any changes**.
- Never generate patches from a commit other than the parent.
- The order is strict: validate originals → setup patch → inject blockers → generate obstructed patches → upload.
- `setup_patch.diff` is only needed when the base codebase leaks blocker answers. Skip Step 6 if not required.
- `golden_patch_obstructed.diff` must **not** contain test files.
- `test_patch_obstructed.diff` must **not** contain source/changelog files.
- Both obstructed patches are generated from staged (`--cached`) diffs, not unstaged diffs.
