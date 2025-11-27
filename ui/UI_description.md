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
            help_texts.py
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

# Category of the asset being uploaded
CATEGORY = ["wardrobe", "chair", "table"]

# Room type where the asset to be deployed
ROOM_TYPE = ["bedroom", "master bedroom", "kids room", "kitchen", "living room", "guest room", "hall", "office space", "Unknown"]

# Style of the asset
STYLE = ["modern", "contemporary", "classic", "minimal", "Unknown"]
```

### 3.3. `constants/help_texts.py`

```python
"""
Help text templates for UI fields.

This module centralizes multi-line help strings for each user-facing field.
The goal is:
- Single source of truth for descriptions, examples, and restrictions.
- Reusable, structured & readable help content.
"""

from typing import Iterable, Optional

def build_help_text(
    description: str,
    examples: Optional[Iterable[str]] = None,
    restrictions: Optional[Iterable[str]] = None,
) -> str:
    """
    Build a formatted multi-line help string for Streamlit's `help=` parameter.

    Format (Markdown):

        Description: ...
        Examples:
        - ...
        - ...
        Restrictions:
        - ...
        - ...

    Args:
        description: Short, human-readable explanation of the field.
        examples: Optional iterable of example values.
        restrictions: Optional iterable of constraints, rules, or notes.

    Returns:
        A multi-line Markdown string suitable for use as `help=` in Streamlit widgets.
    """
    lines: list[str] = []

    # Description
    lines.append(f"**Description:** {description}")

    # Example values
    if examples:
        lines.append("")  # blank line
        lines.append("**Examples:**")
        for ex in examples:
            lines.append(f"- `{ex}`")

    # Restrictions / rules
    if restrictions:
        lines.append("")
        lines.append("**Restrictions:**")
        for r in restrictions:
            lines.append(f"- {r}")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Asset-level field help texts
# ---------------------------------------------------------------------------

CLIENT_NAME_HELP = build_help_text(
    description="Name of Client to which the project was delivered.",
    examples=["Acme Corp", "Ravi Sharma", "Mr. Lopez"],
    restrictions=[
        "This will be stored as-is and may appear in reports.",
        "Maximum allowed characters: 100"
    ]
)

PROJECT_NAME_HELP = build_help_text(
    description="Name of the Project",
    examples=["EASTWOOD RESIDENCE 14-16 STEWART ST EASTWOOD", "THE BRISTOL EMAAR BEACHFRONT TOWER (1B+G+8P+48F)"],
    restrictions=[
        "This will be stored as-is and may appear in reports.",
        "Maximum allowed characters: 256",
        "Please refer to the right end of the CAD file to view the Project Name."
    ]
)

CATEGORY_HELP = build_help_text(
    description="High-level asset category describing what is being designed.",
    examples=["wardrobe", "chair", "table"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option."
    ]
)

SUBCATEGORY_HELP = build_help_text(
    description="More specific type within the category.",
    examples=["walk in", "corner", "study table"],
    restrictions=[
        "Use only lowercase letters and spaces.",
        "Maximum allowed characters: 64",
        "If not known, leave it blank."
    ]
)

PROJECT_TYPE_HELP = build_help_text(
    description="Type of project based on usage context.",
    examples=["residential", "commercial", "hospitality", "office"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option."
    ]
)

ROOM_TYPE_HELP = build_help_text(
    description="Room where this asset is primarily installed.",
    examples=["bedroom", "master bedroom", "kids room", "kitchen"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option.",
        "Select Unknown only if you have no information about room type.",
    ]
)

STYLE_HELP = build_help_text(
    description="Design style associated with the asset.",
    examples=["modern", "contemporary", "classic", "minimal"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option.",
        "Select Unknown only if you have no information about style.",
    ]
)

STUDIO_HELP = build_help_text(
    description="Internal studio code of the person uploading this asset.",
    examples=["B1", "B2", "S1"],
    restrictions=[
        "Can only select from the drop-down"
    ]
)

UPLOADED_BY_HELP = build_help_text(
    description="Name of the Person who is uploading the asset.",
    examples=["Ayush Kumar", "Sachin Maurya"],
    restrictions=[
        "Only use letters and spaces",
        "Format: <First Name><space><Last Name>",
        "Maximum Allowed Characters: 100"
    ]
)

CREATED_BY_HELP = build_help_text(
    description="Name of Person or Team who originally designed/delivered this asset.",
    examples=["Ayush Kumar", "Mirage Inc Consultants"],
    restrictions=[
        "Can be different from Uploaded By.",
        "If not known, leave the default value `Unknown` as-is",
        "Maximum Allowed Characters: 256"
    ]
)

