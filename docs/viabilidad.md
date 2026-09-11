# Evaluación de viabilidad

> Este documento evalúa la viabilidad de negocio, técnica, operativa, temporal y el análisis de competencia del proyecto.

---

## 1. Viabilidad de negocio

*¿Tiene sentido llevar adelante este producto desde el punto de vista de negocio/producto?*

### 1.1 Valor vs. esfuerzo
El producto le pide al usuario que cargue manualmente sus datos de combustible, mantenimiento, reparaciones y otros gastos. Este esfuerzo no es nuevo porque el usuario ya dedica esfuerzo a gestionar esta información de forma dispersa. El producto concentra ese esfuerzo en un único lugar y lo transforma en información de valor: costo real por kilómetro, gasto acumulado por categoría, comparación con su propio histórico y orientación sobre mantenimiento o reemplazo. El esfuerzo de carga se justifica por el análisis obtenido a cambio.

### 1.2 Enfoque sin integraciones
El alcance excluye integraciones automáticas (bancos, talleres, OBD). El valor central de la propuesta está en relacionar y analizar los datos para generar indicadores, no en el mecanismo de carga. Este enfoque es estratégicamente defendible para sostener el valor central dentro del plazo del MVP.

---

## 2. Análisis de competencia y diferenciación

*¿Qué existe hoy que resuelva parte de este problema, y en qué se diferencia esta propuesta?*

### 2.1 Matriz competitiva

| Alternativa | Tipo | Cobertura de gastos | Costo por km | Comparación histórica | Heurística decisión | Integraciones |
|---|---|---|---|---|---|---|
| **Apps de bitácora** (ej. Drivvo) | Competidor directo | Parcial (combustible) | Solo combustible | No | No | Baja |
| **Apps oficiales de marca** | Competidor directo | Solo mantenimiento | No | No | No | Alta |
| **Planillas de cálculo** | Competidor indirecto | Total (100% manual) | Manual | Manual | No | Ninguna |
| **Apps bancarias** | Competidor indirecto | Parcial (general) | No | No | No | Alta |

### 2.2 Diferenciadores
- **Cruce de categorías:** Ninguna alternativa directa releva simultáneamente todas las categorías para calcular un costo real por km integral.
- **Comparación contra el propio histórico:** Detección automática de desvíos del patrón propio del usuario.
- **Heurística de decisión:** Orientación sobre "reparar o reemplazar" a partir del historial, algo inexistente en los competidores relevados.

---

## 3. Viabilidad operativa, temporal y de dominio

*¿El equipo puede ejecutar este proyecto, con estos recursos, dentro de los plazos disponibles?*

### 3.1 Viabilidad operativa
El equipo cuenta con perfiles definidos: Producto y Estrategia, Arquitectura/Tecnología, y Gestión/Operatividad.
- **Condiciones favorables:** No hay dependencias externas críticas (talleres, aseguradoras). Entorno de desarrollo local, gratuito y estandarizado (GitHub, Trello, WhatsApp).
- **Riesgos operativos:** La coordinación de entregas cruzadas (ej. frontend esperando al backend) se mitiga con un cronograma semanal secuenciado que minimiza bloqueos.

### 3.2 Viabilidad temporal
El cronograma de 8 semanas se ajusta al alcance acotado del MVP (cálculos y heurísticas simples sin integraciones externas).
- **Punto de control:** Si en la semana 4 el CRUD de gastos no está operativo, el cronograma debe revisarse de inmediato, ya que todos los indicadores dependen de esta base.

### 3.3 Viabilidad de dominio y conocimiento
- **Comprensión del problema:** Las integrantes del equipo son usuarias de vehículos particulares en Argentina, lo que aporta una comprensión directa de las fricciones reales del mantenimiento cotidiano: la posible pérdida de los comprobantes de pago, la imprevisibilidad en el cálculo de los costos y la falta de seguimiento del costo por kilómetro.
- **Validación del modelo matemático:** Las fórmulas requeridas (cálculo de costo por kilómetro, medias móviles de consumo y comparación de gastos acumulados) se basan en operaciones aritméticas y agregaciones estadísticas estándar, dominadas plenamente por el equipo.
- **Reglas del dominio automotriz:** Se acotan deliberadamente los mantenimientos a intervalos universales estándar (ej. múltiplos de 10.000 km o 1 año) prescindiendo de especificaciones técnicas complejas por fabricante en esta versión, lo que garantiza que la lógica de negocio sea robusta y viable de implementar sin requerir un perito mecánico.

---

## 4. Viabilidad técnica y escalabilidad

### 4.1 Madurez del stack
- **Frontend (React 18.x, TypeScript, Vite):** Ecosistema maduro, tipado estático y excelente rendimiento.
- **Backend (Python 3.10+, FastAPI):** Framework consolidado, async nativo y validación robusta.
- **Base de Datos (PostgreSQL 15+):** Ideal para modelo relacional (usuario → vehículos → gastos) y consultas agregadas.
- **Infraestructura (Render):** Plataforma unificada y confiable para desplegar PWA, Web Service y Base de Datos de manera centralizada.

### 4.2 Complejidad de desarrollo
La complejidad general del proyecto se evalúa como **Baja-Media**. Las operaciones son estándar (CRUD, Autenticación JWT) y la lógica matemática/estadística (costo por km, medias móviles) se apoya en cálculos directos asimilables en los tiempos propuestos.

### 4.3 Riesgos técnicos y mitigaciones
| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **Free tier sleeping (Render)** | Alta | Medio | Documentar el "cold start" en el README; implementar endpoint `/health` para mantener activo en demostraciones. |
| **CORS en producción** | Media | Alto | Configurar `CORS_ORIGINS` con la URL estática del frontend en Render desde el inicio del desarrollo. |
| **Latencia en consultas analíticas y agregaciones** | Baja | Medio | Crear índices en PostgreSQL (`vehicle_id`, `fecha`, `categoria`) para optimizar agregaciones. |