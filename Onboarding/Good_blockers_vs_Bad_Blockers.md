# Good blockers vs Bad Blockers — Outcome Ladybug (Supplemental Module)

---

## Página 1: Supplemental Module: Common Blocker Injection Errors (slide 1/7)

**Imagen 1 — Portada del módulo y Tabla de Contenidos**

Este módulo suplementario cubre los errores de calidad más comunes observados en el diseño de bloqueadores en este proyecto, explicando cómo identificarlos y corregirlos para evitar bloqueadores inválidos, evaluaciones fallidas o datos de entrenamiento deficientes.

El contenido se divide en:
* **Table of Contents — Common Errors**:
  * **Common Error #1**: Blockers That Leak the Solution
  * **Common Error #2**: Blockers That Are Guessable or Not Vast
  * **Common Error #3**: Blockers That Are Not Test-Validated
  * **Conclusion**: Los bloqueadores fuertes son esenciales para producir datos de entrenamiento confiables y de alta calidad. Cada bloqueador debe ser realista, crítico, no adivinable y verificable por pruebas, permaneciendo oculto para el agente.
  * **Reminder**: Pequeños errores en el diseño del bloqueador pueden invalidar la tarea completa. Los contribuidores que envíen repetidamente bloqueadores de baja calidad o inválidos pueden ser eliminados del proyecto.

* **Common Errors (Errores Comunes a Tratar)**:
  * Creating blockers that leak the solution (Crear bloqueadores que filtran la solución).
  * Writing blockers that are guessable or not "vast" (Escribir bloqueadores adivinables o no vastos).
  * Defining blockers that are not test-validated (Definir bloqueadores no validados por pruebas).
  * Using trivial or non-critical ambiguities as blockers (Usar ambigüedades triviales o no críticas).
  * Introducing overlapping or contradictory blockers (Introducir bloqueadores solapados o contradictorios).

---

## Página 2: Pregunta 1 (slide 2/7)

**Imagen 1 — Cuestionario - Pregunta 1**

La plataforma presenta una pregunta de opción múltiple para evaluar el entendimiento del propósito de los bloqueadores en el diseño de tareas:

* **Pregunta**: *"What is the core purpose of a blocker in a SWEAP task?"*
* **Opciones**:
  * **A)** To make the task harder by hiding implementation details
  * **B)** To force the agent to read the code more carefully
  * **C)** To ensure the agent must ask clarifying questions before solving correctly
  * **D)** To reduce the chance that tests pass accidentally

* **Respuesta Correcta**: **C**. El objetivo principal de un bloqueador es forzar la clarificación obligatoria mediante preguntas antes de que el agente pueda resolver la tarea de manera correcta. Esto previene el comportamiento de "one-shotting" o asunciones a ciegas en entornos de producción.

---

## Página 3: Pregunta 2 (slide 3/7)

**Imagen 1 — Cuestionario - Pregunta 2**

La plataforma presenta la segunda pregunta del cuestionario para definir el concepto de un tipo de bloqueador específico:

* **Pregunta**: *"Which of the following best describes a Missing Parameter blocker?"*
* **Opciones**:
  * **A)** A requirement that conflicts with another requirement
  * **B)** A behavioral rule with multiple valid interpretations
  * **C)** A required value or rule that is not specified but is critical to correctness
  * **D)** A cosmetic formatting choice not described in the problem statement

* **Respuesta Correcta**: **C**. Un bloqueador de tipo *Missing Parameter* (parámetro faltante) consiste en la omisión intencional de un valor o una regla que resulta absolutamente crítica para que la implementación sea correcta. Sin este parámetro, el código no puede operar de forma válida, forzando al desarrollador o modelo a preguntar su valor exacto.

---

## Página 4: Pregunta 3 (slide 4/7)

**Imagen 1 — Cuestionario - Pregunta 3**

La plataforma presenta la tercera pregunta del cuestionario para identificar qué constituye un mal bloqueador de tipo parámetro faltante (Missing Parameter):

* **Pregunta**: *"Which example is a BAD missing-parameter blocker?"*
* **Opciones**:
  * **A)** "Rate-limit requests according to internal policy"
  * **B)** "Encrypt sensitive fields per compliance requirements"
  * **C)** "Return an appropriate HTTP status when a resource is not found"
  * **D)** "Session expires after inactivity"

