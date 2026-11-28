# Cómo contribuir

Guía para sumar cambios al proyecto sin pisarnos entre integrantes. Describe el flujo que ya se usa en el historial del repositorio: cada persona trabaja en una **rama por cambio** dentro del repositorio compartido y lo propone con un **pull request (PR)** hacia `main`.

> La regla de oro: **nadie sube directo a `main`**. Todo cambio entra por un PR.

---

## 1. Preparación (una sola vez)

1. Pedir que te agreguen como colaboradora del repositorio (**Settings → Collaborators**), si todavía no tenés permiso de escritura.
2. Clonar el repositorio:

   ```bash
   git clone https://github.com/gabrielamachin/gestor-vehiculos-grupo-117.git
   cd gestor-vehiculos-grupo-117
   ```

3. Poner el proyecto en marcha en tu computadora: [backend](backend/README.md) y [frontend](frontend/README.md).

> Si no tenés permiso de escritura y no podés conseguirlo, ver la sección 5 (trabajo con fork).

---

## 2. Flujo para cada cambio

### 2.1. Partir de `main` actualizado

```bash
git checkout main
git pull origin main      # trae lo que las demás ya fusionaron
```

### 2.2. Crear una rama nueva

Una rama por cambio, con un nombre corto que empiece con el tipo de trabajo:

| Prefijo | Para qué | Ejemplo |
|---|---|---|
| `feat/` | Funcionalidad nueva | `feat/frontend-dashboard` |
| `fix/` | Corrección de un error | `fix/formato-costo-km` |
| `docs/` | Documentación | `docs/actualizar-docs` |
| `test/` | Pruebas | `test/playwright-e2e` |
| `ci/` | Integración continua | `ci/automated-tests` |

```bash
git checkout -b docs/nombre-del-cambio
```

### 2.3. Hacer los cambios y commits

Commits chicos y con mensaje en el formato `tipo(alcance): descripción`, en español y en minúscula. El alcance es opcional:

```text
feat(frontend): agrega carga de kilometraje y planes de mantenimiento
fix: corrige el formato del costo real por kilómetro en las pruebas E2E
docs: actualiza documentación técnica y plan de trabajo
```

```bash
git status                 # ver qué cambió
git add archivo1 archivo2  # agregar archivos puntuales (evitá `git add .` si no revisaste qué entra)
git commit -m "docs: agrega guía de contribución"
```

### 2.4. Verificar antes de subir

Correr las mismas comprobaciones que hará la integración continua (también están como lista en la [plantilla de PR](.github/PULL_REQUEST_TEMPLATE.md)). Solo las que correspondan a lo que tocaste:

| Si tocaste… | Correr |
|---|---|
| Backend | `cd backend && python -m pytest` |
| Frontend | `cd frontend && npm run lint && npm run build` |
| Interfaz o flujos completos | `cd frontend && npm run test:e2e` (ver [frontend/e2e/README.md](frontend/e2e/README.md)) |
| Solo documentación | Releer el diff y comprobar que los enlaces funcionan |

### 2.5. Subir la rama

```bash
git push -u origin docs/nombre-del-cambio
```

### 2.6. Abrir el pull request

1. En GitHub, entrar al repositorio: aparece un cartel **Compare & pull request** para tu rama.
2. Verificar que diga **base: main** y como origen tu rama.
3. Completar la plantilla (resumen, cambios, cómo probar, qué verificaste).
4. Crear el PR. Se ejecuta la CI automáticamente: esperá a que termine en verde. Si falla, corregí en la misma rama y volvé a hacer `git push`; el PR se actualiza solo.
5. Pedir la revisión de una compañera en **Reviewers**.

### 2.7. Después de la revisión

- Si piden cambios: commits nuevos en la misma rama y `git push`.
- Cuando se fusione, volvé a empezar desde el paso 2.1 para el siguiente cambio. La rama vieja se puede borrar:

  ```bash
  git branch -d docs/nombre-del-cambio
  git push origin --delete docs/nombre-del-cambio
  ```

---

## 3. Convenciones para no molestar a las demás

- **Un PR = un tema.** Un PR corto se revisa en minutos; uno grande se posterga.
- **No mezclar cambios no relacionados** (por ejemplo, un arreglo de backend con un cambio de estilos).
- **No reformatear archivos que no tocaste.** Genera conflictos y ruido en la revisión.
- **Antes de empezar algo grande**, avisar al grupo o abrir un *issue*, para evitar que dos personas hagan lo mismo.
- **No fusionar tu propio PR**: lo revisa y lo acepta otra persona del equipo.
- **Si dos PRs tocan el mismo archivo**, el segundo en fusionarse debe actualizar su rama:

  ```bash
  git checkout mi-rama
  git fetch origin
  git merge origin/main    # resolver conflictos si aparecen, luego commit y push
  ```

- **Actualizar [CHANGELOG.md](CHANGELOG.md)** bajo `[Unreleased]` cuando el cambio sea visible para el equipo o para la entrega.
- **Nunca subir secretos**: el archivo `.env` está ignorado; solo se versionan los `.env.example`.

## 4. Convenciones técnicas

- Backend: ver "Convenciones al agregar un módulo" en [backend/README.md](backend/README.md) y la arquitectura en [docs/arquitectura.md](docs/arquitectura.md).
- Frontend: ver "Convenciones" en [frontend/README.md](frontend/README.md).

## 5. Si no tenés permiso de escritura (trabajo con fork)

Si no sos colaboradora del repositorio, podés proponer cambios desde una copia propia:

1. Hacer un **fork** desde GitHub (botón **Fork**) y clonar tu fork.
2. Agregar el repositorio principal como `upstream`:

   ```bash
   git remote add upstream https://github.com/gabrielamachin/gestor-vehiculos-grupo-117.git
   ```

3. Antes de cada rama, traer lo último: `git pull upstream main` (o **Sync fork** en GitHub).
4. Trabajar igual que en la sección 2, pero subiendo la rama a tu fork (`origin`) y abriendo el PR hacia `main` del repositorio principal.
