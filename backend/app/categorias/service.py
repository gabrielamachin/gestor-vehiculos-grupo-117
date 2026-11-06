"""Lógica de negocio del módulo Categorías. No conoce HTTP: lanza errores de dominio.

Las categorías son un catálogo administrado con INSERT/UPDATE sobre la tabla (no hay
pantalla de administración en el MVP). Las funciones de este servicio son la interfaz
que usan los módulos Gastos e Indicadores.
"""
from sqlalchemy.orm import Session

from app.categorias import repository
from app.categorias.models import Categoria
from app.core.errors import ReglaDeNegocio


def listar(db: Session, solo_activas: bool = True) -> list[Categoria]:
    return repository.listar(db, solo_activas)


def obtener(db: Session, categoria_id: int) -> Categoria | None:
    """Cualquier categoría, activa o no (para mostrar el nombre de gastos históricos)."""
    return repository.obtener(db, categoria_id)


def obtener_activa(db: Session, categoria_id: int) -> Categoria:
    """Para registrar un gasto nuevo: la categoría debe existir y estar activa."""
    categoria = repository.obtener(db, categoria_id)
    if categoria is None or not categoria.activa:
        raise ReglaDeNegocio("La categoría no existe o está inactiva")
    return categoria


def obtener_por_codigo(db: Session, codigo: str) -> Categoria | None:
    """Busca por el código estable (ej. 'combustible'). Devuelve None si no existe.

    Indicadores depende de que exista la categoría 'combustible': decide qué hacer si falta.
    """
    return repository.obtener_por_codigo(db, codigo)
