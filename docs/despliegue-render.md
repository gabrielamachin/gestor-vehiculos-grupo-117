# Despliegue en Render

## Blueprint

`render.yaml` define tres recursos:

| Recurso | Nombre | Tipo |
|---|---|---|
| Base de datos | `gestor-vehiculos-db` | PostgreSQL free |
| API | `gestor-vehiculos-api` | Web Service Python |
| Frontend | `gestor-vehiculos-web` | Static Site |

## Configuración del backend

Build:

```bash
cd backend && pip install -r requirements.txt
```

Inicio:

```bash
cd backend && python -m scripts.inicializar_bd && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

El health check configurado es `/health/db`.

Variables:

| Variable | Valor |
|---|---|
| `DATABASE_URL` | Conexión a PostgreSQL administrada por Render |
| `JWT_SECRET` | Valor generado por Render |
| `JWT_EXPIRE_MINUTES` | `60` |
| `CORS_ORIGINS` | URL HTTPS del frontend |
| `COOKIE_SECURE` | `true` |
| `PYTHON_VERSION` | `3.12.0` |

## Configuración del frontend

Build:

```bash
cd frontend && npm ci && npm run build
```

`VITE_API_URL` se establece en `/api`. Las rutas `/api/*` se reescriben al servicio `gestor-vehiculos-api`. Las demás rutas se reescriben a `/index.html` para React Router.

## Publicación

1. En Render, elegir **New > Blueprint** y conectar el repositorio.
2. Crear o confirmar los tres recursos.
3. Esperar la instalación de Python, npm y la compilación PWA.
4. Verificar `https://gestor-vehiculos-api.onrender.com/health`.
5. Verificar `https://gestor-vehiculos-api.onrender.com/health/db`.
6. Abrir el frontend y probar registro, login y creación de un vehículo.

Si las URL cambian, actualizar `CORS_ORIGINS` y las reescrituras de `render.yaml`.

## Inicialización de datos

`inicializar_bd.py` usa `database/schema.sql` solo si la tabla `usuarios` aún no existe. No recrea ni borra datos en una base ya inicializada.

Los scripts `reiniciar_bd.py` y `cargar_datos_demo.py` están destinados a bases de prueba. El reinicio rechaza una base cuyo nombre no contenga `test` o `e2e`.

## PWA

La compilación genera el manifiesto y el service worker mediante `vite-plugin-pwa`. Funciona con actualización automática y modo `standalone`.

- Las rutas locales tienen fallback a `index.html`.
- Los activos locales pueden conservarse en caché.
- Las solicitudes de API no forman parte de una política offline.
- El entorno público debe usar HTTPS para que las cookies y PWA funcionen correctamente.
