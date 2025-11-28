"""
Tag selector component.

Renders multi-select inputs for each tag category based on TAG_OPTIONS,
and synchronizes the selected tags into `st.session_state["asset_tags"]`
in a normalized {category, value} format.
"""

from constants.tag_vocab import TAG_OPTIONS
from state.session_state import get_state
import streamlit as st


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
