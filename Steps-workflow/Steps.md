# 🚀 Armar el entorno — Paso a paso (modo bebé)

> **Mi guía rápida para empezar solo.** Basada en `Guias/2Guia_Codebase_Modifications_QA.md`.
> Docker corre en mi laptop (Windows). Cursor se conecta al contenedor local.
> El `<image>` y el `commit link` me los da el repositorio / interfaz de la tarea.

---

## FASE 0 — Encender Docker en mi laptop (Windows)

**0.1** — Abrir el **CMD** (tecla Windows → escribe `cmd` → Enter).

**0.2** — Encender Docker Desktop:
```cmd
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```
> Abre la app. Esperar ~30 seg a que el ícono de la ballena (abajo derecha) deje de moverse.

**0.3** — Verificar que Docker ya está vivo:
```cmd
docker info
```
> Si muestra info y NO error de "cannot connect" → listo. Si da error, esperar más.

---

## FASE 1 — Descargar y correr la imagen (me la da el repo de la tarea)

**1.1** — Descargar la imagen (pegar el tag que da la tarea):
```cmd
docker pull <image>
```
Ejemplo:
```cmd
docker pull jefzda/sweap-images:ansible.ansible-ansible__ansible-a6e671db25381ed111bbad0ab3e7d97366395d05-v0f01c69f1e2528b935359cfe578530722bca2c59
```
> Tarda (es pesada). Esperar a que termine.

**1.2** — Correr el contenedor (ponerle nombre único en `<your_container_name>`, ej. `task02`):
```cmd
docker run -d --name <your_container_name> --platform linux/amd64 <image> -c "while true; do sleep 3600; done"
```
> `-d` = segundo plano. El `sleep` mantiene vivo el contenedor. Si el nombre ya existe, borrar el viejo: `docker rm <nombre>`.

**1.3** (opcional) — Confirmar que corre:
```cmd
docker ps
```
> Debe aparecer con STATUS "Up".

---

## FASE 2 — Entrar al contenedor desde Cursor

**2.1** — Una sola vez: instalar extensiones en Cursor → **Dev Containers** y **Docker**.

**2.2** — En Cursor: `Ctrl + Shift + P` → **Dev Containers: Attach to Running Container**.

**2.3** — Elegir el nombre del contenedor (Paso 1.2, ej. `task02`).
> Se abre ventana nueva de Cursor **dentro** del contenedor.

**2.4** — Click en **Open Folder** → navegar a `/app` → **OK**.
> Ahora se ven todos los archivos del repo (conf, db, navidrome, task_files, etc.).

---

## FASE 3 — Verificar el parent commit (CRÍTICO, no saltar)

> Todo se construye **sobre el parent commit**. Si trabajo desde otro commit, todo sale mal.

**3.1** — En la tarea, abrir el **commit link** en GitHub. El **parent commit** sale a la derecha (ej. `80b48fc`).

**3.2** — Abrir terminal del contenedor en Cursor (`Terminal → New Terminal`):
```bash
git rev-parse HEAD
```
**3.3** — Los primeros 7 caracteres deben coincidir con el parent de GitHub. Si NO coinciden → parar y revisar.

---

## FASE 4 — Validar los patches originales (que la base no esté rota)

**4.1** — Sacar el golden patch del commit original (pegar el hash del commit de la tarea):
```bash
git show <commit> > golden_patch.diff
```
**4.2** — Aplicarlo al codebase:
```bash
git apply golden_patch.diff
```
**4.3** — Correr SOLO los tests que menciona el test patch:
```bash
pytest <ruta/al/test_file.py>
```
**4.4** — Todos deben dar `PASSED`. Si alguno falla → parar, la base está rota.

---

## FASE 5 — Setup patch (SOLO si la base "regala" las respuestas)

> Si el codebase tiene valores/comentarios/funciones que dejarían al agente resolver el blocker sin preguntar, hay que quitarlos primero. **Si no aplica, saltar toda la Fase 5.**

**5.1** — Volver al estado limpio del parent (revertir el golden patch):
```bash
git checkout -- .
```
**5.2** — Editar los archivos para borrar las pistas que delatan las respuestas.

**5.3** — Generar el setup patch:
```bash
git diff > setup_patch.diff
```
**5.4** — Commitear el setup (vuelve la nueva base):
```bash
git add <setup_files>
git commit -m "Setup changes for blockers"
```

---

## FASE 6 — Inyectar los blockers

**6.1** — Re-aplicar el golden patch encima del setup:
```bash
git apply golden_patch.diff
```
**6.2** — Mirar qué archivos cambia el commit (pestaña **Changes** en Cursor, o el commit URL).

**6.3** — Editar esos archivos para meter los blockers (según el blocker registry de la tarea).

---

## FASE 7 — Generar los patches finales (`.diff`)

**7.1** — Mirar el estado:
```bash
git status
```
**7.2** — Si hay archivos nuevos (untracked), agregarlos:
```bash
git add <file_1> <file_2>
```
**7.3** — Generar el golden obstruido (**SOLO código fuente + changelog, NADA de tests**):
```bash
git diff --cached -- <archivo_fuente_1> <changelog_2> > golden_patch_obstructed.diff
```
**7.4** — Generar el test obstruido (**SOLO tests + test data, NADA de fuente**):
```bash
git diff --cached -- <test_1> <test_data_2> > test_patch_obstructed.diff
```
> Ojo: ambos salen de `--cached` (staged), NO del diff sin stagear.

---

## FASE 8 — Subir los patches a la tarea

**8.1** — En Cursor, click derecho en cada `.diff` del explorer → **Download...**. Bajar:
- `setup_patch.diff` *(si lo creé en Fase 5)*
- `golden_patch_obstructed.diff`
- `test_patch_obstructed.diff`

**8.2** — En la interfaz de la tarea, subir cada `.diff` a su campo correspondiente.

---

## ⚠️ Reglas de oro (las que más se olvidan)
1. **Siempre** verificar `git rev-parse HEAD` = parent commit ANTES de tocar nada.
2. Nunca generar patches desde otro commit que no sea el parent.
3. Orden estricto: validar originales → setup → inyectar blockers → generar obstruidos → subir.
4. `golden_patch_obstructed.diff` **NO** lleva tests. `test_patch_obstructed.diff` **NO** lleva código fuente.
5. Los obstruidos salen de `--cached`, no del unstaged.

---

## Flujo en una línea
```text
docker pull/run → attach Cursor → /app → verificar parent → validar originales → (setup) → inyectar blockers → golden+test obstruidos → subir
```
