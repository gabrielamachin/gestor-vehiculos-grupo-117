"""Pruebas de la sesión por cookie que no necesitan base de datos."""
import uuid

from fastapi.testclient import TestClient

from app.core.security import NOMBRE_COOKIE_SESION, crear_token
from app.main import app


def _navegador() -> TestClient:
    """Cliente nuevo = navegador nuevo (sin cookies compartidas con otras pruebas)."""
    return TestClient(app)


def test_cookie_invalida_responde_401():
    r = _navegador().get("/usuarios/me", headers={"Cookie": f"{NOMBRE_COOKIE_SESION}=basura"})
    assert r.status_code == 401


def test_header_invalido_no_cae_a_la_cookie():
    """Si llega un Authorization inválido se rechaza, aunque la cookie fuera válida."""
    cookie_valida = f"{NOMBRE_COOKIE_SESION}={crear_token(uuid.uuid4())}"
    r = _navegador().get("/usuarios/me", headers={"Authorization": "Bearer basura", "Cookie": cookie_valida})
    assert r.status_code == 401


def test_iniciar_sesion_con_datos_invalidos_responde_422():
    r = _navegador().post("/usuarios/sesion", json={"email": "no-es-email", "password": "x"})
    assert r.status_code == 422
    assert "set-cookie" not in r.headers


def test_cerrar_sesion_borra_la_cookie_y_es_idempotente():
    r = _navegador().delete("/usuarios/sesion")  # sin sesión previa: no falla
    assert r.status_code == 204
    cabecera = r.headers["set-cookie"]
    assert NOMBRE_COOKIE_SESION in cabecera
    assert "Max-Age=0" in cabecera
    assert "HttpOnly" in cabecera
