-- Gestor Inteligente de Vehículos
-- Script de creación de base de datos (DDL) — PostgreSQL

BEGIN;

DROP TABLE IF EXISTS gastos CASCADE;
DROP TABLE IF EXISTS planes_mantenimiento CASCADE;
DROP TABLE IF EXISTS lecturas_kilometraje CASCADE;
DROP TABLE IF EXISTS vehiculos CASCADE;
DROP TABLE IF EXISTS categorias_gasto CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TYPE  IF EXISTS gasto_categoria;


-- ============================================================
-- usuarios
-- ============================================================
CREATE TABLE usuarios (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre         VARCHAR(150) NOT NULL,
    email          VARCHAR(255) NOT NULL UNIQUE,   -- el UNIQUE crea el índice usado en el login
    password_hash  VARCHAR(255) NOT NULL,

    CONSTRAINT chk_usuarios_nombre_no_vacio CHECK (btrim(nombre) <> ''),
    CONSTRAINT chk_usuarios_email_formato   CHECK (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$')
);


-- ============================================================
-- categorias_gasto (catálogo)
-- Agregar una categoría nueva = un INSERT sin migración.
-- ============================================================
CREATE TABLE categorias_gasto (
    id          SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo      VARCHAR(30) NOT NULL UNIQUE,   -- identificador estable que usa el código (ej. 'combustible')
    nombre      VARCHAR(60) NOT NULL UNIQUE,   -- texto que ve el usuario
    tipo_costo  VARCHAR(10) NOT NULL,          -- fijo | variable
    activa      BOOLEAN NOT NULL DEFAULT TRUE, -- se desactiva en lugar de borrar, para conservar el historial

    CONSTRAINT chk_categorias_codigo_formato  CHECK (codigo ~ '^[a-z][a-z0-9_]*$'),
    CONSTRAINT chk_categorias_nombre_no_vacio CHECK (btrim(nombre) <> ''),
    CONSTRAINT chk_categorias_tipo_costo      CHECK (tipo_costo IN ('fijo', 'variable'))
);

INSERT INTO categorias_gasto (codigo, nombre, tipo_costo) VALUES
    ('combustible',   'Combustible',   'variable'),
    ('mantenimiento', 'Mantenimiento', 'variable'),
    ('reparacion',    'Reparación',    'variable'),
    ('seguro',        'Seguro',        'fijo'),
    ('neumaticos',    'Neumáticos',    'variable'),
    ('otro',          'Otros',         'variable');


-- ============================================================
-- vehiculos
-- El kilometraje vigente se deriva de la
-- última fila de lecturas_kilometraje
-- ============================================================
CREATE TABLE vehiculos (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id           UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    alias                VARCHAR(100) NOT NULL,
    kilometraje_inicial  NUMERIC(10,2) NOT NULL,

    -- además de evitar alias repetidos, este índice sirve para "vehículos de un usuario"
    CONSTRAINT uq_vehiculos_usuario_alias        UNIQUE (usuario_id, alias),
    CONSTRAINT chk_vehiculos_alias_no_vacio      CHECK (btrim(alias) <> ''),
    CONSTRAINT chk_vehiculos_km_inicial_no_neg   CHECK (kilometraje_inicial >= 0)
);


-- ============================================================
-- lecturas_kilometraje
-- Historial del odómetro. Una lectura por vehículo y día.
-- ============================================================
CREATE TABLE lecturas_kilometraje (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehiculo_id  UUID NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
    fecha        DATE NOT NULL,
    kilometraje  NUMERIC(10,2) NOT NULL,

    -- el índice del UNIQUE también resuelve "última lectura del vehículo" (fecha DESC LIMIT 1)
    CONSTRAINT uq_lecturas_vehiculo_fecha  UNIQUE (vehiculo_id, fecha),
    CONSTRAINT chk_lecturas_km_no_neg      CHECK (kilometraje >= 0),
    CONSTRAINT chk_lecturas_fecha_no_futura CHECK (fecha <= CURRENT_DATE)
);


-- ============================================================
-- planes_mantenimiento
-- Un vehículo puede tener varios planes (aceite, filtros, distribución, etc.).
-- ============================================================
CREATE TABLE planes_mantenimiento (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehiculo_id   UUID NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
    nombre        VARCHAR(100) NOT NULL,
    intervalo_km  NUMERIC(10,2) NOT NULL,

    CONSTRAINT uq_planes_vehiculo_nombre   UNIQUE (vehiculo_id, nombre),
    -- necesario como destino de la FK compuesta de gastos (garantiza que gasto y plan sean del mismo vehículo)
    CONSTRAINT uq_planes_id_vehiculo       UNIQUE (id, vehiculo_id),
    CONSTRAINT chk_planes_nombre_no_vacio  CHECK (btrim(nombre) <> ''),
    CONSTRAINT chk_planes_intervalo_pos    CHECK (intervalo_km > 0)
);


-- ============================================================
-- gastos
-- ============================================================
CREATE TABLE gastos (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehiculo_id            UUID NOT NULL,
    categoria_id           SMALLINT NOT NULL REFERENCES categorias_gasto(id) ON DELETE RESTRICT,
    plan_mantenimiento_id  UUID,                      -- opcional: plan que este gasto dejó cumplido
    monto                  NUMERIC(12,2) NOT NULL,
    fecha                  DATE NOT NULL,
    kilometraje            NUMERIC(10,2),             -- opcional: obligatorio solo si se asocia a un plan
    descripcion            TEXT,

    CONSTRAINT fk_gastos_vehiculo
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id) ON DELETE CASCADE,

    -- FK compuesta: el plan debe pertenecer al mismo vehículo que el gasto.
    -- Si se borra el plan, el gasto se conserva y solo pierde la asociación.
    CONSTRAINT fk_gastos_plan
        FOREIGN KEY (plan_mantenimiento_id, vehiculo_id)
        REFERENCES planes_mantenimiento (id, vehiculo_id)
        ON DELETE SET NULL (plan_mantenimiento_id),

    CONSTRAINT chk_gastos_monto_positivo   CHECK (monto > 0),
    CONSTRAINT chk_gastos_fecha_no_futura  CHECK (fecha <= CURRENT_DATE),
    CONSTRAINT chk_gastos_km_no_neg        CHECK (kilometraje IS NULL OR kilometraje >= 0),
    CONSTRAINT chk_gastos_plan_requiere_km CHECK (plan_mantenimiento_id IS NULL OR kilometraje IS NOT NULL)
);


-- ============================================================
-- Índices (justificación de cada uno en docs/esquema-db.md, sección 7)
-- PK y UNIQUE ya crean su propio índice, solo se declaran los adicionales.
-- ============================================================

-- Listado cronológico de gastos de un vehículo y totales por rango de fechas
CREATE INDEX idx_gastos_vehiculo_fecha
    ON gastos (vehiculo_id, fecha DESC);

-- Agregaciones por categoría y comparación de combustible contra el historial propio
CREATE INDEX idx_gastos_vehiculo_categoria_fecha
    ON gastos (vehiculo_id, categoria_id, fecha);

-- "Último mantenimiento realizado de cada plan" (para estimar el próximo).
-- Parcial: solo indexa los gastos asociados a un plan.
CREATE INDEX idx_gastos_plan_km
    ON gastos (plan_mantenimiento_id, kilometraje DESC)
    WHERE plan_mantenimiento_id IS NOT NULL;

COMMIT;
