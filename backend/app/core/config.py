"""Configuración de la aplicación, leída de variables de entorno (o del archivo .env)."""
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    jwt_secret: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    # Lista separada por comas; se expone como lista en `cors_origins_lista`.
    cors_origins: str = "http://localhost:5173"

    @field_validator("database_url")
    @classmethod
    def _normalizar_database_url(cls, valor: str) -> str:
        # Render entrega "postgres://...", pero SQLAlchemy 2 solo reconoce "postgresql://".
        if valor.startswith("postgres://"):
            return "postgresql://" + valor[len("postgres://"):]
        return valor

    @property
    def cors_origins_lista(self) -> list[str]:
        return [origen.strip() for origen in self.cors_origins.split(",") if origen.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
