import requests

from constants.config import API_BASE_URL

def post(path: str, json=None, files=None, data=None):
    """
    Simple HTTP POST wrapper for talking to the backend API.

    Args:
        path: API path.
        json: JSON-serializable body
        files: dict for multipart file uploads.
        data: dict for form fields.
    
    Returns:
        Response object.
    
    Raises:
        requests.HTTPError if status is not OK.
    """
    url = f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    resp = requests.post(url, json=json, files=files, data=data)
    resp.raise_for_status()
    return resp