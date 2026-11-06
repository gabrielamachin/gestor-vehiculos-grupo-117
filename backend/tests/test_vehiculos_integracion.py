"""Pruebas de integración de Vehículos contra una PostgreSQL real (ver tests/utils_integracion.py)."""
import pytest

from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, nuevo_usuario

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _crear_vehiculo(client, headers, alias="Auto", km=12000.5):
    return client.post("/vehiculos", json={"alias": alias, "kilometraje_inicial": km}, headers=headers)


def test_crear_y_listar(client):
    a = nuevo_usuario(client)
    r = _crear_vehiculo(client, a)
    assert r.status_code == 201
    assert r.json()["kilometraje_inicial"] == 12000.5  # número JSON, no string

    lista = client.get("/vehiculos", headers=a).json()
    assert [v["alias"] for v in lista] == ["Auto"]


def test_otro_usuario_no_puede_ver_ni_modificar_ni_borrar(client):
    a, b = nuevo_usuario(client), nuevo_usuario(client)
    vehiculo_id = _crear_vehiculo(client, a).json()["id"]

    assert client.get(f"/vehiculos/{vehiculo_id}", headers=b).status_code == 404
    assert client.put(f"/vehiculos/{vehiculo_id}", json={"alias": "Robado"}, headers=b).status_code == 404
    assert client.delete(f"/vehiculos/{vehiculo_id}", headers=b).status_code == 404
    assert client.get("/vehiculos", headers=b).json() == []

    # El dueño sigue viendo su vehículo intacto
    r = client.get(f"/vehiculos/{vehiculo_id}", headers=a)
    assert r.status_code == 200
    assert r.json()["alias"] == "Auto"


def test_alias_repetido_solo_conflicto_dentro_del_mismo_usuario(client):
    a, b = nuevo_usuario(client), nuevo_usuario(client)
    assert _crear_vehiculo(client, a, "Auto").status_code == 201
    assert _crear_vehiculo(client, a, "Auto").status_code == 409
    assert _crear_vehiculo(client, b, "Auto").status_code == 201  # otro usuario, mismo alias: permitido


def test_actualizar_alias(client):
    a = nuevo_usuario(client)
    vid = _crear_vehiculo(client, a, "Auto").json()["id"]
    _crear_vehiculo(client, a, "Moto")

    r = client.put(f"/vehiculos/{vid}", json={"alias": "Auto familiar"}, headers=a)
    assert r.status_code == 200
    assert r.json()["alias"] == "Auto familiar"

    # No se puede tomar el alias de otro vehículo propio
    assert client.put(f"/vehiculos/{vid}", json={"alias": "Moto"}, headers=a).status_code == 409
    # Reenviar el mismo alias no es un conflicto
    assert client.put(f"/vehiculos/{vid}", json={"alias": "Auto familiar"}, headers=a).status_code == 200


def test_eliminar(client):
    a = nuevo_usuario(client)
    vid = _crear_vehiculo(client, a).json()["id"]
    assert client.delete(f"/vehiculos/{vid}", headers=a).status_code == 204
    assert client.get(f"/vehiculos/{vid}", headers=a).status_code == 404
