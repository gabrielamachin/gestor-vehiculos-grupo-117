# Stack tecnológico

## Resumen

| Componente | Tecnología | Uso |
|---|---|---|
| Frontend | React 19, TypeScript 5.7, Vite 6 | PWA, rutas, formularios y dashboard |
| Estilos | Tailwind CSS 4 | Diseño responsive y tema claro/oscuro |
| Backend | Python 3.12, FastAPI | API REST, validación y lógica de negocio |
| Persistencia | PostgreSQL 16 en desarrollo/CI; PostgreSQL administrado en producción | Modelo relacional |
| ORM/DB | SQLAlchemy 2, psycopg2 | Mapeo y sesiones de base de datos |
| Autenticación | JWT firmado con PyJWT y cookie HttpOnly | Sesiones de navegador y clientes HTTP |
| Pruebas | pytest, HTTPX y Playwright | Backend, integración y navegador |
| CI | GitHub Actions | Lint, build, backend y E2E |
| Despliegue | Render Blueprint | API, frontend PWA y PostgreSQL |

Las versiones mínimas declaradas por los requisitos son FastAPI 0.109, Pydantic 2.5, SQLAlchemy 2.0, psycopg2 2.9 y Python 3.12 en CI/despliegue. Los valores reales se fijan con `backend/requirements.txt` y `frontend/package-lock.json`.

## Frontend

- **React 19** y **TypeScript**: componentes tipados y composición por funcionalidades.
- **React Router 7**: rutas públicas y protegidas.
- **Vite 6**: servidor de desarrollo, proxy `/api` y compilación.
- **Tailwind CSS 4**: estilos utilitarios y responsive.
- **vite-plugin-pwa**: manifiesto, service worker y actualización automática.
- **Lexend**: tipografía cargada localmente mediante `@fontsource-variable`.
- **Playwright**: pruebas automatizadas de interfaz en Chromium.

El frontend no guarda el usuario ni el token en `localStorage`. Envía las solicitudes a `/api` y utiliza la cookie HttpOnly `gestor_sesion`; Swagger y clientes externos pueden usar el header `Authorization: Bearer <token>`.

## Backend

- **FastAPI**: routers REST y documentación OpenAPI.
- **Pydantic 2**: validación de entrada y serialización de salida.
- **SQLAlchemy 2**: modelos y sesiones. El esquema no se crea con `create_all`.
- **PostgreSQL**: restricciones, claves foráneas, transacciones e índices.
- **bcrypt**: hash de contraseñas.
- **PyJWT**: creación y validación de tokens.
- **pydantic-settings**: carga de variables de entorno y archivo `.env`.

Cada módulo sigue la estructura `router -> service -> repository -> SQLAlchemy`, salvo indicadores, que calcula datos sobre los servicios de otros módulos.

## Persistencia

El esquema se administra con `database/schema.sql`. Durante el arranque el backend no altera automáticamente las tablas: `python -m scripts.inicializar_bd` crea el esquema únicamente si todavía no existe la tabla `usuarios`. Los scripts de reinicio están protegidos para bases cuyo nombre contenga `test` o `e2e`.

## Pruebas

- `pytest` ejecuta pruebas unitarias, de servicio, API e integración del backend.
- PostgreSQL exclusivo separa las pruebas de integración de la base de desarrollo.
- Playwright inicia un servidor API y uno frontend aislados y usa una base PostgreSQL exclusiva de E2E.

La estrategia y los comandos completos están documentados en [testing.md](testing.md).

## Infraestructura

El archivo `render.yaml` crea:

- una base PostgreSQL administrada;
- un Web Service Python para FastAPI;
- un Static Site para el frontend PWA;
- una reescritura `/api/*` desde el frontend hacia el backend.

El plan gratuito puede suspender servicios por inactividad. `/health` permite comprobaciones livianas y `/health/db` verifica que la API pueda consultar PostgreSQL.
