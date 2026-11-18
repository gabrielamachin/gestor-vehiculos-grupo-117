# Despliegue en Render y PWA

## Servicios

El archivo `render.yaml` define una arquitectura de tres componentes:

1. PostgreSQL administrada (`gestor-vehiculos-db`).
2. API FastAPI (`gestor-vehiculos-api`) en un Web Service.
3. Frontend React/Vite (`gestor-vehiculos-web`) en un Static Site.

## Publicación inicial

1. Conectar el repositorio en **New > Blueprint**.
2. Revisar los nombres y regiones de los servicios antes de aplicar.
3. Aplicar el Blueprint y esperar el build inicial.
4. Abrir `/health/db` del backend para verificar la conexión con PostgreSQL.
5. Abrir el sitio estático y ejecutar un registro o inicio de sesión de prueba.

## Variables de entorno

El backend usa:

| Variable | Uso |
|---|---|
| `DATABASE_URL` | URL interna de PostgreSQL obtenida de la base administrada. |
| `JWT_SECRET` | Secreto generado por Render para firmar tokens JWT. |
| `JWT_EXPIRE_MINUTES` | Duración de los tokens, 60 minutos por defecto. |
| `CORS_ORIGINS` | URL HTTPS exacta del frontend. |
| `COOKIE_SECURE` | Debe ser `true` en producción HTTPS. |

El frontend usa `VITE_API_URL=/api`. Durante el build, Render reescribe `/api/*` hacia el servicio FastAPI.

## Base de datos

El despliegue ejecuta `python -m scripts.inicializar_bd` antes de iniciar el backend. Ese script crea el esquema solamente si todavía no existe la tabla `usuarios`; no elimina datos. Para preparar una base de pruebas, el script `reiniciar_bd` sigue limitado a bases cuyo nombre contenga `test` o `e2e`.

## PWA

El plugin `vite-plugin-pwa` genera el manifiesto y el service worker durante `npm run build`. La aplicación usa actualización automática, modo `standalone`, caché de recursos estáticos y fallback de rutas a `index.html`.

Después de publicar:

1. Abrir el sitio por HTTPS.
2. Verificar en DevTools > Application > Manifest que el nombre, icono y `start_url` sean correctos.
3. Verificar que el service worker esté activo.
4. Probar el funcionamiento básico sin red después de haber cargado la aplicación.

La API no se incluye en la caché offline: el frontend solo almacena los activos locales necesarios para abrir la interfaz.
