"""Acceso a datos de la tabla `categorias_gasto` (solo lectura)."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.categorias.models import Categoria


def listar(db: Session, solo_activas: bool = True) -> list[Categoria]:
    consulta = select(Categoria).order_by(Categoria.nombre)
    if solo_activas:
        consulta = consulta.where(Categoria.activa.is_(True))
    return list(db.scalars(consulta))


def obtener(db: Session, categoria_id: int) -> Categoria | None:
    return db.get(Categoria, categoria_id)


def obtener_por_codigo(db: Session, codigo: str) -> Categoria | None:
    return db.scalar(select(Categoria).where(Categoria.codigo == codigo))
