# Quick guide — `prompt.md` (Step 1)

Pipeline that generates **logical blockers** from the baseline task + patches, in up to **3 rounds**. The agent emits **Blocker DSL** (`.bdsl`); the `build_blockers.py` script produces the final JSON.

---

## 1. Folders and files in the task container

Agent working directory (e.g. `qcfail030601/`). Create the input folder:

```text
<task_container>/
  task_info/
    problem-statement.mdc      # problem statement
    requirement.mdc            # requirements
    public-interface.mdc       # public API
    blocker-distribution.mdc   # how many blockers per type
    golden_patch.mdc           # reference patch (private)
    test_patch.mdc             # test patch (private)
```

**Exact names** (as in `prompt.md`). The orchestrator expects the `.mdc` extension.

**`blocker-distribution.mdc`** — counts per type, in this format:

```text
mp=1 ar=1 cr=1
```

| Alias | Type |
|-------|------|
| `mp` | `missing_parameter` |
| `ar` | `ambiguous_requirement` |
| `cr` | `contradictory_requirement` |

Also copy into the container (or point the agent at the repo):

- `BlockerGenerator/prompt.md`
- `BlockerGenerator/build_blockers.py`
- `BlockerGenerator/skills/` (`project-overview.mdc`, `blocker-generator.mdc`, `blocker-registry.mdc`)

**Outputs** (container root, `--out-dir .`):

| File | Role |
|------|------|
| `round_<N>.bdsl` | Round DSL (written by the agent) |
| `blocker_registry.json` | Cumulative answer key of valid blockers |
| `generation_memory.json` | Loop state + audit trail |
| `existing_registry.json` | Rounds > 1 only (incoming state) |
| `rejection_memory.json` | Rounds > 1 only (accumulated rejections) |
| `abort.json` | Missing input or infeasible task |

---

## 2. How to use `prompt.md`

1. Open `BlockerGenerator/prompt.md` in the agent chat (Cursor / cloud).
2. Ensure the agent **cwd** is the container root (`task_info/` visible).
3. Fill in the placeholders at the end of the prompt (sections below).
4. The agent reads the skills, writes `.bdsl`, and runs `build_blockers.py` — **do not** hand-edit `blocker_registry.json`.

### Round 1 (from scratch)

```text
<existing_registry>     [empty]
<rejection_memory>    [empty]
<round_number>        1
```

Expected command after the DSL:

```bash
python build_blockers.py round_1.bdsl --out-dir .
```

### Multiple turns (rounds 2 and 3)

When `generation_memory.json` has `halt.reason` = `continue` and blockers are still missing:

1. Copy the full contents of **`blocker_registry.json`** → `<existing_registry>`.
2. Copy the **`rejection_memory`** array from **`generation_memory.json`** → `<rejection_memory>`.
3. Set `<round_number>` to `2` or `3`.
4. Start a new prompt / turn with the same updated `prompt.md`.

The agent writes `existing_registry.json` and `rejection_memory.json`, emits `round_<N>.bdsl`, and runs:

```bash
python build_blockers.py round_<N>.bdsl \
  --existing existing_registry.json \
  --rejection-memory rejection_memory.json \
  --out-dir .
```

**Stop the loop** when `halt.reason` is:

- `distribution_satisfied` — target met  
- `distribution_already_satisfied` — nothing to generate this round  
- `budget_exhausted` — 3 rounds without meeting the target  

### Existing blockers (partial registry)

Use on the **first** run with a pre-filled registry:

- Paste existing JSON into `<existing_registry>` (same shape as `blocker_registry.json`).
- Empty `<rejection_memory>` `[]` or history you already have.
- `<round_number>` = `1` (or the next logical round).

The agent computes the per-type **deficit** (`requested − already in registry`) and only generates missing blockers. Entries already in the registry are **immutable** — do not re-emit them in the DSL.

If every type’s deficit is zero, the round emits only `@meta` with `halt: distribution_already_satisfied`.

---

## 3. Memory — what it is

| Concept | Where it lives | Use |
|---------|----------------|-----|
| **Registry** (`blocker_registry.json`) | Cumulative | Answer key for evaluation and Step 2 (obfuscation). Feeds `<existing_registry>` on the next round. |
| **Rejection memory** | Array in `generation_memory.json` → `rejection_memory` | `@rejected` attempts that failed validation. The agent must **avoid repeating** the same patterns (`failure_gate`, `avoid_in_future`, etc.). |
| **`blocker_dataset` (in generation_memory)** | Current round only | Candidate pool, new blockers with `ground_truth_annotation`, audit — **do not** reuse as the registry. |

Practical rule: on the next round, pass **registry + rejection_memory**; ignore the rest of `generation_memory` when filling the prompt.

---

## 4. What gets generated

**`blocker_registry.json`** — main deliverable: `blockers[]` with `id`, `type`, `mode`, `area_of_obstruction`, `description`, `resolution`, `trigger_questions`, `independence`. Valid entries come only from `@blocker` records with `status: valid | repaired_valid`.

**`generation_memory.json`** — control and trace:

- `halt` — stop reason, round, requested vs achieved totals  
- `blocker_dataset` — candidates (`candidate_pool`), round blockers with ground truth, round rejections, notes  
- `rejection_memory` — **accumulated** rejections (all rounds)

The agent writes **`.bdsl`**; the script builds JSON deterministically (counts, deficit, implied checks).

---

## 5. How to run

### Via the agent (normal flow)

1. Set up `task_info/` with all 6 files.  
2. Paste `prompt.md` in chat; fill `<existing_registry>`, `<rejection_memory>`, `<round_number>`.  
3. Let the agent run until `blocker_registry.json` and `generation_memory.json` exist without error.  
4. If `halt.reason` = `continue`, repeat with round +1 and updated JSON (max 3 rounds).

### Manual script (validate / reprocess DSL)

From the container root, with Python 3:

```bash
# Round 1
python build_blockers.py round_1.bdsl --out-dir .

# Rounds 2+
python build_blockers.py round_2.bdsl \
  --existing existing_registry.json \
  --rejection-memory rejection_memory.json \
  --out-dir .
```

If the script fails, fix the `.bdsl` (grammar in `skills/blocker-generator.mdc`) and rerun — do not hand-edit output JSON.

### Absolute path (Windows example)

```bash
cd "c:\Users\leo_m\OneDrive\Documentos\ladybug\qcfail030601"
python "c:\Users\leo_m\OneDrive\Documentos\ladybug\BlockerGenerator\build_blockers.py" round_1.bdsl --out-dir .
```

---

## One-line flow

```text
task_info/*  →  prompt.md (≤3×)  →  round_N.bdsl  →  build_blockers.py  →  blocker_registry.json + generation_memory.json
```

Next pipeline step: Step 2 (task obfuscation using `blocker_registry.json`).
