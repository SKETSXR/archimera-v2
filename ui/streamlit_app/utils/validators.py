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
