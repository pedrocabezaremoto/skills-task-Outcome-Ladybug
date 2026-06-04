# Progreso Actual — Outcome Ladybug

> **Propósito:** Registro vivo del estado ACTUAL del trabajo. Qué se está haciendo ahora y qué falta.
> Cuando algo se complete, muévelo a `Historial/historial.md`.
> **Última actualización:** 2026-06-03

---

## Estado general

Base de conocimiento documentada + **entorno técnico instalado y funcionando**. Listo para trabajar tareas reales.

---

## 🖥️ Entorno técnico (instalado y verificado 2026-06-03)

**Todo corre LOCAL en la laptop de Pedro** (Lenovo IdeaPad Slim 3, i3-N305, 8GB RAM, ~363GB disco libre):

- ✅ Extensión **Dev Containers** en Cursor
- ✅ **WSL2 + Ubuntu** (usuario: pedro)
- ✅ **Docker Desktop** funcionando ("Engine running", `hello-world` corrió OK)
- ✅ Límite de RAM para Docker: archivo `C:\Users\pedro\.wslconfig` → memory=4GB, processors=2
- ⚠️ NO necesita login en Docker (se le da Skip)

**Cómo arrancar una tarea** (cuando acepte una en Outlier):
1. `docker pull <imagen-de-la-tarea>`
2. `docker run -d --name mi_tarea <imagen> -c "while true; do sleep 3600; done"`
3. Cursor: `Ctrl+Shift+P` → Dev Containers: Attach to Running Container → elegir `mi_tarea`
4. Abrir carpeta `/app`

**Decisión laptop vs VPS:** se quedó en LOCAL (laptop). El VPS Contabo NO se usa para esto porque ya tiene producción (chatwoot, n8n, evolution-api) y el disco está al 65%. El contenedor de tarea casi siempre está dormido (poca RAM); el verdadero consumo de RAM en la laptop es Chrome. Recomendación: cerrar pestañas de Chrome al trabajar.

---

## En curso / pendiente

- [ ] **(MAÑANA) Practicar buscar un 2º blocker** en la tarea de ejemplo (uno tipo "ambiguo" o "contradictorio"), para ver que no todos son iguales.
- [ ] **(MAÑANA) Aprender el paso siguiente:** cómo METER el blocker dentro del Problem Statement (dejarlo vago / borrar el dato exacto).
- [ ] Pendiente: practicar el flujo completo de Checks (Check 1 falla / Check 2 pasa).

---

## 📌 Dónde quedamos (2026-06-03)

Pedro es NUEVO en el proyecto y estaba abrumado. Hoy bajamos todo a lo básico. Conceptos clave que YA entendió:

1. **Qué es la tarea:** NO es resolver código. Es ESCONDER un dato importante para que la IA falle al resolver sin preguntar.
2. **Qué modelo usar en Cursor (CORREGIDO 2026-06-03 según comunidad 28-05):** usar GPT-5.4, Opus 4.6, Gemini 3.1 o GPT-5.5. Pedro NO tiene Claude (bloqueado en su país). → Usa **Gemini 3.1 Pro** o **GPT-5.5**. (El Welcome viejo decía lo contrario; manda la comunidad.)
3. **Qué es un "prompt":** es solo texto de instrucciones. Las plantillas ya están en `Guias/` (ej. `4Prompt_...`). Se rellenan los huecos `{{...}}` y se pegan en el chat de IA de Cursor.
4. **Cómo se evidencia que la IA falla:** NO con capturas. Es con el resultado de correr los tests (que salgan en rojo) + Outlier corre su propio Agent Feedback con 3 agentes.

**Ejemplo trabajado hoy** (tarea que Pedro rechazó, proyecto navidrome / Go):
- Blocker de ejemplo encontrado: la lista exacta de "Windows system folders" a ignorar NO está en el Problem Statement pero SÍ en el Golden Patch → blocker tipo `missing_parameter`.
- Se le mostró cómo rellenar el prompt 4 con los datos reales de la tarea y qué `blocker_registry.json` devolvería Cursor.

**Siguiente sesión:** retomar desde el Paso siguiente (meter el blocker en el problem statement) y practicar un 2º blocker.

---

## Notas rápidas

- Las 13 guías oficiales de Outlier ya están guardadas y verificadas en `Guias/` (espejo del sidebar).
- Estructura del proyecto documentada en `../agent.md`.
- ⚠️ Recordar siempre el **thin space** en la respuesta final de la tarea (si no, score = 0).

---

## Plantilla para nueva entrada

```
### [FECHA] — Título corto
- Qué estoy haciendo:
- Estado: (en curso / bloqueado / por revisar)
- Siguiente paso:
```
