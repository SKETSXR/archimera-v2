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