* **Respuesta Correcta**: **C**. El ejemplo *"Return an appropriate HTTP status when a resource is not found"* es un **mal bloqueador** (BAD blocker) porque la respuesta es altamente predecible y adivinable mediante suposiciones y estándares de la industria (el código de estado HTTP estándar y universal para un recurso no encontrado es `404`). Un agente de IA o desarrollador resolverá esto asumiendo el default estándar de la industria sin necesidad de preguntar, anulando el propósito de forzar la clarificación. Las otras opciones (políticas internas, requisitos de cumplimiento específicos o tiempos de inactividad arbitrarios) tienen un espacio de búsqueda masivo que requiere clarificación explícita obligatoria.

---

## Página 5: Pregunta 4 (slide 5/7)

**Imagen 1 — Cuestionario - Pregunta 4**

La plataforma presenta la cuarta pregunta del cuestionario para evaluar la comprensión de la regla del Espacio de Búsqueda Masivo (Vast Search Space):

* **Pregunta**: *"What makes a blocker invalid under the "Vast Search Space" rule?"*
* **Opciones**:
  * **A)** It has multiple possible implementations
  * **B)** It can be solved by reading public requirements
  * **C)** It has only a small, guessable set of reasonable answers
  * **D)** It requires modifying the codebase

* **Respuesta Correcta**: **C**. Bajo la regla de **Vast Search Space** (Espacio de Búsqueda Masivo), un bloqueador se considera **inválido** si tiene únicamente un conjunto pequeño y adivinable de respuestas razonables (por ejemplo, opciones de sí/no, o constantes estándares de la industria). Esto invalida el bloqueador porque permite que el agente asuma o adivine con un alto porcentaje de acierto, evadiendo la necesidad de realizar preguntas de clarificación. Para ser válido, el bloqueador debe forzar un espacio de soluciones tan grande que la adivinación sea inútil.

---

## Página 6: Pregunta 5 (slide 6/7)

**Imagen 1 — Cuestionario - Pregunta 5**

La plataforma presenta la quinta pregunta del cuestionario para identificar qué constituye un bloqueador válido de requisitos ambiguos (Ambiguous Requirement):

* **Pregunta**: *"Which situation represents a valid Ambiguous Requirement blocker?"*
* **Opciones**:
  * **A)** The function name is not specified
  * **B)** The error message punctuation is unclear
  * **C)** The system must "handle deletion appropriately"
  * **D)** The variable should be camelCase or snake_case

* **Respuesta Correcta**: **C**. La instrucción de que el sistema debe *"handle deletion appropriately"* (manejar la eliminación de forma apropiada) representa un **bloqueador ambiguo válido**. Existen múltiples implementaciones técnicas viables y comunes para este requisito (como una eliminación lógica o `soft delete` mediante una columna de estado, o una eliminación física o `hard delete` permanente de la base de datos). Al no especificarse cuál es la esperada, la IA se ve obligada a detenerse y preguntar por el comportamiento exacto. Las otras opciones son inválidas o de otra categoría:
  * **A** es un bloqueador de parámetro faltante o de firma.
  * **B** y **D** son bloqueadores triviales o cosméticos (puntuación o estilos de nomenclatura) que no afectan el comportamiento lógico y se consideran malas prácticas.

---

## Página 7: Conclusión (slide 7/7)

**Imagen 1 — Conclusión del Curso**

El slide final cierra el módulo suplementario con las directrices definitivas de calidad para el proyecto:

* **Mensaje de Cierre**: *"Thank you for taking the time to complete this course. By now, you should have a clear understanding of what makes a strong, valid blocker—and just as importantly, how to recognize and avoid bad blockers that lead to poor task outcomes and low-quality training data."*

* **Recordatorio Clave**: *"Remember: well-designed blockers are not about making tasks harder. They are about introducing the right kind of uncertainty—uncertainty that is realistic, critical, non-guessable, and test-validated, and that forces an agent to ask the right clarifying questions before proceeding."*

* **Directriz de Calidad**: La atención al detalle impacta directamente la calidad y confiabilidad de los conjuntos de datos del proyecto. Se instruye a los participantes a aplicar estos principios de forma consistente en todas las tareas futuras, a revisar minuciosamente su trabajo antes de enviarlo y a utilizar este material suplementario como referencia en caso de duda.

* **Agradecimiento**: *"Thanks again for your time and effort—we appreciate your commitment to quality."*
