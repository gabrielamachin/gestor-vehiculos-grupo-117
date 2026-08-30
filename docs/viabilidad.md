# Evaluación de viabilidad 

> Este documento evalúa la viabilidad de negocio, temporal y técnica del proyecto.

---

## Viabilidad técnica

### Madurez del stack

**Frontend**
- *React 18.x*: Es un framework líder que cuenta con una comunidad importante, cuenta con actualizaciones regulares y soporte a largo plazo.
- *TypeScript 5.x*: Estándar en la industria, tipado estático, detección temprana de errores.
- *Vite 5.x*: Build tool moderno y aceptado por la comunidad.
- *Estado*: Todas las tecnologías son maduras y están en producción en miles de proyectos.

**Backend**
- *FastAPI 0.109+*: Se trata de un framework consolidado y usado por grandes empresas, con buena documentación disponible.
- *Python 3.10+*: Lenguaje estable, actualizaciones regulares, ecosistema grande.
- *Estado*: Stack probado, documentado y con soporte activo.

**Base de Datos**
- *PostgreSQL 15+*: BD más madura del ecosistema Open Source, ACID, alto rendimiento.
- *Estado*: Recomendable para datos relacionales y cálculos matemáticos.

**Infraestructura**
- *Render*: Plataforma consolidada, free tier funcional, integración nativa con GitHub.
- *Railway*: PostgreSQL gestionado, backups automáticos, free tier disponible.
- *Estado*: Ambas plataformas son confiables para proyectos educativos y productivos. Actualmente el equipo se encuentra evaluando cuál de las dos opciones se adapta mejor a las necesidades del proyecto, considerando factores como latencia, facilidad de configuración y costos a futuro. La decisión final será definida antes del inicio del desarrollo.

### Complejidad de desarrollo

| Aspecto | Complejidad | Justificación |
|---------|-------------|---------------|
| CRUD de entidades | Baja | Operaciones estándar |
| Autenticación JWT | Media | Configuración inicial requiere atención, pero está bien documentado |
| Cálculo de costo por km | Baja | Matemática simple (suma de gastos ÷ km) |
| Motor de alertas | Media | Lógica de comparación con promedios históricos |
| Heurística reparar/reemplazar | Baja | Comparación simple de porcentajes |
| Gráficos en frontend | Media | Integración con Recharts/Chart.js |
| Despliegue en la nube | Media | Configuración de variables de entorno y CORS, independientemente de la plataforma elegida |
| **Total** | **Baja-Media** | **Proyecto realizable en el plazo estipulado** |

### Riesgos técnicos y mitigación

**Free tier sleeping (Render)**
- *Probabilidad*: Alta (aplica solo si se elige Render)
- *Impacto*: Medio
- *Mitigación*: Documentar el comportamiento en README. Considerar upgrade a Hobby Plan ($7/mes) si es crítico. Implementar ping automático para mantener activo.

**CORS en producción**
- *Probabilidad*: Media
- *Impacto*: Alto (bloquea toda la comunicación FE-BE)
- *Mitigación*: Configurar `CORS_ORIGINS` con variables de entorno desde el día 1. Probar en staging antes de producción.

**Migraciones automáticas en producción**
- *Probabilidad*: Media
- *Impacto*: Alto (puede romper la BD)
- *Mitigación*: Mantener backups automáticos en la herramienta seleccionada.

**Configuración de variables de entorno**
- *Probabilidad*: Media
- *Impacto*: Medio
- *Mitigación*: Mantener `.env.example` actualizado. Documentar todas las variables requeridas.

**Rendimiento con múltiples vehículos**
- *Probabilidad*: Baja
- *Impacto*: Medio
- *Mitigación*: Índices en PostgreSQL (user_id, vehicle_id, fechas). Consultas optimizadas con SQLAlchemy.

---

### Herramientas y entorno

**Desarrollo local**
- VS Code con extensiones para Python, TypeScript, ESLint, Prettier
- PostgreSQL local (Docker o instalación directa)
- Git para control de versiones
- Postman para testing de API

**Colaboración**
- Repositorio único en GitHub
- Trello para seguimiento de tareas
- Comunicación diaria por grupo de Whatsapp

**Infraestructura de desarrollo**
- Entornos de desarrollo locales (cada integrante)

---

## Análisis de escalabilidad

### Escalabilidad del stack

| Capa | Escalabilidad | Estrategia |
|------|---------------|------------|
| **Frontend** | Alta | CDN maneja tráfico global. Assets estáticos en edge. |
| **Backend** | Media-Alta | FastAPI con async permite manejar múltiples conexiones. Se puede escalar horizontalmente con múltiples instancias en la plataforma elegida. |
| **Base de Datos** | Media | PostgreSQL con índices optimizados. Se puede escalar verticalmente o con réplicas de lectura. |

### Límites del modelo actual

**Free Tier (dependiendo de la plataforma elegida)**
- Render: 512 MB RAM, 1 vCPU, sleep después de inactividad
- Railway: 500 MB de almacenamiento en BD

**Proyección de crecimiento**
- Usuarios: Ideal para ~1,000 usuarios activos en free tier
- Vehículos: Hasta 5,000 vehículos con consultas optimizadas
- Gastos: Hasta 50,000 registros sin degradación de rendimiento

**Estrategia de escalado futuro**
- Migrar a plan de pago en la plataforma elegida para eliminar sleep y aumentar recursos
- Evaluar la incorporación de caché con Redis si el proyecto crece significativamente

---

## Checklist de viabilidad

- [x] Stack tecnológico maduro y probado
- [x] Equipo con habilidades adecuadas
- [x] Presupuesto $0/mes (free tier suficiente)
- [x] Cronograma alineado con entregas de la materia
- [x] Riesgos identificados
- [x] Entorno de desarrollo configurable
- [x] Documentación y recursos disponibles
- [x] Posibilidad de escalar si es necesario
