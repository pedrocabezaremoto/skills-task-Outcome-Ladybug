Follow-up fix for the CRLFWriter task.

The Patch Content Validator flagged that the `InsertedCRs` counter is not genuinely exposed to external consumers: `CRLFWriter` returns `io.Writer` whose concrete type (`crlfWriter`) is unexported, and the test accesses it from inside `package log` (white-box). This must be fixed so the counter is part of the public surface and validated by an EXTERNAL (black-box) test.

Please make ONLY these changes and keep ALL other behaviors identical:

1. In `log/formatters.go`:
   - Make `CRLFWriter(w io.Writer)` return a concrete EXPORTED pointer type that implements `io.Writer` and has an EXPORTED field named exactly `InsertedCRs` of type `int`.
   - Example shape: `type CRLFWriterWrapper struct { w io.Writer; lastByte byte; InsertedCRs int }`, with `func (cw *CRLFWriterWrapper) Write(p []byte) (int, error)`, and `func CRLFWriter(w io.Writer) *CRLFWriterWrapper { return &CRLFWriterWrapper{w: w} }`.
   - `InsertedCRs` increments by 1 each time a `\r` is inserted before a `\n`.
   - Keep: `\n`->`\r\n`; preserve existing `\r\n`; bare `\r` (not followed by `\n`) written through unchanged; null byte `0x00` replaced with `?`; last-byte state persists across Write calls; Write returns the number of INPUT bytes consumed (len of input), not the bytes written downstream.

2. In `log/log.go`: keep `SetOutput` working. `w = CRLFWriter(w)` must still compile (a `*CRLFWriterWrapper` satisfies `io.Writer`).

3. In the test file `log/formatters_test.go`: use `package log_test` (external/black-box). Import the `log` package and access the counter through the exported type returned by `log.CRLFWriter` (e.g., `cw := log.CRLFWriter(buf); ... cw.InsertedCRs`). Keep one test per blocker resolution (LF->CRLF + InsertedCRs count, preserve existing CRLF, null byte -> '?', bare CR preserved, cross-call state persistence, SetOutput).

4. Regenerate the two diffs in the /app root:
   - `golden_patch_obstructed.diff` (source files only: log/formatters.go, log/log.go)
   - `test_patch_obstructed.diff` (test file only: log/formatters_test.go)

5. Re-run the checker and report the final "Overall Result":
   python task_files/task_checker.py --instance-id instance_navidrome__navidrome-9c3b4561652a15846993d477003e111f0df0c585
