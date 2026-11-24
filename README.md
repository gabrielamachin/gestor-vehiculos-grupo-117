# Gestor Inteligente de Vehículos

> Sistema para gestionar gastos de combustible, mantenimiento, seguro y neumáticos, con análisis de costo real por km y alertas inteligentes.

---

## Descripción del proyecto

Aplicación full-stack que permite al dueño de un vehículo registrar todos los gastos asociados al auto y obtener indicadores clave para la toma de decisiones financieras.

## Grupo 117 - Integrantes:
Anahi Betancort - anahi.betancort@gmail.com
Camila Rissi - rissicamila07@gmail.com
Gabriela Machin - gabrielamachin@gmail.com

### Funcionalidades principales

- **Costo real por km**: Suma de todos los gastos ÷ kilómetros recorridos
- **Alertas de gasto**: Detección de aumentos vs. promedio histórico propio
- **Mantenimiento predictivo**: Próxima revisión estimada por kilometraje
- **Gasto anual por categoría**: Combustible, seguros, mantenimiento, neumáticos

### Actores

- **Usuario propietario**: Registra vehículos y gastos, visualiza indicadores
- **Sistema**: Genera alertas y cálculos automáticos

## Entrega del proyecto

- [Video de presentación](URL_DEL_VIDEO)
- [Informe PDF](URL_DEL_INFORME_PDF)

---

## Documentación detallada

La documentación técnica se encuentra en [docs](docs/):

- [Alcance](docs/alcance.md)
- [Arquitectura](docs/arquitectura.md)
- [Módulos](docs/modulos.md)
- [Stack](docs/stack.md)
- [Esquema de base de datos](docs/esquema-db.md)
- [Pruebas](docs/testing.md)
- [Despliegue en Render](docs/despliegue-render.md)
- [Viabilidad](docs/viabilidad.md)
- [Plan de trabajo](docs/plan-de-trabajo.md)

---

## Stack tecnológico

### Frontend
- React 19 — Librería UI
- TypeScript 5.7 — Tipado estático
- Vite 6 — Build tool
- Tailwind CSS 4 — Estilos
- React Router 7 — Enrutamiento
- Playwright — Pruebas E2E

### Backend
- Python 3.10+ — Lenguaje
- FastAPI 0.109+ — Framework web

### Base de datos
- PostgreSQL 15+ — Base de datos relacional
- psycopg2 2.x — Driver

### Infraestructura
- **Plataforma:** Render.
- **CI/CD:** GitHub Actions.

## Despliegue en Render

El proyecto incluye un Blueprint en [render.yaml](render.yaml) para crear:

- una base PostgreSQL administrada;
- el servicio web del backend FastAPI;
- el sitio estático PWA de React/Vite.

1. Desde Render, seleccionar **New > Blueprint** y conectar este repositorio.
2. Confirmar la creación de `gestor-vehiculos-db`, `gestor-vehiculos-api` y `gestor-vehiculos-web`.
3. Si Render asigna URLs distintas a las previstas, actualizar `CORS_ORIGINS`, la reescritura `/api/*` de `render.yaml` y el origen del frontend.
4. Comprobar el estado con `https://gestor-vehiculos-api.onrender.com/health/db`.

La aplicación se instala como PWA desde navegadores compatibles mediante el botón **Instalar aplicación** del navegador. Los activos de la interfaz se almacenan en caché y las rutas internas usan `index.html` como fallback.

Consultar la guía detallada de [despliegue en Render y configuración PWA](docs/despliegue-render.md).