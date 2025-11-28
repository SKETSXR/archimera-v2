#backend/api/routes/assets.py
from __future__ import annotations
from api.deps import get_db
from db.asset_models import AssetCreate, AssetPublic
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from services import asset_service


router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("", response_model=AssetPublic, status_code=status.HTTP_201_CREATED)
def create_asset_endpoint(payload: AssetCreate, db: Database = Depends(get_db)) -> AssetPublic:
    return asset_service.create_asset(db=db, payload=payload)


@router.get("/{asset_id}", response_model=AssetPublic)
def get_asset_endpoint(asset_id: str, db: Database = Depends(get_db)) -> AssetPublic:
    asset = asset_service.get_asset(db=db, asset_id=asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset
