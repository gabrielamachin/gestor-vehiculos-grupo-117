"""Pruebas de la lógica del servicio de Kilometraje, con repositorio y módulo Vehículos reemplazados."""
import uuid
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio
from app.kilometraje import service
from app.kilometraje.schemas import LecturaActualizar, LecturaCrear

VEHICULO = SimpleNamespace(id=uuid.uuid4(), kilometraje_inicial=Decimal("1000"))
FECHA = date(2024, 6, 15)


def _lectura(fecha, km, vehiculo_id=VEHICULO.id):
    return SimpleNamespace(id=uuid.uuid4(), vehiculo_id=vehiculo_id, fecha=fecha, kilometraje=Decimal(km))


@pytest.fixture
def entorno(monkeypatch):
    """Vehículo propio, sin lecturas previas. Cada test ajusta lo que necesite."""
    repo = service.repository
    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", lambda db, vid, uid: VEHICULO)
    monkeypatch.setattr(repo, "obtener_por_fecha", lambda db, vid, f: None)
    monkeypatch.setattr(repo, "anterior_a", lambda db, vid, f, ex=None: None)
    monkeypatch.setattr(repo, "posterior_a", lambda db, vid, f, ex=None: None)
    monkeypatch.setattr(repo, "crear", lambda db, vid, f, km: _lectura(f, km))
    return repo


def _crear(db, km, fecha=FECHA):
    return service.crear(db, uuid.uuid4(), LecturaCrear(vehiculo_id=VEHICULO.id, fecha=fecha, kilometraje=Decimal(km)))


def test_crear_lectura_valida_guarda(entorno):
    db = MagicMock()
    assert _crear(db, "1500").kilometraje == Decimal("1500")
    db.commit.assert_called_once()


def test_menor_al_kilometraje_inicial_se_rechaza(entorno):
    db = MagicMock()
    with pytest.raises(ReglaDeNegocio, match="inicial"):
        _crear(db, "999.99")
    db.commit.assert_not_called()


def test_igual_al_kilometraje_inicial_se_acepta(entorno):
    assert _crear(MagicMock(), "1000").kilometraje == Decimal("1000")


def test_menor_que_la_lectura_anterior_se_rechaza(entorno, monkeypatch):
    monkeypatch.setattr(entorno, "anterior_a", lambda db, vid, f, ex=None: _lectura(date(2024, 6, 1), "2000"))
    with pytest.raises(ReglaDeNegocio, match="anterior|menor"):
        _crear(MagicMock(), "1999")


def test_igual_a_la_lectura_anterior_se_acepta(entorno, monkeypatch):
    # El auto pudo no moverse entre dos lecturas
    monkeypatch.setattr(entorno, "anterior_a", lambda db, vid, f, ex=None: _lectura(date(2024, 6, 1), "2000"))
    assert _crear(MagicMock(), "2000").kilometraje == Decimal("2000")


def test_mayor_que_la_lectura_posterior_se_rechaza(entorno, monkeypatch):
    monkeypatch.setattr(entorno, "posterior_a", lambda db, vid, f, ex=None: _lectura(date(2024, 7, 1), "3000"))
    with pytest.raises(ReglaDeNegocio, match="posterior"):
        _crear(MagicMock(), "3001")


def test_fecha_ya_cargada_responde_conflicto_y_no_guarda(entorno, monkeypatch):
    monkeypatch.setattr(entorno, "obtener_por_fecha", lambda db, vid, f: _lectura(f, "1500"))
    db = MagicMock()
    with pytest.raises(Conflicto):
        _crear(db, "1600")
    db.commit.assert_not_called()


def test_vehiculo_ajeno_responde_no_encontrado(monkeypatch):
    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    with pytest.raises(NoEncontrado):
        _crear(MagicMock(), "1500")


def test_lectura_de_vehiculo_ajeno_se_ve_como_inexistente(monkeypatch):
    """Al editar una lectura ajena el mensaje es el mismo que si no existiera (no revela su existencia)."""
    monkeypatch.setattr(service.repository, "obtener", lambda db, lid: _lectura(FECHA, "1500"))

    def _no_es_mio(db, vid, uid):
        raise NoEncontrado("Vehículo no encontrado")

    monkeypatch.setattr(service.vehiculos_service, "obtener_de_usuario", _no_es_mio)
    with pytest.raises(NoEncontrado, match="Lectura no encontrada"):
        service.actualizar(MagicMock(), uuid.uuid4(), uuid.uuid4(), LecturaActualizar(fecha=FECHA, kilometraje=Decimal("1600")))


def test_actualizar_excluye_la_propia_lectura_al_validar(entorno, monkeypatch):
    """Al editar, la lectura no debe compararse contra su propio valor anterior."""
    propia = _lectura(FECHA, "1500")
    monkeypatch.setattr(service.repository, "obtener", lambda db, lid: propia)
    excluidos = []
    monkeypatch.setattr(entorno, "anterior_a", lambda db, vid, f, ex=None: excluidos.append(ex))
    monkeypatch.setattr(entorno, "actualizar", lambda db, l, f, km: l)

    service.actualizar(MagicMock(), propia.id, uuid.uuid4(), LecturaActualizar(fecha=FECHA, kilometraje=Decimal("1600")))
    assert excluidos == [propia.id]


def test_eliminar_ajena_no_borra(monkeypatch):
    monkeypatch.setattr(service.repository, "obtener", lambda db, lid: None)
    borrar = MagicMock()
    monkeypatch.setattr(service.repository, "eliminar", borrar)
    with pytest.raises(NoEncontrado):
        service.eliminar(MagicMock(), uuid.uuid4(), uuid.uuid4())
    borrar.assert_not_called()
