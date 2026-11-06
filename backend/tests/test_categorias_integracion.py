"""Pruebas de integración de Categorías contra una PostgreSQL real (ver tests/utils_integracion.py)."""
import pytest
from sqlalchemy import text

from app.core.database import get_db
from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, nuevo_usuario

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _codigos(respuesta):
    assert respuesta.status_code == 200
    return [c["codigo"] for c in respuesta.json()]


def test_lista_las_categorias_iniciales_ordenadas_por_nombre(client):
    h = nuevo_usuario(client)
    r = client.get("/categorias", headers=h)
    assert r.status_code == 200

    nombres = [c["nombre"] for c in r.json()]
    assert nombres == sorted(nombres)
    assert set(_codigos(r)) == {"combustible", "mantenimiento", "reparacion", "seguro", "neumaticos", "otro"}

    por_codigo = {c["codigo"]: c for c in r.json()}
    assert por_codigo["seguro"]["tipo_costo"] == "fijo"
    assert por_codigo["combustible"]["tipo_costo"] == "variable"
    assert por_codigo["combustible"]["activa"] is True


def test_una_categoria_inactiva_solo_se_lista_si_se_pide(client):
    h = nuevo_usuario(client)

    # Las categorías se administran con SQL: se desactiva una directamente en la base de pruebas.
    gen = client.app.dependency_overrides[get_db]()
    db = next(gen)
    try:
        db.execute(text("UPDATE categorias_gasto SET activa = FALSE WHERE codigo = 'otro'"))
        db.commit()

        assert "otro" not in _codigos(client.get("/categorias", headers=h))
        assert "otro" in _codigos(client.get("/categorias?incluir_inactivas=true", headers=h))
    finally:
        db.execute(text("UPDATE categorias_gasto SET activa = TRUE WHERE codigo = 'otro'"))
        db.commit()
        gen.close()
