"""Acceso a datos de la tabla `gastos`, incluidas las consultas agregadas. Sin reglas de negocio ni commits."""
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, DateTime, Select, cast, func, select
from sqlalchemy.orm import Session

from app.gastos.models import Gasto
from app.gastos.resumenes import TotalCategoria, TotalMes


def _acotar_fechas(consulta: Select, desde: date | None, hasta: date | None) -> Select:
    if desde is not None:
        consulta = consulta.where(Gasto.fecha >= desde)
    if hasta is not None:
        consulta = consulta.where(Gasto.fecha <= hasta)
    return consulta


def listar(
    db: Session,
    vehiculo_id: uuid.UUID,
    desde: date | None = None,
    hasta: date | None = None,
    categoria_id: int | None = None,
) -> list[Gasto]:
    consulta = _acotar_fechas(select(Gasto).where(Gasto.vehiculo_id == vehiculo_id), desde, hasta)
    if categoria_id is not None:
        consulta = consulta.where(Gasto.categoria_id == categoria_id)
    return list(db.scalars(consulta.order_by(Gasto.fecha.desc(), Gasto.id)))


def obtener(db: Session, gasto_id: uuid.UUID) -> Gasto | None:
    return db.get(Gasto, gasto_id)


def crear(db: Session, vehiculo_id: uuid.UUID, campos: dict) -> Gasto:
    gasto = Gasto(vehiculo_id=vehiculo_id, **campos)
    db.add(gasto)
    db.flush()  # obtiene el id generado por la base
    return gasto


def actualizar(db: Session, gasto: Gasto, campos: dict) -> Gasto:
    for nombre, valor in campos.items():
        setattr(gasto, nombre, valor)
    db.flush()
    return gasto


def eliminar(db: Session, gasto: Gasto) -> None:
    db.delete(gasto)
    db.flush()


# ---------- Consultas agregadas (las usa Indicadores a través del servicio) ----------

def total_gastado(db: Session, vehiculo_id: uuid.UUID, desde: date | None = None, hasta: date | None = None) -> Decimal:
    consulta = select(func.coalesce(func.sum(Gasto.monto), 0)).where(Gasto.vehiculo_id == vehiculo_id)
    return Decimal(db.scalar(_acotar_fechas(consulta, desde, hasta)))


def total_por_categoria(
    db: Session, vehiculo_id: uuid.UUID, desde: date | None = None, hasta: date | None = None
) -> list[TotalCategoria]:
    consulta = (
        select(Gasto.categoria_id, func.sum(Gasto.monto), func.count(Gasto.id))
        .where(Gasto.vehiculo_id == vehiculo_id)
        .group_by(Gasto.categoria_id)
    )
    filas = db.execute(_acotar_fechas(consulta, desde, hasta))
    return [TotalCategoria(categoria_id, Decimal(total), cantidad) for categoria_id, total, cantidad in filas]


def serie_mensual(
    db: Session,
    vehiculo_id: uuid.UUID,
    categoria_id: int,
    desde: date | None = None,
    hasta: date | None = None,
) -> list[TotalMes]:
    """Total gastado por mes en una categoría, de más antiguo a más reciente (solo meses con gastos)."""
    # Se trunca sobre un timestamp sin zona horaria para que el resultado no dependa de la zona de la sesión.
    mes = cast(func.date_trunc("month", cast(Gasto.fecha, DateTime)), Date).label("mes")
    consulta = (
        select(mes, func.sum(Gasto.monto))
        .where(Gasto.vehiculo_id == vehiculo_id, Gasto.categoria_id == categoria_id)
        .group_by(mes)
        .order_by(mes)
    )
    return [TotalMes(m, Decimal(total)) for m, total in db.execute(_acotar_fechas(consulta, desde, hasta))]


def ultimo_km_por_plan(db: Session, vehiculo_id: uuid.UUID) -> dict[uuid.UUID, Decimal]:
    """Mayor kilometraje registrado en gastos asociados a cada plan = km del último mantenimiento realizado."""
    consulta = (
        select(Gasto.plan_mantenimiento_id, func.max(Gasto.kilometraje))
        .where(Gasto.vehiculo_id == vehiculo_id, Gasto.plan_mantenimiento_id.is_not(None))
        .group_by(Gasto.plan_mantenimiento_id)
    )
    return {plan_id: Decimal(km) for plan_id, km in db.execute(consulta)}
