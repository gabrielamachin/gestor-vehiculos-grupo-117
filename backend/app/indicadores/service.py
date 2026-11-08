"""Orquestación de los indicadores. No conoce HTTP: lanza errores de dominio.

Este módulo no tiene tablas propias ni escribe datos: obtiene datos de otros módulos a través
de sus SERVICIOS (nunca de sus repositorios ni modelos) y aplica las fórmulas de calculos.py.
La pertenencia del vehículo se verifica una sola vez, en Vehículos, al comienzo de cada operación.
"""
import uuid
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.categorias import service as categorias_service
from app.core.errors import ReglaDeNegocio
from app.gastos import service as gastos_service
from app.indicadores import calculos
from app.indicadores.resultados import (
    AlertaCombustible,
    CostoPorKm,
    GastoPorCategoria,
    ItemCategoria,
    OrientacionReparacion,
    ProximoMantenimiento,
    ResumenIndicadores,
)
from app.kilometraje import service as kilometraje_service
from app.mantenimiento import service as mantenimiento_service
from app.vehiculos import service as vehiculos_service
from app.vehiculos.models import Vehiculo

# Acoplamiento consciente con los códigos del catálogo (ver esquema-db.md, sección 5.4).
CODIGO_COMBUSTIBLE = "combustible"
CODIGO_REPARACION = "reparacion"

DIAS_12_MESES = 365
DIAS_6_MESES = 182


