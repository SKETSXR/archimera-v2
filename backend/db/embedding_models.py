#backend/db/embedding_models.py
from __future__ import annotations
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class EmbeddingVector(BaseModel):
    vector: List[float]
    dim: int
    faiss_id: Optional[int] = None


class EmbeddingDoc(BaseModel):
    """
    Embedding document for a (asset, view, model_version) triple.
    ML container will mostly use this; defining here keeps schema shared.
    """
    id: str = Field(alias="_id")
    asset_id: str
    view_id: str
    model_version: str

    status: Literal[
        "Pending Processing",
        "Ready for Embedding",
        "Embedded",
        "Error"
    ] = "Pending Processing"

    last_error: Optional[str] = None

    input_embedding: Optional[EmbeddingVector] = None
    output_embedding: Optional[EmbeddingVector] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)
