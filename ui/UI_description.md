# Introduction

This markdown file will serve as a description of the User Interface developed using Streamlit. It will contain all codes as well as the appropriate folder structure for the same.

## 1. UI Container Structure

```text
ui/
    .devcontainer/
        devcontainer.json
    streamlit_app/
        assets/
        components/
            asset_form.py
            file_uploaders.py
            tag_selector.py
            view_form.py
        constants/
            config.py
            tag_vocab.py
            view_types.py
        services/
            asset_api.py
            http_client.py
            view_api.py
        state/
            form_serializers.py
            session_state.py
        utils/
            file_utils.py
            validators.py
        app.py
    requirements.txt
    UI_description.md (The current file)
```

## 2. Requirements File (`ui/requirements.txt`)

```text
###########################################
# Core UI
###########################################
streamlit==1.36.0

###########################################
# HTTP client
###########################################
requests==2.32.3

###########################################
# Validation / models (if you mirror backend schemas)
###########################################
pydantic==2.7.4
ruff==0.14.6

###########################################
# Env / config
###########################################
python-dotenv==1.0.1

###########################################
# Optional: image handling (thumbnails, previews)
###########################################
pillow==10.3.0
```

## 3. Streamlit Application (`ui/streamlit_app/`)

This section contains all the codes for the application

### 3.1. `constants/tag_vocab.py`

```python
"""
Tag vocabulary for Archimera.

This module defines the complete set of selectable tags grouped by
semantic categories. The UI uses this dictionary to render multi-select
controls and ensure consistent tagging.
"""

TAG_OPTIONS = {
    "Materials": [
        "Solid Wood","Engineered Wood","Veneer",
        "Laminate","Metal Frame","Glass Elements",
        "Acrylic","Plastic/PVC","Natural Finish"
    ],
    "Doors & Panels": [
        "Sliding","Hinged","Bi-fold",
        "Pocket Door","Mirror Door","Louvered"
    ],
    "Interior / Storage": [
        "Walk-in","Built-in","Modular",
        "Shelves","Drawers","Hanging",
        "Shoe Storage","Accessory Drawer","Vertical Divider"
    ],
    "Hardware / Mechanism": [
        "Soft-close","Push-to-open","Concealed Hinges",
        "Hydraulic Lift","Integrated"
    ],
    "Finish / Aesthetics": [
        "Matte Finish","High Gloss","Textured Finish",
        "Two-Tone","Hand-Painted","Distressed/Vintage"
    ],
    "Use-case": [
        "Wardrobe","Linen Closet",
        "Wardrobe + Desk","Kids","Walk-through"
    ],
    "Environment / Performance": [
        "Moisture Resistant","Fire-Rated",
        "Eco-friendly","Acoustic Lining"
    ],
    "Size / Configuration": [
        "Corner Unit","Floor-to-Ceiling",
        "Half-height","Custom Width"
    ],
    "Accessories / Extras": [
        "Pull-out Mirror","Lazy Susan","Tie / Belt Rack",
        "Pull-out Ironing Board","Valet Rod"
    ],
    "Style": [
        "Contemporary","Minimal","Scandinavian",
        "Industrial","Traditional","Transitional"
    ]
}
```

### 3.2. `constants/view_types.py`

```python
"""
View- and project-related constant lists for form dropdowns.

These lists keep the UI consistent and avoid magic strings sprinkled
throughout the code.
"""

# Supported view types for each view (per asset)
VIEW_TYPES = ["elevation", "plan", "section", "detail"]

# Supported orientations; "None" is used to represent "not specified"
ORIENTATIONS = ["None", "North", "South", "East", "West"]

# Project type options for asset-level metadata
PROJECT_TYPES = ["residential", "commercial", "hospitality", "office"]

# Studio from where this is getting uploaded
STUDIOS = ["B1", "B2", "F1", "F2", "S1", "S2"]
```

### 3.3. `constants/config.py`

