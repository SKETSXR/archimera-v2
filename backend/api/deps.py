#backend/api/deps.py
from __future__ import annotations
from functools import lru_cache

from core.config import settings
from db.mongo import db_dependency
from fastapi import Depends
from pymongo.database import Database
from storage.base import StorageBackend
from storage.filesystem import FileSystemStorage


def get_db(db: Database = Depends(db_dependency)) -> Database:
    return db


@lru_cache
def _storage_instance() -> StorageBackend:
    return FileSystemStorage(settings.file_base_dir)


def get_storage() -> StorageBackend:
    return _storage_instance()
