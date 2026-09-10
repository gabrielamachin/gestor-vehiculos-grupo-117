# Definición del stack tecnológico

> En este documento se detalla la selección y justificación de las tecnologías utilizadas en el proyecto.

---

## Stack completo

### Frontend

**React con TypeScript**
- *Versión*: React 18.x + TypeScript 5.x
- *Propósito*: Framework UI con tipado estático
- *Justificación*: 
  - React permite construir interfaces de usuario interactivas y modulares.
  - TypeScript agrega tipado estático que reduce errores en tiempo de ejecución.
  - Gran ecosistema de librerías y componentes.
  - Experiencia del equipo en ambas tecnologías.
  - Es recomendable para manejar el estado de la aplicación y renderizar dashboards con datos dinámicos.

### Backend

**Python con FastAPI**
- *Versión*: Python 3.10+ / FastAPI 0.109+
- *Propósito*: Framework web para construir la API REST
- *Justificación*:
  - FastAPI es async nativo, ideal para operaciones de I/O como consultas a BD
  - Documentación automática con Swagger/OpenAPI (para facilitar testing y frontend)
  - Tipado fuerte con Pydantic (validación automática de datos)
  - Alto rendimiento y baja latencia
  - Python tiene un ecosistema maduro para procesamiento de datos (cálculo de costo por km, promedios, alertas)
  - Curva de aprendizaje baja, buena documentación disponible

### Base de datos

**PostgreSQL**
- *Versión*: 15+
- *Propósito*: Base de datos relacional
- *Justificación*:
  - Los datos son inherentemente relacionales (usuario → vehículos → gastos)
  - Soporte ACID para transacciones (importante al registrar gastos y actualizar promedios)
  - Es una buena alternativa para consultas agregadas (SUM, AVG) necesarias para el cálculo de costo por km
  - Soporte nativo para UUID (identificadores únicos)
  - Amplio soporte ORM con SQLAlchemy
  - Escalable y confiable

---

## Despliegue e infraestructura

La infraestructura del proyecto se centraliza íntegramente en **Render**, simplificando la operación y el monitoreo:

- **Frontend:** Render Static Site con auto-deploy desde la rama principal del repositorio de GitHub.
- **Backend:** Render Web Service ejecutando FastAPI mediante entorno virtual de Python y servidor ASGI Uvicorn.
- **Base de Datos:** PostgreSQL administrado provisto por Render (15+), con conexión interna privada entre el Web Service y la base de datos para minimizar la latencia de red.
- **Estrategia ante el Free Tier (Spin Down):** Al operar sobre instancias de nivel gratuito que entran en reposo tras 15 minutos de inactividad, se implementará un endpoint liviano de `/health` consumido periódicamente para asegurar disponibilidad inmediata durante las demostraciones.