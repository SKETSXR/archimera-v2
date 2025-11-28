"""
Tag vocabulary for Archimera.

This module defines the complete set of selectable tags grouped by
semantic categories. The UI uses this dictionary to render multi-select
controls and ensure consistent tagging.
"""

TAG_OPTIONS = {
    "Materials": [
        "Solid Wood",
        "Engineered Wood",
        "Veneer",
        "Laminate",
        "Metal Frame",
        "Glass Elements",
        "Acrylic",
        "Plastic/PVC",
        "Natural Finish"
    ],
    "Doors & Panels": [
        "Sliding",
        "Hinged",
        "Bi-fold",
        "Pocket Door",
        "Mirror Door",
        "Louvered"
    ],
    "Interior / Storage": [
        "Walk-in",
        "Built-in",
        "Modular",
        "Shelves",
        "Drawers",
        "Hanging",
        "Shoe Storage",
        "Accessory Drawer",
        "Vertical Divider"
    ],
    "Hardware / Mechanism": [
        "Soft-close",
        "Push-to-open",
        "Concealed Hinges",
        "Hydraulic Lift",
        "Integrated"
    ],
    "Finish / Aesthetics": [
        "Matte Finish",
        "High Gloss",
        "Textured Finish",
        "Two-Tone",
        "Hand-Painted",
        "Distressed/Vintage"
    ],
    "Use-case": [
        "Wardrobe",
        "Linen Closet",
        "Wardrobe + Desk",
        "Kids",
        "Walk-through"
    ],
    "Environment / Performance": [
        "Moisture Resistant",
        "Fire-Rated",
        "Eco-friendly",
        "Acoustic Lining"
    ],
    "Size / Configuration": [
        "Corner Unit",
        "Floor-to-Ceiling",
        "Half-height",
        "Custom Width"
    ],
    "Accessories / Extras": [
        "Pull-out Mirror",
        "Lazy Susan",
        "Tie / Belt Rack",
        "Pull-out Ironing Board",
        "Valet Rod"
    ],
    "Style": [
        "Contemporary",
        "Minimal",
        "Scandinavian",
        "Industrial",
        "Traditional",
        "Transitional"
    ]
}
