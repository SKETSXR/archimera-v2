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
