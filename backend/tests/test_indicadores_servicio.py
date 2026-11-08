"""Pruebas de la orquestación de Indicadores, con los servicios de los otros módulos reemplazados (sin base de datos)."""
import uuid
from datetime import date, timedelta
from decimal import Decimal as D
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.errors import NoEncontrado, ReglaDeNegocio
from app.gastos.resumenes import TotalCategoria, TotalMes
from app.indicadores import service

VEHICULO = SimpleNamespace(id=uuid.uuid4(), kilometraje_inicial=D("1000"))
COMBUSTIBLE = SimpleNamespace(id=1, codigo="combustible", nombre="Combustible", tipo_costo="variable")
REPARACION = SimpleNamespace(id=3, codigo="reparacion", nombre="Reparación", tipo_costo="variable")
SEGURO = SimpleNamespace(id=4, codigo="seguro", nombre="Seguro", tipo_costo="fijo")
CATEGORIAS = [COMBUSTIBLE, REPARACION, SEGURO]


@pytest.fixture
def entorno(monkeypatch):
    """Vehículo propio con 10.000 km recorridos y $50.000 gastados. Cada test ajusta lo que necesite."""
    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", lambda db, vid, uid: VEHICULO)
    monkeypatch.setattr(service.gastos_service, "total_gastado", lambda db, vid, desde=None, hasta=None: D("50000"))
    monkeypatch.setattr(service.kilometraje_service, "ultima_lectura", lambda db, vid: SimpleNamespace(kilometraje=D("11000")))
    monkeypatch.setattr(service.categorias_service, "listar", lambda db, solo_activas=True: CATEGORIAS)
    por_codigo = {c.codigo: c for c in CATEGORIAS}
    monkeypatch.setattr(service.categorias_service, "obtener_por_codigo", lambda db, codigo: por_codigo.get(codigo))
    monkeypatch.setattr(service.gastos_service, "total_por_categoria", lambda db, vid, desde=None, hasta=None: [])
    monkeypatch.setattr(service.gastos_service, "serie_mensual", lambda db, vid, cid, desde=None, hasta=None: [])
    monkeypatch.setattr(service.gastos_service, "ultimo_km_por_plan", lambda db, vid: {})
    monkeypatch.setattr(service.mantenimiento_service, "listar_planes_de_vehiculo", lambda db, vid: [])


def _usuario():
    return uuid.uuid4()


# ---- pertenencia ----

@pytest.mark.parametrize(
    "operacion",
    [service.costo_por_km, service.gasto_por_categoria, service.alerta_combustible, service.proximos_mantenimientos,
     service.reparar_o_reemplazar, service.resumen],
)
def test_vehiculo_ajeno_responde_no_encontrado_y_no_consulta_nada_mas(operacion, monkeypatch):
    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    def _no_debe_consultarse(*args, **kwargs):
        raise AssertionError("no debería consultar datos de un vehículo ajeno")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    monkeypatch.setattr(service.gastos_service, "total_gastado", _no_debe_consultarse)
    monkeypatch.setattr(service.kilometraje_service, "ultima_lectura", _no_debe_consultarse)
    with pytest.raises(NoEncontrado):
        operacion(MagicMock(), _usuario(), uuid.uuid4())


# ---- costo por km ----

def test_costo_por_km_combina_gastos_y_kilometraje(entorno):
    r = service.costo_por_km(MagicMock(), _usuario(), VEHICULO.id)
    assert (r.estado, r.costo_por_km, r.km_recorridos, r.total_gastado) == ("ok", D("5.00"), D("10000"), D("50000"))


def test_costo_por_km_sin_lecturas(entorno, monkeypatch):
    monkeypatch.setattr(service.kilometraje_service, "ultima_lectura", lambda db, vid: None)
    r = service.costo_por_km(MagicMock(), _usuario(), VEHICULO.id)
    assert r.estado == "sin_lecturas" and r.costo_por_km is None


# ---- gasto por categoría ----

