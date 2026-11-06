"""Pruebas de la API de Mantenimiento que no necesitan base de datos (autenticación y validaciones)."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.security import crear_token
from app.main import app

client = TestClient(app)
ID = uuid.uuid4()


@pytest.mark.parametrize(
    "metodo, ruta",
    [
        ("get", f"/mantenimiento?vehiculo_id={ID}"),
        ("post", "/mantenimiento"),
        ("get", f"/mantenimiento/{ID}"),
        ("put", f"/mantenimiento/{ID}"),
        ("delete", f"/mantenimiento/{ID}"),
    ],
)
def test_todos_los_endpoints_exigen_token(metodo, ruta):
    assert getattr(client, metodo)(ruta).status_code == 401


@pytest.fixture
def auth():
    # Token válido de un usuario cualquiera: alcanza para llegar a la validación del cuerpo.
    return {"Authorization": f"Bearer {crear_token(uuid.uuid4())}"}


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"vehiculo_id": str(ID), "nombre": "   ", "intervalo_km": 10000},          # nombre vacío
        {"vehiculo_id": str(ID), "nombre": "x" * 101, "intervalo_km": 10000},      # nombre demasiado largo
        {"vehiculo_id": str(ID), "nombre": "Aceite", "intervalo_km": 0},           # intervalo cero
        {"vehiculo_id": str(ID), "nombre": "Aceite", "intervalo_km": -5000},       # intervalo negativo
        {"vehiculo_id": str(ID), "nombre": "Aceite", "intervalo_km": 10.123},      # más de 2 decimales
        {"vehiculo_id": str(ID), "nombre": "Aceite"},                              # falta el intervalo
        {"vehiculo_id": "no-es-uuid", "nombre": "Aceite", "intervalo_km": 10000},
        {"nombre": "Aceite", "intervalo_km": 10000},                               # falta vehiculo_id
    ],
)
def test_crear_con_datos_invalidos_responde_422(auth, cuerpo):
    assert client.post("/mantenimiento", json=cuerpo, headers=auth).status_code == 422


def test_listar_sin_vehiculo_id_responde_422(auth):
    assert client.get("/mantenimiento", headers=auth).status_code == 422
