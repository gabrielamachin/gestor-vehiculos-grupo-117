"""Pruebas de la API que no necesitan base de datos (validaciones y autenticación)."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_me_sin_token_responde_401():
    r = client.get("/usuarios/me")
    assert r.status_code == 401


def test_me_con_token_invalido_responde_401():
    r = client.get("/usuarios/me", headers={"Authorization": "Bearer basura"})
    assert r.status_code == 401


def test_registro_con_password_corta_responde_422():
    r = client.post("/usuarios/registro", json={"nombre": "Ana", "email": "ana@mail.com", "password": "123"})
    assert r.status_code == 422


def test_registro_con_email_invalido_responde_422():
    r = client.post("/usuarios/registro", json={"nombre": "Ana", "email": "no-es-email", "password": "clave-segura-123"})
    assert r.status_code == 422


def test_registro_con_nombre_vacio_responde_422():
    r = client.post("/usuarios/registro", json={"nombre": "   ", "email": "ana@mail.com", "password": "clave-segura-123"})
    assert r.status_code == 422
