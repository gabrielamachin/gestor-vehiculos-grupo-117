# Changelog — Gestor Inteligente de Vehículos

> Este proyecto sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y el versionado [Semantic Versioning](https://semver.org/lang/es/). Este documento mantiene el historial real de decisiones y evolución del proyecto.

---

## [Unreleased]

### Added (correcciones de la 2.ª entrega)
- Documentada la estructura interna de la API en `docs/arquitectura.md` (sección 1.4): organización por módulo y, dentro de cada módulo, por responsabilidad (router, schemas, service, repository, models), con reglas de dependencia y estructura del frontend.
- Incorporada la nomenclatura de los módulos en `docs/modulos.md`: un único nombre por concepto, compartido entre documentación, API, base de datos y carpetas.
- Incorporados en `docs/modulos.md` el diagrama de relaciones entre módulos, la tabla de casos de uso por módulo y el diagrama de secuencia del flujo crítico "consultar el costo real por km".
- Modelo de datos ampliado de 3 a 6 tablas: `categorias_gasto`, `lecturas_kilometraje` y `planes_mantenimiento`.
- Incorporada en `docs/esquema-db.md` la justificación de la separación de tablas y la sección sobre dónde se concentra la complejidad de la aplicación.
- Incorporada en `docs/esquema-db.md` (sección 6) la matriz de validación por capa, aclarando que la base de datos es la última línea de defensa y no la única.
- Incorporada en `docs/esquema-db.md` (sección 7) la justificación de cada índice y de los índices descartados.
- Módulo Vehículos (`backend/app/vehiculos/`): alta, listado, consulta, edición de alias y baja de vehículos (prefijo `/vehiculos`). Expone `obtener_de_usuario`, que los demás módulos usan para verificar la pertenencia antes de operar sobre un vehículo.
- Módulo Kilometraje (`backend/app/kilometraje/`): registro, listado, edición y baja de lecturas del odómetro, y consulta de la última lectura, que es el kilometraje actual del vehículo (prefijo `/kilometraje`). Valida que el odómetro no retroceda respecto del kilometraje inicial ni de las demás lecturas, y admite una sola lectura por vehículo y día.
- `core/tipos.py`: tipos compartidos `Kilometros` (validado como `Decimal` y entregado como número JSON) y `FechaNoFutura`.
- Pruebas de servicio, de API y de integración para Vehículos y Kilometraje, incluido el aislamiento entre usuarios. Las de integración corren contra PostgreSQL real y se activan con la variable `TEST_DATABASE_URL`; comparten el helper `tests/utils_integracion.py`.
- Módulo Categorías (`backend/app/categorias/`): consulta del catálogo de categorías de gasto (prefijo `/categorias`). Expone `obtener_activa` y `obtener_por_codigo` para Gastos e Indicadores.
- Módulo Mantenimiento (`backend/app/mantenimiento/`): alta, listado, consulta, edición y baja de planes de mantenimiento por vehículo (prefijo `/mantenimiento`). Expone `obtener_plan_del_vehiculo` y `listar_planes_de_vehiculo` para Gastos e Indicadores.
- Pruebas de servicio, de API y de integración para Categorías y Mantenimiento.

### Added
- Incorporada la arquitectura de la aplicación en `docs/arquitectura.md`: modelo cliente-servidor en 3 capas, justificación del stack, justificación de PWA vs. app móvil nativa y comunicación entre capas.
- Documentada la relación entre las capas de la arquitectura y los módulos definidos en `docs/modulos.md`.
- Incorporado `docs/esquema-db.md` con el modelo relacional del proyecto: diagrama entidad-relación, diccionario de datos, relaciones, decisiones de diseño y validación de cobertura contra el MVP.
- Incorporado `database/schema.sql` con la definición del esquema relacional (usuarios, vehículos y gastos) y sus índices para consultas agregadas.
- Incorporadas restricciones `CHECK` en `database/schema.sql` para reforzar las reglas de integridad del modelo (monto de gasto positivo, coherencia de kilometrajes, formato de email y strings no vacíos).
- Documentada la estrategia de validación en tres capas (UI, backend y base de datos) en `docs/esquema-db.md`.

### Changed (correcciones de la 2.ª entrega)
- Los módulos de `docs/modulos.md` pasan de dividirse por capa a definirse como componentes del dominio: Usuarios, Vehículos, Categorías, Gastos, Kilometraje, Mantenimiento e Indicadores. "Seguridad/Autenticación" se unifica en Usuarios, "Transacciones" en Gastos, y "Analítico y de Alertas" y "Reportes" en Indicadores.
- El contrato de la API pasa a un prefijo por módulo (`/usuarios`, `/vehiculos`, `/categorias`, `/gastos`, `/kilometraje`, `/mantenimiento`, `/indicadores`).
- La categoría de gasto pasa de `enum` a tabla propia: agregar una categoría es un `INSERT`, sin migración.
- `vehiculos.kilometraje_actual` se reemplaza por el historial `lecturas_kilometraje` (el kilometraje actual es la última lectura).
- `vehiculos.intervalo_mantenimiento_km` se reemplaza por `planes_mantenimiento` (varios planes por vehículo); `gastos` incorpora `plan_mantenimiento_id` y `kilometraje` opcionales.
- Agregada la restricción `UNIQUE (usuario_id, alias)` en `vehiculos`.
- Índices de `gastos` rediseñados: se eliminan `idx_gastos_vehiculo_id`, `idx_gastos_fecha` e `idx_gastos_categoria` (redundantes o de baja selectividad) y se incorporan `idx_gastos_vehiculo_fecha` e `idx_gastos_plan_km`.
- Actualizada en `docs/viabilidad.md` la mitigación de latencia de consultas para reflejar los nuevos índices.

### Changed
- Reorganizada la documentación de arquitectura y datos: `docs/arquitectura.md` cubre la arquitectura de la aplicación y `docs/esquema-db.md` el esquema de base de datos, para que cada documento tenga una única responsabilidad.
- Reformulada la descripción del Módulo Analítico y de Alertas en `docs/modulos.md` para alinearla con la terminología unificada.

### Removed
- Removida la sección de arquitectura de datos (Parte 2) de `docs/arquitectura.md`; su contenido se trasladó a `docs/esquema-db.md`.

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
