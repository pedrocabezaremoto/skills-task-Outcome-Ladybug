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
