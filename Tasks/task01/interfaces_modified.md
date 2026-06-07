Type: Function

  Name: CRLFWriter

  Path: log/formatters.go

  Input:

    - w (io.Writer)

  Output: io.Writer

  Description: Public function that wraps a writer so that all written output uses CRLF line endings. The wrapper always performs this normalization on every Write; it does NOT check the operating system itself (the decision to use it only on Windows is made by SetOutput, not by CRLFWriter). The returned writer also exposes a counter that tracks how many carriage-return bytes it has inserted, for telemetry purposes.



Type: Function

  Name: SetOutput

  Path: log/log.go

  Input:

    - w io.Writer

  Output: none

  Description: Configures the global logger to write to the given io.Writer; when running on Windows it first wraps the writer with CRLFWriter to normalize line endings.
