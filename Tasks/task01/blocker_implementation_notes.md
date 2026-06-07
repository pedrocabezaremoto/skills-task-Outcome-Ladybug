# Notas de implementación — Blockers Task 01

> Acompaña a `blocker_registry_draft.json`. Aquí va lo que NO se pone en el registry: qué hay que cambiar en el código/tests y por qué cada blocker es independiente.
> **Última actualización:** 2026-06-04

---

## Resumen de los 5 blockers

| # | id | tipo | área | eje (independiente) | ¿cambia golden? | ¿test nuevo? | confianza |
|---|---|---|---|---|---|---|---|
| 1 | `null_byte_replacement` | missing | requirements | sustitución de byte (0x00) | ✅ sí | ✅ sí | 🟡 media |
| 2 | `write_return_byte_count` | missing | requirements | valor de retorno `n` | ❌ no (ya es así) | ✅ ya existe | 🟡 media |
| 3 | `inserted_cr_counter_field` | missing | interfaces | campo contador del struct | ✅ sí | ✅ sí | 🟠 baja — REVISAR |
| 4 | `bare_cr_handling` | ambiguous | requirements | transformación del `\r` solo | ❌ no (ya es así) | ✅ sí | 🟢 buena |
| 5 | `cross_call_state_persistence` | contradictory | requirements | vida del estado entre llamadas | ❌ no (ya es así) | ❌ ya existe | 🟢 buena |

> ✅ NINGÚN blocker usa área `codebase` → no necesitamos setup patch (arregla el error #2 del feedback).

---

## Qué hay que tocar en el GOLDEN patch

Solo 2 blockers obligan a modificar el golden (`log/formatters.go`):

- **#1 null_byte_replacement:** dentro del `for`, antes de escribir el byte, si `b == 0x00` escribir `'?'` en vez del byte. (El `?` NO cuenta como `\r` insertado para el contador #3.)
- **#3 inserted_cr_counter_field:** agregar campo exportado `InsertedCRs int` al struct, y `cw.InsertedCRs++` cada vez que se inserta un `\r`.

Los blockers #2, #4 y #5 **ya coinciden con el golden original** (no hay que reescribir, solo NO revelar el detalle en el texto).

---

## Qué hay que tocar en el TEST patch

- **#1:** test que escriba `"h\x00i"` y espere `"h?i"`.
- **#3:** test que verifique `InsertedCRs == 2` tras escribir `"a\nb\n"`.
- **#4:** test `Write("a\rb")` espera salida `"a\rb"` (3 bytes).
- **#2:** YA existe (los tests asertan `n=18`, `n=6`, `n=7`).
- **#5:** YA existe (test `"hello\r"` + `"\nworld\n"` → `"hello\r\nworld\r\n"`).

---

## Verificación de INDEPENDENCIA (lo crítico del feedback)

- **#1** toca solo el byte `0x00`. No afecta `\n`, `\r`, el contador ni el retorno.
- **#2** toca solo el número que devuelve `Write`. No revela nada de los demás.
- **#3** toca solo la declaración del campo contador. No cambia la salida de bytes.
- **#4** decide qué SALE cuando hay un `\r` solo (dejarlo). No dice nada sobre el estado entre llamadas (#5).
- **#5** decide si `lastByte` SOBREVIVE entre llamadas. No dice nada sobre qué hacer con un `\r` solo (#4).

→ Resolver uno NO revela la respuesta de otro. ✅

---

## ⚠️ Punto a REVISAR antes de implementar

**Blocker #3 (`inserted_cr_counter_field`) es el más flojo y tiene una complicación técnica:**
- Es un blocker de "nombre de campo" → la guía marca los blockers de nombre como tirando a cosméticos.
- Problema técnico: `CRLFWriter()` devuelve `io.Writer` (interfaz). Para que el test lea `InsertedCRs`, el test tendría que hacer un *type assertion* al struct concreto, o habría que exponer el contador de otra forma. Esto enreda la interfaz pública.

**Opciones si #3 da problemas en validación:**
- (a) Hacer que el test haga type-assert al `*crlfWriter` exportando el tipo.
- (b) Reemplazar #3 por otro missing_parameter (queda pendiente pensar uno mejor en otro eje).

Decisión: lo dejamos como está para la primera pasada; si el `task_checker` o el Patch Content Validator se quejan, lo cambiamos.

---

## Recordatorios

- THIN SPACE (U+2009) en la entrega final o score = 0.
- `description` nunca revela la respuesta ni dice "se borró/modificó X" (self-reference = rebota).
- La contradicción del #5 hay que **plantarla en el texto**: en Requirements agregar la línea "the writer must reset its character state at the start of each Write call to isolate inputs" (que choca con el problem statement que dice "works in multiple steps").
