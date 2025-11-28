#backend/api/routes/views.py
from __future__ import annotations
import json
from typing import Optional

from api.deps import get_db, get_storage
from db.view_models import ViewCreate, ViewPublic
from fastapi import APIRouter, Depends, File, Form, HTTPException, status, UploadFile
from pydantic import ValidationError
from pymongo.database import Database
from services.view_service import create_view as svc_create_view
from storage.base import StorageBackend


router = APIRouter(prefix="/assets/{asset_id}/views", tags=["views"])


@router.post("", response_model=ViewPublic, status_code=status.HTTP_201_CREATED)
async def create_view_endpoint(
    asset_id: str,
    payload_json: str = Form(...),
    sketch: Optional[UploadFile] = File(None),
    cad: Optional[UploadFile] = File(None),
    db: Database = Depends(get_db),
    storage: StorageBackend = Depends(get_storage),
) -> ViewPublic:
    try:
        payload_dict = json.loads(payload_json)
        meta = ViewCreate.model_validate(payload_dict)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid view metadata: {exc}")
    
    if sketch is None and cad is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one of sketch or cad must be provided.")
    
    return svc_create_view(
        db=db,
        storage=storage,
        asset_id=asset_id,
        meta=meta,
        sketch=sketch,
        cad=cad,
    )
