"""Endpoints del módulo Indicadores (prefijo /indicadores). Solo lectura; todos requieren autenticación."""
import uuid
from datetime import date

from fastapi import APIRouter

from app.core.database import DbSession
from app.core.security import UsuarioIdActual
from app.indicadores import service
from app.indicadores.schemas import (
    AlertaCombustibleRespuesta,
    CostoPorKmRespuesta,
    GastoPorCategoriaRespuesta,
    OrientacionReparacionRespuesta,
    ProximoMantenimientoRespuesta,
    ResumenRespuesta,
)

router = APIRouter(prefix="/indicadores/vehiculos/{vehiculo_id}", tags=["Indicadores"])


@router.get("/resumen", response_model=ResumenRespuesta)
def resumen(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Todos los indicadores del vehículo en una sola llamada (pensado para el dashboard)."""
    return service.resumen(db, usuario_id, vehiculo_id)


@router.get("/costo-por-km", response_model=CostoPorKmRespuesta)
def costo_por_km(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Costo real por km: total gastado dividido por los km recorridos desde el kilometraje inicial."""
    return service.costo_por_km(db, usuario_id, vehiculo_id)


@router.get("/gasto-por-categoria", response_model=GastoPorCategoriaRespuesta)
def gasto_por_categoria(
    vehiculo_id: uuid.UUID,
    db: DbSession,
    usuario_id: UsuarioIdActual,
    desde: date | None = None,
    hasta: date | None = None,
):
    """Gasto acumulado por categoría, con porcentaje y totales fijo/variable. Sin fechas: todo el historial."""
    return service.gasto_por_categoria(db, usuario_id, vehiculo_id, desde, hasta)


@router.get("/alerta-combustible", response_model=AlertaCombustibleRespuesta)
def alerta_combustible(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Compara el último mes con gasto en combustible contra el promedio histórico propio."""
    return service.alerta_combustible(db, usuario_id, vehiculo_id)


@router.get("/proximo-mantenimiento", response_model=list[ProximoMantenimientoRespuesta])
def proximo_mantenimiento(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Próximo mantenimiento de cada plan del vehículo, lo más urgente primero."""
    return service.proximos_mantenimientos(db, usuario_id, vehiculo_id)


@router.get("/reparar-o-reemplazar", response_model=OrientacionReparacionRespuesta)
def reparar_o_reemplazar(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Orientación (no tasación) sobre seguir reparando o evaluar un reemplazo, con las señales que la sustentan."""
    return service.reparar_o_reemplazar(db, usuario_id, vehiculo_id)
