# backend/db/common_models.py
from __future__ import annotations
from typing import Annotated, Optional

from pydantic import BaseModel, Field


Country = Annotated[str, Field(min_length=1, max_length=56)]
StateRegion = Annotated[str, Field(min_length=1, max_length=58)]
City = Annotated[str, Field(min_length=1, max_length=100)]
Locality = Annotated[str, Field(min_length=1, max_length=100)]
PostalCode = Annotated[str, Field(min_length=1, max_length=10)]


class FileRef(BaseModel):
    rel_path: str
    content_type: str
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None # e.g. sha256


class Tag(BaseModel):
    category: str
    value: str


class ProjectLocation(BaseModel):
    country: Country
    state: Optional[StateRegion] = None
    city: Optional[City] = None
    locality: Optional[Locality] = None
    postal_code: Optional[PostalCode] = None
