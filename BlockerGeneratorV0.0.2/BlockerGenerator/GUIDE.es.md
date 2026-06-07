# Guía rápida — `prompt.md` (Step 1)

Pipeline que genera **blockers lógicos** a partir de la tarea baseline + patches, en hasta **3 rondas**. El agente emite **Blocker DSL** (`.bdsl`); el script `build_blockers.py` produce el JSON final.

---

## 1. Carpetas y archivos en el contenedor de la tarea

Directorio de trabajo del agente (ej.: `qcfail030601/`). Crea la carpeta de inputs:

```text
<task_container>/
  task_info/
    problem-statement.mdc      # enunciado / problema
    requirement.mdc            # requisitos
    public-interface.mdc       # API pública
    blocker-distribution.mdc   # meta de cuántos blockers por tipo
    golden_patch.mdc           # patch de referencia (privado)
    test_patch.mdc             # patch de pruebas (privado)
```

**Nombres exactos** (como en `prompt.md`). La extensión `.mdc` es la que espera el orquestador.

**`blocker-distribution.mdc`** — cantidad por tipo, en el formato:

```text
mp=1 ar=1 cr=1
```

| Alias | Tipo |
|-------|------|
| `mp` | `missing_parameter` |
| `ar` | `ambiguous_requirement` |
| `cr` | `contradictory_requirement` |

Copia también al contenedor (o apunta al agente al repo):

- `BlockerGenerator/prompt.md`
- `BlockerGenerator/build_blockers.py`
- `BlockerGenerator/skills/` (`project-overview.mdc`, `blocker-generator.mdc`, `blocker-registry.mdc`)

**Salidas** (en la raíz del contenedor, `--out-dir .`):

| Archivo | Función |
|---------|---------|
| `round_<N>.bdsl` | DSL de la ronda (escrito por el agente) |
| `blocker_registry.json` | Gabarito acumulado de blockers válidos |
| `generation_memory.json` | Estado del loop + auditoría |
| `existing_registry.json` | Solo rondas > 1 (estado entrante) |
| `rejection_memory.json` | Solo rondas > 1 (rechazos acumulados) |
| `abort.json` | Si falta input o la tarea no es viable |

---

## 2. Cómo usar `prompt.md`

1. Abre `BlockerGenerator/prompt.md` en el chat del agente (Cursor / cloud).
2. Asegura que el **cwd** del agente sea la raíz del contenedor (`task_info/` visible).
3. Completa los placeholders al final del prompt (ver secciones abajo).
4. El agente lee las skills, genera el `.bdsl` y ejecuta `build_blockers.py` — **no** edites `blocker_registry.json` a mano.

### Ronda 1 (desde cero)

```text
<existing_registry>     [vacío]
<rejection_memory>    [vacío]
<round_number>        1
```

Comando esperado después del DSL:

```bash
python build_blockers.py round_1.bdsl --out-dir .
```

### Varios turnos (rondas 2 y 3)

Cuando `generation_memory.json` tenga `halt.reason` = `continue` y aún falten blockers:

1. Copia el contenido completo de **`blocker_registry.json`** → `<existing_registry>`.
2. Copia el array **`rejection_memory`** dentro de **`generation_memory.json`** → `<rejection_memory>`.
3. Define `<round_number>` como `2` o `3`.
4. Nuevo prompt / nuevo turno con el mismo `prompt.md` actualizado.

El agente guarda `existing_registry.json` y `rejection_memory.json`, emite `round_<N>.bdsl` y ejecuta:

```bash
python build_blockers.py round_<N>.bdsl \
  --existing existing_registry.json \
  --rejection-memory rejection_memory.json \
  --out-dir .
```

**Detén el loop** cuando `halt.reason` sea:

- `distribution_satisfied` — meta cumplida  
- `distribution_already_satisfied` — nada que generar en esta ronda  
- `budget_exhausted` — 3 rondas sin cerrar la meta  

### Ya hay blockers (registry parcial)

