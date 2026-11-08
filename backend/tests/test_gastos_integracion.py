"""Pruebas de integración de Gastos contra una PostgreSQL real (ver tests/utils_integracion.py)."""
import uuid
from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import text

from app.gastos import service
from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, nuevo_usuario, nuevo_vehiculo, sesion_de_prueba

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _categoria(client, headers, codigo) -> int:
    categorias = client.get("/categorias?incluir_inactivas=true", headers=headers).json()
    return next(c["id"] for c in categorias if c["codigo"] == codigo)


def _gasto(client, headers, vehiculo_id, categoria_id, monto, fecha="2024-01-10", **extra):
    cuerpo = {"vehiculo_id": vehiculo_id, "categoria_id": categoria_id, "monto": monto, "fecha": fecha, **extra}
    return client.post("/gastos", json=cuerpo, headers=headers)


def _plan(client, headers, vehiculo_id, nombre="Aceite", intervalo=10000) -> str:
    r = client.post("/mantenimiento", json={"vehiculo_id": vehiculo_id, "nombre": nombre, "intervalo_km": intervalo}, headers=headers)
    assert r.status_code == 201
    return r.json()["id"]


def test_crear_y_listar_del_mas_reciente_al_mas_antiguo(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    comb = _categoria(client, a, "combustible")

    r = _gasto(client, a, vid, comb, 12345.5, "2024-01-10", descripcion="  Carga completa  ")
    assert r.status_code == 201
    assert r.json()["monto"] == 12345.5          # número JSON, no string
    assert r.json()["descripcion"] == "Carga completa"
    assert _gasto(client, a, vid, comb, 100, "2024-03-10").status_code == 201

    lista = client.get(f"/gastos?vehiculo_id={vid}", headers=a).json()
    assert [g["fecha"] for g in lista] == ["2024-03-10", "2024-01-10"]


def test_filtros_por_fecha_y_categoria(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    comb, rep = _categoria(client, a, "combustible"), _categoria(client, a, "reparacion")
    _gasto(client, a, vid, comb, 100, "2024-01-10")
    _gasto(client, a, vid, comb, 200, "2024-02-10")
    _gasto(client, a, vid, rep, 300, "2024-02-15")

    febrero = client.get(f"/gastos?vehiculo_id={vid}&desde=2024-02-01&hasta=2024-02-29", headers=a).json()
    assert sorted(g["monto"] for g in febrero) == [200, 300]

    solo_comb = client.get(f"/gastos?vehiculo_id={vid}&categoria_id={comb}", headers=a).json()
    assert sorted(g["monto"] for g in solo_comb) == [100, 200]

    invertido = client.get(f"/gastos?vehiculo_id={vid}&desde=2024-03-01&hasta=2024-01-01", headers=a)
    assert invertido.status_code == 422


def test_otro_usuario_no_puede_ver_cargar_modificar_ni_borrar(client):
    a, b = nuevo_usuario(client), nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    comb = _categoria(client, a, "combustible")
    gid = _gasto(client, a, vid, comb, 100).json()["id"]
    cuerpo = {"categoria_id": comb, "monto": 999, "fecha": "2024-01-10"}

    assert _gasto(client, b, vid, comb, 50).status_code == 404            # cargar en vehículo ajeno
    assert client.get(f"/gastos?vehiculo_id={vid}", headers=b).status_code == 404
    assert client.get(f"/gastos/{gid}", headers=b).status_code == 404
    assert client.put(f"/gastos/{gid}", json=cuerpo, headers=b).status_code == 404
    assert client.delete(f"/gastos/{gid}", headers=b).status_code == 404

    assert client.get(f"/gastos/{gid}", headers=a).json()["monto"] == 100  # intacto


def test_actualizar_y_eliminar(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    comb, otro = _categoria(client, a, "combustible"), _categoria(client, a, "otro")
    gid = _gasto(client, a, vid, comb, 100).json()["id"]

    r = client.put(f"/gastos/{gid}", json={"categoria_id": otro, "monto": 250.75, "fecha": "2024-02-01", "descripcion": "Lavado"}, headers=a)
    assert r.status_code == 200
    assert (r.json()["categoria_id"], r.json()["monto"], r.json()["descripcion"]) == (otro, 250.75, "Lavado")

    assert client.delete(f"/gastos/{gid}", headers=a).status_code == 204
    assert client.get(f"/gastos/{gid}", headers=a).status_code == 404


def test_categoria_inactiva_no_se_acepta_para_gastos_nuevos(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    otro = _categoria(client, a, "otro")
    existente = _gasto(client, a, vid, otro, 100).json()["id"]

    with sesion_de_prueba(client) as db:
        try:
            db.execute(text("UPDATE categorias_gasto SET activa = FALSE WHERE codigo = 'otro'"))
            db.commit()

            assert _gasto(client, a, vid, otro, 50).status_code == 422          # nuevo: rechazado
            r = client.put(f"/gastos/{existente}", json={"categoria_id": otro, "monto": 120, "fecha": "2024-01-10"}, headers=a)
            assert r.status_code == 200                                          # histórico: editable
        finally:
            db.execute(text("UPDATE categorias_gasto SET activa = TRUE WHERE codigo = 'otro'"))
            db.commit()


def test_kilometraje_no_puede_ser_menor_al_inicial(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    comb = _categoria(client, a, "combustible")
    assert _gasto(client, a, vid, comb, 100, kilometraje=999).status_code == 422
    assert _gasto(client, a, vid, comb, 100, kilometraje=1000).status_code == 201


def test_gasto_de_mantenimiento_asociado_a_un_plan(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    mant, comb = _categoria(client, a, "mantenimiento"), _categoria(client, a, "combustible")
    plan = _plan(client, a, vid)

    ok = _gasto(client, a, vid, mant, 45000, plan_mantenimiento_id=plan, kilometraje=20000)
    assert ok.status_code == 201
    assert ok.json()["plan_mantenimiento_id"] == plan

    # Un plan solo se asocia a gastos de la categoría Mantenimiento
    assert _gasto(client, a, vid, comb, 100, plan_mantenimiento_id=plan, kilometraje=20000).status_code == 422
    # Un plan de otro vehículo no es válido
    otro_vid = nuevo_vehiculo(client, a, alias="Moto")
    assert _gasto(client, a, otro_vid, mant, 100, plan_mantenimiento_id=plan, kilometraje=20000).status_code == 422
    # Un plan inexistente tampoco
    assert _gasto(client, a, vid, mant, 100, plan_mantenimiento_id=str(uuid.uuid4()), kilometraje=20000).status_code == 422


def test_eliminar_un_plan_conserva_sus_gastos(client):
    """Pendiente del módulo Mantenimiento: ON DELETE SET NULL solo anula la asociación."""
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=1000)
    mant = _categoria(client, a, "mantenimiento")
    plan = _plan(client, a, vid)
    gid = _gasto(client, a, vid, mant, 45000, plan_mantenimiento_id=plan, kilometraje=20000).json()["id"]

    assert client.delete(f"/mantenimiento/{plan}", headers=a).status_code == 204

    gasto = client.get(f"/gastos/{gid}", headers=a)
    assert gasto.status_code == 200
    assert gasto.json()["plan_mantenimiento_id"] is None
    assert gasto.json()["kilometraje"] == 20000      # el resto del gasto no se toca
    assert gasto.json()["monto"] == 45000


def test_borrar_el_vehiculo_borra_sus_gastos_en_cascada(client):
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a)
    gid = _gasto(client, a, vid, _categoria(client, a, "combustible"), 100).json()["id"]
    assert client.delete(f"/vehiculos/{vid}", headers=a).status_code == 204
    assert client.get(f"/gastos/{gid}", headers=a).status_code == 404


def test_consultas_agregadas_del_servicio(client):
    """Verifica el SQL de las consultas que usa Indicadores (totales, por categoría, serie mensual, último plan)."""
    a = nuevo_usuario(client)
    vid = nuevo_vehiculo(client, a, km_inicial=0)
    comb, mant = _categoria(client, a, "combustible"), _categoria(client, a, "mantenimiento")
    plan = _plan(client, a, vid)

    _gasto(client, a, vid, comb, 1000, "2024-01-10")
    _gasto(client, a, vid, comb, 500, "2024-01-20")
    _gasto(client, a, vid, comb, 2000, "2024-02-05")
    _gasto(client, a, vid, mant, 3000, "2024-02-10", plan_mantenimiento_id=plan, kilometraje=20000)
    _gasto(client, a, vid, mant, 4000, "2024-03-01", plan_mantenimiento_id=plan, kilometraje=30000)

    vehiculo = uuid.UUID(vid)
    with sesion_de_prueba(client) as db:
        assert service.total_gastado(db, vehiculo) == Decimal("10500")
        assert service.total_gastado(db, vehiculo, date(2024, 2, 1), date(2024, 2, 29)) == Decimal("5000")
        assert service.total_gastado(db, uuid.uuid4()) == Decimal("0")           # sin gastos: 0, no None

        por_categoria = {t.categoria_id: t for t in service.total_por_categoria(db, vehiculo)}
        assert por_categoria[comb].total == Decimal("3500") and por_categoria[comb].cantidad == 3
        assert por_categoria[mant].total == Decimal("7000") and por_categoria[mant].cantidad == 2

        serie = service.serie_mensual(db, vehiculo, comb)
        assert [(t.mes, t.total) for t in serie] == [(date(2024, 1, 1), Decimal("1500")), (date(2024, 2, 1), Decimal("2000"))]

        assert service.ultimo_km_por_plan(db, vehiculo) == {uuid.UUID(plan): Decimal("30000")}
