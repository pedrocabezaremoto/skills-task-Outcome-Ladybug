# Requerimientos — Task 02 (Outcome Ladybug)

> **Tipo:** Blocker Injection
> **ID:** `6a2703ae522946e24d096a01`
> **Proyecto:** dynet (C++) — Log-sigmoid operation
> **Estado:** Nueva
> **⚠️ Recordatorio:** la respuesta final DEBE incluir un **thin space** (U+2009) o score = 0.

---

## 0. Welcome / Project Overview

Welcome to the Outcome Ladybug project. You will be designing SWEAP problems with blockers that prevent an AI agent from correctly solving the task without asking clarifying questions.

You will start with a valid and solvable SWEAP problem, your job is to inject blockers (ambiguities, missing parameters, or contradictions) into the problem.

A successful Blocker Injection task ensures:
- **Failure without help:** An AI agent attempting the blocked SWEAP problem without asking questions will guess wrong and fail.
- **Success with help:** An AI agent that asks the right questions (simulated by a Blocker Registry) will receive the necessary details to solve the blocked SWEAP problem.

**About this Project:** Quality revolves around Agent Feedback, where 3 agents attempt to solve your problem with blockers. Check 1 ensures failure without help and Check 2 ensures success with help. The Agent Feedback is not available as a linter within the task. This is because it can take about an hour or more to retrieve this feedback. We provide the Agent Feedback directly when we SBQ the task to the same CB. Don't worry about the SBQ, it is expected since we need to generate the eval to understand what needs to be fixed in the task.

This project fundamentally works on SBQs and fixing your own tasks in an iterative manner to get good results. You won't get removed from the project as long as you are working towards improving your tasks using the returned feedback.

> ⚠️ **Modelos:** La plataforma advierte "Please don't use the latest models in Cursor...". *(Nota para Pedro: La comunidad aclaró que SÍ se pueden usar los nuevos modelos, mantén tu Gemini 3.1 Pro o GPT-5.5 como de costumbre).*

---

## 1. Initial SWEAP Information

### Code Language
```cpp
C++
```

### Problem Statement
```text
# Title
Log-sigmoid operation is not available in the expression API

## Description
The expression API does not provide a log-sigmoid operation, preventing users from computing the logarithm of the sigmoid function through the standard expression interface.
```

### Requirements
```text
- The expression API must provide a unary `log_sigmoid` operation that accepts an expression as input and returns a new expression.
- Expressions produced by `log_sigmoid` must compute correct gradients with respect to their input during backpropagation when used in a computation graph.
```

### Public Interfaces
```text
- Path: dynet/expr.h
- Name: log_sigmoid
- Type: function
- Input: const Expression& x
- Output: Expression
- Description: Constructs an expression representing the elementwise logarithm of the sigmoid of the input expression within a computation graph.

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
- Description: Node type for log-sigmoid operation in the computation graph. Inherits from Node and implements forward and backward passes for the operation.

- Path: dynet/nodes-arith-unary.h
- Name: dynet::LogSigmoid::supports_multibatch
- Type: Method (const, override)
- Input: None
- Output: bool
- Description: Indicates whether this node supports multibatch processing.

- Path: dynet/nodes-arith-unary.h
- Name: dynet::LogSigmoid::autobatch_sig
- Type: Method (const, override)
- Input: const ComputationGraph &cg, SigMap &sm
- Output: int
- Description: Returns the autobatching signature index for this node type.

- Path: dynet/nodes-arith-unary.h
- Name: dynet::LogSigmoid::autobatch_concat
- Type: Method (const, override)
- Input: const ComputationGraph & cg
- Output: std::vector<int>
- Description: Returns the concatenation dimensions for autobatching.

- Path: dynet/simd-functors.h
- Name: dynet::scalar_log_sigmoid_forward_op
- Type: struct
- Input: NA
- Output: NA
- Description: Implements the forward computation of the log-sigmoid function for a scalar or vectorized input.

- Path: dynet/simd-functors.h
- Name: dynet::scalar_log_sigmoid_forward_op<Scalar>::operator()
- Type: method
- Input: const Scalar& x
- Output: const Scalar
- Description: Computes the elementwise logarithm of the sigmoid function for a single scalar input, in a numerically stable way.

- Path: dynet/simd-functors.h
- Name: dynet::scalar_log_sigmoid_forward_op<Scalar>::packetOp
- Type: method
- Input: const Packet& x
- Output: Packet
- Description: Vectorized computation of log-sigmoid for Eigen packets.

- Path: dynet/simd-functors.h
- Name: dynet::scalar_log_sigmoid_backward_op
- Type: struct
- Input: NA
- Output: NA
- Description: Implements the backward computation (gradient) of the log-sigmoid function.

- Path: dynet/simd-functors.h
- Name: dynet::scalar_log_sigmoid_backward_op<Scalar>::operator()
- Type: method
- Input: const Scalar& t, const Scalar& d
- Output: const Scalar
- Description: Computes the gradient of the log-sigmoid function with respect to its input, used in backpropagation.

- Path: dynet/simd-functors.h
- Name: dynet::scalar_log_sigmoid_backward_op<Scalar>::packetOp
- Type: method
- Input: const Packet& t, const Packet& d
- Output: const Packet
- Description: Vectorized computation of the log-sigmoid gradient for Eigen packets, used in automatic differentiation.

- Path: dynet/nodes-arith-unary.cc
- Name: dynet::LogSigmoid::as_string
- Type: Method 
- Input: const vector<string>& arg_names
- Output: string
- Description: Returns a readable string representation of the node including its argument names.

- Path: dynet/nodes-arith-unary.cc
- Name: dynet::LogSigmoid::dim_forward
- Type: Method
- Input: const vector<Dim>& xs
- Output: Dim
- Description: Validates input dimensions and returns the output dimension for the log-sigmoid operation.

- Path: dynet/nodes-arith-unary.cc
- Name: dynet::LogSigmoid::forward_dev_impl
- Type: Template Method 
- Input: const MyDevice & dev, const vector<const Tensor*>& xs, Tensor& fx
- Output: void
- Description: Computes the forward pass values of log-sigmoid for the current device backend.

- Path: dynet/nodes-arith-unary.cc
- Name: dynet::LogSigmoid::backward_dev_impl
- Type: Template Method
- Input: const MyDevice & dev, const vector<const Tensor*>& xs, const Tensor& fx, const Tensor& dEdf, unsigned i, Tensor& dEdxi
- Output: void
- Description: Accumulates gradients for the selected input of log-sigmoid during backpropagation.
```

