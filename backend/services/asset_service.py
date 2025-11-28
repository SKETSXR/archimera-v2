#backend/services/asset_service.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from db.asset_models import AssetCreate, AssetInDB, AssetPublic, AssetTagTextState
from pymongo.database import Database


def create_asset(db: Database, payload: AssetCreate) -> AssetPublic:
    now = datetime.now(timezone.utc)

    doc = payload.model_dump()
    doc["uploaded_at"] = now
    doc["updated_at"] = now
    # Initialize tag_text_state for ML pipeline
    doc["tag_text_state"] = AssetTagTextState().model_dump()

    result = db["assets"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    asset_in_db = AssetInDB.model_validate(doc)
    return AssetPublic.model_validate(asset_in_db.model_dump(by_alias=False))


def get_asset(db: Database, asset_id: str) -> Optional[AssetPublic]:
    try:
        oid = ObjectId(asset_id)
    except Exception:
        return None
    
    doc = db["assets"].find_one({"_id": oid})
    if not doc:
        return None
    
    doc["_id"] = str(doc["_id"])
    asset_in_db = AssetInDB.model_validate(doc)
    return AssetPublic.model_validate(asset_in_db.model_dump(by_alias=False))
