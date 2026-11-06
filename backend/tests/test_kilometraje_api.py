"""Pruebas de la API de Kilometraje que no necesitan base de datos (autenticación y validaciones)."""
import uuid
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.core.security import crear_token
from app.main import app

client = TestClient(app)
ID = uuid.uuid4()


@pytest.mark.parametrize(
    "metodo, ruta",
    [
        ("get", f"/kilometraje?vehiculo_id={ID}"),
        ("get", f"/kilometraje/ultima?vehiculo_id={ID}"),
        ("post", "/kilometraje"),
        ("get", f"/kilometraje/{ID}"),
        ("put", f"/kilometraje/{ID}"),
        ("delete", f"/kilometraje/{ID}"),
    ],
)
def test_todos_los_endpoints_exigen_token(metodo, ruta):
    assert getattr(client, metodo)(ruta).status_code == 401


@pytest.fixture
def auth():
    # Token válido de un usuario cualquiera: alcanza para llegar a la validación del cuerpo.
    return {"Authorization": f"Bearer {crear_token(uuid.uuid4())}"}


MANANA = (date.today() + timedelta(days=1)).isoformat()


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"vehiculo_id": str(ID), "fecha": MANANA, "kilometraje": 1000},         # fecha futura
        {"vehiculo_id": str(ID), "fecha": "2024-01-10", "kilometraje": -5},     # km negativo
        {"vehiculo_id": str(ID), "fecha": "2024-01-10", "kilometraje": 1.234},  # más de 2 decimales
        {"vehiculo_id": str(ID), "fecha": "no-es-fecha", "kilometraje": 1000},  # fecha inválida
        {"vehiculo_id": "no-es-uuid", "fecha": "2024-01-10", "kilometraje": 1000},
        {"fecha": "2024-01-10", "kilometraje": 1000},                           # falta vehiculo_id
    ],
)
def test_crear_con_datos_invalidos_responde_422(auth, cuerpo):
    assert client.post("/kilometraje", json=cuerpo, headers=auth).status_code == 422


def test_listar_sin_vehiculo_id_responde_422(auth):
    assert client.get("/kilometraje", headers=auth).status_code == 422
