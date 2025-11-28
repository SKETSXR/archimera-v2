"""
Main Streamlit application entrypoint for Archimera UI.

This file wires together the high-level layout, tabs, and form components.
All heavy lifting is delegated to functions in the `components`, `state`,
and `constants` modules.
"""

from components.asset_form import render_asset_form
from components.view_form import render_view_section
from constants.config import APP_TITLE
from services import asset_api, view_api
from state.session_state import init_session_state
import streamlit as st
from utils.validators import validate_data


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
            # if is_valid[0]:
            #     payload = build_submission_payload(asset_metadata, view_metadata_list)
            #     st.success("Form validated! (Mock submission — no persistence yet).")
            #     st.json(payload)
            # else:
            #     st.error(f"validation error: {is_valid[1]}")
            # * Responsive Devs
            if is_valid[0]:
                # 1. Create Asset
                asset_resp = asset_api.create_asset(asset_metadata)
                asset_id = asset_resp["id"]

                # 2. Create each view with metadata + files
                for meta, files in zip(view_metadata_list, view_files_list):
                    view_api.create_view(asset_id, meta, files)
                
                st.success(f"Asset {asset_id} and {len(view_metadata_list)} views submitted.")
            else:
                st.error(f"Validation Error: {is_valid[1]}")


if __name__ == "__main__":
    main()
