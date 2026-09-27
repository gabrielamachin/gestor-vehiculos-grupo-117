-- Gestor Inteligente de Vehículos
-- Script de creación de base de datos (DDL) — PostgreSQL

BEGIN;

DROP TABLE IF EXISTS gastos CASCADE;
DROP TABLE IF EXISTS vehiculos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TYPE IF EXISTS gasto_categoria;


CREATE TYPE gasto_categoria AS ENUM ('combustible', 'mantenimiento', 'reparacion', 'otro');

CREATE TABLE usuarios (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre         VARCHAR(150) NOT NULL,
    email          VARCHAR(255) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,

    CONSTRAINT chk_usuarios_nombre_no_vacio CHECK (btrim(nombre) <> ''),
    CONSTRAINT chk_usuarios_email_formato    CHECK (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$')
);

CREATE TABLE vehiculos (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id                  UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    alias                       VARCHAR(100) NOT NULL,
    kilometraje_inicial         NUMERIC(10,2) NOT NULL,
    kilometraje_actual          NUMERIC(10,2) NOT NULL,
    intervalo_mantenimiento_km  NUMERIC(10,2),

    CONSTRAINT chk_vehiculos_alias_no_vacio       CHECK (btrim(alias) <> ''),
    CONSTRAINT chk_vehiculos_km_inicial_no_neg    CHECK (kilometraje_inicial >= 0),
    CONSTRAINT chk_vehiculos_km_actual_no_neg     CHECK (kilometraje_actual >= 0),
    CONSTRAINT chk_vehiculos_km_actual_ge_inicial CHECK (kilometraje_actual >= kilometraje_inicial),
    CONSTRAINT chk_vehiculos_intervalo_positivo   CHECK (intervalo_mantenimiento_km IS NULL OR intervalo_mantenimiento_km > 0)
);

CREATE TABLE gastos (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehiculo_id   UUID NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
    categoria     gasto_categoria NOT NULL,
    monto         NUMERIC(12,2) NOT NULL,
    fecha         DATE NOT NULL,
    descripcion   TEXT,

    CONSTRAINT chk_gastos_monto_positivo  CHECK (monto > 0),
    CONSTRAINT chk_gastos_fecha_no_futura CHECK (fecha <= CURRENT_DATE)
);

-- Índices para las consultas agregadas del MVP
CREATE INDEX idx_gastos_vehiculo_id ON gastos(vehiculo_id);
CREATE INDEX idx_gastos_fecha       ON gastos(fecha);
CREATE INDEX idx_gastos_categoria   ON gastos(categoria);

-- Índice compuesto para "gastos por vehículo y categoría en un rango de fechas"
CREATE INDEX idx_gastos_vehiculo_categoria_fecha
    ON gastos(vehiculo_id, categoria, fecha);

COMMIT;