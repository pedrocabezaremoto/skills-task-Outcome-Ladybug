# Requirements (modificado — blockers inyectados)

- The expression API must provide a unary `log_sigmoid` operation that accepts an expression as input and returns a new expression.
- Expressions produced by `log_sigmoid` must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, `log_sigmoid` must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- `log_sigmoid` must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

---
<!--
NOTAS QA (no van en el texto entregado):
- #4 elementwise_vs_reduction (CONTRADICCION PLANTADA): las dos ultimas lineas chocan
  (req A "reduce to a single aggregate value" vs req B "one output for every input value / one-to-one").
  Resolucion: gana B (shape-preserving). NO usar la palabra "elementwise" ni "same shape" textual.
- #1 negative_tail_stability / #5 positive_tail_saturation / #3 negative_tail_gradient:
  la linea de "large magnitude ... must match the project's expected behavior" senala que el
  comportamiento en extremos importa, sin revelar los valores (≈x, ≈0, grad≈1). El agente debe preguntar.
- #2 logarithm_base: NO agregar "natural" en ningun lado.
- Terminos PROHIBIDOS (no deben aparecer): elementwise, finite, numerically stable, natural log, ln,
  x - log1pf(expf(x)), sigmoid(-x), 1 - sigmoid.
-->
