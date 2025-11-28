# backend/db/mongo.py
from __future__ import annotations
from typing import Generator, Optional

from core.config import settings
from pymongo import MongoClient
from pymongo.database import Database


_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(settings.mongo_uri)
    return _client


def get_database() -> Database:
    global _db
    if _db is None:
        client = get_client()
        # If URI has DB in it, use that; else fall back to 'cad_db'
        db = client.get_default_database()
        _db = db if db is not None else client["cad_db"]
    return _db


def db_dependency() -> Generator[Database, None, None]:
    """
    FastAPI dependency wrapper. Not strictly needed for connection
    lifecycle with Mongo, but keeps the interface consistent.
    """
    db = get_database()
    try:
        yield db
    finally:
        # We keep the client open; MongoClient is meant to be long-lived.
        pass
