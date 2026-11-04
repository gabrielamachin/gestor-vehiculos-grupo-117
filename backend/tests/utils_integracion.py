"""Utilidades compartidas por las pruebas de integración (PostgreSQL real).

Se ejecutan solo si está definida TEST_DATABASE_URL. ATENCIÓN: cada módulo de pruebas ejecuta
database/schema.sql, que BORRA y recrea las tablas. Usar una base exclusiva para pruebas
(p. ej. gestor_vehiculos_test), nunca la de desarrollo.

    PowerShell:  $env:TEST_DATABASE_URL="postgresql://postgres:CLAVE@localhost:5432/gestor_vehiculos_test"
                 pytest
"""
import os
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

# Uso: pytestmark = SALTAR_SIN_BASE
SALTAR_SIN_BASE = pytest.mark.skipif(
    not TEST_DATABASE_URL, reason="Definir TEST_DATABASE_URL para correr las pruebas de integración"
)

SCHEMA = Path(__file__).resolve().parents[2] / "database" / "schema.sql"
PASSWORD = "clave-segura-123"


def cliente_de_prueba():
    """Generador para usar en un fixture: `yield from cliente_de_prueba()`."""
    assert "test" in TEST_DATABASE_URL.lower(), "TEST_DATABASE_URL debe apuntar a una base de pruebas (nombre con 'test')"

    url = TEST_DATABASE_URL
    for prefijo in ("postgres://", "postgresql://"):
        if url.startswith(prefijo):
            url = "postgresql+psycopg2://" + url[len(prefijo):]
            break
    engine = create_engine(url)

    # Recrea el esquema completo (el script trae su propio BEGIN/COMMIT).
    conexion = engine.raw_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute(SCHEMA.read_text(encoding="utf-8"))
        conexion.commit()
        cursor.close()
    finally:
        conexion.close()

    Sesion = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def _get_db_de_prueba():
        db = Sesion()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db_de_prueba
    yield TestClient(app)
    app.dependency_overrides.pop(get_db, None)
    engine.dispose()


def nuevo_usuario(client) -> dict:
    """Registra un usuario con email único y devuelve sus headers de autenticación."""
    email = f"{uuid.uuid4().hex[:10]}@prueba.com"
    assert client.post("/usuarios/registro", json={"nombre": "Prueba", "email": email, "password": PASSWORD}).status_code == 201
    token = client.post("/usuarios/login", json={"email": email, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def nuevo_vehiculo(client, headers, alias="Auto", km_inicial=1000) -> str:
    """Crea un vehículo y devuelve su id."""
    r = client.post("/vehiculos", json={"alias": alias, "kilometraje_inicial": km_inicial}, headers=headers)
    assert r.status_code == 201
    return r.json()["id"]
