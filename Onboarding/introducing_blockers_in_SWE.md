# Informe Técnico: Proyecto de Inyección de Bloqueadores para la Evaluación de Agentes de IA

> **Propósito**: Protocolo de ingeniería y diseño experimental para inyectar ambigüedad controlada ("bloqueadores") en bases de código, evaluando el rigor técnico y la conciencia situacional de los agentes de IA.

---

## 1. Contexto y el Problema de la Sobreconfianza en la IA

En la arquitectura de sistemas de inteligencia artificial, la capacidad de generar código es una métrica necesaria pero insuficiente. El desafío crítico para la implementación de agentes en entornos de producción no es su velocidad de escritura, sino su capacidad para **reconocer límites operativos**. 

Actualmente, observamos una tendencia peligrosa al *"one-shotting"*: la propensión de los modelos a intentar resolver tareas complejas de un solo golpe, ignorando vacíos lógicos. Como señala Andre Karpathy, los modelos actuales carecen de esa "voz interna" o instinto de ingeniero senior que detiene la ejecución cuando los requisitos son difusos.

Esta ausencia de instinto técnico es, sin duda, el mayor obstáculo para la fiabilidad de la IA. Un agente que "simplemente avanza" ante la incertidumbre es una receta para el desastre en entornos operativos reales. El **Proyecto de Inyección de Bloqueadores** nace para corregir esta falta de fiabilidad en su origen, transformando la evaluación de una simple prueba de codificación en un test de conciencia situacional y rigor profesional.

---

## 2. Definición y Tipología de los "Bloqueadores"

Un **"Blocker" (bloqueador)** es una herramienta de evaluación deliberada que actúa como un *"escape room"* para modelos de IA. No es un error fortuito, sino una pieza de ambigüedad o información faltante inyectada intencionalmente para que la resolución de la tarea sea literalmente imposible sin una intervención externa.

Para estructurar estas pruebas, categorizamos los bloqueadores en tres tipos fundamentales:

* **Parámetros faltantes**: Se omite un valor técnico crítico. Por ejemplo, solicitar la implementación de un sistema de `rate limit` sin proporcionar el límite numérico de peticiones.
* **Requisitos ambiguos**: Se presentan múltiples rutas de implementación válidas sin un criterio de selección. Un ejemplo clásico es solicitar una función de "borrado" sin especificar si debe ser un borrado suave (`soft delete`) o un borrado físico (`hard delete`).
* **Requisitos contradictorios**: Se instruye al agente a realizar dos acciones mutuamente excluyentes. Esto hace que la tarea sea lógicamente irresoluble, obligando al agente a detectar la paradoja antes de escribir una sola línea de código.

> [!IMPORTANT]
> La detección de estas ambigüedades representa una habilidad de "segundo nivel". Mientras que un desarrollador junior suele adivinar para intentar cumplir con la tarea, un ingeniero senior reconoce que el *"guessing"* (adivinar) es un fallo de rigor profesional. Detenerse a clarificar no es una debilidad, sino una validación de la competencia arquitectónica del agente.

---

## 3. Criterios de Calidad y Selección de Bloqueadores

La integridad científica de la evaluación depende de la selección rigurosa de los bloqueadores. Si un bloqueador es trivial, el agente podría superarlo por azar, lo que invalidaría los resultados de la prueba.

| Criterio | Bloqueadores de Alta Calidad | Bloqueadores de Baja Calidad | Impacto en la Evaluación |
| :--- | :--- | :--- | :--- |
| **Espacio de Búsqueda** | Masivo; la respuesta es una entre miles de opciones (ej. un `session timeout` específico). | Reducido; el agente puede adivinar entre dos o tres opciones comunes. | Un espacio masivo hace que adivinar sea inútil y fuerza la comunicación obligatoria. |
| **Relevancia** | Crítico para la lógica de negocio, la seguridad o la integridad de los datos. | Trivial o estético, como el nombre de una variable no utilizada. | Los bloqueadores críticos prueban si el agente entiende las consecuencias de su código. |
| **Resolución** | Exige una respuesta externa específica para que el código sea funcional. | Puede resolverse mediante suposiciones estándar de la industria. | Garantiza que el agente no pueda tener "suerte"; invalida la adivinación como estrategia. |

