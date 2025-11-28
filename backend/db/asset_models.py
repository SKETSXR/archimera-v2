#backend/db/asset_models.py
from __future__ import annotations
from datetime import datetime
from typing import Annotated, List, Literal, Optional

from backend.db.common_models import ProjectLocation, Tag, empty_str_to_none
from pydantic import BaseModel, ConfigDict, Field, field_validator


ClientName = Annotated[str, Field(min_length=1, max_length=100)]
ProjectName = Annotated[str, Field(min_length=1, max_length=256)]
SubCategory = Annotated[str, Field(min_length=1, max_length=64)]
CreatedBy = Annotated[str, Field(min_length=1, max_length=256)]
UploadedBy = Annotated[str, Field(min_length=1, max_length=100)]


class AssetBase(BaseModel):
    client_name: ClientName
    project_name: ProjectName

    category: Literal["wardrobe", "chair", "table"]
    subcategory: Optional[SubCategory] = None

    project_type: Optional[Literal["residential", "commercial", "hospitality", "office"]] = None
    room_type: Optional[Literal["bedroom", "master bedroom", "kids room", "kitchen", "living room", "guest room", "hall", "office space", "Unknown"]] = None
    style: Optional[Literal["modern", "contemporary", "classic", "minimal", "Unknown"]] = None

    created_by: Optional[CreatedBy] = None
    uploaded_by: UploadedBy
    studio: Literal["B1", "B2", "F1", "F2", "S1", "S2"]

    location: ProjectLocation
    tags: List[Tag] = Field(default_factory=list)

    @field_validator("subcategory", "created_by", "project_type", "room_type", "style", mode="before")
    @classmethod
    def _empty_optional_strs(cls, v):
        return empty_str_to_none(v)


class AssetTagTextState(BaseModel):
    """
    ML-side state for converting tags JSON into natural language text.
    """
    tags_text: Optional[str] = None

    status: Literal[
        "Pending Processing",
        "Ready for Embedding",
        "Embedded",
        "Error"
    ] = "Pending Processing"

    last_error: Optional[str] = None


class AssetCreate(AssetBase):
    """
    Incoming payload from the UI for creating an asset.
    """
    pass


class AssetInDB(AssetBase):
    """
    MongoDB representation
    """
    id: str = Field(alias="_id")
    uploaded_at: datetime
    updated_at: datetime

    # Per-asset tag -> text status (for GPT-nano step)
    tag_text_state: AssetTagTextState = Field(default_factory=AssetTagTextState)

    model_config = ConfigDict(populate_by_name=True)


class AssetPublic(AssetBase):
    """
    What we return to the UI.
    """
    id: str
    uploaded_at: datetime
    updated_at: datetime
