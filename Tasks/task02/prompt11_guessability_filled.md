# Guessability (Guía 11) — 5 prompts COMPLETOS listos para pegar en Cursor

> Cada bloque ``` ``` de abajo es UN prompt completo. Copia uno entero → pégalo en el chat del agente del CONTENEDOR → envía → screenshot. Repite cada uno con 2 modelos (Gemini 3.1 Pro y GPT-5.5).
> ANTES: `mv /app/_bgen /root/_bgen` (sacar la solución) y baseline `8ea37f68` sin golden/test.
> Esperado: la descripción del agente NO debe coincidir con la resolución. (#2 sí coincidirá → es esperado.)

---

## PROMPT 1 — negative_tail_stability

```
You are helping with a software task. Assume you are a competent engineer unfamiliar with this repository. Explore the codebase if useful, but do NOT implement anything and do NOT write code or patches.

## Problem Statement
# Title: Log-sigmoid operation is not available in the expression API
## Description: The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

## Requirements
- The expression API must provide a unary log_sigmoid operation that accepts an expression as input and returns a new expression.
- Expressions produced by log_sigmoid must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, log_sigmoid must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- log_sigmoid must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

## Public Interfaces
- dynet/expr.h : log_sigmoid (function), Input const Expression& x, Output Expression.
- dynet/expr.cc : dynet::log_sigmoid (function).
- dynet/nodes-arith-unary.h : dynet::LogSigmoid (struct).

## My Confusion
How should the log-sigmoid function handle large negative input values? The documentation does not specify the expected output behavior for inputs with large negative magnitudes.

## Your Task
Describe in detail the best / most likely thing you would do to resolve this confusion, and why. Use standard engineering practices. Do NOT implement anything. Just describe the approach.
```

---

## PROMPT 2 — logarithm_base

```
You are helping with a software task. Assume you are a competent engineer unfamiliar with this repository. Explore the codebase if useful, but do NOT implement anything and do NOT write code or patches.

## Problem Statement
# Title: Log-sigmoid operation is not available in the expression API
## Description: The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

## Requirements
- The expression API must provide a unary log_sigmoid operation that accepts an expression as input and returns a new expression.
- Expressions produced by log_sigmoid must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, log_sigmoid must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- log_sigmoid must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

## Public Interfaces
- dynet/expr.h : log_sigmoid (function), Input const Expression& x, Output Expression.
- dynet/expr.cc : dynet::log_sigmoid (function).
- dynet/nodes-arith-unary.h : dynet::LogSigmoid (struct).

## My Confusion
Which mathematical base should be used for the logarithm calculation? It is not clear whether to compute a natural logarithm or a base-10 logarithm.

## Your Task
Describe in detail the best / most likely thing you would do to resolve this confusion, and why. Use standard engineering practices. Do NOT implement anything. Just describe the approach.
```

---

## PROMPT 3 — negative_tail_gradient

```
You are helping with a software task. Assume you are a competent engineer unfamiliar with this repository. Explore the codebase if useful, but do NOT implement anything and do NOT write code or patches.

## Problem Statement
# Title: Log-sigmoid operation is not available in the expression API
## Description: The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

## Requirements
- The expression API must provide a unary log_sigmoid operation that accepts an expression as input and returns a new expression.
- Expressions produced by log_sigmoid must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, log_sigmoid must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- log_sigmoid must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

## Public Interfaces
- dynet/expr.h : log_sigmoid (function), Input const Expression& x, Output Expression.
- dynet/expr.cc : dynet::log_sigmoid (function).
- dynet/nodes-arith-unary.h : dynet::LogSigmoid (struct).

## My Confusion
What is the expected behavior of the gradient for large negative inputs? The specifications lack details regarding the derivative's limits when the input magnitude is large and negative.

## Your Task
Describe in detail the best / most likely thing you would do to resolve this confusion, and why. Use standard engineering practices. Do NOT implement anything. Just describe the approach.
```

---

## PROMPT 4 — elementwise_vs_reduction

```
You are helping with a software task. Assume you are a competent engineer unfamiliar with this repository. Explore the codebase if useful, but do NOT implement anything and do NOT write code or patches.

## Problem Statement
# Title: Log-sigmoid operation is not available in the expression API
## Description: The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

## Requirements
- The expression API must provide a unary log_sigmoid operation that accepts an expression as input and returns a new expression.
- Expressions produced by log_sigmoid must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, log_sigmoid must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- log_sigmoid must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

## Public Interfaces
- dynet/expr.h : log_sigmoid (function), Input const Expression& x, Output Expression.
- dynet/expr.cc : dynet::log_sigmoid (function).
- dynet/nodes-arith-unary.h : dynet::LogSigmoid (struct).

## My Confusion
Should the operation compute an elementwise result or aggregate the input tensor into a single scalar? The requirements present conflicting expectations regarding the dimensionality of the returned expression.

## Your Task
Describe in detail the best / most likely thing you would do to resolve this confusion, and why. Use standard engineering practices. Do NOT implement anything. Just describe the approach.
```

---

## PROMPT 5 — positive_tail_saturation

```
You are helping with a software task. Assume you are a competent engineer unfamiliar with this repository. Explore the codebase if useful, but do NOT implement anything and do NOT write code or patches.

## Problem Statement
# Title: Log-sigmoid operation is not available in the expression API
## Description: The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface. The operation will be applied to inputs spanning a wide numeric range during training, so its behavior for large-magnitude inputs must match the project's expected outputs.

## Requirements
- The expression API must provide a unary log_sigmoid operation that accepts an expression as input and returns a new expression.
- Expressions produced by log_sigmoid must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
- The operation will receive inputs of large magnitude (both strongly negative and strongly positive) during training; its forward outputs and its gradients for such inputs must match the project's expected behavior.
- To support its use as a training objective, log_sigmoid must reduce its input into a single aggregate log-likelihood value that summarizes the entire input tensor.
- log_sigmoid must produce one output value for every value in its input tensor, yielding a one-to-one mapping between input and output positions.

## Public Interfaces
- dynet/expr.h : log_sigmoid (function), Input const Expression& x, Output Expression.
- dynet/expr.cc : dynet::log_sigmoid (function).
- dynet/nodes-arith-unary.h : dynet::LogSigmoid (struct).

## My Confusion
How must the output behave when provided with extremely large positive inputs? The requirements do not define the expected saturation point and bounds for the positive tail.

## Your Task
Describe in detail the best / most likely thing you would do to resolve this confusion, and why. Use standard engineering practices. Do NOT implement anything. Just describe the approach.
```
