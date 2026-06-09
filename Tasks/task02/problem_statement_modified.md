# Problem Statement (modificado — blockers inyectados)

# Title
Log-sigmoid operation is not available in the expression API

## Description
The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

---
<!--
NOTAS QA (no van en el texto entregado):
- #2 logarithm_base: se deja "the logarithm of the sigmoid" SIN decir "natural". (resolución: ln → registry)
- #1/#5: "wide numeric range / large-magnitude inputs" señala que el rango importa, pero NO dice qué valor devolver en los extremos. El agente debe preguntar.
- NO usar "elementwise", "finite", "stable", "natural", "ln".
-->
