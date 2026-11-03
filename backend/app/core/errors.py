"""Errores de dominio y su traducción a respuestas HTTP.

Los servicios lanzan estas excepciones y no conocen HTTP; el manejador registrado
en main.py las convierte en la respuesta con el código que corresponde.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ErrorDeDominio(Exception):
    status_code = 400

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class NoAutenticado(ErrorDeDominio):
    status_code = 401


class NoEncontrado(ErrorDeDominio):
    """También se usa cuando el recurso existe pero es de otro usuario (no revela su existencia)."""
    status_code = 404


class Conflicto(ErrorDeDominio):
    status_code = 409


class ReglaDeNegocio(ErrorDeDominio):
    status_code = 422


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(ErrorDeDominio)
    async def _manejar_error_de_dominio(_: Request, exc: ErrorDeDominio) -> JSONResponse:
        headers = {"WWW-Authenticate": "Bearer"} if isinstance(exc, NoAutenticado) else None
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.mensaje}, headers=headers)