# ---------------------------------------------------------------------------
# Location field help texts
# ---------------------------------------------------------------------------

COUNTRY_HELP = build_help_text(
    description="Country where the project is located.",
    examples=["India", "United Arab Emirates", "Singapore"],
    restrictions=[
        "Use full country names (no 2-letter codes).",
        "Maximum allowed characters: 56"
    ]
)

STATE_REGION_HELP = build_help_text(
    description="State or region of the project location.",
    examples=["Maharashtra", "Karnataka", "Dubai", "Bavaria"],
    restrictions=[
        "Use the state/region name as commonly written.",
        "Maximum allowed characters: 58",
        "If not known, leave it blank."
    ]
)

CITY_HELP = build_help_text(
    description="City where the project site is located.",
    examples=["Mumbai", "Bengaluru", "Pune"],
    restrictions=[
        "Should be actual city / town name.",
        "Maximum allowed characters: 100",
        "If not known, leave it blank."
    ]
)

LOCALITY_HELP = build_help_text(
    description="Locality or neighborhood for finer-grained location.",
    examples=["Andheri West", "Baner", "HSR Layout"],
    restrictions=[
        "If not known, leave the default value Unknown as-is.",
        "Maximum Allowed Characters: 100",
        "If not known, leave it blank."
    ]
)

POSTAL_CODE_HELP = build_help_text(
    description="Postal Code / ZIP code of the project location.",
    examples=["400053", "560102"],
    restrictions=[
        "Maximum allowed characters: 10",
        "If not known, leave it blank."
    ]
)


# ---------------------------------------------------------------------------
# View-level field help texts
# ---------------------------------------------------------------------------

VIEW_TYPE_HELP = build_help_text(
    description="Type of drawing view for this asset instance.",
    examples=["elevation", "plan", "section"],
    restrictions=[
        "Must be chosen from the drop-down",
        "If suitable option not found, please contact admin for adding options."
    ]
)

ORIENTATION_HELP = build_help_text(
    description="Orientation of this view in the global layout.",
    examples=["North", "South", "East", "West"],
    restrictions=[
        "Can only select from drop-down",
        "Leave blank if not sure."
    ]
)

SCALE_HELP = build_help_text(
    description="Drawing to real-world scale ratio.",
    examples=["1:20", "1:50", "1:100"],
    restrictions=[
        "Leave blank if not known",
        "The template is <Drawing><:><Real World>"
    ]
)

VIEW_NAME_HELP = build_help_text(
    description="Human-friendly name for this view.",
    examples=["Elevation A", "Section BB", "Wardrobe Front View"],
    restrictions=[
        "Only use alphabets and spaces",
        "Likely to be mentioned at the bottom of the specific view.",
        "Maximum allowed characters: 100",
        "Leave blank if not sure"
    ]
)

VIEW_DESCRIPTION_HELP = build_help_text(
    description="Short description of what this view represents or highlights.",
    examples=[
        "Front elevation of master bedroom wardrobe.",
        "Plan view showing wardrobe + study table integration."
    ],
    restrictions=[
        "Keep it short (single sentence).",
        "Maximum allowed characters: 256",
        "Leave blank if not sure."
    ]
)

SKETCH_UPLOAD_HELP = build_help_text(
    description="Sketch corresponding to this view.",
    examples=["Client hand-drawn sketch", "Internal conceptual sketch"],
    restrictions=[
        "PNG / JPG / JPEG / PDF allowed.",
        "PNG is preferred",
        "Refrain to upload if any format other than the above mentioned ones, and inform admin of the format, such that it can be added later."
    ]
)

CAD_UPLOAD_HELP = build_help_text(
    description="Final CAD file (DWG) for this view.",
    examples=["AutoCAD .dwg file exported from your CAD workstation"],
    restrictions=[
        "Only .dwg files are allowed.",
        "Refrain from uploading any other format files."
    ]
)
```

### 3.4. `constants/config.py`

```python
"""
Configuration constants for the Archimera UI.

This file is intentionally kept minimal; environment-specific values
(e.g., API base URL) can be wired in here later or derived from
environment variables.
"""

APP_TITLE: str = "Archimera"

# Placeholder for future use (when backend API exists)
API_BASE_URL: str = "http://localhost:8000"
```

### 3.5. `state/session_state.py`

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

### 3.6. `state/form_serializers.py`

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

### 3.7. `utils/file_utils.py`

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

### 3.8. `utils/validators.py`

```python
"""
Validation helpers for form inputs and uploaded files.
"""

from typing import Any, Dict, List, Optional, Tuple

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


