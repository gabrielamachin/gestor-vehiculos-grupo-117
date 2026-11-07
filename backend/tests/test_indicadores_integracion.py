"""Pruebas de integración de Indicadores contra una PostgreSQL real (ver tests/utils_integracion.py)."""
from datetime import date, timedelta

import pytest

from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, nuevo_usuario, nuevo_vehiculo

pytestmark = SALTAR_SIN_BASE

RUTAS = ["resumen", "costo-por-km", "gasto-por-categoria", "alerta-combustible", "proximo-mantenimiento", "reparar-o-reemplazar"]


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _categoria(client, headers, codigo) -> int:
    categorias = client.get("/categorias?incluir_inactivas=true", headers=headers).json()
    return next(c["id"] for c in categorias if c["codigo"] == codigo)


def _gasto(client, headers, vehiculo_id, codigo, monto, fecha, **extra):
    cuerpo = {"vehiculo_id": vehiculo_id, "categoria_id": _categoria(client, headers, codigo), "monto": monto, "fecha": str(fecha), **extra}
    r = client.post("/gastos", json=cuerpo, headers=headers)
    assert r.status_code == 201, r.text
    return r.json()


def _lectura(client, headers, vehiculo_id, fecha, km):
    r = client.post("/kilometraje", json={"vehiculo_id": vehiculo_id, "fecha": str(fecha), "kilometraje": km}, headers=headers)
    assert r.status_code == 201, r.text


def _plan(client, headers, vehiculo_id, nombre, intervalo) -> str:
    r = client.post("/mantenimiento", json={"vehiculo_id": vehiculo_id, "nombre": nombre, "intervalo_km": intervalo}, headers=headers)
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _get(client, headers, vehiculo_id, ruta, **params):
    return client.get(f"/indicadores/vehiculos/{vehiculo_id}/{ruta}", headers=headers, params=params)


def test_vehiculo_sin_datos_devuelve_estados_vacios_y_no_errores(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)

    assert _get(client, a, vid, "costo-por-km").json() == {"estado": "sin_lecturas", "costo_por_km": None, "km_recorridos": None, "total_gastado": 0}
    por_categoria = _get(client, a, vid, "gasto-por-categoria").json()
    assert por_categoria["categorias"] == [] and por_categoria["total"] == 0
    assert _get(client, a, vid, "alerta-combustible").json()["estado"] == "sin_datos"
    assert _get(client, a, vid, "proximo-mantenimiento").json() == []
    assert _get(client, a, vid, "reparar-o-reemplazar").json()["estado"] == "sin_datos"


