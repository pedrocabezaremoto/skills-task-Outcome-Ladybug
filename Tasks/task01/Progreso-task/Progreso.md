# Progreso — Task 01 (Outcome Ladybug / navidrome CRLF)

> **Propósito:** Bitácora de esta tarea para que cualquier LLM (o Pedro) entienda QUÉ es la tarea, en qué punto vamos y qué sigue. Leer junto con `../Requerimientos_task.md` (que tiene todos los datos crudos: problem statement, requirements, interfaces, golden/test patch, workflows, checks).
> **Última actualización:** 2026-06-04

---

## 1. ¿Qué es esta tarea? (contexto para un LLM nuevo)

- **Proyecto Outlier:** Outcome Ladybug = **Blocker Injection**. El trabajo NO es resolver código; es **esconder información** (blockers) en una tarea de código ya resuelta, para que un agente de IA falle si NO pregunta, y acierte si SÍ pregunta (vía un Blocker Registry oculto).
- **Esta tarea es un REWORK (SBQ):** "Improve another contributor's completed task". Otro contribuidor ya la hizo, sacó nota baja (**Overall Task = 2**) y nos la pasaron para corregirla según un feedback.
- **ID tarea:** `6a2198ff7d0d8426c25caeb9`
- **Repo base:** navidrome (lenguaje **Go**).
- **Tema del código:** normalización de saltos de línea (CRLF) en los logs de Windows.
- **Commit link:** https://github.com/navidrome/navidrome/commit/23bebe4e06124becf1000e88472ae71a6ca7de4c
- **Imagen Docker:** `jefzda/sweap-images:navidrome.navidrome-navidrome__navidrome-9c3b4561652a15846993d477003e111f0df0c585`
- **instance-id (para task_checker):** `instance_navidrome__navidrome-9c3b4561652a15846993d477003e111f0df0c585`

---

## 2. ¿Qué hace la SOLUCIÓN del código? (golden patch, en simple)

El golden patch agrega 2 cosas en la carpeta `log/`:

1. **`CRLFWriter` (en `log/formatters.go`):** envoltorio de un `io.Writer` que arregla saltos de línea:
   - Convierte `\n` (LF) → `\r\n` (CRLF).
   - Si ya viene `\r\n`, lo deja igual (no duplica el `\r`).
   - Trabaja **byte por byte**, recordando el último byte (`lastByte`) para no meter `\r` doble.
   - **OJO: el original es SIMPLE, sin buffer, sin variable de entorno, sin flush threshold.**

2. **`SetOutput` (en `log/log.go`):** configura a dónde van los logs. Si el SO es **Windows**, envuelve el writer con `CRLFWriter`; si no, lo deja igual.

Resumen: en Windows, los logs pasan por `CRLFWriter` que normaliza los saltos de línea.

---

## 3. FEEDBACK a corregir (lista de control obligatoria) ⭐

1. ❌ El test y golden patch subidos **NO evaluaban/implementaban los blockers** → archivos incorrectos. Hay que subir patches que SÍ funcionen.
2. ❌ **Obstruction areas incorrectas**: faltaba problem statement e interfaces. Regla: solo poner `codebase` cuando hay setup patch.
3. ❌ **Blockers DEPENDIENTES** (el error grande). Parejas malas:
   - `crlf_override_env_var_name` + `crlf_override_activation_value` = un solo switch partido en dos.
   - `normalization_scope_enforcement` atada a esas dos (revela dónde va el env name y el "true").
   - `standalone_cr_handling_conflict` + `crlf_flush_threshold` = ambas asumen un CRLFWriter con buffer (bare-`\r` vs flush 512 bytes).
4. ✅ Acción pedida: rehacer los blockers dependientes (quedarse con uno de cada pareja, rehacer el otro) y que los patches apliquen/evalúen su resolución.

> **Decisión acordada con Pedro:** revisar TODO desde cero, no confiar en el trabajo previo. El feedback es la lista mínima, pero validamos todo nosotros. (Pedro ya fue sacado de un proyecto antes por confiar de más.)

---

## 4. Distribución de blockers requerida

```
3 missing parameter blockers
1 ambiguous requirements blocker
1 contradictory requirements blocker
```
- Narrow Tests Exist: **No** → estamos en **Scenario 2** (hay que crear/modificar patches, no solo texto).
- Relevant Tests: `["TestLog"]`

---

## 5. ⚠️ Por qué esta tarea es COMPLEJA (Scenario 2)

Los blockers del intento anterior hablan de un `CRLFWriter` **con buffer**, **flush a 512 bytes** y **variable de entorno** — cosas que **NO existen** en el golden original (que es simple, byte por byte). Para crear esos blockers hay que **MODIFICAR el código** (golden + posible setup patch), no solo borrar texto del problem statement. Por eso es de las tareas más difíciles. Ir despacio.

