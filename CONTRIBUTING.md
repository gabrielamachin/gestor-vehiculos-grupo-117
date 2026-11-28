# Cómo contribuir

Guía para sumar cambios al proyecto sin pisarnos entre integrantes. Describe el flujo que ya se usa en el historial del repositorio: cada persona trabaja en **su fork**, en una **rama por cambio**, y lo propone con un **pull request (PR)** hacia `main` del repositorio principal.

> La regla de oro: **nadie sube directo a `main`**. Todo cambio entra por un PR.

---

## 1. Preparación (una sola vez)

1. Hacer un **fork** del repositorio principal desde GitHub (botón **Fork**, arriba a la derecha). Crea una copia en tu cuenta; podés romperla sin afectar al resto.
2. Clonar **tu fork** (no el principal):

   ```bash
   git clone https://github.com/TU_USUARIO/gestor-vehiculos-prueba.git
   cd gestor-vehiculos-prueba
   ```

3. Agregar el repositorio principal como `upstream`, para poder traer los cambios de las demás:

   ```bash
   git remote add upstream https://github.com/CamilaRL1/gestor-vehiculos-prueba.git
   git remote -v    # debe mostrar origin (tu fork) y upstream (el principal)
   ```

4. Poner el proyecto en marcha en tu computadora: [backend](backend/README.md) y [frontend](frontend/README.md).

---

## 2. Flujo para cada cambio

### 2.1. Partir de `main` actualizado

```bash
git checkout main
git pull upstream main      # trae lo que las demás ya fusionaron
git push origin main        # opcional: deja tu fork al día
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

### 2.5. Subir la rama a tu fork

```bash
git push -u origin docs/nombre-del-cambio
```

### 2.6. Abrir el pull request

1. En GitHub, entrar a tu fork: aparece un cartel **Compare & pull request**.
2. Verificar que diga **base repository: CamilaRL1/gestor-vehiculos-prueba**, **base: main**, y como origen tu rama.
3. Completar la plantilla (resumen, cambios, cómo probar, qué verificaste).
4. Crear el PR. Se ejecuta la CI automáticamente: esperá a que termine en verde. Si falla, corregí en la misma rama y volvé a hacer `git push`; el PR se actualiza solo.

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
- **Si dos PRs tocan el mismo archivo**, el segundo en fusionarse debe actualizar su rama:

  ```bash
  git checkout mi-rama
  git fetch upstream
  git merge upstream/main    # resolver conflictos si aparecen, luego commit y push
  ```

- **Actualizar [CHANGELOG.md](CHANGELOG.md)** bajo `[Unreleased]` cuando el cambio sea visible para el equipo o para la entrega.
- **Nunca subir secretos**: el archivo `.env` está ignorado; solo se versionan los `.env.example`.

## 4. Convenciones técnicas

- Backend: ver "Convenciones al agregar un módulo" en [backend/README.md](backend/README.md) y la arquitectura en [docs/arquitectura.md](docs/arquitectura.md).
- Frontend: ver "Convenciones" en [frontend/README.md](frontend/README.md).
