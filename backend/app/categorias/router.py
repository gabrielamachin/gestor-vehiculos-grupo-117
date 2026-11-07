"""Endpoints del módulo Categorías (prefijo /categorias). Requieren autenticación."""
from fastapi import APIRouter, Depends

from app.categorias import service
from app.categorias.schemas import CategoriaRespuesta
from app.core.database import DbSession
from app.core.security import get_usuario_id_actual

router = APIRouter(prefix="/categorias", tags=["Categorías"], dependencies=[Depends(get_usuario_id_actual)])


@router.get("", response_model=list[CategoriaRespuesta])
def listar(db: DbSession, incluir_inactivas: bool = False):
    """Categorías de gasto ordenadas por nombre. Por defecto solo las activas."""
    return service.listar(db, solo_activas=not incluir_inactivas)
