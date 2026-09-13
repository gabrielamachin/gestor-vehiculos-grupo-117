# Esquema de la base de datos

## 1. Tecnología

La aplicación utiliza PostgreSQL. El esquema principal se encuentra en
`../db/schema.sql`.

## 2. Entidades principales

### Usuarios

- `id`: clave primaria.
- `nombre`: nombre del usuario.
- `email`: correo único.
- `password`: contraseña almacenada de forma segura.
- `created_at`: fecha de creación.

### Vehículos

- `id`: clave primaria.
- `usuario_id`: referencia a `usuarios.id`.
- `marca`
- `modelo`
- `patente`
- `anio`

### Categorías

- `id`: clave primaria.
- `nombre`: nombre único de la categoría.

### Gastos

- `id`: clave primaria.
- `vehiculo_id`: referencia a `vehiculos.id`.
- `categoria_id`: referencia a `categorias.id`.
- `monto`
- `descripcion`
- `fecha`

## 3. Relaciones

- Un usuario puede tener varios vehículos.
- Un vehículo puede tener varios gastos.
- Una categoría puede estar asociada a varios gastos.
- Cada gasto pertenece a un vehículo y a una categoría.

## 4. Reglas de integridad

- Todas las entidades poseen una clave primaria.
- Las relaciones se implementan mediante claves foráneas.
- El correo del usuario y la patente del vehículo deben ser únicos.
- No se permiten gastos con montos negativos.
- Al eliminar un usuario, se eliminan sus vehículos y gastos asociados.
- Al eliminar una categoría utilizada por gastos, la operación debe impedirse.

## 5. Diagrama entidad-relación
<!-- To do: adjuntar -->