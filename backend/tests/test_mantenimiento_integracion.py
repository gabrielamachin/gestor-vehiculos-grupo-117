"""Pruebas de integración de Mantenimiento contra una PostgreSQL real (ver tests/utils_integracion.py)."""
import pytest

from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, nuevo_usuario, nuevo_vehiculo

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _crear_plan(client, headers, vehiculo_id, nombre="Aceite", intervalo=10000):
    return client.post(
        "/mantenimiento",
        json={"vehiculo_id": vehiculo_id, "nombre": nombre, "intervalo_km": intervalo},
        headers=headers,
    )


def test_crear_y_listar_ordenado_por_nombre(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)

    r = _crear_plan(client, a, vid, "Filtros", 15000.5)
    assert r.status_code == 201
    assert r.json()["intervalo_km"] == 15000.5  # número JSON, no string
    assert _crear_plan(client, a, vid, "Aceite", 10000).status_code == 201

    lista = client.get(f"/mantenimiento?vehiculo_id={vid}", headers=a).json()
    assert [p["nombre"] for p in lista] == ["Aceite", "Filtros"]


def test_nombre_repetido_solo_es_conflicto_dentro_del_mismo_vehiculo(client):
    a = nuevo_usuario(client)
    auto = nuevo_vehiculo(client, a, "Auto")
    moto = nuevo_vehiculo(client, a, "Moto")

    assert _crear_plan(client, a, auto, "Aceite").status_code == 201
    assert _crear_plan(client, a, auto, "Aceite").status_code == 409
    assert _crear_plan(client, a, moto, "Aceite").status_code == 201  # otro vehículo, mismo nombre: permitido


def test_actualizar(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    pid = _crear_plan(client, a, vid, "Aceite", 10000).json()["id"]
    _crear_plan(client, a, vid, "Filtros", 15000)

    r = client.put(f"/mantenimiento/{pid}", json={"nombre": "Aceite y filtro", "intervalo_km": 7500}, headers=a)
    assert r.status_code == 200
    assert r.json()["nombre"] == "Aceite y filtro" and r.json()["intervalo_km"] == 7500

    # No se puede tomar el nombre de otro plan del mismo vehículo
    assert client.put(f"/mantenimiento/{pid}", json={"nombre": "Filtros", "intervalo_km": 7500}, headers=a).status_code == 409
    # Reenviar el mismo nombre no es un conflicto
    assert client.put(f"/mantenimiento/{pid}", json={"nombre": "Aceite y filtro", "intervalo_km": 8000}, headers=a).status_code == 200


def test_otro_usuario_no_puede_ver_crear_modificar_ni_borrar(client):
    a, b = nuevo_usuario(client), nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    pid = _crear_plan(client, a, vid).json()["id"]

    assert _crear_plan(client, b, vid, "Intruso").status_code == 404                 # crear en vehículo ajeno
    assert client.get(f"/mantenimiento?vehiculo_id={vid}", headers=b).status_code == 404
    assert client.get(f"/mantenimiento/{pid}", headers=b).status_code == 404
    assert client.put(f"/mantenimiento/{pid}", json={"nombre": "X", "intervalo_km": 1}, headers=b).status_code == 404
    assert client.delete(f"/mantenimiento/{pid}", headers=b).status_code == 404

    # El plan del dueño quedó intacto
    assert client.get(f"/mantenimiento/{pid}", headers=a).json()["nombre"] == "Aceite"


def test_eliminar_y_borrado_en_cascada_con_el_vehiculo(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    pid = _crear_plan(client, a, vid).json()["id"]
    assert client.delete(f"/mantenimiento/{pid}", headers=a).status_code == 204
    assert client.get(f"/mantenimiento/{pid}", headers=a).status_code == 404

    otro = _crear_plan(client, a, vid, "Filtros").json()["id"]
    assert client.delete(f"/vehiculos/{vid}", headers=a).status_code == 204
    assert client.get(f"/mantenimiento/{otro}", headers=a).status_code == 404
