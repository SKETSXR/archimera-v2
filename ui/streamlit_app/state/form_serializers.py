"""
Form serialization utilities.

These functions take the raw dictionaries returned by the UI layer and
convert them into a single payload that can be sent to the backend API
or stored in a database.

Right now this module is light, but it will grow as the schema evolves.
"""

from datetime import datetime
from typing import Dict, Any, List


def build_submission_payload(asset_metadata: Dict[str, Any],
                             views_metadata: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build the top-level submission payload combining asset metadata and views.

    This function is the canonical place to prepare what will eventually be
    sent to the backend.

    Args:
        asset_metadata: Dictionary returned from `render_asset_form`.
        views: List of dictionaries returned from `render_view_section`.

    Returns:
        dict: Combined payload with timestamps and raw view structures.
    """
    # Attach system-generated timestamps here.
    # These can later be removed from the UI and moved fully to the backend.
    now_utc = datetime.utcnow().isoformat() + "Z"

    payload = {
        "asset": {
            **asset_metadata,
            "uploaded_at": now_utc,
            "updated_at": now_utc,
        },
        "views": views_metadata
    }

    return payload