### Commit Link
```text
https://github.com/clab/dynet/commit/0e5addb8066351e2941151b8fe88264c84156636
```

---

## 2. Golden Patch

```diff
diff --git a/doc/source/python_ref.rst b/doc/source/python_ref.rst
index e887f86e2..6387cf809 100644
--- a/doc/source/python_ref.rst
+++ b/doc/source/python_ref.rst
@@ -189,6 +189,8 @@ Arithmetic operations
 
 .. autofunction:: dynet.log
 
+.. autofunction:: dynet.log_sigmoid
+
 .. autofunction:: dynet.lgamma
 
 .. autofunction:: dynet.sin
diff --git a/dynet/expr.cc b/dynet/expr.cc
index c4d5afa4f..73ec70188 100644
--- a/dynet/expr.cc
+++ b/dynet/expr.cc
@@ -80,6 +80,7 @@ Expression tanh(const Expression& x) { return Expression(x.pg, x.pg->add_functio
 Expression asinh(const Expression& x) { return Expression(x.pg, x.pg->add_function<Asinh>({x.i})); }
 Expression acosh(const Expression& x) { return Expression(x.pg, x.pg->add_function<Acosh>({x.i})); }
 Expression atanh(const Expression& x) { return Expression(x.pg, x.pg->add_function<Atanh>({x.i})); }
+Expression log_sigmoid(const Expression& x) { return Expression(x.pg, x.pg->add_function<LogSigmoid>({x.i})); }
 Expression lgamma(const Expression& x) { return Expression(x.pg, x.pg->add_function<LogGamma>({x.i})); }
 Expression log(const Expression& x) { return Expression(x.pg, x.pg->add_function<Log>({x.i})); }
 Expression exp(const Expression& x) { return Expression(x.pg, x.pg->add_function<Exp>({x.i})); }
diff --git a/dynet/expr.h b/dynet/expr.h
index d7780ad0e..1b3975793 100644
--- a/dynet/expr.h
+++ b/dynet/expr.h
@@ -1020,6 +1020,18 @@ Expression square(const Expression& x);
  */
 Expression cube(const Expression& x);
 
+/**
+ * \ingroup arithmeticoperations
+ * \brief Log sigmoid
+ * \details Calculate elementwise \f$y_i = \ln(\frac{1}{1+e^{-x_i}})\f$
+ * This is more numerically stable than `log(logistic(x))`
+ *
+ * \param x The input expression
+ *
+ * \return An expression where the ith element is equal to \f$y_i = \ln(\frac{1}{1+e^{-x_i}})\f$
+ */
+Expression log_sigmoid(const Expression& x);
+
 /**
  * \ingroup arithmeticoperations
  * \brief Log gamma
diff --git a/dynet/nodes-arith-unary.cc b/dynet/nodes-arith-unary.cc
index d13960ef0..0796b99ef 100644
--- a/dynet/nodes-arith-unary.cc
+++ b/dynet/nodes-arith-unary.cc
@@ -242,6 +242,40 @@ void Abs::backward_dev_impl(const MyDevice & dev,
 }
 DYNET_NODE_INST_DEV_IMPL(Abs)
 
+// ************* LogSigmoid *************
+
+#ifndef __CUDACC__
+
+string LogSigmoid::as_string(const vector<string>& arg_names) const {
+  ostringstream os;
+  os << "log_sigmoid(" << arg_names[0] << ')';
+  return os.str();
+}
+
+Dim LogSigmoid::dim_forward(const vector<Dim>& xs) const {
+  DYNET_ARG_CHECK(xs.size() == 1, "Failed input count check in LogSigmoid")
+  return xs[0];
+}
+
+#endif
+
+template<class MyDevice>
+void LogSigmoid::forward_dev_impl(const MyDevice & dev, const vector<const Tensor*>& xs, Tensor& fx) const {
+  tvec(fx).device(*dev.edevice) = tvec(*xs[0]).unaryExpr(scalar_log_sigmoid_forward_op<float>());
+}
+
+template<class MyDevice>
+void LogSigmoid::backward_dev_impl(const MyDevice & dev,
+                             const vector<const Tensor*>& xs,
+                             const Tensor& fx,
+                             const Tensor& dEdf,
+                             unsigned i,
+                             Tensor& dEdxi) const {
+  tvec(dEdxi).device(*dev.edevice) += tvec(fx).binaryExpr(tvec(dEdf), scalar_log_sigmoid_backward_op<float>());
+}
+DYNET_NODE_INST_DEV_IMPL(LogSigmoid)
+
+
 // ************* LogGamma *************
 
 #ifndef __CUDACC__
diff --git a/dynet/nodes-arith-unary.h b/dynet/nodes-arith-unary.h
index 8e301050f..1c966bfa8 100644
--- a/dynet/nodes-arith-unary.h
+++ b/dynet/nodes-arith-unary.h
@@ -69,6 +69,15 @@ struct Abs : public Node {
   DYNET_NODE_DEFINE_DEV_IMPL()
 };
 
+// y = log_sigmoid x_1
+struct LogSigmoid : public Node {
+  explicit LogSigmoid(const std::initializer_list<VariableIndex>& a) : Node(a) {}
+  virtual bool supports_multibatch() const override { return true; }
+  virtual int autobatch_sig(const ComputationGraph &cg, SigMap &sm) const override { Sig s(nt::logsigmoid); return sm.get_idx(s); }
+  virtual std::vector<int> autobatch_concat(const ComputationGraph & cg) const override { return std::vector<int>(1, 1); }  
+  DYNET_NODE_DEFINE_DEV_IMPL()
+};
+
 // y = lgamma x_1
 struct LogGamma : public Node {
   explicit LogGamma(const std::initializer_list<VariableIndex>& a) : Node(a) {}
diff --git a/dynet/sig.h b/dynet/sig.h
index bbc6d0ce0..acdc33d1f 100644
--- a/dynet/sig.h
+++ b/dynet/sig.h
@@ -13,7 +13,7 @@ namespace dynet {
 
   namespace nt {
     enum NodeType {
-      tanh=1, sqrt, abs, erf, square, cube, exp, loggamma, log, nobackprop, scalegradient, identity, negate, rectify, logistic, softsign, silu,
+      tanh=1, sqrt, abs, erf, square, cube, exp, logsigmoid, loggamma, log, nobackprop, scalegradient, identity, negate, rectify, logistic, softsign, silu,
       sinh, cosh, asinh, acosh, atanh, sin, cos, tan, asin, acos, atan, plus_const, concat, cmult, csum, sum, squared_distance, softmax, pnls, pickrange, scalar_mult,
       input, scalar_input, lookup,
       COMPLEX,
diff --git a/dynet/simd-functors.h b/dynet/simd-functors.h
index d4624ee06..9e2b66a38 100644
--- a/dynet/simd-functors.h
+++ b/dynet/simd-functors.h
@@ -74,12 +74,11 @@ namespace dynet {
 template<typename Scalar> struct scalar_logistic_sigmoid_op {
   EIGEN_EMPTY_STRUCT_CTOR(scalar_logistic_sigmoid_op)
   DYNET_DEVICE_FUNC inline const Scalar operator() (const Scalar& x) const {
-    using std::exp;
     const Scalar one = Scalar(1.0);
     if (x >= 0.0){
-        return one / (one + exp(-x));
+        return one / (one + expf(-x));
     }else{
-        return exp(x) / (one + exp(x));
+        return expf(x) / (one + expf(x));
     }
   }
   template <typename Packet>
@@ -105,6 +104,78 @@ struct functor_traits<dynet::scalar_logistic_sigmoid_op<Scalar> > {
 };
 } }
 
+namespace dynet {
+template<typename Scalar> struct scalar_log_sigmoid_forward_op {
+  EIGEN_EMPTY_STRUCT_CTOR(scalar_log_sigmoid_forward_op)
+  DYNET_DEVICE_FUNC inline const Scalar operator() (const Scalar& x) const {
+    using std::log1pf;
+    // distinguish between positive and negative values of x for precision
+    if (x>0)
+        return -log1pf(expf(-x));
+    else
+        return x - log1pf(expf(x));
+  }
+  template <typename Packet>
+  DYNET_DEVICE_FUNC inline Packet packetOp(const Packet& x) const {
+    using namespace Eigen::internal;
+    const Packet minus_one = pset1<Packet>(-1.0);
+    // Trick to mimick a condition do the computation for both cases and take the min/max with a "pivot" value (here -1) then add. Then substract the excess -1
+    return pmin(
+            padd(
+             // Negative case (close to x)
+             pmin(
+                 minus_one,
+                 psub(x, plog1p(pexp(x)))
+                 ),
+             // Positive case (close to 0)
+             pmax(
+                 minus_one,
+                 pnegate(plog1p(pexp(pnegate(x))))
+                 )
+             ),
+            minus_one);
+  }
+};
+}
+
+namespace Eigen { namespace internal {
+template<typename Scalar>
+struct functor_traits<dynet::scalar_log_sigmoid_forward_op<Scalar> > {
+  enum {
+    Cost = NumTraits<Scalar>::AddCost *6 + NumTraits<Scalar>::MulCost * 4,
+    PacketAccess = packet_traits<Scalar>::HasAdd && packet_traits<Scalar>::HasSub && 
+                   packet_traits<Scalar>::HasMin && packet_traits<Scalar>::HasMax && 
+                   packet_traits<Scalar>::HasLog1p && packet_traits<Scalar>::HasExp &&
+                   packet_traits<Scalar>::HasNegate
+  };
+};
+} }
+
+namespace dynet {
+template<typename Scalar> struct scalar_log_sigmoid_backward_op {
+  EIGEN_EMPTY_STRUCT_CTOR(scalar_log_sigmoid_backward_op)
+  DYNET_DEVICE_FUNC EIGEN_STRONG_INLINE const Scalar operator() (const Scalar& t, const Scalar& d) const { 
+    return (1 - expf(t)) * d;
+  }
+  template<typename Packet>
+  DYNET_DEVICE_FUNC EIGEN_STRONG_INLINE const Packet packetOp(const Packet& t, const Packet& d) const {
+    using namespace Eigen::internal;
+    const Packet one = pset1<Packet>(1);
+    return pmul(psub(one, pexp(t)), d);
+  }
+};
+}
+
+namespace Eigen { namespace internal {
+template<typename Scalar>
+struct functor_traits<dynet::scalar_log_sigmoid_backward_op<Scalar> > {
+  enum {
+    Cost = NumTraits<Scalar>::AddCost + 2 * NumTraits<Scalar>::MulCost,
+    PacketAccess = packet_traits<Scalar>::HasAdd && packet_traits<Scalar>::HasMul && packet_traits<Scalar>::HasExp
+  };
+};
+}}
+
 namespace dynet {
 template<typename Scalar> struct scalar_sqrt_backward_op {
   EIGEN_EMPTY_STRUCT_CTOR(scalar_sqrt_backward_op)
@@ -373,9 +444,8 @@ namespace dynet {
 template<typename Scalar> struct scalar_erf_backward_op {
   EIGEN_EMPTY_STRUCT_CTOR(scalar_erf_backward_op)
   DYNET_DEVICE_FUNC inline const Scalar operator() (const Scalar& x, const Scalar& d) const {
-    using std::exp;
     const Scalar sqrt_pi_over2(1.1283791670955125738961589);
-    return sqrt_pi_over2 * exp(-x * x) * d;
+    return sqrt_pi_over2 * expf(-x * x) * d;
   }
   template <typename Packet>
   DYNET_DEVICE_FUNC inline Packet packetOp(const Packet& x, const Packet& d) const {
@@ -452,8 +522,7 @@ namespace dynet {
 template<typename Scalar> struct scalar_nlsoftmax_backward_op {
   scalar_nlsoftmax_backward_op(const Scalar& lz, const Scalar& err) : logz(lz), d(err) {}
   DYNET_DEVICE_FUNC EIGEN_STRONG_INLINE const Scalar operator()(const Scalar& t) const {
-    using std::exp;
-    return exp(t - logz) * d;
+    return expf(t - logz) * d;
   }
   template <typename Packet>
   DYNET_DEVICE_FUNC EIGEN_STRONG_INLINE const Packet packetOp(const Packet& t) const {
diff --git a/python/_dynet.pxd b/python/_dynet.pxd
index 2f6a3b6e6..0a7d3d48c 100644
--- a/python/_dynet.pxd
+++ b/python/_dynet.pxd
@@ -326,6 +326,7 @@ cdef extern from "dynet/expr.h" namespace "dynet":
     CExpression c_erf "dynet::erf" (CExpression& x) except + #
     CExpression c_cube "dynet::cube" (CExpression& x) except + #
     CExpression c_log "dynet::log" (CExpression& x) except + #
+    CExpression c_log_sigmoid "dynet::log_sigmoid" (CExpression& x) except + #
     CExpression c_lgamma "dynet::lgamma" (CExpression& x) except + #
     CExpression c_logistic "dynet::logistic" (CExpression& x) except + #
     CExpression c_rectify "dynet::rectify" (CExpression& x) except + #        
diff --git a/python/_dynet.pyx b/python/_dynet.pyx
index 65c4c94fb..b1b56b53e 100644
--- a/python/_dynet.pyx
+++ b/python/_dynet.pyx
@@ -3246,6 +3246,19 @@ cpdef Expression log(Expression x):
         dynet.Expression: :math:`y_i = \ln(x_i)`
     """
     return Expression.from_cexpr(x.cg_version, c_log(x.c()))
+cpdef Expression log_sigmoid(Expression x): 
+    """Log sigmoid
+    
+    Calculate elementwise log gamma function :math:`y_i = \ln(\\frac{1}{1+e^{x_i}})`
+    This is more numerically stable than `log(logistic(x))`
+    
+    Args:
+        x (dynet.Expression): Input expression
+    
+    Returns:
+        dynet.Expression: :math:`y_i = \ln(\\frac{1}{1+e^{x_i}})`
+    """
+    return Expression.from_cexpr(x.cg_version, c_log_sigmoid(x.c()))
 cpdef Expression lgamma(Expression x): 
     """Log gamma
     
```

