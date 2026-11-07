"""Lógica de negocio del módulo Gastos. No conoce HTTP: lanza errores de dominio.

Interfaz para Indicadores (al final del archivo): `total_gastado`, `total_por_categoria`,
`serie_mensual` y `ultimo_km_por_plan`. No verifican pertenencia: quien las llama ya verificó
el vehículo con vehiculos.service.obtener_de_usuario.
"""
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.categorias import service as categorias_service
from app.categorias.models import Categoria
from app.core.errors import NoEncontrado, ReglaDeNegocio
from app.gastos import repository
from app.gastos.models import Gasto
from app.gastos.resumenes import TotalCategoria, TotalMes
from app.gastos.schemas import GastoActualizar, GastoCrear
from app.mantenimiento import service as mantenimiento_service
from app.vehiculos import service as vehiculos_service
from app.vehiculos.models import Vehiculo

# Acoplamiento consciente: solo los gastos de esta categoría pueden cumplir un plan de mantenimiento.
CODIGO_CATEGORIA_MANTENIMIENTO = "mantenimiento"


def _validar_rango(desde: date | None, hasta: date | None) -> None:
    if desde is not None and hasta is not None and desde > hasta:
        raise ReglaDeNegocio("La fecha 'desde' no puede ser posterior a la fecha 'hasta'")


def _obtener_gasto_de_usuario(db: Session, gasto_id: uuid.UUID, usuario_id: uuid.UUID) -> tuple[Gasto, Vehiculo]:
    """Un gasto pertenece al usuario si su vehículo le pertenece (se verifica vía el módulo Vehículos)."""
    gasto = repository.obtener(db, gasto_id)
    if gasto is None:
        raise NoEncontrado("Gasto no encontrado")
    try:
        vehiculo = vehiculos_service.obtener_de_usuario(db, gasto.vehiculo_id, usuario_id)
    except NoEncontrado:
        # Mismo mensaje que si no existiera: no se revela que el gasto es de otro usuario.
        raise NoEncontrado("Gasto no encontrado") from None
    return gasto, vehiculo


def _validar_kilometraje_y_plan(
    db: Session,
    vehiculo: Vehiculo,
    categoria: Categoria,
    plan_id: uuid.UUID | None,
    kilometraje: Decimal | None,
) -> None:
    if kilometraje is not None and kilometraje < vehiculo.kilometraje_inicial:
        raise ReglaDeNegocio(
            f"El kilometraje no puede ser menor al inicial del vehículo ({vehiculo.kilometraje_inicial:,.2f} km)"
        )
    if plan_id is not None:
        if categoria.codigo != CODIGO_CATEGORIA_MANTENIMIENTO:
            raise ReglaDeNegocio("Solo los gastos de la categoría Mantenimiento pueden asociarse a un plan de mantenimiento")
        mantenimiento_service.obtener_plan_del_vehiculo(db, plan_id, vehiculo.id)


def listar(
    db: Session,
    usuario_id: uuid.UUID,
    vehiculo_id: uuid.UUID,
    desde: date | None = None,
    hasta: date | None = None,
    categoria_id: int | None = None,
) -> list[Gasto]:
    vehiculos_service.obtener_de_usuario(db, vehiculo_id, usuario_id)
    _validar_rango(desde, hasta)
    return repository.listar(db, vehiculo_id, desde, hasta, categoria_id)


def obtener(db: Session, gasto_id: uuid.UUID, usuario_id: uuid.UUID) -> Gasto:
    return _obtener_gasto_de_usuario(db, gasto_id, usuario_id)[0]


def crear(db: Session, usuario_id: uuid.UUID, datos: GastoCrear) -> Gasto:
    vehiculo = vehiculos_service.obtener_de_usuario(db, datos.vehiculo_id, usuario_id)
    categoria = categorias_service.obtener_activa(db, datos.categoria_id)
    _validar_kilometraje_y_plan(db, vehiculo, categoria, datos.plan_mantenimiento_id, datos.kilometraje)

    gasto = repository.crear(db, vehiculo.id, datos.model_dump(exclude={"vehiculo_id"}))
    db.commit()
    return gasto


def actualizar(db: Session, gasto_id: uuid.UUID, usuario_id: uuid.UUID, datos: GastoActualizar) -> Gasto:
    gasto, vehiculo = _obtener_gasto_de_usuario(db, gasto_id, usuario_id)

    if datos.categoria_id == gasto.categoria_id:
        # Conserva la categoría: se permite aunque se haya desactivado después de cargar el gasto.
        categoria = categorias_service.obtener(db, datos.categoria_id)
    else:
        categoria = categorias_service.obtener_activa(db, datos.categoria_id)
    _validar_kilometraje_y_plan(db, vehiculo, categoria, datos.plan_mantenimiento_id, datos.kilometraje)

    repository.actualizar(db, gasto, datos.model_dump())
    db.commit()
    return gasto


def eliminar(db: Session, gasto_id: uuid.UUID, usuario_id: uuid.UUID) -> None:
    gasto, _ = _obtener_gasto_de_usuario(db, gasto_id, usuario_id)
    repository.eliminar(db, gasto)
    db.commit()


# ---------- Interfaz para Indicadores (no verifican pertenencia del vehículo) ----------

def total_gastado(db: Session, vehiculo_id: uuid.UUID, desde: date | None = None, hasta: date | None = None) -> Decimal:
    """Suma de montos del vehículo (0 si no hay gastos)."""
    return repository.total_gastado(db, vehiculo_id, desde, hasta)


def total_por_categoria(
    db: Session, vehiculo_id: uuid.UUID, desde: date | None = None, hasta: date | None = None
) -> list[TotalCategoria]:
    """Total y cantidad de gastos por categoría (solo categorías con gastos)."""
    return repository.total_por_categoria(db, vehiculo_id, desde, hasta)


def serie_mensual(
    db: Session, vehiculo_id: uuid.UUID, categoria_id: int, desde: date | None = None, hasta: date | None = None
) -> list[TotalMes]:
    """Total por mes de una categoría, de más antiguo a más reciente (solo meses con gastos)."""
    return repository.serie_mensual(db, vehiculo_id, categoria_id, desde, hasta)


def ultimo_km_por_plan(db: Session, vehiculo_id: uuid.UUID) -> dict[uuid.UUID, Decimal]:
    """Para cada plan con mantenimientos registrados: kilometraje del último realizado."""
    return repository.ultimo_km_por_plan(db, vehiculo_id)
