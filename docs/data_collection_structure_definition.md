# Introduction

This document will detail the structure which has been defined for collecting data for Archimera. This structure will be a step towards building a searchable library.

## Objective

Define a fixed, scalable, and unambiguous structure for collecting all asset-related data within Archimera.  
This structure will guide how users upload, categorize, and annotate design assets (sketches and CAD files) and ensure clean ingestion into our retrieval + ML pipeline.

## Scope

We are standardizing **three layers** of data:

1. Asset-level metadata
2. View-level metadata
3. System-generated metadata (worker + ML pipeline)

This structure will be followed uniformly across all data collection, ensuring every future asset is usable for CAD retrieval, embedding generation, and supervised S/T/C dataset building.

## 1. Asset-Level Fields (Captured Once per Asset)

These fields describe the project/design as a whole:

* Client Name
* Project Name
* Category (e.g., wardrobe, kitchen, chair, table)
* Subcategory (e.g., hinged, sliding, corner) - optional
* Project Type (residential / commercial / hospitality / office) - more options can be added.
* Room Type (bedroom, master bedroom, kitchen, etc) - can be optional
* Style (e.g., modern, contemporary, classic) - optional

### Structured Location

* Country
* State / Region
* City
* Locality - optional
* Postal Code / ZIP code - optional

### Ownership / People

* Created By (The person who delivered the asset) - optional
* Uploaded By (The person who is uploading this asset)
* Studio of person uploading the asset (e.g., B2, F1, S1) - optional

### Asset-Level Tags

These will be stored as `{"Category":"Value"}`

* Category (e.g., Materials, UseCase)
* Value (e.g., Solid Wood, Wardrobe)

### Timestamps (System generated)

* Uploaded At
* Updated At

## 2. View-Level Fields (Captured Per View: sketch + CAD)

Every asset contains multiple views (plan, elevation, section, detail).

### Identity

* View Type (elevation / plan / section / detail) - more can be added later
* Orientation (north / south / east / west) - optional
* Scale (will have to enter in `drawing:original` form) - optional
* View Name - optional

### Files

Each view contains:

* Sketch upload (prefered PNG but okay with any image format or even pdf)
* CAD upload (DWG)
* CAD upload (pdf) - might not be necessary
* Rasterized CAD (PNG) - generated, not user uploaded
* CAD Metadata (JSON) - generated, not user uploaded

### View Description

* Description (a small user provided summary for richer embedding context) - optional

### Processing Fields (System Generated)

* Status (Pending processing / Ready for Embedding / Embedded / Error)
* Last Processing Error - optional
* Timestamps

## 3. Embedding / ML Metadata (System-Generated)

These would not be provided by the user, but they are part of the schema.

Each view gets a record containing:

* Input Text Embedding - Generated from Tags.
* Input Sketch Embedding - Generated from Sketch.
* Output CAD Embedding - Generated from raster PNG and text metadata.
* Model Version - The model version to track changes.
* FAISS Index ID - The FAISS ID for the respective embedding in FAISS index file.

## 4. Why this Structure Matters

* Provides a **consistent schema** for ingesting all new data.
* Prevents accumulation of messy or incomplete assets.
* Enables clean mapping to:
  * NAS storage (or any other local storage)
  * MongoDB collections
  * Windows CAD worker
  * Embedding pipeline
  * Retrieval training dataset
* Ensures every dataset sample gets the required **S** (sketch), **T** (tag-text), **C** (CAD metadata) representation.

## 5. Class Definitions (practical version)

We will define some Pydantic models to represent Data Collection:

### Helper functions

```python
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
```

### File Reference

```python
class FileRef(BaseModel):
    rel_path: str
    content_type: str
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None # e.g. sha256, good for dedupe
```

### Tags

```python
class Tag(BaseModel):
    category: str # e.g. "Materials"
    value: str # e.g. "Solid Wood"
```

### Project Location

```python
class ProjectLocation(BaseModel):
    country: str
    state: str
    city: str
    locality: Optional[str] = None
    postal_code: Optional[str] = None
```

### Asset

```python
class Asset(BaseModel):
    id: str = Field(alias="_id") # maps to Mongo _id
    client_name: str
    project_name: str

    category: str # "wardrobe", "kitchen", etc.
    subcategory: Optional[str] = None # "hinged", "sliding", ...

    location: ProjectLocation
    project_type: Literal["residential", "commercial", "hospitality", "office"]
    room_type: Optional[str] = None # "bedroom", "kitchen", ...

    style: Optional[str] = None # "modern", "classic", ...

    created_by: Optional[str] # person who delivered the asset
    uploaded_by: str # person who is uploading the asset
    studio: Literal["B1", "B2", "S1", "F1"] # more can be added

    uploaded_at: datetime
    updated_at: datetime
```

### View Files

```python
class ViewFiles(BaseModel):
    sketch: Optional[FileRef] = None
    cad: Optional[FileRef] = None
    raster: Optional[FileRef] = None # filled by worker
    metadata: Optional[FileRef] = None # filled by worker
```

### View

```python
class View(BaseModel):
    id: str = Field(alias="_id")
    asset_id: str

    view_type: Literal["elevation", "plan", "section", "detail"] # more can be added
    orientation: Optional[Literal["North", "East", "West", "South"]] = None
    scale: Optional[str] = None # Template sketch:original
    view_name: Optional[str] = None

    files: ViewFiles
    description: Optional[str] = None

    status: Literal["Pending Processing", "Ready for Embedding", "Embedded", "Error"] = "Pending Processing"
    last_processing_error: Optional[str] = None
```

### Embedding Vector

```python
class EmbeddingVector(BaseModel):
    vector: List[float]
    dim: int
    faiss_id: Optional[int] = None
```

### Embedding Document

```python
class EmbeddingDoc(BaseModel):
    id: str = Field(alias="_id")
    asset_id: str
    view_id: str
    model_version: str

    input_embedding: Optional[EmbeddingVector] = None
    output_embedding: Optional[EmbeddingVector] = None

    created_at: datetime
    updated_at: datetime
```
