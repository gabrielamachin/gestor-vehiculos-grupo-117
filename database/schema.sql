-- Gestor Inteligente de Vehículos
-- Script de creación de base de datos (DDL) — PostgreSQL 


BEGIN;

DROP TABLE IF EXISTS gastos CASCADE;
DROP TABLE IF EXISTS vehiculos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TYPE IF EXISTS gasto_categoria;

-- gen_random_uuid() es función built-in desde PostgreSQL 13, no requiere extensión.

CREATE TYPE gasto_categoria AS ENUM ('combustible', 'mantenimiento', 'reparacion', 'otro');

CREATE TABLE usuarios (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre         VARCHAR(150) NOT NULL,
    email          VARCHAR(255) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL
);

CREATE TABLE vehiculos (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id                  UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    alias                       VARCHAR(100) NOT NULL,
    kilometraje_inicial         NUMERIC(10,2) NOT NULL,
    kilometraje_actual          NUMERIC(10,2) NOT NULL,
    intervalo_mantenimiento_km  NUMERIC(10,2)
);

CREATE TABLE gastos (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehiculo_id   UUID NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
    categoria     gasto_categoria NOT NULL,
    monto         NUMERIC(12,2) NOT NULL,
    fecha         DATE NOT NULL,
    descripcion   TEXT
);

-- Índices para las consultas agregadas del MVP (docs/viabilidad.md, sección 4.3)
CREATE INDEX idx_gastos_vehiculo_id ON gastos(vehiculo_id);
CREATE INDEX idx_gastos_fecha       ON gastos(fecha);
CREATE INDEX idx_gastos_categoria   ON gastos(categoria);

COMMIT;