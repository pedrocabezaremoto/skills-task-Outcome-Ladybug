Follow-up fix #2 for the CRLFWriter task.

The Patch Content Validator flagged that `CRLFWriter` now returns `*CRLFWriterWrapper`, but the declared public interface is `CRLFWriter(w io.Writer) io.Writer`. The implementation MUST match the declared interface (return `io.Writer`), while still exposing the `InsertedCRs` counter to an external (black-box) test.

Please make ONLY these changes and keep ALL other behaviors identical:

1. In `log/formatters.go`:
   - `CRLFWriter(w io.Writer)` must return `io.Writer` (to match the declared public interface), NOT a concrete type.
   - The concrete type behind it must be EXPORTED, e.g. `type CRLFWriterWrapper struct { w io.Writer; lastByte byte; InsertedCRs int }`, with `func (cw *CRLFWriterWrapper) Write(p []byte) (int, error)`.
   - So: `func CRLFWriter(w io.Writer) io.Writer { return &CRLFWriterWrapper{w: w} }`.
   - Keep ALL behaviors: `\n`->`\r\n`; preserve existing `\r\n`; bare `\r` (not followed by `\n`) written through unchanged; null byte `0x00` replaced with `?`; last-byte state persists across Write calls; `Write` returns the number of INPUT bytes consumed (len of input), NOT bytes written downstream; `InsertedCRs` increments by 1 each time a `\r` is inserted before a `\n`.

2. In `log/log.go`: keep `SetOutput` working (`w = CRLFWriter(w)` compiles since the returned value is `io.Writer`).

3. In `log/formatters_test.go` (package `log_test`, black-box): obtain the writer with `log.CRLFWriter(buf)` and type-assert to the exported type to read the counter, e.g.:
   `cw := log.CRLFWriter(buf).(*log.CRLFWriterWrapper)` and then assert `cw.InsertedCRs`.
   Keep one test per blocker resolution (LF->CRLF + InsertedCRs count, preserve existing CRLF, null byte -> '?', bare CR preserved, cross-call state persistence, SetOutput).

4. Regenerate the two diffs in /app root:
   - `golden_patch_obstructed.diff` (source files only: log/formatters.go, log/log.go)
   - `test_patch_obstructed.diff` (test file only: log/formatters_test.go)

5. Do NOT try to run `go` yourself (your shell has no `go` in PATH). Just regenerate the diffs cleanly. The user will run task_checker manually.