def _verificar_vehiculo(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> Vehiculo:
    return vehiculos_service.obtener_de_usuario(db, vehiculo_id, usuario_id)


def _km_actual(db: Session, vehiculo_id: uuid.UUID) -> Decimal | None:
    ultima = kilometraje_service.ultima_lectura(db, vehiculo_id)
    return ultima.kilometraje if ultima is not None else None


# ---------- Cálculos sobre un vehículo ya verificado ----------

def _costo_por_km(db: Session, vehiculo: Vehiculo) -> CostoPorKm:
    total = gastos_service.total_gastado(db, vehiculo.id)
    return calculos.costo_por_km(total, vehiculo.kilometraje_inicial, _km_actual(db, vehiculo.id))


def _gasto_por_categoria(db: Session, vehiculo: Vehiculo, desde: date | None, hasta: date | None) -> GastoPorCategoria:
    totales = gastos_service.total_por_categoria(db, vehiculo.id, desde, hasta)
    categorias = {c.id: c for c in categorias_service.listar(db, solo_activas=False)}
    total_general = sum((t.total for t in totales), Decimal("0"))

    items = tuple(
        ItemCategoria(
            categoria_id=t.categoria_id,
            codigo=categorias[t.categoria_id].codigo,
            nombre=categorias[t.categoria_id].nombre,
            tipo_costo=categorias[t.categoria_id].tipo_costo,
            total=t.total,
            cantidad=t.cantidad,
            porcentaje=calculos.porcentaje(t.total, total_general),
        )
        for t in sorted(totales, key=lambda t: t.total, reverse=True)
    )
    total_fijo = sum((i.total for i in items if i.tipo_costo == "fijo"), Decimal("0"))
    return GastoPorCategoria(desde, hasta, total_general, total_fijo, total_general - total_fijo, items)


def _alerta_combustible(db: Session, vehiculo: Vehiculo) -> AlertaCombustible:
    combustible = categorias_service.obtener_por_codigo(db, CODIGO_COMBUSTIBLE)
    if combustible is None:  # catálogo sin la categoría: no hay nada que comparar
        return calculos.evaluar_combustible([])
    serie = gastos_service.serie_mensual(db, vehiculo.id, combustible.id)
    return calculos.evaluar_combustible(serie)


def _proximos_mantenimientos(db: Session, vehiculo: Vehiculo) -> tuple[ProximoMantenimiento, ...]:
    planes = mantenimiento_service.listar_planes_de_vehiculo(db, vehiculo.id)
    if not planes:
        return ()
    ultimos = gastos_service.ultimo_km_por_plan(db, vehiculo.id)
    km_actual = _km_actual(db, vehiculo.id)

    resultado = []
    for plan in planes:
        ultimo_km = ultimos.get(plan.id)
        est = calculos.estimar_proximo_mantenimiento(plan.intervalo_km, ultimo_km, km_actual, vehiculo.kilometraje_inicial)
        resultado.append(
            ProximoMantenimiento(plan.id, plan.nombre, plan.intervalo_km, ultimo_km, est.proximo_km, est.km_restantes, est.estado, est.base)
        )
    # Lo más urgente primero; sin lecturas (km_restantes None) al final.
    resultado.sort(key=lambda p: (p.km_restantes is None, p.km_restantes if p.km_restantes is not None else 0))
    return tuple(resultado)


def _reparar_o_reemplazar(db: Session, vehiculo: Vehiculo, hoy: date) -> OrientacionReparacion:
    reparacion = categorias_service.obtener_por_codigo(db, CODIGO_REPARACION)

    def reparaciones(desde: date, hasta: date) -> Decimal:
        if reparacion is None:
            return Decimal("0")
        for fila in gastos_service.total_por_categoria(db, vehiculo.id, desde, hasta):
            if fila.categoria_id == reparacion.id:
                return fila.total
        return Decimal("0")

    desde_12m = hoy - timedelta(days=DIAS_12_MESES)
    desde_6m = hoy - timedelta(days=DIAS_6_MESES)
    fin_previos = desde_6m - timedelta(days=1)  # los dos semestres no se superponen

    return calculos.evaluar_reparar_o_reemplazar(
        gasto_reparaciones_12m=reparaciones(desde_12m, hoy),
        gasto_total_12m=gastos_service.total_gastado(db, vehiculo.id, desde_12m, hoy),
        reparaciones_6m_recientes=reparaciones(desde_6m, hoy),
        reparaciones_6m_previos=reparaciones(desde_12m, fin_previos),
        km_actual=_km_actual(db, vehiculo.id),
    )


# ---------- Interfaz pública (verifican pertenencia) ----------

def costo_por_km(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> CostoPorKm:
    return _costo_por_km(db, _verificar_vehiculo(db, usuario_id, vehiculo_id))


def gasto_por_categoria(
    db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID, desde: date | None = None, hasta: date | None = None
) -> GastoPorCategoria:
    vehiculo = _verificar_vehiculo(db, usuario_id, vehiculo_id)
    if desde is not None and hasta is not None and desde > hasta:
        raise ReglaDeNegocio("La fecha 'desde' no puede ser posterior a la fecha 'hasta'")
    return _gasto_por_categoria(db, vehiculo, desde, hasta)


def alerta_combustible(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> AlertaCombustible:
    return _alerta_combustible(db, _verificar_vehiculo(db, usuario_id, vehiculo_id))


def proximos_mantenimientos(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> tuple[ProximoMantenimiento, ...]:
    return _proximos_mantenimientos(db, _verificar_vehiculo(db, usuario_id, vehiculo_id))


def reparar_o_reemplazar(
    db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID, hoy: date | None = None
) -> OrientacionReparacion:
    return _reparar_o_reemplazar(db, _verificar_vehiculo(db, usuario_id, vehiculo_id), hoy or date.today())


def resumen(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID, hoy: date | None = None) -> ResumenIndicadores:
    """Todos los indicadores en una sola llamada (para el dashboard). El gasto por categoría cubre los últimos 12 meses."""
    hoy = hoy or date.today()
    vehiculo = _verificar_vehiculo(db, usuario_id, vehiculo_id)
    return ResumenIndicadores(
        costo_por_km=_costo_por_km(db, vehiculo),
        gasto_por_categoria=_gasto_por_categoria(db, vehiculo, hoy - timedelta(days=DIAS_12_MESES), hoy),
        alerta_combustible=_alerta_combustible(db, vehiculo),
        proximos_mantenimientos=_proximos_mantenimientos(db, vehiculo),
        reparar_o_reemplazar=_reparar_o_reemplazar(db, vehiculo, hoy),
    )
