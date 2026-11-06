"""Pruebas de la lógica del servicio de Vehículos, con el repositorio reemplazado (sin base de datos)."""
import uuid
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.errors import Conflicto, NoEncontrado
from app.vehiculos import service
from app.vehiculos.schemas import VehiculoActualizar, VehiculoCrear


def _vehiculo(alias="Auto"):
    return SimpleNamespace(id=uuid.uuid4(), alias=alias, kilometraje_inicial=Decimal("1000"))


def test_obtener_de_usuario_inexistente_o_ajeno_responde_no_encontrado(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener_de_usuario", lambda db, vid, uid: None)
    with pytest.raises(NoEncontrado):
        service.obtener_de_usuario(MagicMock(), uuid.uuid4(), uuid.uuid4())


def test_obtener_de_usuario_devuelve_el_vehiculo(monkeypatch):
    v = _vehiculo()
    monkeypatch.setattr(service.repository, "obtener_de_usuario", lambda db, vid, uid: v)
    assert service.obtener_de_usuario(MagicMock(), v.id, uuid.uuid4()) is v


def test_crear_con_alias_repetido_responde_conflicto_y_no_guarda(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener_por_alias", lambda db, uid, alias: _vehiculo())
    db = MagicMock()
    with pytest.raises(Conflicto):
        service.crear(db, uuid.uuid4(), VehiculoCrear(alias="Auto", kilometraje_inicial=Decimal("0")))
    db.commit.assert_not_called()


def test_actualizar_a_alias_de_otro_vehiculo_responde_conflicto(monkeypatch):
    propio = _vehiculo("Auto")
    otro = _vehiculo("Moto")
    monkeypatch.setattr(service.repository, "obtener_de_usuario", lambda db, vid, uid: propio)
    monkeypatch.setattr(service.repository, "obtener_por_alias", lambda db, uid, alias: otro)
    with pytest.raises(Conflicto):
        service.actualizar(MagicMock(), propio.id, uuid.uuid4(), VehiculoActualizar(alias="Moto"))


def test_actualizar_con_su_propio_alias_no_es_conflicto(monkeypatch):
    propio = _vehiculo("Auto")
    monkeypatch.setattr(service.repository, "obtener_de_usuario", lambda db, vid, uid: propio)
    monkeypatch.setattr(service.repository, "obtener_por_alias", lambda db, uid, alias: propio)
    monkeypatch.setattr(service.repository, "actualizar_alias", lambda db, v, alias: v)
    db = MagicMock()
    assert service.actualizar(db, propio.id, uuid.uuid4(), VehiculoActualizar(alias="Auto")) is propio
    db.commit.assert_called_once()


def test_eliminar_ajeno_responde_no_encontrado_y_no_borra(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener_de_usuario", lambda db, vid, uid: None)
    borrar = MagicMock()
    monkeypatch.setattr(service.repository, "eliminar", borrar)
    with pytest.raises(NoEncontrado):
        service.eliminar(MagicMock(), uuid.uuid4(), uuid.uuid4())
    borrar.assert_not_called()
