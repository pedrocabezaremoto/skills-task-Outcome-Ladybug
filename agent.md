# agent.md — Guía de Navegación del Proyecto Outcome Ladybug

> **LÉEME PRIMERO.** Este archivo es el punto de entrada para cualquier LLM/agente que abra este proyecto.
> Explica qué es Outcome Ladybug, cómo está organizada la carpeta y dónde encontrar cada cosa.
> **Última actualización:** 2026-06-03

---

## 1. ¿Qué es este proyecto?

**Outcome Ladybug** es un proyecto de la plataforma **Outlier** sobre **Inyección de Bloqueadores (Blocker Injection)** en tareas de ingeniería de software (SWE).

La idea central: se toma una tarea de código real (problem statement + golden patch + tests) y se le **inyectan "bloqueadores"** — ambigüedades, contradicciones o información faltante — de forma controlada. El objetivo es **evaluar si un agente de IA es capaz de detectar la falta de información y hacer las preguntas correctas (`ask_human()`)** en vez de adivinar.

Cada bloqueador se documenta en un **Blocker Registry** (archivo JSON oculto que actúa como "clave de respuestas"). El agente evaluado NUNCA ve ese registry.

**Tipos de bloqueador:**
1. `missing_parameter` — un valor/parámetro crítico no está especificado.
2. `ambiguous_requirement` — el comportamiento se puede interpretar de varias formas válidas.
3. `contradictory_requirement` — dos o más instrucciones se contradicen.

---

## 🖥️ Entorno de Trabajo de Pedro (QA Programador)

| Componente | Detalle |
|------------|---------|
| **Editor principal** | **Antigravity** — conectado vía SSH al VPS Contabo (servidor en Alemania) |
| **LLMs en Antigravity** | Claude Haiku, Claude Sonnet 4.6, Gemini Pro |

---

## 2. Flujo de trabajo (resumen)

1. **Analizar** la tarea original (problem statement, requirements, interfaces, golden patch, test patch).
2. **Generar el Blocker Registry** → ver `Guias/4Prompt_Blocker_Registry_Generator.md`.
3. **Modificar el codebase / problem statement** para introducir los bloqueadores → ver `Guias/2Guia_Codebase_Modifications_QA.md`.
4. **Generar golden patch + test cases obstruidos** → ver `Guias/10Generate_Golden_Patch_And_Test_Cases.md`.
5. **Correr los Checks de validación** (que el bloqueador realmente bloquea y que el agente con el registry sí lo resuelve):
   - Check 1 (sin resoluciones): `Guias/5Check_Attempter_Check_1.md` + `Guias/9Reviewer_Check_1.md`
   - Check 2 (con resoluciones): `Guias/8Check_Attempter_Check_2.md` + `Guias/6Check_Reviewer_Check_2.md`
6. **Validar calidad** → `Guias/7Prompt_Patch_Content_Validator.md`, `Guias/11Blocker_Guessability_Prompt.md`, `Guias/12...`, `Guias/13Task_Checker_Evals.md`.

---

## 3. Mapa de navegación (estructura de carpetas)

```
/root/skills-task-Outcome-Ladybug/
├── agent.md                    ← ESTE ARCHIVO. Punto de entrada / mapa.
│
├── Onboarding/                 ← Material conceptual de introducción (teoría).
│   ├── Intro-Course.md
│   ├── Taxonomy_introduction.md
│   ├── What_is_a_augmented_problem.md
│   ├── introducing_blockers_in_SWE.md
│   ├── Good_blockers_vs_Bad_Blockers.md
│   └── How_to_use_the_script_in_hil.md
│
├── Guias/                      ← Las 13 páginas oficiales de Outlier (espejo del sidebar).
│   │                             1–3 = guías conceptuales | 4–13 = prompts y checks operativos.
│   ├── 1Guia_outcome_ladybug.md              (Attemper Instructions — guía completa)
│   ├── 2Guia_Codebase_Modifications_QA.md    (Codebase Modifications)
│   ├── 3Guia_Blocker_Registry_Guide.md       (Blocker Registry — referencia)
│   ├── 4Prompt_Blocker_Registry_Generator.md (PROMPT: genera blocker_registry.json)
│   ├── 5Check_Attempter_Check_1.md           (CHECK: agente resuelve SIN resoluciones)
│   ├── 6Check_Reviewer_Check_2.md            (CHECK: por qué falló el agent patch)
│   ├── 7Prompt_Patch_Content_Validator.md    (PROMPT: valida cobertura/separación de patches)
│   ├── 8Check_Attempter_Check_2.md           (CHECK: agente resuelve CON resoluciones)
│   ├── 9Reviewer_Check_1.md                  (CHECK: qué bloqueadores se pudieron adivinar)
│   ├── 10Generate_Golden_Patch_And_Test_Cases.md (PROMPT: genera golden+tests obstruidos)
│   ├── 11Blocker_Guessability_Prompt.md      (PROMPT: ¿el bloqueador es adivinable?)
│   ├── 12Supplementary_Checker_Prompt-For_Check_2.md (CHECK supl. de claridad)
│   └── 13Task_Checker_Evals.md               (11 evals de calidad final de la tarea)
│
├── Progreso-Actual/            ← Estado ACTUAL del trabajo (avances en curso + pendientes).
│   └── Progreso.md
│
└── Historial/                  ← Registro HISTÓRICO de todo lo ya completado.
    └── historial.md
```

---

## 4. Reglas / convenciones del proyecto

- **Numeración 1–13 en `Guias/`** = orden exacto del sidebar de Outlier. Mantenerlo como espejo.
- **No modificar las guías existentes sin permiso explícito de Pedro** (especialmente archivos `.md` de plantillas/guías).
- **Los prompts contienen placeholders `{{...}}`** que se reemplazan con el contenido real (problem statement, golden patch, etc.) antes de usarse.
- **Modelos a usar en Cursor (instrucción de la COMUNIDAD, 28-05-2026 — manda sobre el Welcome viejo):** usar **GPT-5.4, Opus 4.6, Gemini 3.1, o GPT-5.5** (sobre todo en guessability, check 1 y check 2). Para Pedro (sin acceso a Claude): **Gemini 3.1 Pro** o **GPT-5.5**. Evitar Opus 4.7 (no está en la lista aprobada).

---

## 5. Para el próximo LLM: ¿por dónde empiezo?

1. Lee **este `agent.md`** completo.
2. Lee **`Progreso-Actual/Progreso.md`** para saber en qué punto está el trabajo.
3. Si necesitas contexto de lo ya hecho, revisa **`Historial/historial.md`**.
4. Para teoría → `Onboarding/`. Para ejecutar el workflow → `Guias/`.
