# Historial — Outcome Ladybug

> **Propósito:** Registro histórico de TODO lo ya realizado en el proyecto.
> Las entradas más recientes van arriba. No se borra nada de aquí.
> **Última actualización:** 2026-06-03

---

## 2026-06-03 — CORRECCIÓN importante: modelos a usar en Cursor

Pedro compartió un mensaje de la comunidad de Outlier (canal Outcome-lady, 28-05-2026) que ACLARA y CORRIGE lo que decía el Welcome viejo de la tarea.

- **Welcome viejo decía:** NO usar Opus 4.7, Gemini 3.1, GPT 5.5.
- **Comunidad (más reciente, manda):** los modelos de los evals son **GPT-5.4, Opus 4.6 y Gemini 3.1**, o también **GPT-5.5**. Usarlos sobre todo en guessability, check 1 y check 2.

→ Recomendación corregida para Pedro (sin Claude): **Gemini 3.1 Pro** o **GPT-5.5**.
→ Se actualizó esto en `agent.md` y `Progreso.md`. (Antes se había recomendado por error Gemini 2.5 Pro.)

---

## 2026-06-03 — Instalación del entorno técnico (Docker + WSL2 + Cursor)

Se montó el entorno completo de trabajo en la laptop de Pedro, paso a paso (él es nuevo y se guió todo desde cero):

- Instalada la extensión **Dev Containers** en Cursor.
- Instalado **WSL2 + Ubuntu** vía `wsl --install` (usuario: pedro).
- Instalado **Docker Desktop** (con backend WSL2). Verificado: "Engine running" + `docker run hello-world` exitoso.
- Creado `C:\Users\pedro\.wslconfig` con límite memory=4GB, processors=2 (para proteger la RAM de la laptop). Aplicado con `wsl --shutdown`.
- Se le indicó dar **Skip** al login de Docker (no necesita cuenta).

Specs de la laptop (justas): Lenovo IdeaPad Slim 3, i3-N305, 8GB RAM (queda apretada), ~363GB disco libre.

**Decisión local vs VPS:** se evaluó usar el VPS Contabo (8GB RAM, 4 cores) para aliviar la laptop, pero se descartó por ahora: el VPS ya corre producción (EasyPanel con chatwoot, n8n, evolution-api, redis, postgres) y su disco está al ~65% (solo ~25GB libres), y las imágenes sweap son grandes. Riesgo de llenar disco y afectar producción. Se queda en LOCAL; el contenedor de tarea casi siempre duerme (poca RAM), el mayor consumo en la laptop es Chrome.

Entorno LISTO para empezar tareas reales.

---

## 2026-06-03 — Sesión de onboarding / aprender a empezar una tarea

Pedro rechazó una tarea real hoy por ser nuevo y no saber por dónde empezar. Sesión enfocada en bajar todo a lo básico (estaba abrumado).

Lo que se cubrió y quedó entendido:

- **Concepto central del proyecto:** el trabajo NO es resolver el código, es ESCONDER un dato crítico (blocker) para que la IA falle al intentar resolver sin preguntar.
- **Modelos en Cursor:** prohibidos Opus 4.7 / Gemini 3.1 / GPT 5.5. Pedro no tiene acceso a Claude (bloqueado en su país). Recomendación: **Gemini 2.5 Pro** (1ª) o **Gemini 3.5 Flash** (2ª).
- **Qué es un prompt:** texto de instrucciones; las plantillas están en `Guias/`, se rellenan los `{{...}}` y se pegan en el chat de IA de Cursor.
- **Cómo se evidencia el fallo de la IA:** con resultados de tests (rojo), NO con capturas. Outlier además corre su propio Agent Feedback con 3 agentes.
- **Trampa del Welcome:** debe incluirse un "thin space" en la respuesta o el score es 0.

**Ejemplo real trabajado** (tarea rechazada, proyecto navidrome / Go — revert de walkDirTree a OS filesystem):
- Identificado un blocker `missing_parameter`: la lista exacta de "Windows system folders" a ignorar está en el Golden Patch pero no en el Problem Statement.
- Se mostró el prompt 4 ya rellenado con los datos de la tarea y un ejemplo de `blocker_registry.json` resultante.

Quedamos en retomar mañana: meter el blocker en el problem statement + practicar un 2º blocker (ambiguo/contradictorio).

---

## 2026-06-03 — Documentación y estructura del proyecto

- Guardadas y verificadas las **13 guías oficiales** de Outlier en `Guias/` (numeración 1–13 = espejo del sidebar):
  - 1–3: guías conceptuales (Attemper Instructions, Codebase Modifications, Blocker Registry).
  - 4–13: prompts y checks operativos (Generator, Check 1, Check 2, Validator, Reviewers, Golden/Tests generator, Guessability, Supplementary Checker, Task Checker Evals).
  - Verificado: sin basura de codificación, contenido completo, notas de setup y placeholders `{{...}}` intactos.
- Creado el archivo raíz `agent.md` con explicación del proyecto + mapa de navegación para el próximo LLM.
- Creada la carpeta `Progreso-Actual/` con `Progreso.md`.
- Creada la carpeta `Historial/` con este `historial.md`.

---

## Plantilla para nueva entrada

```
## [FECHA] — Título de lo realizado
- Detalle 1
- Detalle 2
```
