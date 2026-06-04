# Guía Técnica de Taxonomía y Protocolo para la Inyección de Bloqueadores

> **Propósito**: Protocolo de ingeniería de control de calidad para la transformación estructurada de commits crudos en tareas enriquecidas con taxonomías de bloqueadores rigurosas y entornos de validación controlados.

---

## 1. Contextualización del Ecosistema de Inyección de Bloqueadores

El propósito de este protocolo es establecer el estándar de ingeniería para la transformación de commits de código crudos en tareas de documentación técnica de alta fidelidad. En el desarrollo convencional, la trazabilidad suele ser deficiente; un desarrollador promedio suele publicar cambios con descripciones mínimas (ej. *"Fix bug X"*). Para el entrenamiento de modelos de lenguaje avanzados, esta carencia de contexto es inaceptable.

La inyección de bloqueadores actúa como un mecanismo riguroso de **control de calidad (QA)** diseñado para evaluar la robustez de las soluciones de software. Al aumentar un commit con requerimientos detallados e interfaces públicas, elevamos el nivel de exigencia del conjunto de datos. 

La transición de una simple línea de código a una tarea estructurada permite que el sistema de evaluación no solo verifique la corrección del código, sino también la capacidad de razonamiento lógico ante obstrucciones técnicas artificiales pero verosímiles. La **precisión taxonómica** en esta fase es obligatoria; cualquier fallo en la integridad de la base de datos inicial compromete la validez de todas las fases técnicas subsiguientes.

---

## 2. Estructura de Datos Base: El Punto de Partida de la Tarea

La arquitectura de cada tarea se fundamenta en tres pilares de información que constituyen la "fuente de verdad" del sistema. Estos componentes deben ser analizados exhaustivamente antes de proceder con cualquier inyección:

* **`Problem Statement`**: La narrativa técnica que define el desafío, el contexto del error o la mejora solicitada.
* **`Requirements`**: El desglose de especificaciones funcionales que la solución debe cumplir. Es el área primaria para la generación de ambigüedades.
* **`Interfaces`**: La definición de los puntos de interacción pública del código. Su integridad debe mantenerse para evitar inconsistencias estructurales.

### Comparativa de Valor Añadido: GitHub vs. Protocolo de Aumentación

| Información Cruda de GitHub | Tarea Aumentada (Estándar Senior) |
| :--- | :--- |
| Mensajes de commit volátiles (ej. `"updated logic"`). | Definición formal del tipo de problema y contexto. |
| Requerimientos implícitos u omitidos. | Requerimientos técnicos explícitos y granulares. |
| Sin documentación de interfaces. | Contratos de interfaces públicas claramente definidos. |
| Inútil para validación sistémica de modelos. | Estructura optimizada para inyección de obstrucciones. |

La validación de estos componentes requiere una confirmación empírica en un entorno controlado para asegurar que la tarea sea resoluble.

---

## 3. Entorno de Ejecución y Validación Técnica vía Docker

Para garantizar que un parche sea funcional, el especialista debe operar sobre una instancia aislada. El uso de **Docker** es una decisión estratégica: permite recrear el estado exacto del repositorio antes de la solución y ejecutar pruebas de regresión.

> [!IMPORTANT]
> **Lógica de Despliegue Condicional**: Es imperativo notar que el entorno de Docker y los campos de carga de parches están sujetos a la configuración de la tarea. Si se selecciona **`Yes`** en la opción **`Narrow Tests`**, la interfaz de Docker y las secciones de parches permanecerán ocultas. El entorno de validación solo se despliega cuando se selecciona **`No`** en **`Narrow Tests`**.

### Componentes Críticos de la Instancia de Validación:

* **`Commit Previo`**: Punto de partida para verificar el estado del código base.
* **`Verificación Fail-to-Pass`**: Protocolo obligatorio donde se confirma que los tests fallan sin la solución y pasan satisfactoriamente tras aplicarla.
* **`Generación de Parches`**: Creación de archivos `.patch` precisos que capturen los cambios exactos de la solución y los casos de prueba.

---

## 4. Protocolo de Gestión de Parches (Golden, Test y Setup)

La integridad sistémica de la tarea depende de la correcta carga de archivos y datos. Un error en la asignación de parches invalida la tarea de forma inmediata.

* **`Test Patch` (Archivo `.patch`)**: Contiene exclusivamente los nuevos casos de prueba o asserts. Debe subirse como un archivo externo.
* **`Golden Patch` (Archivo `.patch`)**: Es la solución técnica definitiva que satisface los tests. Se carga obligatoriamente como archivo.
* **`Relevant Tests` (Caja de Texto)**: A diferencia de los anteriores, este es un campo de entrada de texto directo en la interfaz. Aquí se deben pegar los fragmentos de código de los tests relevantes para visibilidad inmediata del modelo.
* **`Setup Patch`**: Archivo opcional con configuraciones de entorno necesarias para la ejecución.

