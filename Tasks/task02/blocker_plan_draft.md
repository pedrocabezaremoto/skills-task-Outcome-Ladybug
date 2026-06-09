# Borrador Blocker Plan — Task 02 (dynet / log_sigmoid)

> Part 3.1 de la Guía 1. Borrador de los 5 blockers ANTES de tocar nada.
> Basado en el código real del commit `0e5addb8` (bajado de GitHub) + requerimientos del panel.
> **Escenario:** 2 (Codebase Modifications Required) — Narrow Tests = No.
> **Distribución:** 3 missing_parameter + 1 ambiguous + 1 contradictory.
> **Última actualización:** 2026-06-09

---

## Contexto técnico (lo que revela el golden patch)

- **Forward estable con branching:** `x>0 → -log1pf(expf(-x))` ; `x≤0 → x - log1pf(expf(x))`. El doc dice: *"more numerically stable than `log(logistic(x))`"*.
- **Backward:** `(1 - expf(fx)) * dEdf` = `1 - sigmoid(x)`. Usa la salida `fx`, no la entrada.
- **Log natural (ln)** vía `log1pf`. **float32** (`expf`/`log1pf`).
- **Multibatch:** `supports_multibatch() = true`. `dim_forward` devuelve `xs[0]` (misma forma).
- **Test original:** solo `log_sigmoid_gradient` (un `check_grad`).

> ⚠️ **Tarea matemáticamente "delgada":** las únicas palancas fuertes y testeables son **estabilidad numérica** y **base del log**. Los demás blockers salen débiles. Ver sección de RIESGOS.

---

## Resumen de los 5 blockers (borrador)

| # | id | tipo | área | eje (independiente) | ¿cambia golden? | ¿test nuevo? | confianza |
|---|---|---|---|---|---|---|---|
| 1 | `negative_tail_stability` | missing | requirements | salida finita en x muy negativo (no -inf) | ❌ no (ya es estable) | ✅ sí | 🟢 buena |
| 2 | `log_base` | ambiguous | requirements | base del logaritmo (ln vs log10) | ❌ no | ✅ sí | 🟡 media (lectura dominante) |
| 3 | `stable_vs_composition` | contradictory | requirements | método: nodo estable dedicado vs componer `log(logistic(x))` | ❌ no | ✅ sí | 🟢 buena (grounded en el doc) |
| 4 | `multibatch_support` | missing | public_interface | soporta batch + preserva Dim | ❌ no (ya soporta) | ✅ sí | 🟠 baja — REVISAR |
| 5 | `positive_tail_gradient` | missing | requirements | gradiente → 0 en x muy positivo | ❌ no | ✅ sí | 🟠 baja — REVISAR |

> ✅ Ningún blocker necesita área `codebase` → **no haría falta setup_patch** (salvo que al "destapar" el texto haya que quitar pistas del código; revisar).

---

## Detalle por blocker (Decision Point / Expected Outcome / Location / Test)

### #1 `negative_tail_stability` — missing_parameter 🟢
- **Decision Point:** ¿qué devuelve `log_sigmoid` para un x muy negativo (saturación)?
- **Expected Outcome:** valor **finito ≈ x** (p.ej. `log_sigmoid(-30) ≈ -30`), nunca `-inf`/`NaN`.
- **Location (texto a aflojar):** Requirements — quitar cualquier mención a estabilidad/"more stable than log(logistic)".
- **Resolución (oculta, va al registry):** debe ser numéricamente estable; para `x≤0` usar `x - ln(1+e^x)`. `log_sigmoid(-30) ≈ -30.0` (tol 1e-3).
- **Test nuevo:** assert `log_sigmoid(-30)` finito y `|res-(-30)| < 1e-3`. Un `log(logistic(x))` ingenuo da `-inf` → falla.

### #2 `log_base` — ambiguous_requirement 🟡
- **Element ambiguo:** "logarithm of the sigmoid" — no dice qué base.
- **Lectura A (ln):** `log_sigmoid(0)=ln(0.5)≈-0.6931`; grad = `1-sigmoid(x)`.
- **Lectura B (log10):** `log_sigmoid(0)=log10(0.5)≈-0.3010`; grad escalado por `1/ln(10)`.
- **Resolución:** **log natural (ln)** (golden usa `log1pf`).
- **Test nuevo:** assert `log_sigmoid(0) ≈ -0.6931`.
- **⚠️ Riesgo:** en ML "log" = ln es lectura dominante → puede rebotar como `dominant_reading`.

