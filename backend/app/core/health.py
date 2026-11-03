"""Endpoints de salud. /health es liviano (para mantener activa la instancia free de Render)."""
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import DbSession

router = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/health/db")
def health_db(db: DbSession) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="No hay conexión con la base de datos")
    return {"status": "ok", "database": "ok"}