```python
"""
Configuration constants for the Archimera UI.

This file is intentionally kept minimal; environment-specific values
(e.g., API base URL) can be wired in here later or derived from
environment variables.
"""

APP_TITLE: str = "Archimera Data Collector"

# Placeholder for future use (when backend API exists)
API_BASE_URL: str = "http://localhost:8000"
```

### 3.4. `state/session_state.py`

```python
"""
Session state helpers for the Archimera Streamlit app.

This module centralizes all Streamlit `st.session_state` initialization
and provides a small accessor to avoid directly scattering raw
`st.session_state` calls everywhere.
"""

import streamlit as st


def init_session_state() -> None:
    """
    Initialize keys in `st.session_state` if they are not already present.

    Keys initialized:
        - asset_tags: list of selected tags at the asset level.
        - views: list of per-view dictionaries (metadata + files).
    """
    default_values = {
        "asset_tags": [],
        "views": []
    }

    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default


def get_state():
    """
    Return the current Streamlit session state object.

    Returns:
        SessionState: The Streamlit session_state proxy object.
    """
    return st.session_state
```

### 3.5. `state/form_serializers.py`

```python
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
                             views: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        "views": views
    }

    return payload
```

### 3.6. `utils/file_utils.py`

```python
"""
File utility helpers.

These helpers are not deeply used yet, but will be handy when:
- Sending files to backend APIs.
- Storing file metadata in Mongo.
- Logging or debugging uploads.
"""

from typing import Optional, Dict, Any


def extract_file_metadata(upload) -> Optional[Dict[str, Any]]:
    """
    Extract basic metadata from a Streamlit UploadedFile object.

    Args:
        upload: A Streamlit UploadedFile object or None.

    Returns:
        dict or None: A dictionary containing filename, size, and MIME type,
                      or None if no file was provided.
    """
    if upload is None:
        return None

    return {
        "filename": upload.name,
        "size_bytes": upload.size,
        "mime_type": upload.type,
    }
```

### 3.7. `utils/validators.py`

```python
"""
Validation helpers for form inputs and uploaded files.
"""

from typing import Optional

import streamlit as st


def validate_dwg(file) -> None:
    """
    Validate that a given uploaded file is a .dwg CAD file.

    Args:
        file: A Streamlit UploadedFile object or None.

    Side-effects:
        If the file is non-None and does not end with `.dwg`, a Streamlit
        error message is displayed.

    Notes:
        This is a lightweight validation and does not inspect the file
        contents, only the filename.
    """
    if file is None:
        # No file uploaded; nothing to validate yet
        return

    filename: str = file.name.lower()

    if not filename.endswith(".dwg"):
        st.error("Invalid CAD file. Only .dwg files are allowed.")


def normalize_text_field(value: str | None, to_lower: bool = True) -> str | None:
    """
    Normalize a free-text field by stripping whitespace and optionally lowercasing.

    Args:
        value: Raw string or None.
        to_lower: Whether to convert to lowercase.

    Returns:
        Normalized string or None if empty.
    """
    if not value:
        return None
    v = value.strip()
    if v.lower() == "none":
        return None
    return v.lower() if to_lower else v


def require_non_empty(label: str, value: str) -> None:
    """
    Simple UI-side check to ensure a field is not empty.

    Args:
        label: Human-readable field name.
        value: Input value.

    Side-effects:
        Displays a warning if value is empty.
    """
    if not value or not value.strip():
        st.warning(f"{label} is currently empty. Backend may reject this later.")
```

### 3.8. `services/http_client.py`

```python
import requests

from constants.config import API_BASE_URL

def post(path: str, json=None, files=None, data=None):
    """
    Simple HTTP POST wrapper for talking to the backend API.

    Args:
        path: API path.
        json: JSON-serializable body
        files: dict for multipart file uploads.
        data: dict for form fields.
    
    Returns:
        Response object.
    
    Raises:
        requests.HTTPError if status is not OK.
    """
    url = f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    resp = requests.post(url, json=json, files=files, data=data)
    resp.raise_for_status()
    return resp
```

