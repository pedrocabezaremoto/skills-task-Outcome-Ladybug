# Intro Course — Outcome Ladybug (Blocker Injection)

---

## Página 1: Bienvenida e Introducción

**Imagen 1 — Portada del curso**

El curso se llama **Blocker Injection**. Es una técnica de diseño de tareas donde le pones información incompleta, ambigua o contradictoria a un agente de IA, para ver si sabe pedir clarificación en vez de adivinar. El subtítulo lo dice directo: *"Designing tasks that force clarification through ambiguity, missing information, and contradictions"* — o sea, diseñar tareas que fuercen al agente a preguntar porque no tiene todo claro. El curso vive dentro de **Part 1: Onboarding** y tiene 6 secciones, 16 minutos en total.

**Imagen 2 — Tabla de Contenidos (slide 1/6)**

El curso tiene 4 bloques principales:

- **01 — Foundations & Purpose** → Qué es Blocker Injection y para qué sirve.
- **02 — Blocker Types & Strategy** → Los tipos de blockers que existen y cómo usarlos.
- **03 — End-to-End Workflow** → El flujo completo de trabajo en 4 pasos:
  - Paso 1: Initial Analysis (analizar el problema)
  - Paso 2: Blocker Injection (inyectar el blocker)
  - Paso 3: Registry & Validation (registrar y validar)
  - Paso 4: Final Task Checks (verificación final)
- **04 — Registry, Validation & Wrap-Up** → Cómo registrar todo y cerrar la tarea.

---

## Página 2: Fundamentos y Propósito (01 — Foundations and Purpose)

**Imagen 1 — Slide de sección**

Es el slide de entrada a la sección 01. Solo dice **"Foundations and Purpose"** — indica que empieza el bloque donde te explican qué es Blocker Injection y por qué existe. Es como el "capítulo 1" del curso.

**Imagen 2 — ¿Qué es Blocker Injection?**

Define la técnica de forma concreta:

> *"Blocker Injection es una técnica de diseño de tareas donde información clave es intencionalmente faltante, ambigua o contradictoria."*

El objetivo es asegurarse de que:
- Un agente **no pueda resolver la tarea correctamente** sin hacer preguntas de clarificación.
- Si el agente adivina o asume, produce comportamiento incorrecto.
- El agente debe reconocer la incertidumbre y pedir clarificación.

Nota clave del slide: *"Esto testea la calibración del agente, no solo su habilidad de programar."* — O sea, no es solo que sepa escribir código, sino que sepa cuándo le falta información.

**Imagen 3 — Por qué importa Blocker Injection**

Compara dos realidades:

| Problema real (lado rojo) | Lo que Blocker Injection evalúa (lado verde) |
|---|---|
| Los agentes fallan porque hacen suposiciones silenciosas | Si el agente detecta ambigüedad |
| Proceden con contexto incompleto | Si sabe cuándo le falta información |
| No piden clarificación | Si usa herramientas de clarificación en vez de adivinar |

Conclusión del slide (en amarillo): **"El comportamiento correcto es hacer preguntas, no resolver de un solo tiro."**

---

## Página 3: Tipos de Blocker y Estrategia (02 — Blocker Types & Strategy)

**Imagen 1 — Slide de sección**

Slide de entrada a la sección 02: **"Blocker Types & Strategy"**. Aquí ya entras a la parte técnica: qué tipos de blockers existen y cómo decidir cuál usar.

**Imagen 2 — ¿Qué cuenta como un Blocker válido?**

Un blocker válido debe cumplir 6 criterios:

| Criterio | Descripción |
|---|---|
| **Realistic** (Realista) | Debe ser plausible en trabajo de ingeniería real. No inventar escenarios raros. |
| **Critical** (Crítico) | Si el agente lo resuelve mal, el output es incorrecto o inutilizable. |
| **Objective** (Objetivo) | Tiene exactamente una resolución correcta, no varias válidas. |
| **Non-guessable** (No adivinable) | El espacio de soluciones es tan grande que el agente no puede adivinar por fuerza bruta. |
| **Independent** (Independiente) | Resolver un blocker no revela la respuesta de otro. |
| **Non-contrived** (No forzado) | No es un truco ni un detalle de formato. Es una duda real. |

Regla de oro del slide: **"Si el agente no lo clarifica, el resultado debe ser incorrecto."**

**Imagen 3 — Tipos de Blockers**

Hay exactamente **3 tipos** de blockers:

- **Missing Parameters** (Parámetros faltantes) → Valores requeridos que no están especificados. Ejemplos: límites, formatos, algoritmos, umbrales, políticas.
- **Ambiguous Requirements** (Requisitos ambiguos) → Existen múltiples implementaciones razonables, pero solo una es correcta.
- **Contradictory Requirements** (Requisitos contradictorios) → Instrucciones que se contradicen entre sí y requieren clarificación para resolverse.

Regla importante: **cada tarea debe incluir entre 3 y 5 blockers**, según las reglas del assignment.

**Imagen 4 — Estrategia de Inyección**

La estrategia depende de si la tarea ya tiene **narrow tests** (tests específicos/estrechos):

