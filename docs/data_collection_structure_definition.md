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
