"""Pruebas de la lógica del servicio de Categorías, con el repositorio reemplazado (sin base de datos)."""
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.categorias import service
from app.core.errors import ReglaDeNegocio


def _categoria(activa=True):
    return SimpleNamespace(id=1, codigo="combustible", nombre="Combustible", tipo_costo="variable", activa=activa)


def test_obtener_activa_devuelve_la_categoria(monkeypatch):
    c = _categoria()
    monkeypatch.setattr(service.repository, "obtener", lambda db, cid: c)
    assert service.obtener_activa(MagicMock(), 1) is c


def test_obtener_activa_inexistente_se_rechaza(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, cid: None)
    with pytest.raises(ReglaDeNegocio):
        service.obtener_activa(MagicMock(), 99)


def test_obtener_activa_inactiva_se_rechaza(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, cid: _categoria(activa=False))
    with pytest.raises(ReglaDeNegocio):
        service.obtener_activa(MagicMock(), 1)


def test_obtener_devuelve_categorias_inactivas_para_el_historial(monkeypatch):
    c = _categoria(activa=False)
    monkeypatch.setattr(service.repository, "obtener", lambda db, cid: c)
    assert service.obtener(MagicMock(), 1) is c


def test_obtener_por_codigo_inexistente_devuelve_none(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener_por_codigo", lambda db, codigo: None)
    assert service.obtener_por_codigo(MagicMock(), "no-existe") is None
