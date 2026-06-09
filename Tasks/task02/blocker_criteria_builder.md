# Blocker Registry Criteria Builder — task02 (para llenar en la plataforma)

> 5 criterios (uno por blocker). Dale "Add Criteria" hasta tener 5.
> Area of obstruction = **Requirements** en los 5. Type = marcar el checkbox indicado.

---

## Criterio 1
- **Blocker number:** negative_tail_stability_1
- **Area of obstruction:** Requirements
- **Type:** ☑ Missing Parameters
- **Description:**
How should the log-sigmoid function handle large negative input values? The documentation does not specify the expected output behavior for inputs with large negative magnitudes.
- **Resolution:**
For large-magnitude negative x the result must stay finite and approach x itself: log_sigmoid(-30.0) must be approximately -30.0 (within 1e-2), never -inf or NaN.
- **Trigger Questions:**
  - What should the output be for large negative inputs like -30.0?
  - How is numerical stability maintained when x is a large negative number?
  - Should log_sigmoid return -inf or NaN for extremely small sigmoid outputs?
  - Is there a specific fallback or limit for the function when inputs are very negative?

---

## Criterio 2
- **Blocker number:** logarithm_base_2
- **Area of obstruction:** Requirements
- **Type:** ☑ Ambiguous requirements
- **Description:**
Which mathematical base should be used for the logarithm calculation? The interface descriptions do not clarify whether to compute a natural logarithm or a base-10 logarithm.
- **Resolution:**
Use the natural logarithm (base e). log_sigmoid(0) must equal ln(0.5) which is approximately -0.6931.
- **Trigger Questions:**
  - Which base is intended for the logarithm operation?
  - Should I implement the natural logarithm or base-10?
  - What is the expected exact output for log_sigmoid evaluated at zero?

---

## Criterio 3
- **Blocker number:** negative_tail_gradient_3
- **Area of obstruction:** Requirements
- **Type:** ☑ Missing Parameters
- **Description:**
What is the expected behavior of the gradient for large negative inputs? The specifications lack details regarding the derivative's limits when the input magnitude is large and negative.
- **Resolution:**
The gradient of log_sigmoid w.r.t. its input is sigmoid(-x) = 1 - sigmoid(x); for large negative x it must approach 1.0 and stay finite (gradient at x=-30 is approximately 1.0).
- **Trigger Questions:**
  - What should the gradient be when evaluated at a large negative input?
  - How does the derivative behave for extremely small sigmoid values?
  - Is the gradient expected to remain finite and approach 1.0 for large negative x?

---

## Criterio 4
- **Blocker number:** elementwise_vs_reduction_4
- **Area of obstruction:** Requirements
- **Type:** ☑ Contradictory requirements
- **Description:**
Should the operation compute an elementwise result or aggregate the input tensor into a single scalar? The requirements present conflicting expectations regarding the dimensionality of the returned expression.
- **Resolution:**
The operation is elementwise and shape-preserving: the output Dim equals the input Dim (one value per element). It does NOT reduce or aggregate to a scalar.
- **Trigger Questions:**
  - Is the output shape identical to the input shape?
  - Does this function reduce the input tensor to a single scalar?
  - Should the log-sigmoid operation be applied elementwise to the input tensor?
  - Which requirement wins regarding the output dimensionality of the function?

---

## Criterio 5
- **Blocker number:** positive_tail_saturation_5
- **Area of obstruction:** Requirements
- **Type:** ☑ Missing Parameters
- **Description:**
How must the output behave when provided with extremely large positive inputs? The requirements do not define the expected saturation point and bounds for the positive tail.
- **Resolution:**
For large positive x the output must be finite, <= 0, and approach 0 from below: log_sigmoid(30.0) is approximately 0 (a tiny negative value near -1e-13); never positive, +inf, or NaN.
- **Trigger Questions:**
  - What is the expected output behavior for large positive inputs like 30.0?
  - Should the function ever return a positive value for extremely large positive x?
  - How is the output constrained as the input becomes increasingly positive?
  - What is the theoretical upper limit for the function output?
