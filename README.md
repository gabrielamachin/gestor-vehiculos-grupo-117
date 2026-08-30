# Gestor Inteligente de Vehículos

> Sistema para gestionar gastos de combustible, mantenimiento, seguro y neumáticos, con análisis de costo real por km y alertas inteligentes.

---

## Descripción del proyecto

Aplicación full-stack que permite al dueño de un vehículo registrar todos los gastos asociados al auto y obtener indicadores clave para la toma de decisiones financieras.

### Funcionalidades principales

- **Costo real por km**: Suma de todos los gastos ÷ kilómetros recorridos
- **Alertas de gasto**: Detección de aumentos vs. promedio histórico propio
- **Mantenimiento predictivo**: Próxima revisión estimada por kilometraje
- **Gasto anual por categoría**: Combustible, seguros, mantenimiento, neumáticos

### Actores

- **Usuario propietario**: Registra vehículos y gastos, visualiza indicadores
- **Sistema**: Genera alertas y cálculos automáticos

---

## Stack tecnológico

### Frontend
- React 18.x — Librería UI
- TypeScript 5.x — Tipado estático
- Vite 5.x — Build tool
- Tailwind CSS 3.x — Estilos

### Backend
- Python 3.10+ — Lenguaje
- FastAPI 0.109+ — Framework web

### Base de datos
- PostgreSQL 15+ — Base de datos relacional
- psycopg2 2.x — Driver

### Infraestructura
- A definir entre Render y Railway.
- GitHub Actions — CI/CD
