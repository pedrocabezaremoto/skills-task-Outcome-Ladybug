# Public Interfaces (modificado — blockers inyectados)

- Path: dynet/expr.h
- Name: log_sigmoid
- Type: function
- Input: const Expression& x
- Output: Expression
- Description: Constructs an expression representing the logarithm of the sigmoid of the input expression within a computation graph.

- Path: dynet/expr.cc
- Name: dynet::log_sigmoid
- Type: Function
- Input: const Expression& x
- Output: Expression
- Description: Implementation of the unary log-sigmoid operation that returns an expression representing the logarithm of the sigmoid function applied to the input expression.

- Path: dynet/nodes-arith-unary.h
- Name: dynet::LogSigmoid
- Type: struct
- Input: NA
- Output: NA

---
<!--
NOTAS QA (no van en el texto entregado):
- CAMBIO CLAVE: se quito la palabra "elementwise" de las descripciones (en el original decia
  "elementwise logarithm of the sigmoid"). Esa palabra FILTRABA el blocker #4 (elementwise vs reduction).
- Se conserva "Input: const Expression& x" (NO bloqueamos el tipo de parametro en el set testeable).
- No se revela forma/estabilidad/base aqui.
-->
