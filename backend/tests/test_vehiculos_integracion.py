"""Pruebas de integración de Vehículos contra una PostgreSQL real.

Se ejecutan solo si está definida TEST_DATABASE_URL. ATENCIÓN: cada corrida ejecuta
database/schema.sql, que BORRA y recrea las tablas. Usar una base exclusiva para pruebas
(p. ej. gestor_vehiculos_test), nunca la de desarrollo.

    PowerShell:  $env:TEST_DATABASE_URL="postgresql://postgres:CLAVE@localhost:5432/gestor_vehiculos_test"
                 pytest tests/test_vehiculos_integracion.py
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

pytestmark = pytest.mark.skipif(
    not TEST_DATABASE_URL, reason="Definir TEST_DATABASE_URL para correr las pruebas de integración"
)

SCHEMA = Path(__file__).resolve().parents[2] / "database" / "schema.sql"
PASSWORD = "clave-segura-123"


@pytest.fixture(scope="module")
def client():
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


def _nuevo_usuario(client) -> dict:
    """Registra un usuario con email único y devuelve sus headers de autenticación."""
    email = f"{uuid.uuid4().hex[:10]}@prueba.com"
    assert client.post("/usuarios/registro", json={"nombre": "Prueba", "email": email, "password": PASSWORD}).status_code == 201
    token = client.post("/usuarios/login", json={"email": email, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _crear_vehiculo(client, headers, alias="Auto", km=12000.5):
    return client.post("/vehiculos", json={"alias": alias, "kilometraje_inicial": km}, headers=headers)


def test_crear_y_listar(client):
    a = _nuevo_usuario(client)
    r = _crear_vehiculo(client, a)
    assert r.status_code == 201
    assert r.json()["kilometraje_inicial"] == 12000.5  # número JSON, no string

    lista = client.get("/vehiculos", headers=a).json()
    assert [v["alias"] for v in lista] == ["Auto"]


def test_otro_usuario_no_puede_ver_ni_modificar_ni_borrar(client):
    a, b = _nuevo_usuario(client), _nuevo_usuario(client)
    vehiculo_id = _crear_vehiculo(client, a).json()["id"]

    assert client.get(f"/vehiculos/{vehiculo_id}", headers=b).status_code == 404
    assert client.put(f"/vehiculos/{vehiculo_id}", json={"alias": "Robado"}, headers=b).status_code == 404
    assert client.delete(f"/vehiculos/{vehiculo_id}", headers=b).status_code == 404
    assert client.get("/vehiculos", headers=b).json() == []

    # El dueño sigue viendo su vehículo intacto
    r = client.get(f"/vehiculos/{vehiculo_id}", headers=a)
    assert r.status_code == 200
    assert r.json()["alias"] == "Auto"


def test_alias_repetido_solo_conflicto_dentro_del_mismo_usuario(client):
    a, b = _nuevo_usuario(client), _nuevo_usuario(client)
    assert _crear_vehiculo(client, a, "Auto").status_code == 201
    assert _crear_vehiculo(client, a, "Auto").status_code == 409
    assert _crear_vehiculo(client, b, "Auto").status_code == 201  # otro usuario, mismo alias: permitido


def test_actualizar_alias(client):
    a = _nuevo_usuario(client)
    vid = _crear_vehiculo(client, a, "Auto").json()["id"]
    _crear_vehiculo(client, a, "Moto")

    r = client.put(f"/vehiculos/{vid}", json={"alias": "Auto familiar"}, headers=a)
    assert r.status_code == 200
    assert r.json()["alias"] == "Auto familiar"

    # No se puede tomar el alias de otro vehículo propio
    assert client.put(f"/vehiculos/{vid}", json={"alias": "Moto"}, headers=a).status_code == 409
    # Reenviar el mismo alias no es un conflicto
    assert client.put(f"/vehiculos/{vid}", json={"alias": "Auto familiar"}, headers=a).status_code == 200


def test_eliminar(client):
    a = _nuevo_usuario(client)
    vid = _crear_vehiculo(client, a).json()["id"]
    assert client.delete(f"/vehiculos/{vid}", headers=a).status_code == 204
    assert client.get(f"/vehiculos/{vid}", headers=a).status_code == 404
