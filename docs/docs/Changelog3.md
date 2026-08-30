# Changelog — Gestor Inteligente de Vehículos

> Este proyecto sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y el versionado [Semantic Versioning](https://semver.org/lang/es/). Las pautas de registro de cambios se definen en `docs/changelog-pautas.md` (Integrante 2). Este documento mantiene el historial real de decisiones y evolución del proyecto (Integrante 3).

---

## [Unreleased]

### Added
- Definición de la sección "Viabilidad operativa y temporal" en `docs/viabilidad.md`.
- Definición de la sección "Análisis de competencia y diferenciación" en `docs/viabilidad.md`.
- Creación de `docs/plan-de-trabajo.md` con cronograma de 8 semanas, entregables por etapa y riesgos operativos.

### Changed
- Pendiente: actualizar `docs/plan-de-trabajo.md` una vez se cierre la decisión de infraestructura (Render vs. Railway) documentada en `docs/stack.md`.

---

## [0.1.0] - Documentación inicial del proyecto

### Added
- Definición del problema y propuesta de solución en `docs/alcance.md` (Integrante 1), incluyendo validación con evidencia externa (Synchrony 2025, Andor et al. 2020, encuestas de mantenimiento vehicular en EE. UU., cobertura periodística local).
- Definición del alcance del producto (MVP) y del alcance del proyecto en `docs/alcance.md` (Integrante 1).
- Evaluación de viabilidad de negocio en `docs/viabilidad.md` (Integrante 1).
- Definición del stack tecnológico en `docs/stack.md`: React + TypeScript + Vite + Tailwind CSS (frontend), Python + FastAPI (backend), PostgreSQL (base de datos) (Integrante 2).
- Evaluación de viabilidad técnica y de escalabilidad en `docs/viabilidad.md`, incluyendo tabla de complejidad de desarrollo y checklist de viabilidad (Integrante 2).
- Documentación de riesgos técnicos y mitigaciones (free tier sleeping, CORS, migraciones, variables de entorno, rendimiento) en `docs/viabilidad.md` (Integrante 2).
- Estructura de carpetas del repositorio (`docs/`, `backend/`, `frontend/`, `.env.example`) documentada en `README.md`.

### Technical
- Decisión de arquitectura: separación de frontend, backend y base de datos como servicios independientes, con despliegue en la nube.
- Definición del formato de Changelog (Keep a Changelog + Semantic Versioning) en `docs/changelog-pautas.md` (Integrante 2).

### Decisiones del equipo
- Entre las tres ideas de proyecto evaluadas (Gestor Inteligente de Vehículo, Sistema de reposición de stock para comercios, Plataforma de intercambio circular de libros), se seleccionó **Gestor Inteligente de Vehículo** por su menor riesgo técnico, dependencia exclusiva de datos cargados por el usuario y facilidad de demostración en vivo.
- Entre las dos propuestas de stack evaluadas (enfoque relacional/transaccional vs. enfoque documental/NoSQL), se seleccionó el **enfoque relacional** (React + FastAPI + PostgreSQL), dado que los datos del proyecto (usuario → vehículos → gastos) son inherentemente relacionales.

### Pendiente
- Decisión final entre Render y Railway como plataforma de despliegue (`docs/stack.md`), a resolver antes de la semana 6 del cronograma (`docs/plan-de-trabajo.md`).
