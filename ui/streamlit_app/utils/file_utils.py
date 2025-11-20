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