### 3.9. `services/asset_api.py`

```python
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

from http_client import post


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
```

### 3.10. `services/view_api.py`

```python
import json
from typing import Dict, Any

from http_client import post


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
```

### 3.11. `components/tag_selector.py`

```python
"""
Tag selector component.

Renders multi-select inputs for each tag category based on TAG_OPTIONS,
and synchronizes the selected tags into `st.session_state["asset_tags"]`
in a normalized {category, value} format.
"""

import streamlit as st

from constants.tag_vocab import TAG_OPTIONS
from state.session_state import get_state


def render_tag_selector() -> None:
    """
    Render multi-select controls for each tag category.

    This function:
        - Loops over all tag categories.
        - For each category, renders a multi-select of possible tags.
        - Rebuilds `session_state["asset_tags"]` as a flat list of
          {category: str, value: str} dictionaries.
    """
    state = get_state()

    # Reset asset_tags and recompute from all category widgets
    state["asset_tags"] = []

    for category, options in TAG_OPTIONS.items():
        key = f"tag_select_{category}"

        # Multi-select per category; Streamlit will remember selections by key
        selected_values = st.multiselect(
            label=f"{category}",
            options=options,
            key=key,
            help="Select one or more tags for this category."
        )

        # Append all selected tags for this category into session state
        for value in selected_values:
            state["asset_tags"].append({
                "category": category,
                "value": value
            })

    # Show a preview of what was collected
    if state["asset_tags"]:
        st.write("#### Selected Tags:")
        st.json(state["asset_tags"])
```

### 3.12. `components/file_uploaders.py`

```python
"""
File uploader components.

This module defines thin wrapper functions around Streamlit file uploaders,
keeping validation and configuration in a single place.
"""

import streamlit as st
from utils.validators import validate_dwg

def sketch_uploader(key: str):
    """
    Render a file uploader widget for sketch files.

    Allowed formats: PNG, JPG, JPEG, PDF.

    Args:
        key: Unique Streamlit key for this uploader widget.

    Returns:
        UploadedFile or None: The uploaded file object, or None if no file was selected.
    """
    file = st.file_uploader(
        label="Sketch Upload (PNG / JPG / JPEG / PDF)",
        type=["png", "jpg", "jpeg", "pdf"],
        key=key,
        help="Upload the sketch for this view. Prefer PNG/JPG, PDF also allowed."
    )
    return file

def cad_uploader(key: str):
    """
    Render a file uploader widget for CAD (.dwg) files.

    Args:
        key: Unique Streamlit key for this uploader widget.

    Returns:
        UploadedFile or None: The uploaded DWG file object, or None if not provided.
    """
    file = st.file_uploader(
        label="CAD Upload (DWG)",
        type=["dwg"],
        key=key,
        help="Upload the DWG file for this view."
    )

    # Run a simple validation to ensure correct file type/extension
    validate_dwg(file)
    return file
```

### 3.13. `components/asset_form.py`

