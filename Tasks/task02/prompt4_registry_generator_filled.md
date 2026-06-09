# Prompt LLENO — Blocker Registry Generator (Guía 4) para task02 (dynet log_sigmoid)

> Pegar TODO lo de abajo (dentro del bloque) en un agente de Cursor, con cwd = `/app/_bgen`.
> Genera `blocker_registry.json` realizando los 5 blockers testeables ya diseñados.

---

```
You are generating a `blocker_registry.json` for a Blocker Injection task (Outcome Ladybug project, dynet C++ log_sigmoid). Follow the rules below EXACTLY.

# STEP 0 — Read these files first (they are in the current working directory):
- task_info/problem-statement.mdc
- task_info/requirement.mdc
- task_info/public-interface.mdc
- task_info/golden_patch.mdc   (reference solution — private, for grounding resolutions)
- task_info/test_patch.mdc     (reference tests — private)

# What makes a valid blocker
Every blocker MUST be: realistic, CRITICAL (a wrong guess changes observable output), OBJECTIVE (one exact resolution), backed by a large answer space, INDEPENDENT from the others, UNCONTAMINATED (not recoverable from the repo/tests/convention/defaults), not a gotcha, and VALIDATABLE BY A NARROW TEST — i.e. if the agent guesses wrong, a test must FAIL.

# Required distribution (exact)
3 missing_parameter, 1 ambiguous_requirement, 1 contradictory_requirement.

# TARGET BLOCKERS — produce EXACTLY these 5
For each one, write a registry entry with: a `description` that explains WHY it is a blocker WITHOUT revealing the answer (and never self-referential, never says "was removed"); the EXACT `resolution` given below; and 3-5 varied `trigger_questions` (complete sentences). Each blocker is validated by the narrow test noted (this is why it is testable — do not put the test in the registry, it is only for your understanding).

1) id: negative_tail_stability | type: missing_parameter | area_of_obstruction: requirements
   resolution: For large-magnitude negative x the result must stay finite and approach x itself: log_sigmoid(-30.0) must be approximately -30.0 (within 1e-2), never -inf or NaN.
   validated by test: forward value at x=-30 is finite and ≈ -30.

2) id: logarithm_base | type: ambiguous_requirement | area_of_obstruction: requirements
   resolution: Use the natural logarithm (base e). log_sigmoid(0) must equal ln(0.5) ≈ -0.6931.
   validated by test: forward value at x=0 ≈ -0.6931 (a base-10 implementation gives -0.3010 and FAILS).

3) id: negative_tail_gradient | type: missing_parameter | area_of_obstruction: requirements
   resolution: The gradient of log_sigmoid w.r.t. its input is sigmoid(-x) = 1 - sigmoid(x); for large negative x it must approach 1.0 and stay finite (gradient at x=-30 ≈ 1.0).
   validated by test: gradient at x=-30 ≈ 1.0, finite.

4) id: elementwise_vs_reduction | type: contradictory_requirement | area_of_obstruction: requirements
   resolution: The operation is elementwise and shape-preserving: the output Dim equals the input Dim (one value per element). It does NOT reduce or aggregate to a scalar.
   validated by test: a vector input produces a vector output of the same shape (a reduction to scalar FAILS).
   note: the contradiction is planted in the Requirements text ("reduce to a single aggregate value" vs "one output per input value"); the resolution is that the shape-preserving requirement wins.

5) id: positive_tail_saturation | type: missing_parameter | area_of_obstruction: requirements
   resolution: For large positive x the output must be finite, <= 0, and approach 0 from below: log_sigmoid(30.0) ≈ 0 (a tiny negative value near -1e-13); never positive, +inf, or NaN.
   validated by test: forward value at x=+30 is finite, <= 0, and ≈ 0.

# Rules for the fields
- description: AT MOST two sentences, frames the gap as a question, NEVER reveals the resolution or how it was created.
- resolution: use the EXACT text given above (you may add a short concrete example), never vague words like "appropriate".
- trigger_questions: 3-5, complete sentences, varied phrasing (What / How / Should I / Which / Is it), self-contained, never self-referential.
- Do NOT add, drop, or rename any of the 5 blockers. Keep the exact ids and types above.

# OUTPUT
Write the file `blocker_registry.json` in the current working directory with this schema:
{
  "blockers": [
    { "id": "...", "type": "...", "area_of_obstruction": "...", "description": "...", "resolution": "...", "trigger_questions": ["...", "...", "..."] }
  ],
  "distribution_notes": "Achieved 3 missing_parameter, 1 ambiguous_requirement, 1 contradictory_requirement. Every blocker is validated by a narrow test on observable behavior (forward value, gradient, or shape)."
}

Output ONLY the JSON file written to disk. Confirm the path when done.
```