| Escenario 01 — Ya existen narrow tests | Escenario 02 — No existen narrow tests |
|---|---|
| Eliminar detalles críticos de implementación del texto | Introducir narrowness (especificidad) en la tarea |
| No cambiar los tests existentes | Agregar requisitos de implementación específicos |
| Los tests fallan a menos que el agente haga las preguntas correctas | Crear nuevos patches para forzarlos |

Objetivo siempre igual: **forzar clarificación antes de la implementación correcta.**

---

## Página 4: Flujo de Trabajo de Extremo a Extremo (03 — End-to-End Workflow)

**Imagen 1 — Slide de sección**

Slide de entrada a la sección 03: **"End-to-End Workflow"**. Aquí te explican el flujo completo de trabajo, paso a paso, desde que recibes la tarea hasta que la entregas.

**Imagen 2 — Paso 1: Initial Analysis (Análisis Inicial)**

Antes de tocar nada, debes revisar todos los inputs que te dan:

- **Code language** → El lenguaje de programación de la tarea
- **Problem statement** → El enunciado del problema
- **Requirements and public interfaces** → Los requisitos y las interfaces públicas definidas
- **Official solution** → La solución oficial de referencia
- **Relevant tests** → Los tests que ya existen
- **Narrow test indicator** → Si los tests son "narrow" (específicos/estrechos) o no

Este análisis define **qué se puede modificar y dónde se pueden inyectar los blockers.**

**Imagen 3 — Modificaciones Textuales**

Los blockers se inyectan modificando el texto de la tarea en 3 lugares:

| Dónde | Qué hacer |
|---|---|
| **Problem Statement** | Eliminar valores específicos / reemplazar detalles con lenguaje vago |
| **Requirements** | Introducir contradicciones / esconder parámetros requeridos |
| **Public Interfaces** | Asegurarse de que las descripciones no revelen las resoluciones |

Regla clave: **el texto debe guiar al agente hacia la incertidumbre, no hacia la respuesta.**

**Imagen 4 — Creación de Patches (cuando se requiere)**

Cuando no existen narrow tests, hay que crear 3 tipos de patches:

- **Setup Patch** → Prepara el entorno de ejecución.
- **Test Patch** → Valida que la resolución correcta funcione.
- **Golden Patch** → Es la solución final esperada (la respuesta correcta al blocker).

Regla: **todos los patches deben estar alineados con los blockers inyectados.** No pueden contradecirse entre sí.

---

## Página 5: Registro, Validación y Cierre (04 — Registry, Validation & Wrap-Up)

**Imagen 1 — Slide de sección**

Slide de entrada a la sección 04: **"Registry, Validation & Wrap-Up"**. La parte final del flujo: registrar los blockers correctamente y validar que todo esté bien antes de entregar.

**Imagen 2 — Blocker Registry (Registro de Blockers)**

El Blocker Registry es la **llave de respuestas oculta** — el documento donde guardas toda la info de cada blocker. Por cada blocker debes registrar 6 campos:

| Campo | Qué es |
|---|---|
| **Blocker name** | ID único del blocker |
| **Area of obstruction** | En qué parte de la tarea vive el blocker |
| **Type of obstruction** | Qué tipo es (Missing / Ambiguous / Contradictory) |
| **Description** | Descripción del blocker **sin revelar la respuesta** |
| **Exact resolution** | La resolución exacta y correcta |
| **3-5 trigger questions** | Preguntas que el agente podría hacer para desbloquearlo |

El registry es lo que alimenta la evaluación y el matching de clarificaciones del sistema.

**Imagen 3 — Trigger Questions (Preguntas Disparadoras)**

Las trigger questions representan cómo un agente podría pedir clarificación sobre un blocker. Deben cumplir 3 condiciones:

- **Varied in phrasing** → Escritas de formas distintas (no todas iguales).
- **Targeted to a specific blocker** → Cada pregunta apunta a un blocker específico, no genérica.
- **Specific enough to unlock the resolution** → Suficientemente específica para que el sistema pueda devolver la resolución correcta.

Regla: **si la pregunta es irrelevante, el sistema no devuelve ninguna resolución.**

**Imagen 4 — Good vs Bad Blockers**

La distinción más importante del curso:

| Blockers Buenos | Blockers Malos |
|---|---|
| Afectan la correctitud o el cumplimiento de la tarea | Detalles triviales de formato |
| Tienen exactamente una resolución correcta | Preferencias de estilo |
| No se pueden inferir del código ni de los tests | Defaults que cualquiera asumiría |
| | Información fácilmente descubrible en el código |

Conclusión del slide: **"Los blockers son sobre incertidumbre con significado, no sobre trampas."**

---

## Página 6: Conclusión (slide 6/6)

**Imagen 1 — Resumen Final**

El curso cierra con un resumen de todo lo aprendido:

- Blocker Injection testea si los agentes piden preguntas de clarificación
- Los blockers deben ser realistas, críticos y objetivos
- Usar información faltante, ambigua o contradictoria
- Inyectar entre 3 y 5 blockers por tarea
- Elegir la estrategia según si hay narrow tests o no
- Documentar todo en el Blocker Registry

**"Thank you for your contribution!"** — fin del Intro Course.




