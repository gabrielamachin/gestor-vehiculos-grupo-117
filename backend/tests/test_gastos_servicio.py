"""Pruebas de la lógica del servicio de Gastos, con repositorio y otros módulos reemplazados (sin base de datos)."""
import uuid
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.errors import NoEncontrado, ReglaDeNegocio
from app.gastos import service
from app.gastos.schemas import GastoActualizar, GastoCrear

VEHICULO = SimpleNamespace(id=uuid.uuid4(), kilometraje_inicial=Decimal("1000"))
FECHA = date(2024, 6, 15)


def _categoria(codigo="combustible", activa=True, id=1):
    return SimpleNamespace(id=id, codigo=codigo, activa=activa)


def _gasto(categoria_id=1):
    return SimpleNamespace(id=uuid.uuid4(), vehiculo_id=VEHICULO.id, categoria_id=categoria_id)


@pytest.fixture
def entorno(monkeypatch):
    """Vehículo propio, categoría activa 'combustible' y plan válido. Cada test ajusta lo que necesite."""
    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", lambda db, vid, uid: VEHICULO)
    monkeypatch.setattr(service.categorias_service, "obtener_activa", lambda db, cid: _categoria(id=cid))
    monkeypatch.setattr(service.categorias_service, "obtener", lambda db, cid: _categoria(id=cid))
    monkeypatch.setattr(service.mantenimiento_service, "obtener_plan_del_vehiculo", lambda db, pid, vid: SimpleNamespace(id=pid))
    monkeypatch.setattr(service.repository, "crear", lambda db, vid, campos: SimpleNamespace(id=uuid.uuid4(), **campos))
    return service.repository


def _datos(**cambios):
    base = dict(vehiculo_id=VEHICULO.id, categoria_id=1, monto=Decimal("5000"), fecha=FECHA)
    return GastoCrear(**{**base, **cambios})


def test_crear_gasto_valido_guarda(entorno):
    db = MagicMock()
    service.crear(db, uuid.uuid4(), _datos())
    db.commit.assert_called_once()


def test_crear_con_categoria_inactiva_o_inexistente_se_rechaza(entorno, monkeypatch):
    def _rechazar(db, cid):
        raise ReglaDeNegocio("La categoría no existe o está inactiva")

    monkeypatch.setattr(service.categorias_service, "obtener_activa", _rechazar)
    db = MagicMock()
    with pytest.raises(ReglaDeNegocio):
        service.crear(db, uuid.uuid4(), _datos())
    db.commit.assert_not_called()


def test_crear_en_vehiculo_ajeno_responde_no_encontrado(monkeypatch):
    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    with pytest.raises(NoEncontrado):
        service.crear(MagicMock(), uuid.uuid4(), _datos())


def test_kilometraje_menor_al_inicial_se_rechaza(entorno):
    with pytest.raises(ReglaDeNegocio, match="inicial"):
        service.crear(MagicMock(), uuid.uuid4(), _datos(kilometraje=Decimal("999")))


def test_kilometraje_igual_al_inicial_se_acepta(entorno):
    service.crear(MagicMock(), uuid.uuid4(), _datos(kilometraje=Decimal("1000")))


def test_plan_solo_se_acepta_en_categoria_mantenimiento(entorno):
    # La categoría del entorno es 'combustible'
    with pytest.raises(ReglaDeNegocio, match="Mantenimiento"):
        service.crear(MagicMock(), uuid.uuid4(), _datos(plan_mantenimiento_id=uuid.uuid4(), kilometraje=Decimal("5000")))


def test_plan_en_categoria_mantenimiento_valida_el_plan(entorno, monkeypatch):
    monkeypatch.setattr(service.categorias_service, "obtener_activa", lambda db, cid: _categoria("mantenimiento", id=cid))
    consultados = []

    def _plan(db, pid, vid):
        consultados.append((pid, vid))
        return SimpleNamespace(id=pid)

    monkeypatch.setattr(service.mantenimiento_service, "obtener_plan_del_vehiculo", _plan)
    plan_id = uuid.uuid4()
    service.crear(MagicMock(), uuid.uuid4(), _datos(plan_mantenimiento_id=plan_id, kilometraje=Decimal("5000")))
    assert consultados == [(plan_id, VEHICULO.id)]


def test_plan_ajeno_al_vehiculo_se_rechaza(entorno, monkeypatch):
    monkeypatch.setattr(service.categorias_service, "obtener_activa", lambda db, cid: _categoria("mantenimiento", id=cid))

    def _rechazar(db, pid, vid):
        raise ReglaDeNegocio("El plan de mantenimiento no existe o no pertenece al vehículo")

    monkeypatch.setattr(service.mantenimiento_service, "obtener_plan_del_vehiculo", _rechazar)
    db = MagicMock()
    with pytest.raises(ReglaDeNegocio):
        service.crear(db, uuid.uuid4(), _datos(plan_mantenimiento_id=uuid.uuid4(), kilometraje=Decimal("5000")))
    db.commit.assert_not_called()


# ---- actualizar ----

def test_actualizar_conserva_categoria_inactiva(entorno, monkeypatch):
    """Editar un gasto viejo no debe fallar porque su categoría se desactivó después."""
    gasto = _gasto(categoria_id=7)
    monkeypatch.setattr(service.repository, "obtener", lambda db, gid: gasto)
    monkeypatch.setattr(service.categorias_service, "obtener", lambda db, cid: _categoria(activa=False, id=cid))

    def _no_debe_pedir_activa(db, cid):
        raise AssertionError("no debería exigir categoría activa si no cambia")

    monkeypatch.setattr(service.categorias_service, "obtener_activa", _no_debe_pedir_activa)
    monkeypatch.setattr(service.repository, "actualizar", lambda db, g, campos: g)

    db = MagicMock()
    service.actualizar(db, gasto.id, uuid.uuid4(), GastoActualizar(categoria_id=7, monto=Decimal("100"), fecha=FECHA))
    db.commit.assert_called_once()


def test_actualizar_a_otra_categoria_exige_que_este_activa(entorno, monkeypatch):
    gasto = _gasto(categoria_id=7)
    monkeypatch.setattr(service.repository, "obtener", lambda db, gid: gasto)

    def _rechazar(db, cid):
        raise ReglaDeNegocio("La categoría no existe o está inactiva")

    monkeypatch.setattr(service.categorias_service, "obtener_activa", _rechazar)
    with pytest.raises(ReglaDeNegocio):
        service.actualizar(MagicMock(), gasto.id, uuid.uuid4(), GastoActualizar(categoria_id=8, monto=Decimal("100"), fecha=FECHA))


def test_gasto_de_vehiculo_ajeno_se_ve_como_inexistente(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, gid: _gasto())

    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    with pytest.raises(NoEncontrado, match="Gasto no encontrado"):
        service.actualizar(MagicMock(), uuid.uuid4(), uuid.uuid4(), GastoActualizar(categoria_id=1, monto=Decimal("1"), fecha=FECHA))


def test_eliminar_ajeno_no_borra(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, gid: None)
    borrar = MagicMock()
    monkeypatch.setattr(service.repository, "eliminar", borrar)
    with pytest.raises(NoEncontrado):
        service.eliminar(MagicMock(), uuid.uuid4(), uuid.uuid4())
    borrar.assert_not_called()


# ---- listar ----

def test_listar_con_rango_invertido_se_rechaza(entorno):
    with pytest.raises(ReglaDeNegocio, match="desde"):
        service.listar(MagicMock(), uuid.uuid4(), VEHICULO.id, desde=date(2024, 2, 1), hasta=date(2024, 1, 1))
