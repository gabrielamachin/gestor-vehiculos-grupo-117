# Plan de trabajo — Gestor Inteligente de Vehículos

**Documento:** `docs/plan-de-trabajo.md`
**Responsable:** Integrante 3 — Gestión del Proyecto, Operatividad y Asistencia IA

> Este documento define el cronograma, las tareas y los entregables del proyecto. El alcance del producto y del proyecto se definen en `docs/alcance.md`; el stack tecnológico y las decisiones de arquitectura se definen en `docs/stack.md` y `docs/arquitectura.md`. Este plan no redefine esas decisiones, las toma como dato de entrada para organizar la ejecución.

---

## 1. Objetivo general

Desarrollar, dentro del plazo asignado por la cátedra para el TPI, una Progressive Web App que implemente las funcionalidades del MVP definidas en `docs/alcance.md` (sección 8.1), con el stack tecnológico definido en `docs/stack.md`, desplegada en un servicio en la nube.

## 2. Objetivos específicos

- Implementar el modelo de datos y el CRUD de vehículos y gastos por categoría.
- Implementar el cálculo de costo real por kilómetro y el gasto acumulado por categoría.
- Implementar la comparación de gasto de combustible contra el promedio histórico propio del usuario.
- Implementar la estimación de próximo mantenimiento por kilometraje.
- Implementar la heurística de orientación "reparar o reemplazar".
- Desplegar la aplicación completa (frontend, backend y base de datos) en la infraestructura elegida.

## 3. Alcance y no alcance

Se remite íntegramente a `docs/alcance.md` (secciones 8.1 y 8.2). Este plan de trabajo no agrega ni quita funcionalidades respecto de lo ya definido allí; cualquier tarea que implique una funcionalidad no listada en la sección 8.1 debe tratarse como fuera de alcance y no debe planificarse en este cronograma.

## 4. Supuestos del cronograma

- El equipo cuenta con 3 integrantes, cada uno a cargo de su perfil (Producto y Negocio, Arquitectura y Tecnología, Gestión y Operatividad), colaborando de forma transversal en el desarrollo.
- El cronograma se organiza en **8 semanas**, ajustable según el plazo real de entrega definido por la cátedra.
- La decisión de despliegue (Render vs. Railway, pendiente en `docs/stack.md`) debe cerrarse antes de comenzar la semana 6, para no bloquear la etapa de despliegue.

## 5. Cronograma por semana

| Semana | Foco | Tareas principales |
|---|---|---|
| 1 | Setup del proyecto | Repositorio único en GitHub, estructura de carpetas (`backend/`, `frontend/`, `docs/`), configuración de entorno local, `.env.example`. Cierre del modelo de datos (`docs/arquitectura.md`). |
| 2 | Entidades base | CRUD de usuarios y vehículos (backend + frontend). Autenticación básica (JWT). |
| 3-4 | Gestión de gastos | CRUD de gastos por categoría (combustible, mantenimiento, reparaciones, otros). Registro de kilometraje asociado. |
| 4-5 | Indicadores centrales | Cálculo de costo real por km. Gasto acumulado por categoría con gráfico (Recharts/Chart.js). |
| 5-6 | Motor de alertas y estimaciones | Comparación de gasto de combustible vs. promedio histórico propio. Estimación de próximo mantenimiento por kilometraje. |
| 6-7 | Heurística de decisión y pulido | Heurística "reparar o reemplazar". Revisión de UI/UX, manejo de estados vacíos (usuario sin historial cargado). |
| 7 | Despliegue | Configuración de variables de entorno, CORS, despliegue de backend, frontend y base de datos en la plataforma elegida. |
| 8 | Cierre | Carga de datos de demostración, pruebas end-to-end, documentación final, preparación de la presentación. |

## 6. Entregables por etapa

| Etapa | Entregable |
|---|---|
| Semana 2 | Modelo de datos cerrado + CRUD de vehículos funcional |
| Semana 4 | CRUD de gastos operativo |
| Semana 5 | Costo por km y gasto anual por categoría visibles en el frontend |
| Semana 6 | Alertas de combustible y estimación de mantenimiento funcionando |
| Semana 7 | Heurística reparar/reemplazar + aplicación desplegada en un entorno accesible |
| Semana 8 | Documentación completa (`docs/`), datos de demo cargados, proyecto listo para presentación |

## 7. Riesgos operativos y de ejecución, y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Indefinición prolongada entre Render y Railway retrasa el despliegue | Media | Alto | Fijar fecha límite de decisión (antes de semana 6), documentada en `docs/stack.md` |
| Curva de aprendizaje del stack (FastAPI, TypeScript) consume más tiempo del previsto | Media | Medio | Priorizar un "hola mundo" end-to-end en la semana 1, antes de avanzar con features |
| Falta de datos de prueba realistas dificulta demostrar las alertas y la heurística | Media | Alto | Precargar 2-3 vehículos con historial simulado desde la semana 2, en paralelo al desarrollo |
| Descoordinación entre los tres perfiles (producto, arquitectura, gestión) genera trabajo duplicado o inconsistente | Baja | Medio | Repositorio único con documentación centralizada (`docs/`), seguimiento en Trello, comunicación diaria por WhatsApp (ya definido en `docs/viabilidad.md`) |
| Alcance que crece durante el desarrollo ("ya que estamos, agreguemos X") | Media | Alto | Revisar `docs/alcance.md` (sección 8.2) en cada instancia de avance del equipo |

## 8. Recursos humanos necesarios

- 3 integrantes, cada uno con dedicación parcial (proyecto académico), distribuidos según los perfiles ya definidos: Producto y Negocio, Arquitectura y Tecnología, Gestión y Operatividad.
- No se contempla incorporar roles adicionales (por ejemplo, diseño UI dedicado o QA independiente); estas tareas se distribuyen entre los tres integrantes según la etapa del cronograma.

## 9. Criterios de éxito del MVP

- El sistema calcula correctamente el costo por km a partir de datos cargados de prueba.
- El sistema detecta al menos un caso de alerta de gasto de combustible fuera del promedio histórico del propio usuario.
- La heurística "reparar o reemplazar" devuelve un resultado coherente con los datos cargados, presentado explícitamente como orientación y no como tasación.
- La aplicación está desplegada y accesible públicamente para la presentación final.