def test_costo_por_km_y_gasto_por_categoria(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    _lectura(client, a, vid, "2024-06-01", 11000)
    _gasto(client, a, vid, "combustible", 30000, "2024-02-10")
    _gasto(client, a, vid, "reparacion", 20000, "2024-03-10")
    _gasto(client, a, vid, "seguro", 50000, "2024-04-10")

    costo = _get(client, a, vid, "costo-por-km").json()
    assert costo == {"estado": "ok", "costo_por_km": 10.0, "km_recorridos": 10000.0, "total_gastado": 100000.0}

    r = _get(client, a, vid, "gasto-por-categoria").json()
    assert [(c["codigo"], c["total"], c["porcentaje"], c["cantidad"]) for c in r["categorias"]] == [
        ("seguro", 50000, 50.0, 1), ("combustible", 30000, 30.0, 1), ("reparacion", 20000, 20.0, 1),
    ]
    assert (r["total"], r["total_fijo"], r["total_variable"]) == (100000, 50000, 50000)

    desde_marzo = _get(client, a, vid, "gasto-por-categoria", desde="2024-03-01").json()
    assert desde_marzo["total"] == 70000 and len(desde_marzo["categorias"]) == 2

    assert _get(client, a, vid, "gasto-por-categoria", desde="2024-03-01", hasta="2024-01-01").status_code == 422


def test_alerta_de_combustible(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)

    for mes in (1, 2):
        _gasto(client, a, vid, "combustible", 10000, f"2024-0{mes}-10")
    assert _get(client, a, vid, "alerta-combustible").json()["estado"] == "historial_insuficiente"

    _gasto(client, a, vid, "combustible", 10000, "2024-03-10")
    _gasto(client, a, vid, "combustible", 6000, "2024-04-05")    # dos cargas el mismo mes: se suman
    _gasto(client, a, vid, "combustible", 9000, "2024-04-25")
    r = _get(client, a, vid, "alerta-combustible").json()
    assert r["estado"] == "alerta"
    assert r["mes_evaluado"] == "2024-04-01"
    assert r["gasto_mes"] == 15000 and r["promedio_historico"] == 10000 and r["desvio_pct"] == 50.0
    assert r["meses_en_historial"] == 3 and r["umbral_pct"] == 20.0


def test_proximo_mantenimiento_ordenado_por_urgencia(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    aceite, correa = _plan(client, a, vid, "Aceite", 10000), _plan(client, a, vid, "Correa", 15000)
    _plan(client, a, vid, "Frenos", 20000)
    _gasto(client, a, vid, "mantenimiento", 45000, "2024-02-01", plan_mantenimiento_id=aceite, kilometraje=20000)
    _gasto(client, a, vid, "mantenimiento", 80000, "2024-01-15", plan_mantenimiento_id=correa, kilometraje=10000)
    _lectura(client, a, vid, "2024-05-01", 29500)

    r = _get(client, a, vid, "proximo-mantenimiento").json()
    assert [(p["nombre"], p["estado"], p["proximo_km"], p["km_restantes"], p["base"]) for p in r] == [
        ("Correa", "vencido", 25000, -4500, "ultimo_mantenimiento"),
        ("Aceite", "proximo", 30000, 500, "ultimo_mantenimiento"),
        ("Frenos", "al_dia", 40000, 10500, "multiplos"),
    ]
    assert r[0]["ultimo_km"] == 10000 and r[2]["ultimo_km"] is None


def test_reparar_o_reemplazar_con_senales(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    hoy = date.today()
    _lectura(client, a, vid, hoy - timedelta(days=10), 160000)
    _gasto(client, a, vid, "reparacion", 80000, hoy - timedelta(days=30))     # últimos 6 meses
    _gasto(client, a, vid, "reparacion", 30000, hoy - timedelta(days=250))    # 6 meses previos
    _gasto(client, a, vid, "combustible", 100000, hoy - timedelta(days=100))

    r = _get(client, a, vid, "reparar-o-reemplazar").json()
    assert r["estado"] == "considerar_reemplazo"
    assert {s["codigo"] for s in r["senales"] if s["cumplida"]} == {"peso_reparaciones", "reparaciones_en_aumento", "kilometraje_elevado"}
    assert r["aviso"]


def test_resumen_reune_todos_los_indicadores(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    _lectura(client, a, vid, date.today() - timedelta(days=5), 6000)
    _gasto(client, a, vid, "combustible", 5000, date.today() - timedelta(days=30))
    _plan(client, a, vid, "Aceite", 10000)

    r = _get(client, a, vid, "resumen").json()
    assert set(r) == {"costo_por_km", "gasto_por_categoria", "alerta_combustible", "proximos_mantenimientos", "reparar_o_reemplazar"}
    assert r["costo_por_km"]["costo_por_km"] == 1.0                      # 5.000 / 5.000 km
    assert r["gasto_por_categoria"]["total"] == 5000                     # últimos 12 meses
    assert len(r["proximos_mantenimientos"]) == 1
    assert r["alerta_combustible"]["estado"] == "historial_insuficiente"


def test_otro_usuario_no_puede_ver_los_indicadores(client):
    a, b = nuevo_usuario(client), nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    for ruta in RUTAS:
        assert _get(client, b, vid, ruta).status_code == 404, ruta
        assert _get(client, a, vid, ruta).status_code == 200, ruta
