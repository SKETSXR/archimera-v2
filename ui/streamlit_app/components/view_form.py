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