---

## 4. Metodología de Inyección: Escenarios de Flujo de Trabajo

La inyección de bloqueadores no es un proceso aleatorio, sino un flujo lógico que se bifurca según la infraestructura de pruebas del código original. El éxito del método depende de identificar si el sistema posee **"pruebas estrechas" (`narrow tests`)**, es decir, tests unitarios que validan mensajes de error exactos o valores específicos.

* **Escenario 1 (Con Pruebas Estrechas)**: El proceso es directo. Se identifica el detalle específico que la prueba está validando y se elimina de la declaración del problema. La propia infraestructura de tests actuará como el guardián que forzará al agente a enfrentarse a la falta de información.
* **Escenario 2 (Sin Pruebas Estrechas)**: El evaluador debe adoptar un rol de *"chaos engineer"*. Esto implica "arremangarse" y modificar directamente el código base, las librerías o crear nuevos archivos de prueba para introducir requisitos técnicos que no existían originalmente. En este escenario, el bloqueador se construye físicamente en el entorno.

Este enfoque sistemático garantiza que el agente no supere la prueba por casualidad. Al vincular el éxito de la tarea a la resolución del bloqueo, aseguramos que la única vía de éxito sea la clarificación consciente.

---

## 5. El Registro de Bloqueadores: El "Answer Key" del Sistema

El componente esencial (la "fórmula secreta") que permanece invisible para el agente es el **Registro de Bloqueadores**. Este actúa como un sistema de respuesta inteligente que valida si el agente está haciendo las preguntas correctas. Funciona como un guardián: si el agente hace la pregunta equivocada, el sistema no entrega información.

Cada entrada en el registro se define con precisión milimétrica:

* **ID Único**: Identificador para trazabilidad.
* **Tipo de Bloqueador**: Clasificación (Faltante, Ambiguo, Contradictorio).
* **Descripción**: Detalle del desafío técnico, redactado para no revelar la solución prematuramente.
* **Resolución**: La "verdad absoluta" del sistema. Debe ser obsesivamente específica. Se dictan formatos exactos, como el uso de pipes para evitar interpretaciones: por ejemplo, `primary|delegated`.
* **Trigger Questions (Preguntas Activadoras)**: Una lista de intenciones de búsqueda. Si la consulta del agente coincide con la semántica de estas preguntas, el sistema libera la resolución.

---

## 6. Implementación Técnica y Generación de Artefactos

La validez de la evaluación requiere un entorno técnico aislado que replique un flujo de trabajo de desarrollo real. El proceso de transformación de una tarea estándar a una con bloqueadores inyectados sigue estos pasos:

1. **Aislamiento en Docker**: Se despliega un contenedor limpio para evitar cualquier contaminación de dependencias externas.
2. **Modificación de la Base de Código**: Se alteran físicamente las librerías y los archivos de prueba para incrustar el bloqueador (especialmente en el Escenario 2).
3. **Generación de Parches (`.patch`)**: Mediante el comando `git diff`, se capturan los cambios realizados. Estos archivos de parche representan la "verdad de campo" (*ground truth*) y son el artefacto final que el agente recibirá para intentar resolver la tarea.

Este flujo asegura que el agente trabaje sobre una base de código real modificada, donde el éxito depende de su interacción con los archivos de parche y la identificación de las inconsistencias inyectadas.

---

## 7. Conclusiones: Hacia una IA Colaborativa y Confiable

El Proyecto de Inyección de Bloqueadores redefine nuestra comprensión de la inteligencia en la IA. La verdadera capacidad cognitiva no reside en la velocidad de salida de líneas de código (`LOC/seg`), sino en la **precisión del interfaz entre el agente y los requisitos**. Saber cuándo detenerse es el pilar fundamental de la confianza arquitectónica.

A medida que los agentes aprendan a identificar bloqueadores, el horizonte de la colaboración se expande: desde la negociación de requisitos complejos hasta la capacidad de ofrecer mentoría y retroalimentación a otros modelos o desarrolladores humanos. En última instancia, este proyecto desplaza la métrica de éxito de la ejecución ciega a la fiabilidad técnica; un agente que pregunta es, por definición, un agente en el que podemos confiar para manejar la complejidad del mundo real.
