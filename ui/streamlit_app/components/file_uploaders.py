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