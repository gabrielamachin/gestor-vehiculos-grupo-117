# Evaluación de Viabilidad

## Viabilidad de negocio

El producto está dirigido a usuarios particulares que poseen uno o varios vehículos y necesitan centralizar combustible, mantenimiento, reparaciones y otros gastos. El problema tiene sentido económico porque la dispersión de comprobantes y registros dificulta conocer el costo real de conservación y anticipar gastos.

### Propuesta de valor

La aplicación transforma los datos cargados manualmente por el usuario en información útil:

- costo acumulado y costo real por kilómetro;
- distribución de gastos por categoría;
- comparación del gasto de combustible con el propio historial;
- estimación de próximos mantenimientos;
- Orientación sobre "reparar o reemplazar".

El valor no depende de integraciones externas ni de fuentes de datos que excedan el alcance del MVP. El usuario ingresa sus registros una sola vez y obtiene indicadores que por sí solos pueden ayudar a presupuestar, detectar desvíos y tomar decisiones.

### Público objetivo

El público inicial son propietarios particulares de vehículos que realizan seguimiento ocasional de gastos y mantienen comprobantes en medios físicos o aplicaciones distintas. Se prioriza la gestión individual y no se contempla la administración de flotas ni la participación de talleres o aseguradoras.

### Esfuerzo y retorno

El modelo requiere carga manual. La aplicación compensa ese esfuerzo al eliminar duplicación de registros, conservar el historial y automatizar cálculos que actualmente suelen hacerse por memoria o en planillas.

La viabilidad comercial debe validarse observando si los usuarios:

- registran gastos de forma periódica;
- consultan los indicadores;
- encuentran útil la estimación de mantenimiento;
- mantienen activos sus vehículos en la aplicación.

El proyecto puede comenzar como una herramienta personal o académica sin costos de integración externa. Si evolucionara a un producto comercial, sería necesario validar su disposición a pagar y definir una propuesta de monetización sin afectar la utilidad básica.

### Diferenciación

Frente a planillas y aplicaciones que registran un solo rubro, el proyecto combina gastos, kilometraje y mantenimientos en una misma visión. Su diferencia principal es relacionar estos datos para calcular indicadores por vehículo y compararlos con el historial propio del usuario.

Las herramientas basadas en integraciones externas podrían ofrecer automatización, pero requieren infraestructura y fuentes de datos que están fuera del alcance de esta primera versión.

## Viabilidad funcional

El alcance puede resolverse con datos manuales y cálculos directos. Las operaciones principales son CRUD, agregaciones y reglas sobre fechas y kilómetros. No depende de integraciones externas ni modelos predictivos.

El usuario recibe valor al centralizar gastos y ver métricas comparables. El valor depende de la calidad y cantidad de los datos cargados, por lo que la interfaz debe indicar explícitamente los casos insuficientes.

## Viabilidad técnica

La separación React/FastAPI/PostgreSQL coincide con las responsabilidades del proyecto:

- React permite construir formularios y dashboard responsive.
- FastAPI ofrece validación, routers y OpenAPI.
- PostgreSQL garantiza integridad referencial y restricciones.
- SQLAlchemy permite reemplazar consultas manuales por modelos y repositorios.
- Playwright prueba la integración real navegador/API/base.
- Render permite publicar los tres componentes desde un único Blueprint.

El backend conserva una estructura por capas dentro de cada módulo. Las dependencias son acotadas y no existen ciclos entre los servicios.

## Escalabilidad

El modelo actual está orientado a un MVP académico o pequeño. Puede crecer mediante:

- índices adicionales según consultas reales;
- migraciones versionadas;
- caché solo si la carga y latencia lo justifican;
- particionamiento o exportaciones solo ante volúmenes mayores;
- un servicio de analítica separado si aumenta mucho la carga.

No conviene incorporar estas capacidades sin evidencia de necesidad.

## Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Render suspende instancias gratuitas | Media | Medio | Health checks y tolerancia a arranque en frío |
| Datos insuficientes de un usuario | Alta | Medio | Estados explícitos sin datos |
| CORS mal configurado | Media | Alto | Lista `CORS_ORIGINS` y pruebas de navegador |
| Reinicio de una base equivocada | Baja | Alto | Guardas por nombre de base |
| Secretos expuestos | Baja | Alto | Variables de entorno y generación de JWT en Render |
| Credenciales débiles | Media | Alto | bcrypt y validación de inputs |

## Operación y mantenimiento

La aplicación dispone de health checks, scripts de inicialización, datos de demo, CI y documentación. Las pruebas actuales cubren rutas críticas, pero una nueva migración o cambio de contrato debe ejecutarse en una base separada antes de producción.
