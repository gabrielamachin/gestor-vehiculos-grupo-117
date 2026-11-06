"""Pruebas de la lógica del servicio de Mantenimiento, con repositorio y módulo Vehículos reemplazados."""
import uuid
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio
from app.mantenimiento import service
from app.mantenimiento.schemas import PlanActualizar, PlanCrear

VEHICULO = SimpleNamespace(id=uuid.uuid4())


def _plan(nombre="Aceite", vehiculo_id=VEHICULO.id):
    return SimpleNamespace(id=uuid.uuid4(), vehiculo_id=vehiculo_id, nombre=nombre, intervalo_km=Decimal("10000"))


@pytest.fixture
def entorno(monkeypatch):
    """Vehículo propio y sin planes. Cada test ajusta lo que necesite."""
    repo = service.repository
    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", lambda db, vid, uid: VEHICULO)
    monkeypatch.setattr(repo, "obtener_por_nombre", lambda db, vid, n: None)
    monkeypatch.setattr(repo, "crear", lambda db, vid, n, km: _plan(n))
    return repo


def _crear(db, nombre="Aceite"):
    return service.crear(db, uuid.uuid4(), PlanCrear(vehiculo_id=VEHICULO.id, nombre=nombre, intervalo_km=Decimal("10000")))


def test_crear_plan_valido_guarda(entorno):
    db = MagicMock()
    assert _crear(db).nombre == "Aceite"
    db.commit.assert_called_once()


def test_crear_con_nombre_repetido_responde_conflicto_y_no_guarda(entorno, monkeypatch):
    monkeypatch.setattr(entorno, "obtener_por_nombre", lambda db, vid, n: _plan(n))
    db = MagicMock()
    with pytest.raises(Conflicto):
        _crear(db)
    db.commit.assert_not_called()


def test_crear_en_vehiculo_ajeno_responde_no_encontrado(monkeypatch):
    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    with pytest.raises(NoEncontrado):
        _crear(MagicMock())


def test_plan_de_vehiculo_ajeno_se_ve_como_inexistente(monkeypatch):
    """El mensaje es el mismo que si el plan no existiera (no revela que es de otro usuario)."""
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: _plan())

    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    with pytest.raises(NoEncontrado, match="Plan de mantenimiento no encontrado"):
        service.actualizar(MagicMock(), uuid.uuid4(), uuid.uuid4(), PlanActualizar(nombre="X", intervalo_km=Decimal("5000")))


def test_actualizar_al_nombre_de_otro_plan_responde_conflicto(entorno, monkeypatch):
    propio, otro = _plan("Aceite"), _plan("Filtros")
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: propio)
    monkeypatch.setattr(entorno, "obtener_por_nombre", lambda db, vid, n: otro)
    with pytest.raises(Conflicto):
        service.actualizar(MagicMock(), propio.id, uuid.uuid4(), PlanActualizar(nombre="Filtros", intervalo_km=Decimal("5000")))


def test_actualizar_con_su_propio_nombre_no_es_conflicto(entorno, monkeypatch):
    propio = _plan("Aceite")
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: propio)
    monkeypatch.setattr(entorno, "obtener_por_nombre", lambda db, vid, n: propio)
    monkeypatch.setattr(entorno, "actualizar", lambda db, p, n, km: p)
    db = MagicMock()
    service.actualizar(db, propio.id, uuid.uuid4(), PlanActualizar(nombre="Aceite", intervalo_km=Decimal("8000")))
    db.commit.assert_called_once()


def test_eliminar_ajeno_no_borra(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: None)
    borrar = MagicMock()
    monkeypatch.setattr(service.repository, "eliminar", borrar)
    with pytest.raises(NoEncontrado):
        service.eliminar(MagicMock(), uuid.uuid4(), uuid.uuid4())
    borrar.assert_not_called()


# ---- Interfaz para Gastos ----

def test_obtener_plan_del_vehiculo_devuelve_el_plan(monkeypatch):
    p = _plan()
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: p)
    assert service.obtener_plan_del_vehiculo(MagicMock(), p.id, VEHICULO.id) is p


def test_obtener_plan_del_vehiculo_inexistente_se_rechaza(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: None)
    with pytest.raises(ReglaDeNegocio):
        service.obtener_plan_del_vehiculo(MagicMock(), uuid.uuid4(), VEHICULO.id)


def test_obtener_plan_del_vehiculo_de_otro_vehiculo_se_rechaza(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, pid: _plan(vehiculo_id=uuid.uuid4()))
    with pytest.raises(ReglaDeNegocio):
        service.obtener_plan_del_vehiculo(MagicMock(), uuid.uuid4(), VEHICULO.id)
