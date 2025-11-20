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
