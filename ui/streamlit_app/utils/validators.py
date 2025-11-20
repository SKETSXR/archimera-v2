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
