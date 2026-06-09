# Notas de implementación — Blockers Task 02 (dynet log_sigmoid) — set TESTEABLE

> Acompaña a `blocker_registry_testable.json`. Estos 5 blockers se construyeron a mano priorizando **TESTEABILIDAD**: cada uno cambia un observable (valor forward, gradiente o forma) que un narrow test valida, de modo que **si el agente adivina mal, su patch FALLA**. (Las versiones auto-generadas fallaron: ronda 1 = recuperables del repo; ronda 2 = no testeables.)
> **Escenario:** 2 (Codebase Modifications Required). **Distribución:** mp=3, ar=1, cr=1.
> **Última actualización:** 2026-06-09

---

## Resumen de los 5 blockers

| # | id | tipo | observable que pinea el test | ¿el agente puede FALLAR? | confianza |
|---|---|---|---|---|---|
| 1 | `negative_tail_stability` | mp | forward en x=-30 (finito ≈ -30) | ✅ naive `log(sigmoid)` → -inf | 🟢 buena |
| 2 | `logarithm_base` | ar | forward en x=0 (≈ -0.6931 = ln) | ✅ log10 → -0.301 | 🟡 media |
| 3 | `negative_tail_gradient` | mp | gradiente en x=-30 (≈ 1.0) | ⚠️ parcial (ver riesgos) | 🟠 baja |
| 4 | `elementwise_vs_reduction` | cr | forma de salida (vector→vector) | ✅ si reduce → shape mismatch | 🟡 media |
| 5 | `positive_tail_saturation` | mp | forward en x=+30 (≈ 0⁻, finito) | ⚠️ débil (ver riesgos) | 🟠 baja |

---

## Test que valida cada blocker (lo que hay que poner en el test_patch_obstructed)

- **#1:** `Expression y = log_sigmoid(input(-30.0)); BOOST_CHECK(std::isfinite(y_val) && std::abs(y_val - (-30.0)) < 1e-2);`
- **#2:** `Expression y = log_sigmoid(input(0.0)); BOOST_CHECK(std::abs(y_val - (-0.6931f)) < 1e-3);`
- **#3:** gradient check / `BOOST_CHECK(std::abs(grad_at(-30.0) - 1.0f) < 1e-2);`
- **#4:** input shape `{4}` → `BOOST_CHECK(y.dim() == Dim({4}));` (si el agente reduce a escalar, falla).
- **#5:** `Expression y = log_sigmoid(input(30.0)); BOOST_CHECK(std::isfinite(y_val) && y_val <= 0.0f && y_val > -1e-6f);`

> El `check_grad` original se mantiene; estos se AGREGAN como narrow tests.

## Qué tocar en el texto (Part 4) y en los patches

- **#1, #3, #5 (estabilidad/colas):** en Requirements, **quitar** cualquier mención a "numerically stable" / "more stable than log(logistic)". El golden ya es estable (`x - log1pf(expf(x))`), no se reescribe — solo NO revelar el detalle en el texto.
- **#2 (base):** en Problem Statement/Requirements decir solo "logarithm of the sigmoid" (sin "natural"). Golden usa `log1pf` (ln), no cambia.
- **#4 (contradicción):** **plantar las dos exigencias chocantes en Requirements** — "must collapse the input into a single aggregate log-likelihood" + "must return an expression with the same shape as the input". El golden ya es elementwise (`dim_forward → xs[0]`).
- **setup_patch:** opcionalmente quitar comentarios/doc del header (`expr.h`) que dicen la fórmula exacta y "more numerically stable than log(logistic(x))", para que #1/#3/#5 no se adivinen leyendo el doc.

---

## Independencia (honesto)

- **#1** = valor forward en cola NEGATIVA.
- **#2** = valor forward en x=0 (base del log).
- **#3** = valor del GRADIENTE en cola negativa.
- **#4** = FORMA de la salida.
- **#5** = valor forward en cola POSITIVA.

Cinco observables distintos. **Riesgo de dependencia leve #1↔#3** (ambos cola negativa) — pero uno mide el forward y el otro el gradiente, tests separados. Aceptable, pero es el punto más débil de independencia.

---

## ⚠️ RIESGOS — leer antes de implementar

1. **#3 (negative_tail_gradient):** el gradiente de log_sigmoid es matemáticamente único (`sigmoid(-x)`). Un agente competente lo computa bien por cálculo. El único "diente" real es la estabilidad numérica en x=-30, y el `check_grad` (diferencias finitas) puede no estresar ese extremo. **Candidato a rebotar** como "no fuerza pregunta". Es el más flojo de los mp.
2. **#5 (positive_tail_saturation):** en la cola POSITIVA, hasta `log(sigmoid(x))` ingenuo funciona (sigmoid(30)≈1, log(1)=0). El caso de fallo es débil — solo falla si el agente hace algo raro (clamp, signo). **Relleno testeable.**
3. **#2 (logarithm_base):** lectura dominante (en ML "log" = ln). Defendible porque el texto no dice "natural", pero puede rebotar como `dominant_reading`.
4. **#4 (elementwise_vs_reduction):** "elementwise" es el default obvio. La contradicción inyectada lo vuelve pregunta real, pero el eval puede marcarlo como `satisfiable`/obvio.

**Sólido de verdad: solo #1.** #2 y #4 medios. #3 y #5 flojos pero testeables.

---

## 🚩 FLAG OBLIGATORIO AL ENTREGAR — TAREA DELGADA

Esta tarea (`log_sigmoid`) es **matemáticamente delgada**: tiene **un solo eje fuerte** que es a la vez observable + testeable + no-recuperable (la **estabilidad numérica**). Se confirmó en 3 intentos:
- Ronda 1 (auto): blockers recuperables copiando ops hermanas.
- Ronda 2 (auto): blockers no-testeables (detalles internos que no cambian el output).
- Set manual (este): testeables, pero solo ~1-2 fuertes; el resto es relleno honesto.

**Informar al equipo en el submit** que la tarea no soporta 5 blockers fuertes e independientes, y que se entrega el mejor esfuerzo testeable para iterar vía SBQ.

---

## Recordatorios
- **THIN SPACE (U+2009)** en la entrega final o score = 0.
- `description` nunca revela la respuesta ni dice "se quitó X" (self-reference rebota).
- Las contradicciones (#4) van **plantadas en el texto** de Requirements, no solo en el registry.
