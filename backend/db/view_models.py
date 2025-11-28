#backend/db/view_models.py
from __future__ import annotations
from datetime import datetime
from typing import Annotated, Literal, Optional

from db.common_models import FileRef
from pydantic import BaseModel, ConfigDict, Field


Scale = Annotated[str, Field(pattern=r"^\s*1\s*:\s*[1-9]\d*(?:\.\d+)?\s*$", min_length=1, max_length=10)]
ViewName = Annotated[str, Field(min_length=1, max_length=100)]
ViewDescription = Annotated[str, Field(min_length=1, max_length=256)]


class ViewFiles(BaseModel):
    sketch: Optional[FileRef] = None
    cad: Optional[FileRef] = None
    raster: Optional[FileRef] = None
    metadata: Optional[FileRef] = None


class ViewBase(BaseModel):
    asset_id: str

    view_type: Literal["elevation", "plan", "section", "detail"]
    orientation: Optional[Literal["North", "East", "West", "South"]] = None
    scale: Optional[Scale] = None
    view_name: Optional[ViewName] = None
    description: Optional[ViewDescription] = None

    files: ViewFiles = Field(default_factory=ViewFiles)


class ViewCreate(BaseModel):
    """
    Metadata sent from the UI inside payload_json.
    """
    view_type: Literal["elevation", "plan", "section", "detail"]
    orientation: Optional[Literal["North", "East", "West", "South"]] = None
    scale: Optional[Scale] = None
    view_name: Optional[ViewName] = None
    description: Optional[ViewDescription] = None


class ViewInDB(ViewBase):
    id: str = Field(alias="_id")

    status: Literal[
        "Pending Processing",
        "Ready for Embedding",
        "Embedded",
        "Error"
    ] = "Pending Processing"
    last_processing_error: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class ViewPublic(ViewBase):
    id: str
    status: str
    last_processing_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