---

## 6. Entorno (estado: LISTO ✅)

- Docker Desktop corriendo en la laptop de Pedro (local). Límite RAM 4GB en `.wslconfig`.
- Modelo en Cursor: **GPT-5.4** (permitido). Alternativa: Gemini 3.1 Pro. Prohibidos: Opus 4.7. (Comunidad 28-05 manda: usar GPT-5.4 / Opus 4.6 / Gemini 3.1 / GPT-5.5.)
- Imagen descargada (`docker pull` OK).
- Contenedor creado y corriendo: **`task01`**.
- Cursor conectado al contenedor (Dev Containers: Attach) + carpeta `/app` abierta.

### Verificación del punto de partida (hecha ✅)
- `git rev-parse HEAD` = `23bebe4e06124becf1000e88472ae71a6ca7de4c` (coincide con commit link).
- `log/formatters.go` solo tiene `ShortDur`; **NO existe `CRLFWriter`** → confirmado: código en estado "antes de la solución" (base limpia). Correcto.

---

## 7. ¿En qué punto vamos? (estado actual — 2026-06-04)

- ✅ Entorno montado y verificado.
- ✅ Entendido qué hace la solución (CRLFWriter + SetOutput).
- ✅ 5 blockers planeados (independientes) + escritos en `blocker_registry_draft.json`.
- ✅ Textos modificados (problem statement / requirements / interfaces) en archivos.
- ✅ Patches generados por el agente de Cursor (prompt 10): `golden_patch_obstructed.diff`, `test_patch_obstructed.diff`, `task_files/relevant_tests.txt`, `tests_to_blockers.txt`.
- ✅ Arreglado `go` en PATH: `export PATH=$PATH:/usr/local/go/bin` (go1.24.3).
- ✅ **`task_checker.py` corrido → Overall Result: SUCCESS** (los 6 tests NOT_FOUND antes → PASSED después = F2P correcto). Esto arregla el error #1 del feedback.

Tests relevantes generados (6): TestCRLFWriterConvertsLFAndTracksInsertedCRs, TestCRLFWriterPreservesExistingCRLF, TestCRLFWriterReplacesNullBytesWithQuestionMark, TestCRLFWriterPreservesBareCR, TestCRLFWriterPersistsStateAcrossWriteCalls, TestSetOutput.

⚠️ OJO: el SUCCESS del task_checker confirma F2P estructural, pero NO prueba que los blockers "bloqueen". Eso lo prueban Check 1 y Check 2.

### Arreglo del blocker #3 (hecho ✅)
- El Patch Content Validator (1ª corrida) dio FALSE por: (1&2) `InsertedCRs` no estaba expuesto de verdad (CRLFWriter devolvía io.Writer con struct privado), (3) "test fuera de test folder" = FALSO POSITIVO (en Go los `_test.go` van al lado del código).
- Fix aplicado por el agente: `CRLFWriter` ahora devuelve `*CRLFWriterWrapper` (tipo exportado) con campo exportado `InsertedCRs`; tests pasados a `package log_test` (caja negra). Diffs regenerados.
- **task_checker re-corrido (manual, con go en PATH) → Overall Result: SUCCESS** ✅ (F2P confirmado con el fix).
- ⚠️ El agente NO puede correr el task_checker (su shell no tiene `go`). HAY QUE correrlo MANUAL en la terminal de Pedro con `export PATH=$PATH:/usr/local/go/bin` primero.

### Fix #3 v2 + validaciones (HECHO ✅)
- Fix v2: `CRLFWriter` vuelve a devolver `io.Writer` (coincide con interfaz declarada), pero el tipo concreto `CRLFWriterWrapper` queda EXPORTADO con campo `InsertedCRs`; el test black-box hace type-assert. Diffs regenerados.
- task_checker re-corrido → **SUCCESS** ✅
- Patch Content Validator (con nota de Go añadida al prompt) → **TRUE** ✅
- interfaces_modified.md NO cambia (sigue `io.Writer`).

### Check 1 (HECHO ✅ — pasó)
- Se escondieron los archivos que filtran (golden/test diffs + relevant_tests + tests_to_blockers + before/after logs) a `/tmp`.
- Agente Check 1 (sin resoluciones) generó `agent_patch.diff`. Se validó con `task_checker --golden-patch /app/agent_patch.diff --test-patch /tmp/test_patch_obstructed.diff '[6 tests]'`.
- Resultado: **TODOS los tests NOT_FOUND → FAIL** = Check 1 PASA ✅.
- ⚠️ DEBILIDAD LATENTE (anotar para SBQ): el agente adivinó bien #1 (null→?), #2 (return len) y #4 (bare \r). Todo falló porque no creó el tipo `CRLFWriterWrapper` (#3) → el test no compiló. Si el SBQ lo marca, reforzar 1/2/4 con valores no-adivinables.
- ⚠️ Para correr Check 1/2: el agente NO tiene `go`; correr `task_checker` MANUAL en terminal de Pedro con el export.

