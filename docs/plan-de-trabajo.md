# Plan de trabajo

## Estado actual

El MVP principal está implementado: autenticación, vehículos, categorías, gastos, lecturas, planes e indicadores cuentan con backend, frontend y pruebas.

## Evidencia del cronograma original

La planificación inicial se organizó en ocho semanas. La versión anterior del cronograma contemplaba las siguientes etapas:

| Semana original | Planificación prevista |
|---|---|
| 1 | Setup del repositorio, estructura del proyecto, entorno local y cierre del modelo inicial |
| 2 | CRUD de usuarios y vehículos, con autenticación básica |
| 3-4 | CRUD de gastos por categoría y registro de kilometraje |
| 4-5 | Costo real por km y gasto acumulado por categoría |
| 5-6 | Alertas de combustible y estimación de próximos mantenimientos |
| 6-7 | Heurística reparar/reemplazar y pulido de interfaz |
| 7 | Despliegue del frontend, backend y base de datos |
| 8 | Datos de demostración, pruebas E2E y documentación final |

Este cronograma representaba una estimación académica inicial. El desarrollo real mostró que algunos conceptos necesitaban separarse en más entidades y que la integración, las pruebas y el despliegue requerían trabajo adicional.

## Ajustes realizados al cronograma

El cronograma se ajustó por resultados intermedios, correcciones de arquitectura y prioridades técnicas:

1. **Revisión del modelo antes de completar los módulos:** el modelo inicial se amplió de tres tablas a seis. Se incorporaron `categorias_gasto`, `lecturas_kilometraje` y `planes_mantenimiento`, además de la asociación entre gastos y planes. Por esto, las entidades base quedaron documentadas antes de finalizar el backend.
2. **Desarrollo vertical por módulo:** en vez de concentrar primero todos los CRUD, se completaron iteraciones consecutivas de vehículos y kilometraje, categorías y mantenimiento, y finalmente gastos e indicadores. Esta secuencia redujo dependencias pendientes entre módulos.
3. **Autenticación integrada desde el inicio del backend:** el módulo Usuarios y la estructura base de la API quedaron disponibles antes de comenzar el CRUD completo del frontend.
4. **Frontend construida después de estabilizar la API:** el dashboard, los formularios y las pantallas de edición se añadieron cuando ya existían los servicios principales del backend.
5. **Pruebas incorporadas durante la implementación:** no se dejaron exclusivamente para la semana final. Se agregaron pruebas unitarias y de integración por módulo y, posteriormente, pruebas E2E con Playwright.
6. **CI incorporado antes del cierre:** el workflow pasó a ejecutar análisis y compilación del frontend, pruebas del backend y pruebas E2E con PostgreSQL desechable.
7. **Despliegue agregado como fase verificable:** Render y PWA no se trataron solo como una publicación final. Se configuraron, se corrigió el Blueprint y se agregó documentación de operación.
8. **Pulido posterior al MVP funcional:** modo oscuro, mejoras responsive, formato de indicadores y ajustes de contraste se realizaron después de completar las funcionalidades principales.

## Cronograma ajustado comparado con el original

| Área | Plan original | Ajuste real |
|---|---|---|
| Entidades y relaciones | Se cerrarían en la semana 1 | Se revisaron durante septiembre y octubre; el modelo ampliado quedó registrado como corrección de arquitectura |
| Usuarios y vehículos | Semana 2 | Se implementaron antes de completar los restantes módulos |
| Kilometraje y mantenimiento | Implícitos dentro de gastos o la semana 3-5 | Se separaron como módulos propios con sus propias APIs y pruebas |
| Gastos e indicadores | Semana 3-6 | Se completaron como una iteración backend/frontend posterior a las entidades base |
| Dashboard | Previsto junto a indicadores | Se agregó una vez disponible el API de vehículo e indicadores |
| Pruebas E2E | Semana 8 | Se desarrollaron y documentaron después del flujo funcional, y quedaron integradas en CI |
| Despliegue en Render | Semana 7 | Se configuró a mitad de noviembre y se corrigió con ajustes posteriores del Blueprint |
| Cierre visual y documentación | Semana 8 | Continuó hasta el pulido final de responsive, modo oscuro y documentos técnicos |

## Evidencia histórica del ajuste

Los registros del repositorio respaldan esta evolución:

- Septiembre de 2026: documentación inicial, esquema de base de datos y arquitectura.
- 1-3 de noviembre: estructura base del backend y módulo Usuarios.
- 4-10 de noviembre: vehículos, kilometraje, categorías, mantenimiento y gastos.
- 7-10 de noviembre: incorporación de indicadores y pantallas principales del frontend.
- 12-15 de noviembre: kilometraje y planes en interfaz, mejoras de mensajes y edición/baja de vehículos.
- 15-17 de noviembre: suite Playwright y ejecución automatizada en GitHub Actions.
- 18 de noviembre: configuración de Render y PWA.
- 23 de noviembre: pulido responsive y modo oscuro.

La misma evolución aparece reflejada en `CHANGELOG.md`, en las ramas fusionadas y en el historial de Git. Estas referencias permiten distinguir la planificación inicial de las decisiones tomadas durante el desarrollo.

## Objetivos cumplidos

- [x] Repositorio único con backend, frontend, base de datos y documentación.
- [x] Modelo PostgreSQL normalizado con restricciones e índices.
- [x] Registro, login y sesión JWT por cookie.
- [x] CRUD de vehículos con aislamiento por usuario.
- [x] CRUD de gastos y asociación con planes.
- [x] CRUD de lecturas de kilometraje.
- [x] CRUD de planes de mantenimiento.
- [x] Indicadores de costo por km, categorías, combustible y mantenimiento.
- [x] Orientación heurística reparar/reemplazar.
- [x] PWA responsive.
- [x] Datos de demostración y scripts de inicialización.
- [x] Pruebas unitarias, de servicio, API, integración y E2E.
- [x] CI en GitHub Actions.
- [x] Blueprint de despliegue en Render.

## Tareas siguientes sugeridas

- Verificar y actualizar periódicamente el despliegue público.
- Revisar seguridad de secretos y permisos de bases de datos.
- Añadir pruebas para nuevos módulos antes de modificar su contrato.
- Mantener documentación y esquema sincronizados con migraciones futuras.
- Documentar el proceso de rollback y restauración de base.

## Riesgos y mitigaciones

| Riesgo | Mitigación aplicada |
|---|---|
| Datos incompletos | Los indicadores devuelven estados sin datos o insuficientes |
| Acceso a datos ajenos | Los servicios verifican pertenencia con el usuario del JWT |
| Reinicio accidental de producción | Los scripts destructivos rechazan bases que no contienen `test` o `e2e` |
| Cambios incompatibles | CI ejecuta lint, build, backend y Playwright |
| CORS incorrecto | `CORS_ORIGINS` admite una lista separada por comas |
| Servicio suspendido por inactividad | `/health` permite comprobación liviana; `/health/db` verifica PostgreSQL |
| Dependencias diferentes | El lockfile npm y los requirements fijan el entorno reproducible |

## Criterios de cierre

- Las pruebas y el build pasan en CI.
- Cada recurso protegido valida el usuario autenticado.
- El esquema puede inicializarse desde `database/schema.sql`.
- Los datos de demo no se usan en pruebas contra una base de desarrollo.
- El despliegue público responde a `/health/db`.
