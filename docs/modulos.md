# Definición y Listado de Módulos

> Este documento detalla los módulos principales que componen la aplicación, divididos por capa arquitectónica.

## 1. Capa Frontend (Progressive Web App - React)

* **Módulo de Autenticación y Perfil:** Gestión del login, registro y recuperación de contraseña del usuario.
* **Módulo de Gestión de Vehículos (CRUD):** Interfaz para que el usuario pueda dar de alta, modificar o eliminar sus vehículos.
* **Módulo de Registro de Gastos:** Formularios de carga rápida orientados a dispositivos móviles para ingresar tickets de combustible, mantenimiento, reparaciones y otros.
* **Módulo de Dashboard y Métricas:** Visualización de gráficos (Recharts/Chart.js) y métricas clave como el costo real por kilómetro y promedios históricos.

## 2. Capa Backend (API REST - FastAPI)

* **Módulo de Seguridad (Auth):** Emisión y validación de tokens JWT para proteger los endpoints.
* **Módulo de Vehículos:** Lógica de negocio para administrar la flota personal del usuario.
* **Módulo de Transacciones:** Endpoints para registrar y categorizar los gastos asociados a un vehículo específico.
* **Módulo Analítico y de Alertas:** Motor encargado de calcular el costo por kilómetro, comparar consumos contra el historial y ejecutar la heurística de reparar o reemplazar.

## 3. Capa de Persistencia (PostgreSQL)

* **Módulo de Usuarios:** gestión de usuarios, credenciales y perfiles.
* **Módulo de Vehículos:** almacenamiento de vehículos asociados a cada usuario.
* **Módulo de Gastos:** registro de gastos, categorías, fechas y montos.
* **Módulo de Reportes:** consultas agregadas para métricas y gráficos.

## 4. Interfaces entre módulos

| Módulo | Consume | Proporciona |
|---|---|---|
| Dashboard | Vehículos, gastos y reportes | Métricas y gráficos |
| Gastos | Vehículos y categorías | Registro de gastos |
| Alertas | Historial de gastos y kilometraje | Recomendaciones |
| Autenticación | Usuarios | Sesión y token JWT |

## 5. Permisos

- Cada usuario solo puede acceder a sus propios vehículos y gastos.
- Los endpoints protegidos requieren un token JWT válido.
- Las operaciones de modificación deben verificar la pertenencia del recurso.

## 6. Estado de implementación

- [ ] Autenticación
- [ ] Gestión de vehículos
- [ ] Registro de gastos
- [ ] Dashboard
- [ ] Reportes
- [ ] Alertas