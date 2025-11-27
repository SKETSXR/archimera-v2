"""
asset_api.py

Client-side wrapper for interacting with the backend Asset API.
This module is used by the Streamlit UI to create assets in MongoDB
through the backend service.

Responsibilities:
    - POST /assets  → Create a new asset document
    - (future) GET /assets/{id} → Fetch an asset
    - (future) PUT /assets/{id} → Update an asset

Notes:
    - This module only deals with asset-level metadata.
    - All view uploads (sketch + CAD files) are handled by `view_api.py`
      because those require multipart file uploads.
"""

import json
from typing import Dict, Any

from .http_client import post


def create_asset(asset_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new asset in the backend.

    This sends an asset metadata payload as JSON to the backend API.
    The backend:
        - Validates the metadata
        - Assigns an asset ID (or uses provided one)
        - Stores it in MongoDB
        - Returns the stored asset with `_id` and timestamps
    
    Args:
        asset_metadata (dict): The normalized asset metadata produced by `render_asset_form()` in the UI.
    
    Returns:
        dict:
            Parsed JSON response containing:
                - id / _id
                - client_name, project_name, category, etc.
                - timestamps
                - any automatic fields set by the backend
    
    Raises:
        requests.HTTPError:
            If the backend responds with 4xx or 5xx.
    """
    # NOTE: This sends normal JSON (NOT multipart)
    response = post("/assets", json=asset_metadata)
    return response.json()
