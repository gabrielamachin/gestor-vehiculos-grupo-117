"""Pruebas de la API de Gastos que no necesitan base de datos (autenticación y validaciones)."""
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
        ("get", f"/gastos?vehiculo_id={ID}"),
        ("post", "/gastos"),
        ("get", f"/gastos/{ID}"),
        ("put", f"/gastos/{ID}"),
        ("delete", f"/gastos/{ID}"),
    ],
)
def test_todos_los_endpoints_exigen_token(metodo, ruta):
    assert getattr(client, metodo)(ruta).status_code == 401


@pytest.fixture
def auth():
    # Token válido de un usuario cualquiera: alcanza para llegar a la validación del cuerpo.
    return {"Authorization": f"Bearer {crear_token(uuid.uuid4())}"}


def _cuerpo(**cambios):
    base = {"vehiculo_id": str(ID), "categoria_id": 1, "monto": 5000, "fecha": "2024-01-10"}
    return {**base, **cambios}


MANANA = (date.today() + timedelta(days=1)).isoformat()


@pytest.mark.parametrize(
    "cuerpo",
    [
        _cuerpo(monto=0),                                    # monto cero
        _cuerpo(monto=-10),                                  # monto negativo
        _cuerpo(monto=10.123),                               # más de 2 decimales
        _cuerpo(monto=10**10),                               # no entra en NUMERIC(12,2)
        _cuerpo(fecha=MANANA),                               # fecha futura
        _cuerpo(fecha="no-es-fecha"),
        _cuerpo(categoria_id=0),
        _cuerpo(categoria_id="combustible"),                 # la categoría va por id
        _cuerpo(kilometraje=-1),
        _cuerpo(descripcion="x" * 501),                      # descripción demasiado larga
        _cuerpo(plan_mantenimiento_id=str(uuid.uuid4())),    # plan sin kilometraje
        _cuerpo(plan_mantenimiento_id="no-es-uuid", kilometraje=5000),
        {k: v for k, v in _cuerpo().items() if k != "monto"},        # falta el monto
        {k: v for k, v in _cuerpo().items() if k != "vehiculo_id"},  # falta el vehículo
    ],
)
def test_crear_con_datos_invalidos_responde_422(auth, cuerpo):
    assert client.post("/gastos", json=cuerpo, headers=auth).status_code == 422


def test_listar_sin_vehiculo_id_responde_422(auth):
    assert client.get("/gastos", headers=auth).status_code == 422


def test_listar_con_fecha_invalida_responde_422(auth):
    assert client.get(f"/gastos?vehiculo_id={ID}&desde=ayer", headers=auth).status_code == 422
