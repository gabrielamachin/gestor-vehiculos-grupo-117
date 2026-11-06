"""Pruebas de la API de Categorías que no necesitan base de datos."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_listar_exige_token():
    assert client.get("/categorias").status_code == 401