```python
"""
Asset-level form component.

This module renders all fields that are captured once per asset:
client, project, location, project type, style, and asset-level tags.
"""

import streamlit as st
from typing import Dict, Any

from components.tag_selector import render_tag_selector
from constants.view_types import PROJECT_TYPES, STUDIOS
from state.session_state import get_state
from utils.validators import normalize_text_field, require_non_empty


def render_asset_form() -> Dict[str, Any]:
    """
    Render the asset-level metadata form and return captured values.

    The function renders:
        - Client, project, category, subcategory
        - Project type, room type, style
        - Created by, uploaded by, studio
        - Location (country, state, city, locality, postal code)
        - Tag selector (uses predefined tag vocab)

    Returns:
        dict: A dictionary containing all asset-level metadata and tags.
    """
    st.markdown("### 1. Asset-Level Metadata")

    col1, col2, col3 = st.columns(3)

    # Basic project/asset identifiers
    with col1:
        client_name = st.text_input("Client Name")
        project_name = st.text_input("Project Name")
        category = st.text_input("Category (e.g., wardrobe, kitchen)")
        subcategory = st.text_input("Subcategory (optional)")

    # Project context fields
    with col2:
        project_type = st.selectbox("Project Type", PROJECT_TYPES)
        room_type = st.text_input("Room Type (optional)")
        style = st.text_input("Style (e.g., modern, classic)")

    # People + studio context
    with col3:
        created_by = st.text_input("Created By (optional)")
        uploaded_by = st.text_input("Uploaded By")
        studio = st.selectbox("Studio", STUDIOS)

    # Validating that Location fields are non empty
    require_non_empty("Country", country)
    require_non_empty("State / Region", state)
    require_non_empty("City", city)
    
    # Location fields
    st.markdown("### 2. Project Location")
    colL1, colL2 = st.columns(2)

    with colL1:
        country = st.text_input("Country")
        state = st.text_input("State / Region")
        city = st.text_input("City")

    with colL2:
        locality = st.text_input("Locality (optional)")
        postal_code = st.text_input("Postal Code / ZIP (optional)")

    # Tag selection (predefined vocab, multi-select)
    st.markdown("### 3. Asset-Level Tags")
    render_tag_selector()

    state = get_state()

    category_norm = normalize_text_field(category)
    subcategory_norm = normalize_text_field(subcategory)
    room_type_norm = normalize_text_field(room_type)
    style_norm = normalize_text_field(style)

    # Build and return the asset metadata dictionary
    asset_metadata: Dict[str, Any] = {
        "client_name": client_name,
        "project_name": project_name,
        "category": category_norm,
        "subcategory": subcategory_norm or None,
        "project_type": project_type.strip().lower(),
        "room_type": room_type_norm or None,
        "style": style_norm or None,
        "created_by": created_by or None,
        "uploaded_by": uploaded_by,
        "studio": studio or None,
        "location": {
            "country": country,
            "state": state,
            "city": city,
            "locality": locality or None,
            "postal_code": postal_code or None,
        },
        # Tags are read directly from session state (set by tag selector)
        "tags": state["asset_tags"],
    }

    return asset_metadata
```

### 3.14. `components/view_form.py`

```python
"""
View-level form component.

Handles the per-view fields for an asset. Each view includes:
- View type (elevation / plan / section / detail)
- Orientation (optional)
- Scale and view name (optional)
- Description
- Sketch upload
- CAD upload
"""

import uuid
from typing import List, Dict, Any, Tuple

import streamlit as st

from components.file_uploaders import sketch_uploader, cad_uploader
from constants.view_types import VIEW_TYPES, ORIENTATIONS
from state.session_state import get_state
from utils.validators import normalize_text_field

def _create_empty_view() -> Dict[str, Any]:
    """
    Create a new empty view structure with a unique ID.

    Returns:
        dict: View dictionary with minimal structure:
              {"id": <view_id>, "data": {}}
    """
    return {
        "id": f"view_{uuid.uuid4().hex[:6]}",
        "data": {}
    }


def render_view_section() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Render the 'Add Views' section and return structured view data.

    This function:
        - Allows adding multiple views via an "Add New View" button.
        - For each existing view, renders an expander with its fields.
        - Binds all widget values to unique keys using the view's ID.
        - Returns a list of fully populated view dictionaries.

    Returns:
        list[dict]: List of view dictionaries containing metadata and file objects.
    """
    state = get_state()

    st.markdown("## 4. Add Views (Sketch + CAD)")

    # On click, append a new empty view to session state
    if st.button("➕ Add New View"):
        state["views"].append(_create_empty_view())

    all_views_metadata: List[Dict[str, Any]] = []
    all_views_files: List[Dict[str, Any]] = []

    # Iterate over existing views in session state and render one section per view
    for view in state["views"]:
        view_id = view["id"]

        with st.expander(f"📐 View: {view_id}", expanded=False):
            # View metadata
            col1, col2 = st.columns(2)

            with col1:
                view_type = st.selectbox(
                    "View Type",
                    VIEW_TYPES,
                    key=f"{view_id}_type"
                )
                orientation_raw = st.selectbox(
                    "Orientation (optional)",
                    ORIENTATIONS,
                    key=f"{view_id}_orientation"
                )
                # Normalize "None" to actual None
                orientation = None if orientation_raw == "None" else orientation_raw

            with col2:
                scale = st.text_input(
                    "Scale (optional, e.g., 1:50)",
                    key=f"{view_id}_scale"
                )
                view_name = st.text_input(
                    "View Name (optional)",
                    key=f"{view_id}_name"
                )

            description = st.text_area(
                "Description (optional)",
                key=f"{view_id}_desc"
            )

            st.markdown("### Upload Files")

            # File uploads are just raw UploadedFile objects for now;
            # later they will be serialized or passed to backend for storage.
            sketch_file = sketch_uploader(key=f"{view_id}_sketch")
            cad_file = cad_uploader(key=f"{view_id}_cad")

            # Store the collected values back into the 'data' field
            view_metadata = {
                "view_type": view_type,
                "orientation": orientation,
                "scale": scale or None,
                "view_name": normalize_text_field(view_name, to_lower=False) or None,
                "description": description or None,
            }
            
            # Raw files objects kept separate for multipart upload
            view_files = {
                "sketch_file": sketch_file,
                "cad_file": cad_file,
            }

            all_views_metadata.append(view_metadata)
            all_views_files.append(view_files)

    return all_views_metadata, all_views_files
```

