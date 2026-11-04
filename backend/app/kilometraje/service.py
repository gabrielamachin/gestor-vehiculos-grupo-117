"""Lógica de negocio del módulo Kilometraje. No conoce HTTP: lanza errores de dominio.

Regla central: el odómetro nunca retrocede. Es una regla entre filas (compara contra otras
lecturas y contra el kilometraje inicial del vehículo), por eso un CHECK no puede expresarla:
este servicio es la única capa que la valida.

`ultima_lectura` es la interfaz que usa el módulo Indicadores.
"""
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio
from app.kilometraje import repository
from app.kilometraje.models import LecturaKilometraje as Lectura
from app.kilometraje.schemas import LecturaActualizar, LecturaCrear
from app.vehiculos import service as vehiculos_service
from app.vehiculos.models import Vehiculo

_MENSAJE_FECHA = "Ya existe una lectura para ese vehículo en esa fecha"


def _fmt_fecha(fecha: date) -> str:
    return fecha.strftime("%d/%m/%Y")


def _fmt_km(km: Decimal) -> str:
    return f"{km:,.2f}"


def _es_fecha_duplicada(error: IntegrityError) -> bool:
    """Distingue el UNIQUE (vehiculo_id, fecha) de otras violaciones de integridad (p. ej. una FK)."""
    diag = getattr(error.orig, "diag", None)
    return getattr(diag, "constraint_name", None) == "uq_lecturas_vehiculo_fecha"


def _validar_coherencia(
    db: Session, vehiculo: Vehiculo, fecha: date, kilometraje: Decimal, excluir_id: uuid.UUID | None = None
) -> None:
    """El kilometraje debe ser >= al inicial y respetar el orden cronológico de las demás lecturas."""
    if kilometraje < vehiculo.kilometraje_inicial:
        raise ReglaDeNegocio(
            f"El kilometraje no puede ser menor al inicial del vehículo ({_fmt_km(vehiculo.kilometraje_inicial)} km)"
        )

    anterior = repository.anterior_a(db, vehiculo.id, fecha, excluir_id)
    if anterior is not None and kilometraje < anterior.kilometraje:
        raise ReglaDeNegocio(
            f"El kilometraje no puede ser menor al de la lectura del {_fmt_fecha(anterior.fecha)} "
            f"({_fmt_km(anterior.kilometraje)} km)"
        )

    posterior = repository.posterior_a(db, vehiculo.id, fecha, excluir_id)
    if posterior is not None and kilometraje > posterior.kilometraje:
        raise ReglaDeNegocio(
            f"El kilometraje no puede ser mayor al de la lectura posterior del {_fmt_fecha(posterior.fecha)} "
            f"({_fmt_km(posterior.kilometraje)} km)"
        )


def _obtener_lectura_de_usuario(db: Session, lectura_id: uuid.UUID, usuario_id: uuid.UUID) -> tuple[Lectura, Vehiculo]:
    """Una lectura pertenece al usuario si su vehículo le pertenece (se verifica vía el módulo Vehículos)."""
    lectura = repository.obtener(db, lectura_id)
    if lectura is None:
        raise NoEncontrado("Lectura no encontrada")
    try:
        vehiculo = vehiculos_service.obtener_de_usuario(db, lectura.vehiculo_id, usuario_id)
    except NoEncontrado:
        # Mismo mensaje que si no existiera: no se revela que la lectura es de otro usuario.
        raise NoEncontrado("Lectura no encontrada") from None
    return lectura, vehiculo


def listar(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> list[Lectura]:
    vehiculos_service.obtener_de_usuario(db, vehiculo_id, usuario_id)
    return repository.listar_por_vehiculo(db, vehiculo_id)


def obtener(db: Session, lectura_id: uuid.UUID, usuario_id: uuid.UUID) -> Lectura:
    return _obtener_lectura_de_usuario(db, lectura_id, usuario_id)[0]


def ultima_lectura(db: Session, vehiculo_id: uuid.UUID) -> Lectura | None:
    """Kilometraje actual de un vehículo: su última lectura, o None si todavía no tiene.

    Interfaz para otros módulos (Indicadores). NO verifica pertenencia: quien la llama debe
    haberla verificado antes con vehiculos.service.obtener_de_usuario.
    """
    return repository.ultima(db, vehiculo_id)


def ultima(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> Lectura | None:
    """Versión para la API: verifica pertenencia antes de consultar."""
    vehiculos_service.obtener_de_usuario(db, vehiculo_id, usuario_id)
    return ultima_lectura(db, vehiculo_id)


def crear(db: Session, usuario_id: uuid.UUID, datos: LecturaCrear) -> Lectura:
    vehiculo = vehiculos_service.obtener_de_usuario(db, datos.vehiculo_id, usuario_id)

    if repository.obtener_por_fecha(db, vehiculo.id, datos.fecha) is not None:
        raise Conflicto(_MENSAJE_FECHA)
    _validar_coherencia(db, vehiculo, datos.fecha, datos.kilometraje)

    try:
        lectura = repository.crear(db, vehiculo.id, datos.fecha, datos.kilometraje)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if _es_fecha_duplicada(error):  # dos solicitudes simultáneas para la misma fecha
            raise Conflicto(_MENSAJE_FECHA) from error
        raise
    return lectura


def actualizar(db: Session, lectura_id: uuid.UUID, usuario_id: uuid.UUID, datos: LecturaActualizar) -> Lectura:
    lectura, vehiculo = _obtener_lectura_de_usuario(db, lectura_id, usuario_id)

    existente = repository.obtener_por_fecha(db, vehiculo.id, datos.fecha)
    if existente is not None and existente.id != lectura.id:
        raise Conflicto(_MENSAJE_FECHA)
    _validar_coherencia(db, vehiculo, datos.fecha, datos.kilometraje, excluir_id=lectura.id)

    try:
        repository.actualizar(db, lectura, datos.fecha, datos.kilometraje)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if _es_fecha_duplicada(error):
            raise Conflicto(_MENSAJE_FECHA) from error
        raise
    return lectura


def eliminar(db: Session, lectura_id: uuid.UUID, usuario_id: uuid.UUID) -> None:
    """Borrar una lectura nunca rompe la coherencia de las demás."""
    lectura, _ = _obtener_lectura_de_usuario(db, lectura_id, usuario_id)
    repository.eliminar(db, lectura)
    db.commit()
