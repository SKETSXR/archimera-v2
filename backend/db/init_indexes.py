#backend/db/init_indexes.py
from __future__ import annotations
from backend.db.mongo import get_database
from pymongo import ASCENDING, TEXT
from pymongo.database import Database


def ensure_indexes(db: Database | None = None) -> None:
    """
    Ensure collections exist and basic indexes are created.

    This is idempotent: safe to call multiple times.
    """

    if db is None:
        db = get_database()

    # --- assets collection ---
    assets = db["assets"]

    # Common lookups / filters: by client, project, category, tags
    assets.create_index([("client_name", ASCENDING)], name="client_name_idx")
    assets.create_index([("project_name", ASCENDING)], name="project_name_idx")
    assets.create_index([("category", ASCENDING)], name="category_idx")

    # Tag-based filtering (per-asset tags)
    assets.create_index(
        [("tags.category", ASCENDING), ("tags.value", ASCENDING)],
        name="tags_category_value_idx",
    )

    # Optional: text index over tag text (when GPT-nano fills it later)
    assets.create_index(
        [("tag_text_state.tags_text", TEXT)],
        name="tag_text_state_text_idx",
        default_language="english",
    )

    # --- views collection ---
    views = db["views"]

    # Fast lookup of all views for an asset
    views.create_index([("asset_id", ASCENDING)], name="asset_id_idx")

    # Processing queues: find views by status
    views.create_index([("status", ASCENDING)], name="status_idx")

    # Combined: all pending views for a given asset (CAD worker, ML, etc.)
    views.create_index(
        [("asset_id", ASCENDING), ("status", ASCENDING)],
        name="asset_status_idx",
    )

    # --- embedding_docs collection ---
    embeddings = db["embedding_docs"]

    embeddings.create_index(
        [("asset_id", ASCENDING)],
        name="emb_asset_id_idx",
    )
    embeddings.create_index(
        [("view_id", ASCENDING)],
        name="emb_view_id_idx",
    )
    embeddings.create_index(
        [("status", ASCENDING)],
        name="emb_status_idx",
    )
    embeddings.create_index(
        [("model_version", ASCENDING)],
        name="emb_model_version_idx",
    )

    # Combined: all embedding docs ready for embedding for a given model
    embeddings.create_index(
        [("status", ASCENDING), ("model_version", ASCENDING)],
        name="emb_status_model_idx",
    )
