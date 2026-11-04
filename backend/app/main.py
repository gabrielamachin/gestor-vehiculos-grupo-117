from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import health
from app.core.config import get_settings
from app.core.errors import registrar_manejadores
from app.usuarios.router import router as usuarios_router
from app.vehiculos.router import router as vehiculos_router 
from app.kilometraje.router import router as kilometraje_router


def crear_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title="Gestor Inteligente de Vehículos", version="0.1.0")

    # CORS con la URL exacta del frontend (variable CORS_ORIGINS). El JWT viaja en el
    # header Authorization, no en cookies, por eso no se habilitan credenciales.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_lista,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    registrar_manejadores(app)

    app.include_router(health.router)
    app.include_router(usuarios_router)
    app.include_router(vehiculos_router)
    app.include_router(kilometraje_router)
    return app


app = crear_app()