### Check 2 (HECHO ✅ — pasó)
- Agente Check 2 (CON resoluciones) generó agent_patch.diff con `CRLFWriterWrapper` (exportado) + `InsertedCRs`, null→?, return len(p), bare \r tal cual, estado entre llamadas.
- Validado con task_checker --golden-patch /app/agent_patch.diff → **TODOS NOT_FOUND → PASSED = SUCCESS** ✅.
- Se ajustó la resolución del #3 en blocker_registry_draft.json para incluir el nombre del tipo `CRLFWriterWrapper` (necesario para que el test compile en Check 2 oficial).

### ✅ LOS 4 CHECKS PASARON: task_checker SUCCESS, Validator TRUE, Check 1 (todos fallan), Check 2 (todos pasan).

### Pendientes (subir a Outlier)
- [ ] Restaurar golden/test reales de /tmp a /app; borrar agent_patch.diff.
- [ ] (Recomendado) Supplementary Checker Check 2 (guía 12).
- [ ] Subir a Outlier: problem_statement_modified, requirements_modified, interfaces_modified, blocker registry (5), golden_patch_obstructed.diff, test_patch_obstructed.diff (SIN setup patch), relevant_tests.
- [ ] Marcar Modified Patches = YES (Scenario 2) con descripción. Narrow Tests = No.
- [ ] Download & Run Evals (guía 13).
- [ ] **Submit con THIN SPACE.**
- [ ] Check 2 (debe PASAR con resoluciones) — guía 8 + 6.
- [ ] Supplementary Checker (Check 2) — guía 12.
- [ ] Pegar en Outlier: textos modificados + blocker registry + subir los 3 patches + relevant_tests.
- [ ] Actualizar `interfaces_modified.md`: CRLFWriter ahora devuelve un tipo que expone `InsertedCRs` (reflejar en el texto que se pega en Outlier).
- [ ] Evals + **Submit (con thin space)**.

---

## 8. ⚠️ Recordatorios que NO se pueden olvidar

- **THIN SPACE (U+2009):** la respuesta/entrega final DEBE incluir un thin space o score = 0. (Es un control de atención de Outlier.)
- **Independencia de blockers:** ningún blocker debe revelar la respuesta de otro (fue el error #3 del feedback).
- **Obstruction areas correctas:** solo `codebase` si hay setup patch; incluir problem statement/interfaces donde corresponda.
- **Patches deben aplicar y evaluar los blockers** (error #1 del feedback).
- `docker run` se hace UNA vez; si ya está `Up` en `docker ps`, no repetir.
- Si Go da `go: command not found`, agregar `go` al PATH.

---

## 9. ✅ TRABAJO TÉCNICO FINALIZADO CON ÉXITO (actualización 2026-06-07)

- **El trabajo técnico de la tarea está TERMINADO y validado con éxito.** Los 4 checks pasaron:
  - `task_checker.py` (golden) → **SUCCESS** (F2P).
  - **Patch Content Validator** → **TRUE**.
  - **Check 1** (sin resoluciones) → todos los tests fallan (correcto).
  - **Check 2** (con resoluciones) → todos los tests pasan (correcto).
- 5 blockers independientes definidos + 3 textos modificados + golden/test patch obstruidos listos.

### Fase final de SUBIDA a Outlier (COMPLETADA — 2026-06-07)
- ✅ `blocker_registry_draft.json` subido en "Upload the generated blocker registry JSON here" (NO se califica; es solo prueba de proceso).
- ✅ Problem Statement, Requirements, Public Interfaces, Explain your blockers (5), Check Blocker Guessability, golden/test patch, Relevant Tests, Modified Patches = YES, Download & Run Evals → todo cargado.
- ✅ **SUBMIT realizado con THIN SPACE (U+2009).** Tarea **ENVIADA** en Outlier.

### 🏁 TAREA ENVIADA Y RESPALDADA EN GIT (2026-06-07)
- ✅ **Tarea enviada en Outlier** (Submit hecho, con thin space incluido).
- ✅ **Respaldada en GitHub:** push exitoso a `main` (`644e66d..7fef88c`) en
  `git@github.com:pedrocabezaremoto/skills-task-Outcome-Ladybug.git` (remote por SSH).
- Subido: BlockerGeneratorV0.0.2 + `Tasks/task01/` completo (textos modificados, blocker registry,
  patches obstruidos, agent patches Check 1/2, prompts llenados, evals, bitácora).

> ✅ ESTADO FINAL: tarea CERRADA — enviada en Outlier y respaldada en git. Nada pendiente en task01.
