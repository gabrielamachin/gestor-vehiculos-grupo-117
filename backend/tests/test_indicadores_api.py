"""Pruebas de la API de Indicadores que no necesitan base de datos (autenticación y validaciones)."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.security import crear_token
from app.main import app

client = TestClient(app)
ID = uuid.uuid4()
BASE = f"/indicadores/vehiculos/{ID}"
RUTAS = ["resumen", "costo-por-km", "gasto-por-categoria", "alerta-combustible", "proximo-mantenimiento", "reparar-o-reemplazar"]


@pytest.mark.parametrize("ruta", RUTAS)
def test_todos_los_endpoints_exigen_token(ruta):
    assert client.get(f"{BASE}/{ruta}").status_code == 401


@pytest.fixture
def auth():
    # Token válido de un usuario cualquiera: alcanza para llegar a la validación de parámetros.
    return {"Authorization": f"Bearer {crear_token(uuid.uuid4())}"}


@pytest.mark.parametrize("ruta", RUTAS)
def test_id_con_formato_invalido_responde_422(auth, ruta):
    assert client.get(f"/indicadores/vehiculos/no-es-un-uuid/{ruta}", headers=auth).status_code == 422


def test_gasto_por_categoria_con_fecha_invalida_responde_422(auth):
    assert client.get(f"{BASE}/gasto-por-categoria?desde=ayer", headers=auth).status_code == 422
