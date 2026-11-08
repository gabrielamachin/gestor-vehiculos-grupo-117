# Frontend — Gestor Inteligente de Vehículos

PWA responsive (mobile-first) con React, TypeScript, Vite, Tailwind CSS y React Router. Se comunica con la API del [backend](../backend/README.md) mediante un único cliente HTTP.

## Puesta en marcha local

Desde la carpeta `frontend/`:

```bash
npm install
npm run dev
```

Abre en http://localhost:5173. Requiere la API corriendo en `http://localhost:8000`: el servidor de Vite reenvía `/api/*` a esa dirección (ver `vite.config.ts`), de modo que el navegador siempre habla con un único origen.

| Script | Qué hace |
|---|---|
| `npm run dev` | Servidor de desarrollo con recarga |
| `npm run build` | Chequea tipos y genera `dist/` |
| `npm run lint` | Análisis estático |
| `npm run preview` | Sirve `dist/` localmente |

## Autenticación

La sesión usa una **cookie `HttpOnly`** que la API establece en `POST /usuarios/sesion` y borra en `DELETE /usuarios/sesion`. El JavaScript nunca ve el token (no se usa `localStorage`), por lo que un script malicioso no puede robarlo. Para saber si hay sesión, la app consulta `GET /usuarios/me` al abrirse.

Para que la cookie sea de primera parte, la API se consume **en el mismo origen** que el frontend, bajo `/api`:

- Desarrollo: proxy de Vite (`vite.config.ts`).
- Producción: regla de reescritura del Static Site de Render (`/api/*` → la API).

## Variables de entorno

Ninguna es obligatoria. `VITE_API_URL` (opcional, por defecto `/api`) solo se define si la API está en otro origen.

## Estructura

Mismo criterio que el backend: una carpeta por módulo del dominio (ver [docs/modulos.md](../docs/modulos.md)).

```text
src/
├── main.tsx              # punto de entrada: router + proveedor de sesión
├── app/                  # rutas, layout y guardas de acceso (RutaProtegida / RutaPublica)
├── shared/
│   ├── api/              # cliente HTTP (normaliza errores, avisa si la sesión venció) y ApiError
│   └── componentes/      # UI reutilizable: Boton, Campo, Alerta, Cargando, TarjetaAuth
└── features/
    ├── usuarios/         # login, registro, AuthProvider, useAuth
    └── vehiculos/        # (por ahora solo lectura)
```

Para agregar un módulo: crear `src/features/<modulo>/` con `tipos.ts`, `api.ts` (usa `solicitar` de `shared/api/cliente`) y sus pantallas; registrar las rutas en `app/App.tsx`.

## Convenciones

- Todas las llamadas a la API pasan por `solicitar()`; no usar `fetch` directo en los componentes.
- No guardar el token en el navegador: la autenticación es la cookie HttpOnly.
- Los errores llegan como `ApiError` con el mensaje listo para mostrar (`mensajeDeError`).
- Un 401 en un endpoint protegido (sesión vencida) vuelve al login automáticamente.
- Los componentes cargan datos con `useEffect` y un estado `cargando | error | ok`.
