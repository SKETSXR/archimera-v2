#backend/services/view_service.py
from __future__ import annotations
from datetime import datetime, timezone

from bson import ObjectId
from backend.db.view_models import ViewCreate, ViewFiles, ViewInDB, ViewPublic
from fastapi import HTTPException, status
from pymongo.database import Database
from backend.services.asset_service import get_asset
from backend.storage.base import StorageBackend


def create_view(
        db: Database,
        storage: StorageBackend,
        asset_id: str,
        meta: ViewCreate,
        sketch,
        cad,
) -> ViewPublic:
    # Ensure asset exists
    asset = get_asset(db, asset_id)
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    
    now = datetime.now(timezone.utc)
    view_oid = ObjectId()
    view_id_str = str(view_oid)

    files: ViewFiles = storage.save_view_files(
        asset_id=asset_id,
        view_id=view_id_str,
        sketch=sketch,
        cad=cad,
    )

    base_doc = {
        "_id": view_oid,
        "asset_id": asset_id,
        "view_type": meta.view_type,
        "orientation": meta.orientation,
        "scale": meta.scale,
        "view_name": meta.view_name,
        "description": meta.description,
        "files": files.model_dump(),
        "status": "Pending Processing",
        "last_processing_error": None,
        "created_at": now,
        "updated_at": now,
    }

    db["views"].insert_one(base_doc)

    base_doc["_id"] = view_id_str
    view_in_db = ViewInDB.model_validate(base_doc)
    return ViewPublic.model_validate(view_in_db.model_dump(by_alias=False))