def test_gasto_por_categoria_ordena_calcula_porcentajes_y_separa_fijo_de_variable(entorno, monkeypatch):
    monkeypatch.setattr(
        service.gastos_service, "total_por_categoria",
        lambda db, vid, desde=None, hasta=None: [
            TotalCategoria(COMBUSTIBLE.id, D("30000"), 3),
            TotalCategoria(SEGURO.id, D("50000"), 5),
            TotalCategoria(REPARACION.id, D("20000"), 1),
        ],
    )
    r = service.gasto_por_categoria(MagicMock(), _usuario(), VEHICULO.id)
    assert [i.codigo for i in r.categorias] == ["seguro", "combustible", "reparacion"]
    assert [i.porcentaje for i in r.categorias] == [D("50.00"), D("30.00"), D("20.00")]
    assert (r.total, r.total_fijo, r.total_variable) == (D("100000"), D("50000"), D("50000"))


def test_gasto_por_categoria_sin_gastos(entorno):
    r = service.gasto_por_categoria(MagicMock(), _usuario(), VEHICULO.id)
    assert r.categorias == () and r.total == D("0") and r.total_fijo == D("0")


def test_gasto_por_categoria_pasa_el_rango_de_fechas(entorno, monkeypatch):
    recibido = []
    monkeypatch.setattr(service.gastos_service, "total_por_categoria",
                        lambda db, vid, desde=None, hasta=None: recibido.append((desde, hasta)) or [])
    service.gasto_por_categoria(MagicMock(), _usuario(), VEHICULO.id, date(2024, 1, 1), date(2024, 3, 31))
    assert recibido == [(date(2024, 1, 1), date(2024, 3, 31))]


def test_gasto_por_categoria_con_rango_invertido_se_rechaza(entorno):
    with pytest.raises(ReglaDeNegocio):
        service.gasto_por_categoria(MagicMock(), _usuario(), VEHICULO.id, date(2024, 3, 1), date(2024, 1, 1))


# ---- alerta de combustible ----

def test_alerta_combustible_con_serie(entorno, monkeypatch):
    serie = [TotalMes(date(2024, m, 1), D(t)) for m, t in [(1, 100), (2, 100), (3, 100), (4, 150)]]
    consultadas = []
    monkeypatch.setattr(service.gastos_service, "serie_mensual",
                        lambda db, vid, cid, desde=None, hasta=None: consultadas.append(cid) or serie)
    r = service.alerta_combustible(MagicMock(), _usuario(), VEHICULO.id)
    assert r.estado == "alerta"
    assert consultadas == [COMBUSTIBLE.id]  # pidió la serie de la categoría 'combustible'


def test_alerta_combustible_sin_la_categoria_en_el_catalogo(entorno, monkeypatch):
    monkeypatch.setattr(service.categorias_service, "obtener_por_codigo", lambda db, codigo: None)
    assert service.alerta_combustible(MagicMock(), _usuario(), VEHICULO.id).estado == "sin_datos"


# ---- próximo mantenimiento ----

def _plan(nombre, intervalo):
    return SimpleNamespace(id=uuid.uuid4(), nombre=nombre, intervalo_km=D(intervalo))


def test_proximos_mantenimientos_lo_mas_urgente_primero(entorno, monkeypatch):
    aceite, frenos, correa = _plan("Aceite", "10000"), _plan("Frenos", "20000"), _plan("Correa", "15000")
    monkeypatch.setattr(service.mantenimiento_service, "listar_planes_de_vehiculo", lambda db, vid: [frenos, aceite, correa])
    monkeypatch.setattr(service.gastos_service, "ultimo_km_por_plan", lambda db, vid: {aceite.id: D("20000"), correa.id: D("10000")})
    monkeypatch.setattr(service.kilometraje_service, "ultima_lectura", lambda db, vid: SimpleNamespace(kilometraje=D("29500")))

    r = service.proximos_mantenimientos(MagicMock(), _usuario(), VEHICULO.id)
    assert [(p.nombre, p.estado, p.km_restantes) for p in r] == [
        ("Correa", "vencido", D("-4500")),     # 10.000 + 15.000 = 25.000 < 29.500
        ("Aceite", "proximo", D("500")),       # 20.000 + 10.000 = 30.000
        ("Frenos", "al_dia", D("10500")),      # sin historial: próximo múltiplo de 20.000 = 40.000
    ]
    assert r[2].base == "multiplos" and r[0].base == "ultimo_mantenimiento"
    assert r[0].ultimo_km == D("10000") and r[2].ultimo_km is None


