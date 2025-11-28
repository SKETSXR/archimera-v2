"""
Configuration constants for the Archimera UI.

This file is intentionally kept minimal; environment-specific values
(e.g., API base URL) can be wired in here later or derived from
environment variables.
"""
import os

APP_TITLE: str = "Archimera"

# Placeholder for future use (when backend API exists)
API_BASE_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
