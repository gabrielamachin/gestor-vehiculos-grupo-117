"""Pruebas de integración de la sesión por cookie contra una PostgreSQL real (ver tests/utils_integracion.py)."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.security import NOMBRE_COOKIE_SESION
from app.main import app
from tests.utils_integracion import PASSWORD, SALTAR_SIN_BASE, cliente_de_prueba

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _registrar(client) -> str:
    email = f"{uuid.uuid4().hex[:10]}@prueba.com"
    r = client.post("/usuarios/registro", json={"nombre": "Prueba", "email": email, "password": PASSWORD})
    assert r.status_code == 201
    return email


def _navegador() -> TestClient:
    """Cliente nuevo = navegador nuevo, con su propio almacén de cookies."""
    return TestClient(app)


def test_la_sesion_guarda_una_cookie_httponly_y_no_expone_el_token(client):
    email = _registrar(client)
    navegador = _navegador()

    r = navegador.post("/usuarios/sesion", json={"email": email, "password": PASSWORD})
    assert r.status_code == 200
    assert r.json()["email"] == email
    assert "access_token" not in r.json()  # el JavaScript nunca recibe el token

    cabecera = r.headers["set-cookie"]
    assert f"{NOMBRE_COOKIE_SESION}=" in cabecera
    assert "HttpOnly" in cabecera
    assert "samesite=lax" in cabecera.lower()
    assert "Path=/" in cabecera
    assert "Max-Age=" in cabecera

    # El navegador reenvía la cookie solo: no hace falta ningún header
    assert navegador.get("/usuarios/me").json()["email"] == email


def test_credenciales_invalidas_no_crean_cookie(client):
    email = _registrar(client)
    navegador = _navegador()

    r = navegador.post("/usuarios/sesion", json={"email": email, "password": "otra-clave-123"})
    assert r.status_code == 401
    assert "set-cookie" not in r.headers
    assert navegador.get("/usuarios/me").status_code == 401


def test_cerrar_sesion_invalida_la_cookie(client):
    email = _registrar(client)
    navegador = _navegador()
    navegador.post("/usuarios/sesion", json={"email": email, "password": PASSWORD})
    assert navegador.get("/usuarios/me").status_code == 200

    assert navegador.delete("/usuarios/sesion").status_code == 204
    assert navegador.get("/usuarios/me").status_code == 401


def test_el_header_bearer_sigue_funcionando_y_tiene_precedencia_sobre_la_cookie(client):
    email_a, email_b = _registrar(client), _registrar(client)
    navegador = _navegador()
    navegador.post("/usuarios/sesion", json={"email": email_a, "password": PASSWORD})  # cookie de A

    token_b = client.post("/usuarios/login", json={"email": email_b, "password": PASSWORD}).json()["access_token"]
    r = navegador.get("/usuarios/me", headers={"Authorization": f"Bearer {token_b}"})
    assert r.json()["email"] == email_b


def test_la_cookie_da_acceso_a_los_recursos_del_usuario_y_a_nadie_mas(client):
    """Las reglas de pertenencia valen igual con cookie: un usuario no ve los vehículos de otro."""
    email_a, email_b = _registrar(client), _registrar(client)
    a, b = _navegador(), _navegador()
    a.post("/usuarios/sesion", json={"email": email_a, "password": PASSWORD})
    b.post("/usuarios/sesion", json={"email": email_b, "password": PASSWORD})

    vid = a.post("/vehiculos", json={"alias": "Auto", "kilometraje_inicial": 1000}).json()["id"]
    assert a.get(f"/vehiculos/{vid}").status_code == 200
    assert b.get(f"/vehiculos/{vid}").status_code == 404
    assert b.get("/vehiculos").json() == []
