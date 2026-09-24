# Changelog — Gestor Inteligente de Vehículos

> Este proyecto sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y el versionado [Semantic Versioning](https://semver.org/lang/es/). Este documento mantiene el historial real de decisiones y evolución del proyecto.

---

## [Unreleased]

### Added
- Incorporada la arquitectura de la aplicación en `docs/arquitectura.md`: modelo cliente-servidor en 3 capas, justificación del stack, comunicación entre capas y correspondencia con los servicios de Render (Static Site, Web Service, Postgres).
- Documentada la relación entre las capas de la arquitectura y los módulos definidos en `docs/modulos.md`.

### Changed
- Reformulada la descripción del Módulo Analítico y de Alertas en `docs/modulos.md` para alinearla con la terminología unificada.

---

## [0.2.0] - 2026-09-10

### Added
- Incorporado el análisis de viabilidad de dominio y conocimiento del equipo en `docs/viabilidad.md`.
- Documentada la adopción de Render como plataforma definitiva de despliegue en `docs/stack.md`, `docs/viabilidad.md` y `README.md`.

### Changed
- Refactorizada la sección de impacto en `docs/alcance.md` con enfoque cuantitativo y consecuencias financieras reales.
- Actualizada la evidencia de validación del problema en `docs/alcance.md`, priorizando datos y fuentes del contexto económico argentino.
- Redefinidos los objetivos específicos de `docs/plan-de-trabajo.md` orientándolos a metas de entrega y gestión del proyecto.
- Reformulados los criterios de éxito del proyecto en `docs/plan-de-trabajo.md` incorporando métricas cuantificables de impacto sobre el usuario.
- Reorganizada la matriz de riesgos en `docs/plan-de-trabajo.md` y `docs/viabilidad.md`, priorizando el impacto de la curva de aprendizaje técnico y ajustando las consideraciones de rendimiento.
- Unificación de los archivos `viabilidad.md` y `viabilidad-operativa-competencia.md` para evitar fragmentación en el repositorio.

### Removed
- Eliminadas las referencias y análisis comparativos inconclusos relativos a Railway en toda la documentación.
- Removida la redundancia de alcance en `docs/plan-de-trabajo.md` mediante enlace relativo a `docs/alcance.md`.
- Eliminada la carpeta anidada `docs/docs/` y el archivo duplicado `Changelog3.md`.

---

## [0.1.0] - Documentación inicial del proyecto

### Added
- Definición del problema, propuesta de solución y validación con evidencia externa en `docs/alcance.md`.
- Definición del alcance del producto (MVP) y del proyecto.
- Evaluación inicial de viabilidad de negocio, técnica y operativa.
- Definición del stack tecnológico inicial: React + TypeScript + Vite + Tailwind CSS, Python + FastAPI, PostgreSQL.
- Estructura de carpetas del repositorio y pautas de control de versiones.

### Technical
- Decisión de arquitectura: separación de frontend, backend y base de datos como servicios independientes, con despliegue en la nube.

### Decisiones del equipo
- Se seleccionó "Gestor Inteligente de Vehículo" frente a otras alternativas por su menor riesgo técnico y dependencia exclusiva de datos del usuario.
- Se seleccionó el enfoque relacional (React + FastAPI + PostgreSQL) dado que los datos del proyecto son inherentemente relacionales.