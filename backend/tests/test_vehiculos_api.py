"""Pruebas de la API de Vehículos que no necesitan base de datos (autenticación y validaciones)."""
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
        ("get", "/vehiculos"),
        ("post", "/vehiculos"),
        ("get", f"/vehiculos/{ID}"),
        ("put", f"/vehiculos/{ID}"),
        ("delete", f"/vehiculos/{ID}"),
    ],
)
def test_todos_los_endpoints_exigen_token(metodo, ruta):
    r = getattr(client, metodo)(ruta)
    assert r.status_code == 401


@pytest.fixture
def auth():
    # Token válido de un usuario cualquiera: alcanza para llegar a la validación del cuerpo.
    return {"Authorization": f"Bearer {crear_token(uuid.uuid4())}"}


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"alias": "   ", "kilometraje_inicial": 1000},      # alias vacío
        {"alias": "x" * 101, "kilometraje_inicial": 1000},  # alias demasiado largo
        {"alias": "Auto", "kilometraje_inicial": -1},       # km negativo
        {"alias": "Auto", "kilometraje_inicial": 10.123},   # más de 2 decimales
        {"alias": "Auto", "kilometraje_inicial": 10**9},    # no entra en NUMERIC(10,2)
        {"alias": "Auto"},                                  # falta el km
    ],
)
def test_crear_con_datos_invalidos_responde_422(auth, cuerpo):
    assert client.post("/vehiculos", json=cuerpo, headers=auth).status_code == 422


def test_id_con_formato_invalido_responde_422(auth):
    assert client.get("/vehiculos/no-es-un-uuid", headers=auth).status_code == 422