def validate_data(asset_metadata: Dict[str, Any]) -> Tuple[bool, str]:
    """
    A function which will validate user entered data and check for corrections if any.

    Args:
        asset_metadata: User entered information about assets.
    
    Returns:
        bool:
            True if data is correct and in sync with the format.
            False if there are inconsistencies.
        str:
            OK if bool is True
            Message describing the issue if bool is False.
    """
    # Checking Asset Level Metadata for correctness
    if len(asset_metadata["client_name"]) == 0:
        return (False, "Client Name can not be Empty.")
    if len(asset_metadata["project_name"]) == 0:
        return (False, "Project Name can not be Empty.")
    if len(asset_metadata["uploaded_by"]) == 0:
        return (False, "Please add your name in Uploaded By.")
    if asset_metadata["studio"] is None:
        return (False, "Please select your Studio.")
    if len(asset_metadata["location"]["country"]) == 0:
        return (False, "Country of Project cannot be Empty.")
    return (True, "OK")
```

### 3.9. `services/http_client.py`

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

### 3.10. `services/asset_api.py`

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

### 3.11. `services/view_api.py`

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

### 3.12. `components/tag_selector.py`

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

### 3.13. `components/file_uploaders.py`

```python
"""
File uploader components.

This module defines thin wrapper functions around Streamlit file uploaders,
keeping validation and configuration in a single place.
"""

import streamlit as st
from utils.validators import validate_dwg

def sketch_uploader(key: str, help: str):
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
        help=help
    )
    return file

def cad_uploader(key: str, help: str):
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
        help=help
    )

    # Run a simple validation to ensure correct file type/extension
    validate_dwg(file)
    return file
```

### 3.14. `components/asset_form.py`

```python
"""
Asset-level form component.

This module renders all fields that are captured once per asset:
client, project, location, project type, style, and asset-level tags.
"""

import streamlit as st
from typing import Dict, Any

from components.tag_selector import render_tag_selector
from constants.view_types import PROJECT_TYPES, STUDIOS, CATEGORY, ROOM_TYPE, STYLE
from constants.help_texts import CLIENT_NAME_HELP, PROJECT_NAME_HELP, CATEGORY_HELP, SUBCATEGORY_HELP, PROJECT_TYPE_HELP, ROOM_TYPE_HELP, STYLE_HELP, STUDIO_HELP, UPLOADED_BY_HELP, CREATED_BY_HELP, COUNTRY_HELP, STATE_REGION_HELP, CITY_HELP, LOCALITY_HELP, POSTAL_CODE_HELP
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

    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    row3_col1, row3_col2, row3_col3 = st.columns(3)

    # Basic project/asset identifiers
    with row1_col1:
        client_name = st.text_input(label="Client Name :red[*]", max_chars=100, help=CLIENT_NAME_HELP, placeholder="ENTER CLIENT NAME")
    with row1_col2:
        project_name = st.text_input(label="Project Name :red[*]", max_chars=256, help=PROJECT_NAME_HELP, placeholder="ENTER PROJECT NAME")
    with row1_col3:
        category = st.selectbox(label="Category :red[*]", options=CATEGORY, index=0, help=CATEGORY_HELP)
    with row2_col1:
        subcategory = st.text_input(label="Subcategory", max_chars=64, help=SUBCATEGORY_HELP, placeholder="ENTER SUBCATEGORY")

    # Project context fields
    with row2_col2:
        project_type = st.selectbox(label="Project Type", options=PROJECT_TYPES, index=None, help=PROJECT_TYPE_HELP, placeholder="SELECT PROJECT TYPE")
    with row2_col3:
        room_type = st.selectbox(label="Room Type", options=ROOM_TYPE, index=None, help=ROOM_TYPE_HELP, placeholder="SELECT ROOM TYPE")
    with row2_col4:
        style = st.selectbox(label="style", options=STYLE, index=None, help=STYLE_HELP, placeholder="SELECT STYLE")

    # People + studio context
    with row3_col1:
        created_by = st.text_input(label="Created By", value="Unknown", max_chars=256, help=CREATED_BY_HELP)
    with row3_col2:
        uploaded_by = st.text_input(label="Uploaded By :red[*]", max_chars=100, help=UPLOADED_BY_HELP, placeholder="ENTER YOUR NAME")
    with row3_col3:
        studio = st.selectbox(label="Studio :red[*]", options=STUDIOS, index=None, help=STUDIO_HELP, placeholder="SELECT YOUR STUDIO")

    
    # Location fields
    st.markdown("### 2. Project Location")
    row1_colL1, row1_colL2 = st.columns(2)
    row2_colL1, row2_colL2, row2_colL3 = st.columns(3)

    with row1_colL1:
        country = st.text_input(label="Country :red[*]", max_chars=56, help=COUNTRY_HELP, placeholder="ENTER COUNTRY")
    with row1_colL2:
        state_region = st.text_input(label="State / Region", max_chars=58, help=STATE_REGION_HELP, placeholder="ENTER STATE")
    with row2_colL1:
        city = st.text_input(label="City", max_chars=100, help=CITY_HELP, placeholder="ENTER CITY")
    with row2_colL2:
        locality = st.text_input(label="Locality", max_chars=100, help=LOCALITY_HELP, placeholder="ENTER LOCALITY")
    with row2_colL3:
        postal_code = st.text_input(label="Postal Code / ZIP", max_chars=10, help=POSTAL_CODE_HELP, placeholder="ENTER POSTAL CODE")
    
    # Basic non-empty checks AFTER fields are defined
    # require_non_empty("Country", country)
    # require_non_empty("State / Region", state_region)
    # require_non_empty("City", city)

    # Tag selection (predefined vocab, multi-select)
    st.markdown("### 3. Asset-Level Tags")
    render_tag_selector()

    session_state = get_state()

    category_norm = normalize_text_field(category)
    subcategory_norm = normalize_text_field(subcategory)
    # room_type_norm = normalize_text_field(room_type)
    # style_norm = normalize_text_field(style)

    # Build and return the asset metadata dictionary
    asset_metadata: Dict[str, Any] = {
        "client_name": client_name,
        "project_name": project_name,
        "category": category_norm,
        "subcategory": subcategory_norm or None,
        "project_type": project_type,
        "room_type": room_type or None,
        "style": style or None,
        "created_by": created_by or None,
        "uploaded_by": uploaded_by,
        "studio": studio or None,
        "location": {
            "country": country,
            "state": state_region,
            "city": city,
            "locality": locality or None,
            "postal_code": postal_code or None,
        },
        # Tags are read directly from session state (set by tag selector)
        "tags": session_state["asset_tags"],
    }

    return asset_metadata
