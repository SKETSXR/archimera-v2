"""
Help text templates for UI fields.

This module centralizes multi-line help strings for each user-facing field.
The goal is:
- Single source of truth for descriptions, examples, and restrictions.
- Reusable, structured & readable help content.
"""

from typing import Iterable, Optional

def build_help_text(
    description: str,
    examples: Optional[Iterable[str]] = None,
    restrictions: Optional[Iterable[str]] = None,
) -> str:
    """
    Build a formatted multi-line help string for Streamlit's `help=` parameter.

    Format (Markdown):

        Description: ...
        Examples:
        - ...
        - ...
        Restrictions:
        - ...
        - ...

    Args:
        description: Short, human-readable explanation of the field.
        examples: Optional iterable of example values.
        restrictions: Optional iterable of constraints, rules, or notes.

    Returns:
        A multi-line Markdown string suitable for use as `help=` in Streamlit widgets.
    """
    lines: list[str] = []

    # Description
    lines.append(f"**Description:** {description}")

    # Example values
    if examples:
        lines.append("")  # blank line
        lines.append("**Examples:**")
        for ex in examples:
            lines.append(f"- `{ex}`")

    # Restrictions / rules
    if restrictions:
        lines.append("")
        lines.append("**Restrictions:**")
        for r in restrictions:
            lines.append(f"- {r}")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Asset-level field help texts
# ---------------------------------------------------------------------------

CLIENT_NAME_HELP = build_help_text(
    description="Name of Client to which the project was delivered.",
    examples=["Acme Corp", "Ravi Sharma", "Mr. Lopez"],
    restrictions=[
        "This will be stored as-is and may appear in reports.",
        "Maximum allowed characters: 100"
    ]
)

PROJECT_NAME_HELP = build_help_text(
    description="Name of the Project",
    examples=["EASTWOOD RESIDENCE 14-16 STEWART ST EASTWOOD", "THE BRISTOL EMAAR BEACHFRONT TOWER (1B+G+8P+48F)"],
    restrictions=[
        "This will be stored as-is and may appear in reports.",
        "Maximum allowed characters: 256",
        "Please refer to the right end of the CAD file to view the Project Name."
    ]
)

CATEGORY_HELP = build_help_text(
    description="High-level asset category describing what is being designed.",
    examples=["wardrobe", "chair", "table"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option."
    ]
)

SUBCATEGORY_HELP = build_help_text(
    description="More specific type within the category.",
    examples=["walk in", "corner", "study table"],
    restrictions=[
        "Use only lowercase letters and spaces.",
        "Maximum allowed characters: 64",
        "If not known, leave it blank."
    ]
)

PROJECT_TYPE_HELP = build_help_text(
    description="Type of project based on usage context.",
    examples=["residential", "commercial", "hospitality", "office"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option."
    ]
)

ROOM_TYPE_HELP = build_help_text(
    description="Room where this asset is primarily installed.",
    examples=["bedroom", "master bedroom", "kids room", "kitchen"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option.",
        "Select Unknown only if you have no information about room type.",
    ]
)

STYLE_HELP = build_help_text(
    description="Design style associated with the asset.",
    examples=["modern", "contemporary", "classic", "minimal"],
    restrictions=[
        "Can only select from the drop-down",
        "If you do not find the appropriate option, please contact admin for adding the option.",
        "Select Unknown only if you have no information about style.",
    ]
)

STUDIO_HELP = build_help_text(
    description="Internal studio code of the person uploading this asset.",
    examples=["B1", "B2", "S1"],
    restrictions=[
        "Can only select from the drop-down"
    ]
)

UPLOADED_BY_HELP = build_help_text(
    description="Name of the Person who is uploading the asset.",
    examples=["Ayush Kumar", "Sachin Maurya"],
    restrictions=[
        "Only use letters and spaces",
        "Format: <First Name><space><Last Name>",
        "Maximum Allowed Characters: 100"
    ]
)

