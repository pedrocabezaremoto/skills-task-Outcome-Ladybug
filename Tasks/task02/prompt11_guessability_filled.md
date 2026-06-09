# Prompts de Guessability (Guía 11) — task02, listos para Cursor

> Correr 1 por blocker, **2 veces cada uno con 2 modelos distintos** (Gemini 3.1 Pro y GPT-5.5).
> Contenedor en baseline **`8ea37f68`**, SIN golden/test aplicados (que el agente NO vea la solución).
> Setup patch: NO necesario (en baseline no existe el código de log_sigmoid → no hay leak).
> El agente debe DESCRIBIR (no implementar). Esperado: que su descripción **NO coincida** con la resolución.

---

## BLOQUE COMÚN (va en los 5 prompts, arriba)

```
You are helping with a software task. Assume you are a competent engineer who is unfamiliar with this repository. Explore the codebase if useful, but do NOT implement anything and do NOT write code or patches.

## Problem Statement
# Title
Log-sigmoid operation is not available in the expression API
## Description
The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

## Requirements
- The expression API must provide a unary `log_sigmoid` operation that accepts an expression as input and returns a new expression.
- Expressions produced by `log_sigmoid` must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, `log_sigmoid` must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- `log_sigmoid` must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

## Public Interfaces
- Path: dynet/expr.h | Name: log_sigmoid | function | Input: const Expression& x | Output: Expression | Constructs an expression representing the logarithm of the sigmoid of the input within a computation graph.
- Path: dynet/expr.cc | Name: dynet::log_sigmoid | Function | Input: const Expression& x | Output: Expression.
- Path: dynet/nodes-arith-unary.h | Name: dynet::LogSigmoid | struct.

## My Confusion
<<AQUÍ VA LA DESCRIPCIÓN DEL BLOCKER — ver abajo>>

## Your Task
Describe in detail the best / most likely thing you would do to resolve this confusion, and why. Use your knowledge of standard engineering practices. Do NOT implement anything. Just describe the approach.
```

---

## Las 5 "My Confusion" (una por corrida)

**1 — negative_tail_stability:**
How should the log-sigmoid function handle large negative input values? The documentation does not specify the expected output behavior for inputs with large negative magnitudes.

**2 — logarithm_base:**
Which mathematical base should be used for the logarithm calculation? It is not clear whether to compute a natural logarithm or a base-10 logarithm.

**3 — negative_tail_gradient:**
What is the expected behavior of the gradient for large negative inputs? The specifications lack details regarding the derivative's limits when the input magnitude is large and negative.

**4 — elementwise_vs_reduction:**
Should the operation compute an elementwise result or aggregate the input tensor into a single scalar? The requirements present conflicting expectations regarding the dimensionality of the returned expression.

**5 — positive_tail_saturation:**
How must the output behave when provided with extremely large positive inputs? The requirements do not define the expected saturation point and bounds for the positive tail.

---

## Resultado esperado por blocker (lo que confirmaron los evals)
- #1, #3, #4, #5 → la descripción del agente NO coincide con la resolución → ✅ NO guessable. Screenshot bueno.
- #2 (logarithm_base) → el agente dirá "natural log" → COINCIDE → guessable. Screenshot que muestra el guess → responder "Yes" en la pregunta (es blocker original, no introducido/facilitado por ti).