### #3 `stable_vs_composition` — contradictory_requirement 🟢
- **Req A (inyectar):** "por claridad, implementar `log_sigmoid` componiendo las ops existentes `log` y `logistic` (es decir `log(logistic(x))`)."
- **Req B (inyectar):** "la operación debe ser numéricamente estable y nunca producir `inf`/`NaN` para inputs de gran magnitud."
- **Por qué se contradicen:** `log(logistic(x))` literal se desborda a `-inf` en x muy negativo → no puede ser estable. No se satisfacen ambas.
- **Resolución:** nodo dedicado estable (NO composición literal); priorizar estabilidad. Golden = nodo `LogSigmoid` con branching.
- **Test:** mismo de estabilidad (finito en -30).
- **⚠️ SOLAPA con #1** (ambos se validan con "finito en -30"). Ver RIESGOS.

### #4 `multibatch_support` — missing_parameter 🟠
- **Decision Point:** ¿debe soportar input por lotes (multibatch) y preservar la forma?
- **Expected Outcome:** input batched procesado elementwise, `Dim` salida == `Dim` entrada.
- **Resolución:** debe soportar multibatch (golden: `supports_multibatch()=true`, `dim_forward → xs[0]`).
- **Test nuevo:** input batched → checar forma + valores.
- **⚠️ Débil:** un agente lo hace de forma natural (elementwise). Candidato a rebotar como `small_answer_space`.

### #5 `positive_tail_gradient` — missing_parameter 🟠
- **Decision Point:** ¿cuánto vale el gradiente para x muy positivo?
- **Expected Outcome:** gradiente `→ 0` (porque `d/dx = 1-sigmoid(x) → 0`), finito.
- **Resolución:** grad = `1 - sigmoid(x)`; en `x=+30 ≈ 0`.
- **Test nuevo:** gradient check en x=+30 ≈ 0.
- **Independencia vs #1:** #1 = forward / cola negativa ; #5 = backward / cola positiva (ortogonal-ish).
- **⚠️ Débil:** "gradiente correcto" ya lo pide el requirement → puede verse como no-blocker.

---

## Verificación de INDEPENDENCIA (lo crítico)

- **#1** solo cola negativa del FORWARD (valor finito ≈ x).
- **#2** solo la BASE del log (valor en x=0). No dice nada de estabilidad ni batch.
- **#4** solo forma/batch. Ortogonal a valores.
- **#5** solo cola positiva del BACKWARD (gradiente→0).
- **#3 ↔ #1: SOLAPAN.** Ambos se prueban con "finito en -30". Esto es contaminación/dependencia → hay que resolverlo.

---

## ⚠️ RIESGOS — leer antes de implementar

1. **#1 y #3 se pisan** (misma observación testeable: estabilidad en cola negativa). Opciones:
   - (a) Quedarse con **#3** (contradicción, más fuerte y grounded en el doc) y **reemplazar #1** por otro missing_parameter en otro eje.
   - (b) Quedarse con **#1** y mover la contradicción a otro eje (más difícil de fundamentar aquí).
   - Recomendado: **(a)**.
2. **#2** tiene lectura dominante (ln). Defendible porque el texto literal no dice "natural", pero puede rebotar.
3. **#4 y #5 son débiles** (answer space chico / ya implícitos). Probable feedback negativo en el SBQ.
4. **La tarea es delgada:** material fuerte real = estabilidad + base. Honestamente solo hay ~2 blockers sólidos; los otros 3 son de relleno y casi seguro habrá que iterarlos con el Agent Feedback (el panel mismo dice que el flujo es iterativo vía SBQ).

---

## Recomendación de siguiente paso

1. **Correr el Blocker Registry Generator** (`BlockerGenerator/prompt.md`) con el golden+test patch reales → puede minar puntos de decisión grounded que se me escapen y dar candidatos más fuertes que este análisis a mano.
2. Resolver el solape **#1/#3** (opción a).
3. Recién ahí pasar a Part 4 (modificar el texto) y generar patches.

---

## Recordatorios
- **THIN SPACE (U+2009)** en la entrega final o score = 0.
- `description` nunca revela la respuesta ni dice "se quitó/modificó X" (self-reference rebota).
- Las contradicciones (#3) hay que **plantarlas en el texto** (Requirements), no solo en el registry.