CREATED_BY_HELP = build_help_text(
    description="Name of Person or Team who originally designed/delivered this asset.",
    examples=["Ayush Kumar", "Mirage Inc Consultants"],
    restrictions=[
        "Can be different from Uploaded By.",
        "If not known, leave the default value `Unknown` as-is",
        "Maximum Allowed Characters: 256"
    ]
)

# ---------------------------------------------------------------------------
# Location field help texts
# ---------------------------------------------------------------------------

COUNTRY_HELP = build_help_text(
    description="Country where the project is located.",
    examples=["India", "United Arab Emirates", "Singapore"],
    restrictions=[
        "Use full country names (no 2-letter codes).",
        "Maximum allowed characters: 56"
    ]
)

STATE_REGION_HELP = build_help_text(
    description="State or region of the project location.",
    examples=["Maharashtra", "Karnataka", "Dubai", "Bavaria"],
    restrictions=[
        "Use the state/region name as commonly written.",
        "Maximum allowed characters: 58",
        "If not known, leave it blank."
    ]
)

CITY_HELP = build_help_text(
    description="City where the project site is located.",
    examples=["Mumbai", "Bengaluru", "Pune"],
    restrictions=[
        "Should be actual city / town name.",
        "Maximum allowed characters: 100",
        "If not known, leave it blank."
    ]
)

LOCALITY_HELP = build_help_text(
    description="Locality or neighborhood for finer-grained location.",
    examples=["Andheri West", "Baner", "HSR Layout"],
    restrictions=[
        "If not known, leave the default value Unknown as-is.",
        "Maximum Allowed Characters: 100",
        "If not known, leave it blank."
    ]
)

POSTAL_CODE_HELP = build_help_text(
    description="Postal Code / ZIP code of the project location.",
    examples=["400053", "560102"],
    restrictions=[
        "Maximum allowed characters: 10",
        "If not known, leave it blank."
    ]
)


# ---------------------------------------------------------------------------
# View-level field help texts
# ---------------------------------------------------------------------------

VIEW_TYPE_HELP = build_help_text(
    description="Type of drawing view for this asset instance.",
    examples=["elevation", "plan", "section"],
    restrictions=[
        "Must be chosen from the drop-down",
        "If suitable option not found, please contact admin for adding options."
    ]
)

ORIENTATION_HELP = build_help_text(
    description="Orientation of this view in the global layout.",
    examples=["North", "South", "East", "West"],
    restrictions=[
        "Can only select from drop-down",
        "Leave blank if not sure."
    ]
)

SCALE_HELP = build_help_text(
    description="Drawing to real-world scale ratio.",
    examples=["1:20", "1:50", "1:100"],
    restrictions=[
        "Leave blank if not known",
        "The template is <Drawing><:><Real World>"
    ]
)

VIEW_NAME_HELP = build_help_text(
    description="Human-friendly name for this view.",
    examples=["Elevation A", "Section BB", "Wardrobe Front View"],
    restrictions=[
        "Only use alphabets and spaces",
        "Likely to be mentioned at the bottom of the specific view.",
        "Maximum allowed characters: 100",
        "Leave blank if not sure"
    ]
)

VIEW_DESCRIPTION_HELP = build_help_text(
    description="Short description of what this view represents or highlights.",
    examples=[
        "Front elevation of master bedroom wardrobe.",
        "Plan view showing wardrobe + study table integration."
    ],
    restrictions=[
        "Keep it short (single sentence).",
        "Maximum allowed characters: 256",
        "Leave blank if not sure."
    ]
)

SKETCH_UPLOAD_HELP = build_help_text(
    description="Sketch corresponding to this view.",
    examples=["Client hand-drawn sketch", "Internal conceptual sketch"],
    restrictions=[
        "PNG / JPG / JPEG / PDF allowed.",
        "PNG is preferred",
        "Refrain to upload if any format other than the above mentioned ones, and inform admin of the format, such that it can be added later."
    ]
)

CAD_UPLOAD_HELP = build_help_text(
    description="Final CAD file (DWG) for this view.",
    examples=["AutoCAD .dwg file exported from your CAD workstation"],
    restrictions=[
        "Only .dwg files are allowed.",
        "Refrain from uploading any other format files."
    ]
)