# Viabilidad Operativa, Temporal y Análisis de Competencia

**Documento:** `docs/viabilidad-operativa-competencia.md`  
**Responsable:** Integrante 3 — Gestión del Proyecto, Operatividad y Asistencia IA  

> Este documento complementa la evaluación de viabilidad del proyecto, enfocándose en la capacidad operativa del equipo, la factibilidad del cronograma y el análisis comparativo con soluciones existentes en el mercado.

---

## 1. Viabilidad operativa y temporal

*¿El equipo puede ejecutar este proyecto, con estos recursos, dentro de los plazos disponibles?*

### 1.1 Viabilidad operativa

El equipo está compuesto por 3 integrantes, cada uno responsable de un perfil definido: Producto y Estrategia de Negocio, Arquitectura y Tecnología, y Gestión del Proyecto y Operatividad.

**Condiciones operativas favorables:**
- El proyecto no depende de recursos externos al equipo (talleres, aseguradoras, proveedores de datos), conforme al criterio de corte del MVP definido en `docs/alcance.md`.
- El entorno de desarrollo es completamente local y gratuito, sin barreras de acceso para ningún integrante.
- La comunicación y el seguimiento de tareas ya están definidos (Trello, WhatsApp, repositorio único en GitHub), reduciendo el riesgo de descoordinación.

**Riesgos operativos identificados:**
- La dedicación del equipo es parcial (proyecto académico compatibilizado con otras materias), por lo que la disponibilidad horaria real puede ser menor a la ideal.
- Al ser un equipo de 3 personas con roles diferenciados, el mayor riesgo operativo no es la falta de habilidades técnicas sino la coordinación de entregas cruzadas (por ejemplo, que el frontend quede a la espera de un endpoint del backend); esto se mitiga con el cronograma por semana definido en `docs/plan-de-trabajo.md`, que secuencia las tareas para minimizar bloqueos.

### 1.2 Viabilidad temporal

El cronograma propuesto en `docs/plan-de-trabajo.md` distribuye el desarrollo en 8 semanas, desde el cierre del modelo de datos hasta el despliegue final y la documentación. Este plazo se ajusta al alcance acotado en `docs/alcance.md`: todas las funcionalidades del MVP son cálculos o heurísticas simples sobre datos cargados por el usuario, sin integraciones externas, lo cual es consistente con la complejidad de desarrollo evaluada como "Baja-Media".

**Puntos de control temporal:**
- Si al finalizar la semana 4 el CRUD de gastos no está operativo, el cronograma completo debe revisarse, ya que todos los indicadores (costo por km, alertas, heurística) dependen de esos datos.
- La decisión de infraestructura (Render/Railway) tiene una fecha límite explícita (antes de la semana 6) para no comprometer la etapa de despliegue.

**Conclusión de viabilidad operativa y temporal:** Dado el alcance acotado del MVP, la ausencia de dependencias externas críticas y la distribución de roles ya definida, el proyecto es ejecutable dentro de un cronograma de 8 semanas con el equipo actual.

---

## 2. Análisis de competencia y diferenciación

*¿Qué existe hoy que resuelva parte de este problema, y en qué se diferencia esta propuesta?*

### 2.1 Matriz competitiva

| Alternativa | Tipo | Cobertura de categorías de gasto | Costo por km | Comparación con histórico propio | Heurística reparar/reemplazar | Dependencia de integraciones |
|---|---|---|---|---|---|---|
| **Apps de bitácora** (ej. Drivvo, Fuelio) | Competidor directo | Parcial (orientadas principalmente a combustible) | Algunas la calculan solo para combustible | No | No | Baja (carga manual) |
| **Apps oficiales de service/marca** | Competidor directo | Solo mantenimiento programado | No | No | No | Alta (atadas a la marca) |
| **Planillas de cálculo** (Excel/Sheets) | Competidor indirecto | Total, pero 100% manual | Solo si el usuario arma la fórmula | Solo si el usuario lo calcula a mano | No | Ninguna |
| **Apps bancarias** | Competidor indirecto | Parcial (gasto general, no específico del vehículo) | No | No | No | Alta (depende de la tarjeta/cuenta) |
| **Memoria / Papel** | Statu quo | Ninguna estructurada | No | No | No | Ninguna |

### 2.2 Diferenciadores

Conforme a la propuesta de valor definida en `docs/alcance.md`, el diferencial radica en:

- **Cruce de categorías:** Ninguna de las alternativas directas releva simultáneamente combustible, mantenimiento, reparaciones y otros gastos para calcular un costo real por km integral.
- **Comparación contra el propio histórico:** Ni las apps de bitácora ni las apps bancarias detectan automáticamente cuándo un gasto se desvía del patrón propio del usuario.
- **Heurística de decisión:** Ninguna alternativa relevada ofrece una orientación sobre "reparar o reemplazar" a partir del historial de gastos cargado.

### 2.3 Simulación de escenarios y conclusiones

- **Resistencia ante competidores gratuitos:** Dado que la mayoría de competidores directos ya tienen versiones gratuitas, la diferenciación no se apoya en el precio, sino en el análisis cruzado de categorías y la heurística de decisión.
- **Funcionalidad mínima indispensable:** Un registro de gastos simple y rápido de cargar; sin esto, la propuesta no iguala a una planilla personal.
- **Sostenibilidad del diferencial:** El registro por categorías es copiable a corto plazo; sin embargo, la heurística de decisión y la comparación histórica requieren lógica de negocio compleja que representa una ventaja más sólida a mediano plazo.