### 3.15. `app.py`

```python
"""
Main Streamlit application entrypoint for Archimera UI.

This file wires together the high-level layout, tabs, and form components.
All heavy lifting is delegated to functions in the `components`, `state`,
and `constants` modules.
"""

import streamlit as st

from components.asset_form import render_asset_form
from components.view_form import render_view_section
from services import asset_api, view_api
from state.session_state import init_session_state
from state.form_serializers import build_submission_payload
from constants.config import APP_TITLE


def main() -> None:
    """
    Main function that builds the Streamlit UI.

    This function:
        - Configures the page.
        - Initializes session state.
        - Renders two main tabs:
            1. Asset Addition
            2. Asset Retrieval (placeholder for now)
        - Handles "Submit" action for asset addition.
    """
    # Basic page configuration
    st.set_page_config(page_title=APP_TITLE, layout="wide")

    # Make sure all session state keys exist
    init_session_state()

    st.title("🗂️ Archimera — Asset Management Console")

    # Two main tabs: one for data collection, one for retrieval
    tab_add, tab_search = st.tabs(["➕ Asset Addition", "🔍 Asset Retrieval"])

    # -----------------------------
    # TAB: Retrieval (placeholder)
    # -----------------------------
    with tab_search:
        st.header("🚧 Asset Retrieval")
        st.info("This module is currently in development. Chill, it’s coming.")

    # -----------------------------
    # TAB: Asset Addition (active)
    # -----------------------------
    with tab_add:
        st.subheader("Add a New Asset")

        # Render forms for asset metadata and view data
        asset_metadata = render_asset_form()
        view_metadata_list, view_files_list = render_view_section()

        # Action button to "submit" the asset (mock only for now)
        if st.button("🚀 Submit Asset (Mock — nothing is stored)"):
            # payload = build_submission_payload(asset_metadata, views)
            # st.success("Form validated! (Mock submission — no persistence yet).")
            # st.json(payload)
            # * Responsive Devs
            # 1. Create Asset
            asset_resp = asset_api.create_asset(asset_metadata)
            asset_id = asset_resp["id"]

            # 2. Create each view with metadata + files
            for meta, files in zip(view_metadata_list, view_files_list):
                view_api.create_view(asset_id, meta, files)
            
            st.success(f"Asset {asset_id} and {len(view_metadata_list)} views submitted.")


if __name__ == "__main__":
    main()
```