---

## 3. Test Patch

```diff
diff --git a/tests/test-nodes.cc b/tests/test-nodes.cc
index 67f46eb45..1ed6ffadb 100644
--- a/tests/test-nodes.cc
+++ b/tests/test-nodes.cc
@@ -893,6 +893,15 @@ BOOST_AUTO_TEST_CASE( cube_gradient ) {
   BOOST_CHECK(check_grad(mod, z, 0));
 }
 
+// Expression log_sigmoid(const Expression& x);
+BOOST_AUTO_TEST_CASE( log_sigmoid_gradient ) {
+  dynet::ComputationGraph cg;
+  Expression x2 = parameter(cg, param2);
+  Expression y = log_sigmoid(x2);
+  Expression z = to_scalar(y);
+  BOOST_CHECK(check_grad(mod, z, 0));
+}
+
 // Expression lgamma(const Expression& x);
 BOOST_AUTO_TEST_CASE( lgamma_gradient ) {
   dynet::ComputationGraph cg;
```

---

## 4. Relevant Tests & Blockers Distribution

### Narrow Tests Exist
```text
No
```

### Relevant Tests
```json
[
  "test-nodes::node_test/strided_select_gradient4",
  "test-nodes::node_test/scalarmultiply_gradient",
  "test-nodes::node_test/contract3d_batch_1d_gradient",
  "test-trainers::trainer_test/cyclical_sgd_direction",
  "test-nodes::node_test/std_dim_gradient3",
  "test-rnn::rnn_test/lstm_node_multi_input_fwd",
  "test-nodes::node_test/cdiv_broadcast3_gradient",
  "test-nodes::node_test/colwise_add_batch2_gradient",
  "test-nodes::node_test/min_gradient",
  "test-nodes::node_test/weight_norm_backward_gradient",
  "test-nodes::node_test/argmax_forward",
  "test-nodes::node_test/circ_conv_gradient",
  "test-nodes::node_test/cadd_broadcast3_gradient",
  "test-nodes::node_test/hingeptr_gradient",
  "test-nodes::node_test/scalar_expr_add_2_gradient",
  "test-nodes::node_test/sinh_gradient",
  "test-nodes::node_test/contract3d_1d_gradient",
  "test-nodes::node_test/log_gradient",
  "test-nodes::node_test/pickptr_gradient",
  "test-nodes::node_test/sparse_input_test",
  "test-nodes::node_test/contract3d_batch_1d_batch_gradient",
  "test-rnn::rnn_test/lstm_node_fwd",
  "test-nodes::node_test/logsumexp_gradient",
  "test-rnn::rnn_test/lstm_node_c_gradient",
  "test-nodes::node_test/cmult_gradient",
  "test-nodes::node_test/std_dim_gradient4",
  "test-nodes::node_test/abs_gradient",
  "test-nodes::node_test/l2_norm_gradient",
  "test-nodes::node_test/moment_dim_gradient3",
  "test-softmax::softmax_test/standard_softmax_batch_grad",
  "test-io::io_test/test_save_populate_parameter",
  "test-nodes::node_test/average_gradient",
  "test-nodes::node_test/gradient_sanity_test",
  "test-nodes::node_test/acosh_gradient",
  "test-nodes::node_test/negate_gradient",
  "test-rnn::rnn_test/lstm_node_dropout_multi_input_fwd",
  "test-nodes::node_test/concatenate_batch_gradient",
  "test-nodes::node_test/multiplyscalar_gradient",
  "test-nodes::node_test/select_cols_multiple_gradient",
  "test-nodes::node_test/zeros_value",
  "test-exec::exec_test/autobatch_lstm_gradient",
  "test-nodes::node_test/contract3d_1d_1d_gradient",
  "test-params::params_test/set_value",
  "test-nodes::node_test/filter1d_narrow_gradient",
  "test-params::params_test/test_parameter_class",
  "test-nodes::node_test/max_gradient",
  "test-nodes::node_test/cmult_broadcast2_gradient",
  "test-nodes::node_test/colwise_add_batch1_gradient",
  "test-nodes::node_test/cmult_broadcast3_gradient",
  "test-nodes::node_test/addscalar_gradient",
  "test-nodes::node_test/sum_gradient",
  "test-nodes::node_test/circ_corr_gradient",
  "test-nodes::node_test/cdiv_broadcast_gradient_scalar",
  "test-nodes::node_test/std_batches_gradient",
  "test-trainers::trainer_test/simple_sgd_direction",
  "test-nodes::node_test/reshape_gradient",
  "test-nodes::node_test/maxpooling2d_same_gradient",
  "test-nodes::node_test/strided_select_gradient3",
  "test-nodes::node_test/scalar_expr_sub_2_gradient",
  "test-trainers::trainer_test/momentum_sgd_direction",
  "test-nodes::node_test/maxpooling2d_same_gradient_two",
  "test-nodes::node_test/average_cols_gradient",
  "test-tensor::tensor_test/argmax",
  "test-nodes::node_test/selu_gradient",
  "test-nodes::node_test/multiply_batch_gradient",
  "test-nodes::node_test/silu_gradient",
  "test-dim::dim_test/test_dim_truncate_no_trailing_one",
  "test-trainers::trainer_test/amsgrad_direction",
  "test-nodes::node_test/cadd_broadcast2_gradient",
  "test-softmax::softmax_test/cf_softmax_batch_grad",
  "test-nodes::node_test/conv2d_same_gradient",
  "test-nodes::node_test/std_dim_value",
  "test-nodes::node_test/log_softmax_autobatch_gradient",
  "test-nodes::node_test/binary_log_loss_gradient",
  "test-trainers::trainer_test/adadelta_direction",
  "test-dim::dim_test/test_dim_truncate_all_one",
  "test-nodes::node_test/l2_norm_batch_gradient",
  "test-nodes::node_test/kmax_pooling_keq1_gradient",
  "test-nodes::node_test/scalar_expr_add_1_gradient",
  "test-nodes::node_test/cadd_broadcast2_neg_val",
  "test-nodes::node_test/pick_range_dim_gradient",
  "test-rnn::rnn_test/vanilla_lstm_ln_gradient",
  "test-nodes::node_test/select_rows_autobatch_gradient",
  "test-nodes::node_test/cos_gradient",
  "test-nodes::node_test/pairwise_rank_loss_gradient",
  "test-nodes::node_test/acos_gradient",
  "test-nodes::node_test/softmax_cols_colbatch_gradient",
  "test-nodes::node_test/conv2d_valid_gradient",
  "test-nodes::node_test/pickneglogsoftmax_batch_gradient",
  "test-nodes::node_test/cdiv_batch_gradient",
  "test-nodes::node_test/squared_distance_batchleft_gradient",
  "test-nodes::node_test/add_gradient",
  "test-nodes::node_test/logsumexp_vector_gradient",
  "test-nodes::node_test/pick_gradient",
  "test-nodes::node_test/sparsemax_loss_gradient",
  "test-nodes::node_test/cmult_broadcast_gradient_scalar",
  "test-trainers::trainer_test/adagrad_direction",
  "test-nodes::node_test/sum_elems_gradient",
  "test-nodes::node_test/reshape_batch_gradient",
  "test-nodes::node_test/hinge_dim_gradient",
  "test-nodes::node_test/atan_gradient",
  "test-nodes::node_test/conv2d_valid_singlefilter_gradient",
  "test-io::io_test/test_save_populate_sub_pc",
  "test-nodes::node_test/asinh_gradient",
  "test-nodes::node_test/argmax_backward",
  "test-softmax::softmax_test/cf_softmax_grad",
  "test-nodes::node_test/hinge_multiple_gradient",
  "test-trainers::trainer_test/adam_direction",
  "test-nodes::node_test/scalaradd_gradient",
  "test-nodes::node_test/scalar_cdiv_batch2_gradient",
  "test-nodes::node_test/sum_cols_gradient",
  "test-nodes::node_test/strided_select_gradient_noop",
  "test-nodes::node_test/lookup_autobatch_dim_test",
  "test-nodes::node_test/sparsemax_gradient",
  "test-nodes::node_test/concatenate_cols_gradient",
  "test-nodes::node_test/maxpooling2d_valid_gradient",
  "test-rnn::rnn_test/lstm_node_multi_input_bwd",
  "test-nodes::node_test/lookup_autobatch_diffmodel_test",
  "test-nodes::node_test/log_sigmoid_gradient",
  "test-nodes::node_test/dot_product_batch_gradient",
  "test-nodes::node_test/log_softmax_colbatch_gradient",
  "test-nodes::node_test/straight_through_backward",
  "test-nodes::node_test/cube_gradient",
  "test-nodes::node_test/scalar_expr_sub_1_gradient",
  "test-nodes::node_test/binary_log_loss_edgecases",
  "test-rnn::rnn_test/gru_gradient",
  "test-nodes::node_test/select_rows_gradient",
  "test-params::params_test/scale_grad",
  "test-nodes::node_test/fold_rows_gradient",
  "test-nodes::node_test/strided_select_gradient5",
  "test-nodes::node_test/scalar_expr_add_batch1_gradient",
  "test-nodes::node_test/possion_loss_gradient",
  "test-nodes::node_test/affine_gradient",
  "test-nodes::node_test/tanh_gradient",
  "test-nodes::node_test/mean_dim_gradient",
  "test-nodes::node_test/concatenate_cols_vecmatrix_gradient",
  "test-nodes::node_test/lookup_autobatch_and_manbatch_test",
  "test-nodes::node_test/mean_batches_gradient_multidim",
  "test-nodes::node_test/exp_gradient",
  "test-params::params_test/test_parametercollection_with_builder",
  "test-nodes::node_test/cadd_scalar_gradient",
  "test-rnn::rnn_test/fast_lstm",
  "test-nodes::node_test/lgamma_gradient",
  "test-params::params_test/init_saxe",
  "test-nodes::node_test/concatenate_to_batch_gradient",
  "test-nodes::node_test/squared_distance_batchboth_gradient",
  "test-nodes::node_test/std_dim_gradient",
  "test-nodes::node_test/affine_batch2_gradient",
  "test-nodes::node_test/layer_norm_forward",
  "test-nodes::node_test/colwise_add_gradient",
  "test-nodes::node_test/squared_distance_gradient",
  "test-nodes::node_test/pick_batch_gradient",
  "test-nodes::node_test/moment_dim_gradient4",
  "test-io::io_test/test_save_populate_pc",
  "test-rnn::rnn_test/lstm_node_dropout_batch_bwd",
  "test-nodes::node_test/asin_gradient",
  "test-nodes::node_test/moment_batches_gradient",
  "test-nodes::node_test/pickneglogsoftmax_gradient",
  "test-nodes::node_test/restricted_log_softmax_gradient",
  "test-nodes::node_test/scalar_expr_sub_batch1_gradient",
  "test-nodes::node_test/erf_gradient",
  "test-nodes::node_test/squared_distance_batchright_gradient",
  "test-nodes::node_test/squared_norm_batch_gradient",
  "test-nodes::node_test/sqrt_gradient",
  "test-nodes::node_test/scalarsubtract_gradient",
  "test-rnn::rnn_test/lstm_node_gates_dropout_fwd",
  "test-dim::dim_test/test_dim_truncate_multiple_one",
  "test-nodes::node_test/logsumexp_inequal_batch_gradient",
  "test-nodes::node_test/affine_batch_col_gradient",
  "test-nodes::node_test/contract3d_1d_batch_gradient",
  "test-nodes::node_test/log_softmax_gradient",
  "test-nodes::node_test/pick_batch_broadcast_gradient",
  "test-nodes::node_test/lookup_matrix_test",
  "test-nodes::node_test/logsumexp_singleelem_batch_gradient",
  "test-io::io_test/test_save_load_parameter_nonzerograd",
  "test-nodes::node_test/transpose_higherorder_gradient",
  "test-nodes::node_test/lookup_test",
  "test-nodes::node_test/scalar_expr_sub_batch2_gradient",
  "test-params::params_test/test_parameter_collection",
  "test-nodes::node_test/softmax_batch_gradient",
  "test-nodes::node_test/sum_dim_gradient",
  "test-nodes::node_test/moment_dim_gradient",
  "test-nodes::node_test/pick_range_gradient",
  "test-nodes::node_test/affine_batch_gradient",
  "test-nodes::node_test/concatenate_gradient",
  "test-nodes::node_test/inverse_gradient",
  "test-nodes::node_test/scalar_cmult_batch_gradient",
  "test-trainers::trainer_test/simple_sgd_update_subset",
  "test-nodes::node_test/dividescalar_gradient",
  "test-nodes::node_test/std_elems_gradient",
  "test-trainers::trainer_test/momentum_restart_correctness",
  "test-nodes::node_test/affine_batch3_gradient",
  "test-nodes::node_test/dot_product_matrix_gradient",
  "test-nodes::node_test/select_cols_oob",
  "test-nodes::node_test/atanh_gradient",
  "test-nodes::node_test/weight_norm_forward",
  "test-nodes::node_test/trace_of_product_gradient",
  "test-nodes::node_test/rectify_gradient",
  "test-nodes::node_test/strided_select_gradient2",
  "test-rnn::rnn_test/compact_vanilla_lstm_gradient",
  "test-nodes::node_test/elu_gradient",
  "test-nodes::node_test/layer_norm_backward_gradient",
  "test-nodes::node_test/logdet_gradient",
  "test-rnn::rnn_test/lstm_node_batched_forward",
  "test-nodes::node_test/hinge_batch_gradient",
  "test-nodes::node_test/softmax_gradient",
  "test-nodes::node_test/cmult_batch_gradient",
  "test-nodes::node_test/moment_dim_gradient2",
  "test-nodes::node_test/gradient_value_test",
  "test-nodes::node_test/select_rows_multiple_gradient",
  "test-rnn::rnn_test/lstm_node_dropout_bwd",
  "test-softmax::softmax_test/standard_softmax_grad",
  "test-params::params_test/scale",
  "test-nodes::node_test/cosh_gradient",
  "test-nodes::node_test/select_rows_oob",
  "test-trainers::trainer_test/rmsprop_direction",
  "test-nodes::node_test/cdiv_gradient",
  "test-nodes::node_test/cadd_gradient",
  "test-nodes::node_test/constant_value",
  "test-nodes::node_test/sin_gradient",
  "test-nodes::node_test/scalar_cdiv_gradient",
  "test-nodes::node_test/softmax_colbatch_gradient",
  "test-nodes::node_test/scalar_cmult_gradient",
  "test-nodes::node_test/sum_batch_gradient",
  "test-nodes::node_test/scalar_expr_add_batch2_gradient",
  "test-nodes::node_test/huber_distance_gradient",
  "test-nodes::node_test/kmax_pooling_keq2_gradient",
  "test-rnn::rnn_test/lstm_node_gates_fwd",
  "test-nodes::node_test/softsign_gradient",
  "test-nodes::node_test/mean_elems_gradient",
  "test-rnn::rnn_test/lstm_node_gates_bwd",
  "test-nodes::node_test/select_cols_gradient",
  "test-trainers::trainer_test/eg_direction",
  "test-nodes::node_test/sum_batches_gradient",
  "test-nodes::node_test/sanity_test",
  "test-rnn::rnn_test/lstm_node_h_fwd",
  "test-nodes::node_test/scalar_cdiv_batch1_gradient",
  "test-io::io_test/test_save_load_parameter",
  "test-nodes::node_test/logistic_gradient",
  "test-nodes::node_test/dot_product_gradient",
  "test-nodes::node_test/pick_batch_elem_gradient",
  "test-nodes::node_test/strided_select_gradient",
  "test-nodes::node_test/moment_elems_gradient",
  "test-nodes::node_test/l1_distance_gradient",
  "test-rnn::rnn_test/simple_rnn_gradient",
  "test-nodes::node_test/hinge_gradient",
  "test-rnn::rnn_test/lstm_node_c_fwd",
  "test-nodes::node_test/logsumexp_dim_gradient",
  "test-nodes::node_test/multiply_gradient",
  "test-nodes::node_test/tan_gradient",
  "test-nodes::node_test/mean_batches_gradient",
  "test-nodes::node_test/subtractscalar_gradient",
  "test-rnn::rnn_test/vanilla_lstm_gradient",
  "test-nodes::node_test/square_gradient",
  "test-dim::dim_test/test_dim_truncate_trailing_one",
  "test-dynet::aligned_allocator",
  "test-rnn::rnn_test/lstm_node_dropout_multi_input_bwd",
  "test-rnn::rnn_test/lstm_node_h_gradient",
  "test-nodes::node_test/pick_batch_elems_gradient",
  "test-nodes::node_test/cadd_broadcast_gradient_scalar",
  "test-nodes::node_test/log_softmax_batch_gradient",
  "test-nodes::node_test/pow_gradient",
  "test-rnn::rnn_test/lstm_node_bwd",
  "test-nodes::node_test/transpose_gradient",
  "test-nodes::node_test/squared_norm_gradient",
  "test-nodes::node_test/cdiv_broadcast2_gradient",
  "test-nodes::node_test/subtract_gradient",
  "test-rnn::rnn_test/lstm_gradient"
]
```

### Blockers Distribution
Se requiere generar exactamente **5 bloqueadores** en total:
- **3** `missing parameter blockers`
- **1** `ambiguous requirements blocker`
- **1** `contradictory requirements blocker`