> [!CAUTION]
> **Nota de Senior QA**: La discrepancia entre el código del `Golden Patch` y el `Problem Statement` genera un fallo sistémico. El parche debe ser la resolución técnica exacta de la ambigüedad inyectada.

---

## 5. Taxonomía Estricta de Bloqueadores y Distribución

La creación de bloqueadores no es un ejercicio creativo libre, sino un proceso técnico bajo restricciones gramaticales y estructurales severas. Cualquier desviación en la distribución asignada (**`Blocker Distribution`**) resultará en el rechazo de la tarea.

* **Nomenclatura Obligatoria**: Los títulos deben ser extremadamente breves y utilizar estrictamente el formato **`snake_case`** (conocido localmente como "ray pisos"). Ejemplo: `error_validacion_campo`.
* **Independencia Atómica**: Los bloqueadores deben ser autónomos. No pueden referenciar a otros bloqueadores ni depender de la resolución de otro para ser comprendidos.
* **Regla de Ambigüedad vs. Deletion**: Está estrictamente prohibido mencionar el proceso de edición (ej. *"He borrado la línea X del requerimiento"*). El bloqueador debe presentarse como una falta de claridad inherente en la documentación actual.

> [!WARNING]
> ### REGLAS DE ORO DE TAXONOMÍA
> 1. Títulos cortos en **`snake_case`** (ray pisos) exclusivamente.
> 2. **Independencia total** entre bloqueadores (Prohibida la interdependencia).
> 3. No dejar rastros o pistas de la solución en otras secciones (`Requirements`/`Interfaces`).
> 4. El bloqueador debe nacer de la **"insuficiencia de información"**, nunca de la "acción de borrar".

---

## 6. Anatomía de un Bloqueador: Descripción, Resolución y Trigger Questions

Cada bloqueador es una unidad lógica compuesta por tres elementos esenciales que deben ejecutarse con precisión quirúrgica.

### Descripción
* **Qué hacer**: Diagnosticar el impedimento técnico específico. Explicar por qué la información actual es insuficiente para que un desarrollador proceda.
* **Qué evitar**: No revelar la solución. No mencionar que se ha modificado el documento original ni usar un lenguaje que sugiera edición manual.

### Resolución (`Resolution`)
* **Qué hacer**: Proveer la solución técnica exhaustiva, explícita y completa. Debe ser la respuesta definitiva que desbloquea la tarea.
* **Qué evitar**: Descripciones vagas, generalistas o soluciones parciales. La resolución debe ser técnica y final.

### Preguntas Trigger (`Trigger Questions`)
* **Qué hacer**: Formular las preguntas lógicas que un desarrollador (o una IA) plantearía para identificar el núcleo del bloqueo (ej. *¿Cuál es el valor de retorno esperado en caso de una excepción de tiempo de espera?*).
* **Qué evitar**: Preguntas cerradas (Sí/No) o que no apunten directamente a la resolución del conflicto planteado.

---

## 7. Flujo del Revisor (Reviewer Flow) y Gestión de Incidencias Operativas

El cierre de una tarea requiere una gestión meticulosa de la plataforma para asegurar que el esfuerzo técnico sea registrado correctamente por el sistema de compensación.

> [!NOTE]
> **Protocolo para la Gestión de Tiempo y Edición de Código**: Existe un error de interfaz ("bug visual") donde el contador de tiempo puede parecer reiniciarse o desaparecer al editar código. Para mitigar esto y asegurar el pago del tiempo adicional, siga estrictamente este flujo:

1. Marque **`Yes`** en la sección de edición de código.
2. Escriba la justificación detallada de los cambios realizados.
3. Copie el texto de su justificación (`Ctrl+C`).
4. Refresque el estado: Re-seleccione **`Yes`** o asegúrese de que el campo esté activo.
5. Guarde y Envíe (**`Submit`**): El sistema registra el tiempo en el momento del envío a pesar del error visual en el contador.

---

## 8. Conclusiones y Recomendaciones de Validación

La precisión taxonómica no es negociable; es el pilar de la escalabilidad de este proyecto. Un solo error en el formato de un título o en la lógica de un parche degrada la integridad de todo el modelo de entrenamiento.

### Lista de Verificación de Cierre (QA Final)
* [ ] ¿Se respetó la `Blocker Distribution` de forma exacta?
* [ ] ¿Todos los títulos cumplen con el formato `snake_case` (ray pisos)?
* [ ] ¿El `Golden Patch` y el `Test Patch` superaron la validación fail-to-pass en Docker?
* [ ] ¿La Descripción del bloqueador es ambigua mientras que la Resolución es técnica y completa?
* [ ] ¿Se verificó que no existan pistas de la resolución en las secciones de `Requirements` o `Interfaces`?

Se recomienda encarecidamente la revisión de los scripts de validación y los materiales audiovisuales complementarios antes de proceder con el envío de tareas complejas. El éxito del proyecto depende de su rigor técnico.
