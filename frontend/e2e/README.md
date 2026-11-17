# Pruebas end-to-end (Playwright)

Manejan un navegador real contra la aplicación completa (frontend + API + PostgreSQL) y verifican los flujos
principales como el usuario final. Complementan las pruebas del backend (`backend/tests`), que no cubren la interfaz.

## Cobertura

| Archivo | Qué verifica |
|---|---|
| `auth.spec.ts` | Registro, sesión que sobrevive a recargar, cierre de sesión, login con contraseña incorrecta, redirección al login |
| `flujo.spec.ts` | Vehículo → lectura de kilometraje → gasto hasta ver el costo real por km; validaciones del formulario de gasto |
| `borrar-vehiculo.spec.ts` | Baja de un vehículo vacío y con datos (confirmación escrita), cancelar con Esc o botón, baja de un gasto |
| `aislamiento.spec.ts` | Un usuario no puede ver ni abrir el vehículo de otro (interfaz y API) |
| `dashboard-demo.spec.ts` | Con los datos de demo, cada indicador muestra el estado previsto (alerta, vencido, reemplazo, vacío) |
| `responsive.spec.ts` | A 360 px de ancho no hay desborde horizontal; deja capturas en el informe |

## Preparación (una sola vez)

1. **Crear una base de datos exclusiva** para estas pruebas, por ejemplo `gestor_vehiculos_e2e` (pgAdmin → Create → Database).
   Cada corrida **borra y recrea todas sus tablas**; por seguridad el script se niega a actuar si el nombre de la base no
   contiene `e2e` o `test`. Puede ser la misma que usás para las pruebas de integración del backend.
2. Desde `frontend/`:

   ```powershell
   npm install
   npx playwright install chromium
   ```

3. El backend necesita su entorno virtual en `backend/.venv` (el ya existente). No hace falta activarlo.

## Ejecución

Desde `frontend/`:

```powershell
$env:E2E_DATABASE_URL="postgresql://postgres:TU_CLAVE@localhost:5432/gestor_vehiculos_e2e"
npm run test:e2e
```

**Antes de ejecutarlas, cerrar la API y frontend de desarrollo** (puertos 8000 y 5173). Las pruebas levantan los suyos
y, a propósito, se niegan a arrancar si esos puertos están ocupados. De esta manera, nunca se prueba contra la base de desarrollo.

| Comando | Para qué |
|---|---|
| `npm run test:e2e` | Corre todo y deja un informe |
| `npm run test:e2e:informe` | Abre el informe HTML (resultados, capturas de 360 px, trazas de fallos) |
| `npm run test:e2e:ui` | Modo interactivo: elegir pruebas y ver cada paso |
| `npx playwright test auth` | Solo un archivo |
| `npx playwright test --headed` | Con el navegador visible |

Si una prueba falla, el informe incluye una captura y una traza (`trace`) con cada paso, la red y la consola.
Los informes y resultados se generan en `frontend/playwright-report/` y `frontend/test-results/`. Son artefactos locales
de cada ejecución y no hace falta versionarlos.

## CI

El workflow `.github/workflows/ci.yml` ejecuta estas pruebas en GitHub Actions junto con el lint y build del frontend
y la suite del backend. Usa PostgreSQL desechable con una base cuyo nombre incluye `test`; no requiere secretos de
repositorio ni accede a bases locales, de desarrollo o de producción. Si E2E falla, el informe de Playwright se
publica como artefacto de la ejecución.

## Cómo funcionan

- `playwright.config.ts` levanta la API (`uvicorn`, contra la base E2E) y el frontend (`npm run dev`).
- `global-setup.ts` recrea el esquema (`backend/scripts/reiniciar_bd.py`) y carga los datos de demo
  (`backend/scripts/cargar_datos_demo.py`) antes de empezar.
- **Cada prueba usa su propio usuario** (registrado por la API), por lo que no dependen del orden. Las del dashboard usan el
  usuario demo, que es de solo lectura: ninguna prueba debe modificarlo ni borrarlo.
- Los datos de arranque se crean por la API (`ayudas.ts`) y la interfaz se usa solo para lo que se quiere probar. Es más
  rápido y menos frágil.
- Los elementos se buscan por **rol y texto visible** (`getByRole`, `getByLabel`), como los percibe el usuario: si se cambia
  un texto de la interfaz, hay que actualizarlo en las pruebas.

## Agregar una prueba

1. Crear `e2e/algo.spec.ts` e importar `test` y `expect` de `@playwright/test`.
2. Abrir sesión con `conSesion(page)` (usuario nuevo) o `conSesionDemo(page)`.
3. Preparar datos con `crearVehiculoPorApi`, `crearGastoPorApi`, etc., y recién después manejar la interfaz.
4. Esperar con `expect(...)` (reintenta solo) y nunca con pausas fijas.

## Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `Falta la variable E2E_DATABASE_URL` | Definirla en la misma terminal (ver arriba) |
| `... is already used` | Hay una API o un frontend de desarrollo abiertos: cerrarlos |
| `Por seguridad solo se reinicia una base cuyo nombre contenga...` | La base E2E debe llamarse como `gestor_vehiculos_e2e` |
| Error al ejecutar Python o `No module named ...` | Falta `backend/.venv`: crearlo e instalar `requirements.txt`, o definir `E2E_PYTHON` con la ruta a otro Python |
| Timeout esperando un servidor | Se ven los logs en la terminal; suele ser un error de arranque de la API o del frontend |
