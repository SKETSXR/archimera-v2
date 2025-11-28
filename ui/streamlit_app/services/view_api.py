import json
from typing import Any, Dict

from .http_client import post


def create_view(asset_id: str, view_metadata: Dict[str, Any], view_files: Dict[str, Any]) -> dict:
    """
    Create a new view for an asset with metadata and files.

    Sends:
        - payload_json (view_metadata)
        - sketch (file)
        - cad (file)
    
    Args:
        asset_id: ID of the asset this view belongs to.
        view_metadata: JSON-safe metadata dict (no file objects).
        view_files: Dict with keys sketch_file, cad_file.
    
    Returns:
        dict: Parsed JSON response from backend.
    """
    files = {}
    if view_files.get("sketch_file"):
        files["sketch"] = view_files["sketch_file"]
    if view_files.get("cad_file"):
        files["cad"] = view_files["cad_file"]
    
    data = {
        "payload_json": json.dumps(view_metadata)
    }

    resp = post(f"/assets/{asset_id}/views", files=files, data=data)
    return resp.json()