def test_proximos_mantenimientos_sin_lecturas_van_al_final(entorno, monkeypatch):
    monkeypatch.setattr(service.mantenimiento_service, "listar_planes_de_vehiculo", lambda db, vid: [_plan("Aceite", "10000")])
    monkeypatch.setattr(service.kilometraje_service, "ultima_lectura", lambda db, vid: None)
    r = service.proximos_mantenimientos(MagicMock(), _usuario(), VEHICULO.id)
    assert r[0].estado == "sin_lecturas" and r[0].km_restantes is None


def test_proximos_mantenimientos_sin_planes(entorno):
    assert service.proximos_mantenimientos(MagicMock(), _usuario(), VEHICULO.id) == ()


# ---- reparar o reemplazar ----

def test_reparar_o_reemplazar_usa_ventanas_que_no_se_superponen(entorno, monkeypatch):
    hoy = date(2024, 6, 30)
    desde_12m, desde_6m = hoy - timedelta(days=365), hoy - timedelta(days=182)
    ventanas_por_categoria, ventanas_total = [], []

    def total_por_categoria(db, vid, desde=None, hasta=None):
        ventanas_por_categoria.append((desde, hasta))
        return [TotalCategoria(REPARACION.id, D("1000"), 1)]

    monkeypatch.setattr(service.gastos_service, "total_por_categoria", total_por_categoria)
    monkeypatch.setattr(service.gastos_service, "total_gastado",
                        lambda db, vid, desde=None, hasta=None: ventanas_total.append((desde, hasta)) or D("2000"))

    service.reparar_o_reemplazar(MagicMock(), _usuario(), VEHICULO.id, hoy=hoy)

    assert ventanas_total == [(desde_12m, hoy)]
    assert sorted(ventanas_por_categoria) == sorted([
        (desde_12m, hoy),                              # 12 meses
        (desde_6m, hoy),                               # últimos 6 meses
        (desde_12m, desde_6m - timedelta(days=1)),     # 6 meses previos: termina un día antes de que empiecen los recientes
    ])


def test_reparar_o_reemplazar_distingue_la_categoria_reparacion(entorno, monkeypatch):
    # El vehículo gastó en combustible y reparación: solo cuenta la categoría 'reparacion' como reparaciones.
    monkeypatch.setattr(service.gastos_service, "total_por_categoria",
                        lambda db, vid, desde=None, hasta=None: [TotalCategoria(COMBUSTIBLE.id, D("90000"), 9), TotalCategoria(REPARACION.id, D("10000"), 1)])
    monkeypatch.setattr(service.gastos_service, "total_gastado", lambda db, vid, desde=None, hasta=None: D("100000"))
    monkeypatch.setattr(service.kilometraje_service, "ultima_lectura", lambda db, vid: SimpleNamespace(kilometraje=D("80000")))
    r = service.reparar_o_reemplazar(MagicMock(), _usuario(), VEHICULO.id, hoy=date(2024, 6, 30))
    assert r.estado == "reparar"  # 10% de peso: ninguna señal


def test_reparar_o_reemplazar_sin_la_categoria_reparacion(entorno, monkeypatch):
    por_codigo = {"combustible": COMBUSTIBLE}
    monkeypatch.setattr(service.categorias_service, "obtener_por_codigo", lambda db, codigo: por_codigo.get(codigo))
    r = service.reparar_o_reemplazar(MagicMock(), _usuario(), VEHICULO.id, hoy=date(2024, 6, 30))
    assert r.estado in {"reparar", "evaluar"}  # hay gastos (50.000) pero ninguna reparación


# ---- resumen ----

def test_resumen_incluye_todos_los_indicadores_y_acota_el_gasto_por_categoria_a_12_meses(entorno, monkeypatch):
    hoy = date(2024, 6, 30)
    rangos = []
    monkeypatch.setattr(service.gastos_service, "total_por_categoria",
                        lambda db, vid, desde=None, hasta=None: rangos.append((desde, hasta)) or [])
    r = service.resumen(MagicMock(), _usuario(), VEHICULO.id, hoy=hoy)

    assert r.costo_por_km.estado == "ok"
    assert r.alerta_combustible.estado == "sin_datos"
    assert r.proximos_mantenimientos == ()
    assert r.reparar_o_reemplazar.estado in {"reparar", "evaluar", "considerar_reemplazo", "sin_datos"}
    assert (r.gasto_por_categoria.desde, r.gasto_por_categoria.hasta) == (hoy - timedelta(days=365), hoy)
    assert (hoy - timedelta(days=365), hoy) in rangos
