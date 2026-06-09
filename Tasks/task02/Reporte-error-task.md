# Reporte de error — Task 02 (dynet / Outcome Ladybug)

> **ID tarea:** `6a2703ae522946e24d096a01`
> **Tipo:** Defecto de setup (Docker baseline incorrecto)
> **Estado:** Detectado el 2026-06-09. Pendiente de reportar al equipo (se reporta al final).

---

## Resumen

El Dockerfile de la tarea fija el repositorio en el **commit equivocado**, por lo que el golden patch **no aplica** sobre el baseline del contenedor.

## Detalle técnico

| Elemento | Commit |
|---|---|
| Commit del golden patch (panel de la tarea) | `0e5addb8066351e2941151b8fe88264c84156636` |
| Parent esperado de ese commit (baseline correcto) | `8ea37f68c6307e0d44cf9c719d23bd3f9793be1e` |
| Commit que el Dockerfile hace `git checkout` | `22b44958476731af4d1fdbc553626eca3a27e808` |

`22b44958` corresponde a *"Updated DynetSharp for .NET 6.0 (#1667)"*, una rama/cambio sin relación con la feature log_sigmoid.

## Evidencia (dentro del contenedor)

```bash
# HEAD del contenedor (incorrecto)
git rev-parse HEAD
# -> 22b44958476731af4d1fdbc553626eca3a27e808

# El golden patch NO aplica sobre 22b44958
git show 0e5addb8... > /tmp/official.diff
git apply --check /tmp/official.diff
# -> error: patch does not apply (todos los archivos:
#    doc/source/python_ref.rst, dynet/expr.cc, dynet/expr.h,
#    dynet/nodes-arith-unary.cc, dynet/sig.h, dynet/simd-functors.h,
#    python/_dynet.pxd, python/_dynet.pyx)

# Sobre el parent correcto 8ea37f68 SÍ aplica
git checkout 8ea37f68c6307e0d44cf9c719d23bd3f9793be1e
git apply --check /tmp/official.diff
# -> ✅ aplica limpio
```

## Impacto

- Sobre `22b44958` no se puede validar ni inyectar blockers (el código base no coincide con el patch).
- El task_checker / validaciones fallarían si se corren contra el baseline del Dockerfile.

## Workaround aplicado

Se trabaja desde `8ea37f68` haciendo `git checkout 8ea37f68...` dentro del contenedor. **Nota:** al reiniciar/reconstruir el contenedor vuelve a `22b44958`; hay que re-aplicar el checkout.

## Fix sugerido para el Dockerfile

```dockerfile
# Cambiar:
RUN git checkout 22b44958476731af4d1fdbc553626eca3a27e808
# Por (parent del golden patch):
RUN git checkout 8ea37f68c6307e0d44cf9c719d23bd3f9793be1e
```

---

# Hallazgo 2 — La tarea es DELGADA / mal candidato para Blocker Injection

> **Tipo:** Defecto de diseño de tarea (no soporta la distribución pedida con blockers válidos).
> **Estado:** Detectado 2026-06-09 mientras se construían/validaban los blockers.

## Resumen
`log_sigmoid` es una función **elementwise sin parámetros** y matemáticamente simple. **No soporta** la distribución pedida (3 missing_parameter + 1 ambiguous + 1 contradictory) con blockers que sean a la vez naturales, críticos, independientes y **no adivinables**. Evidencia acumulada de los propios checks de la plataforma:

## Evidencia

### A. Criteria Builder (AI helper) — 4 tarjetas
- **Contrived:** `elementwise_vs_reduction` (cr) marcado como contradicción artificial → el task **no tiene contradicción natural**.
- **Not Critical:** `logarithm_base` (ar) → la base es convención (ln); no es ambigüedad crítica → el task **no tiene ambigüedad crítica natural**.
- **Description Error:** `negative_tail_stability`, `negative_tail_gradient`, `positive_tail_saturation` están mal tipados como `missing_parameter`; en realidad son ambigüedades de comportamiento, porque **log_sigmoid no tiene parámetros numéricos** que omitir.

### B. Guessability prompt (Guía 11) — corrido en Cursor, 2 modelos
`negative_tail_stability` salió **ADIVINADO por Gemini 3.1 Pro Y GPT-5.4**. Ambos describieron la resolución exacta sin verla:
- "para x muy negativo, log_sigmoid(x) ≈ x, no -inf"
- "gradiente → 1.0 en la cola negativa"
- "elementwise, la reducción a escalar se hace aparte con sum_elems"

**Causas (ninguna culpa del contributor):**
1. **Matemática elemental:** `log_sigmoid(x) ≈ x` para `x→-∞` se deriva por cálculo.
2. **Contaminación del codebase BASELINE (pre-existente):** los agentes encontraron `scalar_logistic_sigmoid_op` (sigmoid estable con rama por signo), `LogSumExp` (comentado como "careful"/estable), y sobre todo **`examples/noise-contrastive-estimation/nce.h`** que YA usa `log(logistic(...))`. Esas pistas existen en el repo desde antes del task.

## Impacto
- Los blockers numéricos (#1/#3/#5) son adivinables vía exploración del codebase + matemática → no fuerzan pregunta (riesgo de fallar Check 1).
- El ar (#2) y el cr (#4) son forzados/contrived.

## Manejo (path A — entregar e iterar)
- Guessability: subir screenshots (incl. adivinadas) + responder **"Yes"** (blockers originales, no introducidos/facilitados por el contributor → no requieren fix, per la nota de la plataforma).
- Submit con esta nota de mal-fit.

## Recomendación al equipo
Esta tarea (`log_sigmoid`) no es buen candidato para Blocker Injection con distribución 3mp+1ar+1cr: no tiene parámetros, ni contradicción/ambigüedad natural, y su comportamiento es matemáticamente derivable + contaminado por ejemplos pre-existentes del repo (`nce.h`). Sugerir reasignar o relajar la distribución.
