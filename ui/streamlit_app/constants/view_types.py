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

# Studio from where this is getting uploaded
STUDIOS = ["B1", "B2", "F1", "F2", "S1", "S2"]

# Category of the asset being uploaded
CATEGORY = ["wardrobe", "chair", "table"]

# Room type where the asset to be deployed
ROOM_TYPE = ["bedroom", "master bedroom", "kids room", "kitchen", "living room", "guest room", "hall", "office space", "Unknown"]

# Style of the asset
STYLE = ["modern", "contemporary", "classic", "minimal", "Unknown"]