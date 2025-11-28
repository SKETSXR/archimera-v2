# backend/db/common_models.py
from __future__ import annotations
from typing import Annotated, Optional, Any

from pydantic import BaseModel, Field, field_validator

def empty_str_to_none(v: Any) -> Any:
    """
    Normalize empty strings from the UI to None for optional fields.
    """
    if isinstance(v, str) and v.strip() == "":
        return None
    return v

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

    @field_validator("state", "city", "locality", "postal_code", mode="before")
    @classmethod
    def _empty_str_to_none(cls, v):
        return empty_str_to_none(v)
