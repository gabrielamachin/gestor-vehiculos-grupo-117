"""Pruebas de integración de Kilometraje contra una PostgreSQL real (ver tests/utils_integracion.py)."""
import pytest

from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, nuevo_usuario, nuevo_vehiculo

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _cargar(client, headers, vehiculo_id, fecha, km):
    return client.post("/kilometraje", json={"vehiculo_id": vehiculo_id, "fecha": fecha, "kilometraje": km}, headers=headers)


def test_crear_y_listar_de_la_mas_reciente_a_la_mas_antigua(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)

    assert _cargar(client, a, vid, "2024-01-10", 1500).status_code == 201
    assert _cargar(client, a, vid, "2024-03-10", 2500.5).status_code == 201

    lista = client.get(f"/kilometraje?vehiculo_id={vid}", headers=a).json()
    assert [l["fecha"] for l in lista] == ["2024-03-10", "2024-01-10"]
    assert lista[0]["kilometraje"] == 2500.5  # número JSON, no string


def test_ultima_lectura_y_null_sin_lecturas(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    assert client.get(f"/kilometraje/ultima?vehiculo_id={vid}", headers=a).json() is None

    # Se cargan fuera de orden: la última es la de fecha más reciente, no la última cargada
    _cargar(client, a, vid, "2024-05-01", 3000)
    _cargar(client, a, vid, "2024-02-01", 1800)
    ultima = client.get(f"/kilometraje/ultima?vehiculo_id={vid}", headers=a).json()
    assert ultima["fecha"] == "2024-05-01"
    assert ultima["kilometraje"] == 3000


def test_el_odometro_no_puede_retroceder(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)

    assert _cargar(client, a, vid, "2024-01-10", 999).status_code == 422   # menor al inicial
    assert _cargar(client, a, vid, "2024-02-10", 2000).status_code == 201
    assert _cargar(client, a, vid, "2024-03-10", 1999).status_code == 422  # retrocede respecto de la anterior
    assert _cargar(client, a, vid, "2024-03-10", 2000).status_code == 201  # igual: el auto no se movió
    assert _cargar(client, a, vid, "2024-01-20", 2001).status_code == 422  # supera a una lectura posterior
    assert _cargar(client, a, vid, "2024-01-20", 1500).status_code == 201  # entre medio, coherente


def test_una_lectura_por_vehiculo_y_dia(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    assert _cargar(client, a, vid, "2024-01-10", 1500).status_code == 201
    assert _cargar(client, a, vid, "2024-01-10", 1600).status_code == 409


def test_actualizar_no_se_compara_contra_si_misma(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    _cargar(client, a, vid, "2024-01-10", 1500)
    lid = _cargar(client, a, vid, "2024-02-10", 2000).json()["id"]
    _cargar(client, a, vid, "2024-03-10", 2500)

    ok = client.put(f"/kilometraje/{lid}", json={"fecha": "2024-02-10", "kilometraje": 2400}, headers=a)
    assert ok.status_code == 200 and ok.json()["kilometraje"] == 2400

    # Mover la lectura a otra fecha: se valida contra las demás, no contra su valor anterior
    assert client.put(f"/kilometraje/{lid}", json={"fecha": "2024-02-20", "kilometraje": 2600}, headers=a).status_code == 422
    assert client.put(f"/kilometraje/{lid}", json={"fecha": "2024-01-10", "kilometraje": 2400}, headers=a).status_code == 409


def test_otro_usuario_no_puede_ver_cargar_modificar_ni_borrar(client):
    a, b = nuevo_usuario(client), nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    lid = _cargar(client, a, vid, "2024-01-10", 1500).json()["id"]

    assert _cargar(client, b, vid, "2024-02-10", 1600).status_code == 404            # cargar en vehículo ajeno
    assert client.get(f"/kilometraje?vehiculo_id={vid}", headers=b).status_code == 404
    assert client.get(f"/kilometraje/ultima?vehiculo_id={vid}", headers=b).status_code == 404
    assert client.get(f"/kilometraje/{lid}", headers=b).status_code == 404
    assert client.put(f"/kilometraje/{lid}", json={"fecha": "2024-01-10", "kilometraje": 9999}, headers=b).status_code == 404
    assert client.delete(f"/kilometraje/{lid}", headers=b).status_code == 404

    # La lectura del dueño quedó intacta
    assert client.get(f"/kilometraje/{lid}", headers=a).json()["kilometraje"] == 1500


def test_eliminar_y_borrado_en_cascada_con_el_vehiculo(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    lid = _cargar(client, a, vid, "2024-01-10", 1500).json()["id"]
    assert client.delete(f"/kilometraje/{lid}", headers=a).status_code == 204
    assert client.get(f"/kilometraje/{lid}", headers=a).status_code == 404

    otra = _cargar(client, a, vid, "2024-02-10", 1600).json()["id"]
    assert client.delete(f"/vehiculos/{vid}", headers=a).status_code == 204
    assert client.get(f"/kilometraje/{otra}", headers=a).status_code == 404
