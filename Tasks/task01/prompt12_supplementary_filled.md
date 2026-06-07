You are reviewing a task for clarity and solvability. You are NOT solving the task, and you are NOT providing implementation advice.

## Problem Statement

# Windows Log Output: Line Ending Normalization Problem
Navidrome does not format log output correctly for Windows users. Logs use only LF (\n), which is hard to read in Windows editors; when logs are written in parts or carriage returns are present, output can become inconsistent. On Windows, LF should be converted to CRLF; existing CRLF should be preserved; this should work even when logs are written in multiple steps.

## Requirements

- When a line feed character (LF, \n) is written, it is automatically converted to a carriage return + line feed (CRLF, \r\n) in the log output on Windows.
- If a carriage return + line feed sequence (\r\n) already exists, it is preserved as-is and no additional conversion is performed.
- Null bytes (0x00) that appear in log data can corrupt the output when viewed on Windows and must be replaced with an appropriate placeholder character before being written.
- When the writer inserts additional bytes into the stream, the value returned by Write must follow the project's standard byte-count convention.
- To keep each write self-contained, the writer must reset its internal character state at the beginning of every Write call so that inputs are processed in isolation.

## Public Interfaces

- CRLFWriter(w io.Writer) io.Writer  [log/formatters.go] - wraps a writer to add CRLF line endings on Windows; the returned writer also exposes a counter that tracks how many carriage-return bytes it has inserted, for telemetry purposes.
- SetOutput(w io.Writer)  [log/log.go] - configures the global logger to write to the given io.Writer; on Windows it first wraps the writer with CRLFWriter.

## Additional Clarifications (blocker id, description, resolution)

1. null_byte_replacement — desc: requirement says null bytes must be replaced but not with which char. resolution: replace each 0x00 with exactly '?' (0x3F); "h\x00i" -> "h?i".
2. write_return_byte_count — desc: unspecified what Write returns when extra CRs are inserted. resolution: Write returns the number of INPUT bytes consumed (len of input), not bytes written downstream; "hello\nworld\nagain\n" (18) returns 18, not 21.
3. inserted_cr_counter_field — desc: interface says a counter is exposed but not the exact name/type. resolution: CRLFWriter returns io.Writer backed by an exported type named exactly CRLFWriterWrapper, with an exported field InsertedCRs int incremented per inserted \r; type-assert to *CRLFWriterWrapper to read it; after "a\nb\n", InsertedCRs == 2.
4. bare_cr_handling — desc: undefined what happens to a lone \r not followed by \n. resolution: a standalone \r is written through unchanged, byte-for-byte; "a\rb" -> "a\rb".
5. cross_call_state_persistence — desc: problem says works across multiple Write steps, a requirement says reset state each Write (conflict). resolution: state (last byte) persists across Write calls; "hello\r" then "\nworld\n" -> "hello\r\nworld\r\n".

## Ideal Solution

@golden_patch_obstructed.diff

## Tests for Ideal Solution

@test_patch_obstructed.diff

## Your Task

Review the materials above and identify ONLY evidence-backed clarity issues that are still likely to prevent a competent but repo-unfamiliar engineer from implementing the ideal solution correctly, EVEN AFTER reading the problem statement and the additional clarifications.

Do NOT list issues that would merely make the task easier. Only flag issues likely to cause an incorrect implementation, a failed tested behavior, or a missed blocker resolution.

## Strict Rules
- This is NOT a solving task. Do NOT give implementation/validation/testing advice.
- Do NOT comment on test files, test quality/structure/naming, type hints, spelling, or out-of-scope issues.
- Do NOT propose anything that states, narrows, or strongly implies a blocker resolution.
- Do NOT convert ideal-solution details or test-enforced behavior into public spec unless it is clearly a true public contract.
- Use the ideal solution and tests only to diagnose missing clarity; do NOT reverse-engineer them into answer-like hints.
- Only include items concretely supported by the materials. Be succinct.

## Severity Calibration
- HIGH: missing clarity likely to cause a competent repo-unfamiliar engineer to implement behavior that fails the ideal-solution tests or misses a blocker resolution. Use HIGH sparingly. Any HIGH item must state the likely incorrect implementation it would cause.
- LOW: may cause some confusion but a competent engineer could still plausibly implement correctly.

## Output Format
For each valid item:
- Severity: HIGH | LOW
- Issue:
- Why it matters:
- Likely incorrect outcome if not clarified:
- Recommended area to improve: Problem Statement | Requirements | Public Interfaces | Blocker Resolution

If there are no valid items, output exactly:
NOTHING TO ADD
