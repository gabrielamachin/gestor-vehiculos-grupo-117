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

## Decisión de despliegue

Actualmente el equipo se encuentra **evaluando dos opciones** para el despliegue del proyecto: **Render** y **Railway**. Ambas plataformas ofrecen free tiers que se ajustan a las necesidades del proyecto, pero presentan características y limitaciones diferentes que se deben analizar con más detalle antes de tomar una decisión final.

### Opción A: Render (Todo en una plataforma)

**Descripción**: Render permite alojar el frontend (Static Site), el backend (Web Service) y la base de datos (PostgreSQL) en una misma plataforma.

**Ventajas**:
- Centralización de todos los servicios en un solo proveedor
- Comunicación interna entre backend y base de datos (menor latencia)
- Un único dashboard para monitorear todos los componentes
- Auto-deploy desde GitHub para todos los servicios
- Documentación clara y actualizada

**Limitaciones**:
- El free tier del Web Service ya no está disponible después de 15 minutos de inactividad
- 512 MB de RAM y 1 vCPU para el backend (de todas maneras se considera suficiente para el proyecto)
- 1 GB de almacenamiento para PostgreSQL en free tier

### Opción B: Railway (Backend + BD) + Vercel/Netlify (Frontend)

**Descripción**: Railway aloja el backend y la base de datos, mientras que Vercel o Netlify alojan el frontend (Static Site con CDN global).

**Ventajas**:
- Railway ofrece un free tier generoso para backend y PostgreSQL
- Vercel/Netlify tienen CDN global para el frontend (mejor rendimiento)
- Cada plataforma está especializada en su área (Vercel para frontend, Railway para backend)
- Mayor flexibilidad para escalar cada componente por separado

**Limitaciones**:
- Dos plataformas diferentes (más complejidad en configuración y monitoreo)
- Mayor latencia entre frontend y backend (tráfico entre nubes diferentes)
- CORS debe configurarse con dominios de ambas plataformas
- Más variables de entorno para gestionar