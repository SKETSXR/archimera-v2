"""
View- and project-related constant lists for form dropdowns.

These lists keep the UI consistent and avoid magic strings sprinkled
throughout the code.
"""

# Supported view types for each view (per asset)
VIEW_TYPES = ["elevation", "plan", "section", "detail"]

# Supported orientations; "None" is used to represent "not specified"
ORIENTATIONS = ["None", "North", "South", "East", "West"]

# Project type options for asset-level metadata
PROJECT_TYPES = ["residential", "commercial", "hospitality", "office"]