```

### 3.15. `components/view_form.py`

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
from constants.help_texts import VIEW_TYPE_HELP, ORIENTATION_HELP, SCALE_HELP, VIEW_NAME_HELP, VIEW_DESCRIPTION_HELP, SKETCH_UPLOAD_HELP, CAD_UPLOAD_HELP
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
                    label="View Type :red[*]",
                    options=VIEW_TYPES,
                    help=VIEW_TYPE_HELP,
                    key=f"{view_id}_type"
                )
                orientation_raw = st.selectbox(
                    label="Orientation",
                    options=ORIENTATIONS,
                    help=ORIENTATION_HELP,
                    key=f"{view_id}_orientation"
                )
                # Normalize "None" to actual None
                orientation = None if orientation_raw == "None" else orientation_raw

            with col2:
                scale = st.text_input(
                    label="Scale",
                    help=SCALE_HELP,
                    key=f"{view_id}_scale",
                    placeholder="ENTER SCALE"
                )
                view_name = st.text_input(
                    label="View Name",
                    max_chars=100,
                    help=VIEW_NAME_HELP,
                    key=f"{view_id}_name",
                    placeholder="ENTER VIEW NAME"
                )

            description = st.text_area(
                label="Description",
                max_chars=256,
                help=VIEW_DESCRIPTION_HELP,
                key=f"{view_id}_desc"
            )

            st.markdown("### Upload Files")

            # File uploads are just raw UploadedFile objects for now;
            # later they will be serialized or passed to backend for storage.
            sketch_file = sketch_uploader(key=f"{view_id}_sketch", help=SKETCH_UPLOAD_HELP)
            cad_file = cad_uploader(key=f"{view_id}_cad", help=CAD_UPLOAD_HELP)

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

### 3.16. `app.py`

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
from utils.validators import validate_data
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
            is_valid = validate_data(asset_metadata)
            if is_valid[0]:
                payload = build_submission_payload(asset_metadata, view_metadata_list)
                st.success("Form validated! (Mock submission — no persistence yet).")
                st.json(payload)
            else:
                st.error(f"validation error: {is_valid[1]}")
            # * Responsive Devs
            # 1. Create Asset
            # asset_resp = asset_api.create_asset(asset_metadata)
            # asset_id = asset_resp["id"]

            # # 2. Create each view with metadata + files
            # for meta, files in zip(view_metadata_list, view_files_list):
            #     view_api.create_view(asset_id, meta, files)
            
            # st.success(f"Asset {asset_id} and {len(view_metadata_list)} views submitted.")


if __name__ == "__main__":
    main()
```
