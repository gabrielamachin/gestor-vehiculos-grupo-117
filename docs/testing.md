# Pruebas

## Estrategia

La suite combina cuatro niveles:

1. Pruebas unitarias de fórmulas y funciones puras.
2. Pruebas de servicios y validaciones de reglas de negocio.
3. Pruebas API e integración con PostgreSQL.
4. Pruebas E2E con navegador, API y base de datos reales.

## Pruebas del backend

Los archivos están en `backend/tests/`.

| Tipo | Archivos principales |
|---|---|
| Autenticación y seguridad | `test_security.py`, `test_sesion_api.py`, `test_sesion_integracion.py` |
| Usuarios y API general | `test_api.py` |
| Vehículos | `test_vehiculos_*` |
| Categorías | `test_categorias_*` |
| Gastos | `test_gastos_*` |
| Kilometraje | `test_kilometraje_*` |
| Mantenimiento | `test_mantenimiento_*` |
| Indicadores | `test_indicadores_*` |
| Datos de demostración | `test_demo_integracion.py` |

Ejecución local:

```powershell
cd backend
$env:TEST_DATABASE_URL="postgresql://postgres:TU_CLAVE@localhost:5432/gestor_vehiculos_test"
python -m pytest
```

Sin `TEST_DATABASE_URL`, las pruebas que requieren PostgreSQL se omiten. Las pruebas de integración ejecutan el esquema sobre la base indicada y pueden eliminar sus tablas.

La base debe ser exclusiva y puede llamarse `gestor_vehiculos_test` o `gestor_vehiculos_e2e`.

## Pruebas Playwright

Los archivos están en `frontend/e2e/`:

| Archivo | Cobertura |
|---|---|
| `auth.spec.ts` | Registro, login, sesión persistente y logout |
| `flujo.spec.ts` | Vehículo, lectura, gasto y costo por km |
| `borrar-vehiculo.spec.ts` | Confirmaciones y bajas con datos |
| `aislamiento.spec.ts` | Separación de recursos entre usuarios |
| `dashboard-demo.spec.ts` | Indicadores con datos de demostración |
| `responsive.spec.ts` | Diseño a 360 px sin desbordamiento |

Preparación:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt

cd ..\frontend
npm ci
npx playwright install chromium
```

Ejecutar:

```powershell
cd frontend
$env:E2E_DATABASE_URL="postgresql://postgres:TU_CLAVE@localhost:5432/gestor_vehiculos_e2e"
npm run test:e2e
```

Configuración adicional:

- `E2E_PYTHON` permite indicar otro ejecutable de Python.
- Playwright inicia la API en el puerto 8000 y el frontend en el 5173.
- Se niega a reutilizar servidores ya abiertos en esos puertos.
- No ejecuta contra una base cuyo nombre no contenga `test` o `e2e`.

Comandos útiles:

```powershell
npm run test:e2e:informe
npm run test:e2e:ui
npx playwright test auth
npx playwright test --headed
```

Los informes quedan en `frontend/playwright-report/` y `frontend/test-results/`. Ante un fallo se conservan captura y traza.

## CI

El workflow `.github/workflows/ci.yml` ejecuta:

- lint del frontend;
- análisis de tipos y compilación;
- pruebas de pytest con PostgreSQL 16;
- instalación de Chromium;
- suite Playwright con PostgreSQL desechable.

Las ejecuciones se realizan en pull requests, pushes a `main` y manualmente.

## Datos seguros

Las pruebas deben usar exclusivamente bases de prueba. No apunten a PostgreSQL de desarrollo o producción mediante `TEST_DATABASE_URL` o `E2E_DATABASE_URL`.
