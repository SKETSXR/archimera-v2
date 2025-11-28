# backend/core/config.py
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global settings for the backend.

    Reads env vars:
        MONGO_URI - full URI, ideally with DB: mongodb://mongo:27017/cad_db
        FILE_BASE_DIR - where the NAS is mounted inside the container (e.g., /mnt/assets)
    """
    mongo_uri: str = "mongodb://mongo:27017/cad_db"
    file_base_dir: str = "/mnt/assets"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
    )


settings = Settings()