Úsalo en la **primera** ejecución del prompt con registry prellenado:

- Pega el JSON existente en `<existing_registry>` (mismo formato que `blocker_registry.json`).
- `<rejection_memory>` vacío `[]` o el historial que ya tengas.
- `<round_number>` = `1` (o la ronda lógica siguiente).

El agente calcula el **déficit** por tipo (`pedido − ya en el registry`) y solo genera los blockers faltantes. Los blockers ya en el registry son **inmutables** — no los reemites en el DSL.

Si el déficit ya es cero en todos los tipos, la ronda emite solo `@meta` con `halt: distribution_already_satisfied`.

---

## 3. Memoria — qué es

| Concepto | Dónde vive | Uso |
|----------|------------|-----|
| **Registry** (`blocker_registry.json`) | Acumulativo | Gabarito para evaluación y Step 2 (ofuscación). Vuelve a `<existing_registry>` en la siguiente ronda. |
| **Rejection memory** | Array en `generation_memory.json` → `rejection_memory` | Intentos `@rejected` que fallaron validación. El agente debe **evitar repetir** los mismos patrones (`failure_gate`, `avoid_in_future`, etc.). |
| **`blocker_dataset` (en generation_memory)** | Solo de la ronda actual | Pool de candidatos, blockers nuevos con `ground_truth_annotation`, auditoría — **no** reutilizar como registry. |

Regla práctica: en la ronda siguiente, pasa **registry + rejection_memory**; ignora el resto de `generation_memory` para alimentar el prompt.

---

## 4. Qué se genera

**`blocker_registry.json`** — producto principal: lista `blockers[]` con `id`, `type`, `mode`, `area_of_obstruction`, `description`, `resolution`, `trigger_questions`, `independence`. Las entradas válidas vienen solo de registros `@blocker` con `status: valid | repaired_valid`.

**`generation_memory.json`** — control y trazabilidad:

- `halt` — motivo de parada, ronda, totales pedidos vs logrados  
- `blocker_dataset` — candidatos (`candidate_pool`), blockers de la ronda con ground truth, rechazados de la ronda, notas  
- `rejection_memory` — rechazos **acumulados** (todas las rondas)

El agente escribe **`.bdsl`**; el script arma los JSON de forma determinística (conteos, déficit, checks implícitos).

---

## 5. Cómo ejecutar

### Con el agente (flujo normal)

1. Arma `task_info/` con los 6 archivos.  
2. Pega `prompt.md` en el chat; completa `<existing_registry>`, `<rejection_memory>`, `<round_number>`.  
3. Deja que el agente corra hasta que existan `blocker_registry.json` y `generation_memory.json` sin error.  
4. Si `halt.reason` = `continue`, repite con ronda +1 y los JSON actualizados (máx. 3 rondas).

### Script manual (validar / reprocesar DSL)

En la raíz del contenedor, con Python 3:

```bash
# Ronda 1
python build_blockers.py round_1.bdsl --out-dir .

# Rondas 2+
python build_blockers.py round_2.bdsl \
  --existing existing_registry.json \
  --rejection-memory rejection_memory.json \
  --out-dir .
```

Si el script falla, corrige el `.bdsl` (gramática en `skills/blocker-generator.mdc`) y vuelve a ejecutar — no edites el JSON de salida a mano.

### Ruta absoluta (ejemplo Windows)

```bash
cd "c:\Users\leo_m\OneDrive\Documentos\ladybug\qcfail030601"
python "c:\Users\leo_m\OneDrive\Documentos\ladybug\BlockerGenerator\build_blockers.py" round_1.bdsl --out-dir .
```

---

## Flujo en una línea

```text
task_info/*  →  prompt.md (≤3×)  →  round_N.bdsl  →  build_blockers.py  →  blocker_registry.json + generation_memory.json
```

Siguiente paso del pipeline: Step 2 (ofuscación de la tarea usando `blocker_registry.json`).
