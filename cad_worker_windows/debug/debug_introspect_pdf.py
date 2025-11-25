"""
Debug script for wardrobe/closet detail PDFs.

- Reads the PDF exported from DWG (e.g. "Walk in Closet Detail.pdf")
- Extracts all text spans with:
    - text
    - bbox (x0, y0, x1, y1)
    - font size
    - font name

- Heuristically classifies spans into:
    - view_titles      (e.g. "TYPICAL W1 WALK-IN CLOSET DETAIL - ELEVATION")
    - component_labels (e.g. "SAFE", "SHOE LEDGE", "METAL LUGGAGE RUNNERS")
    - dims             (strings that look like dimensions: 1'-6", 5'-0", 2800, etc.)
    - codes            (hardware/material codes like "HD 214", "WD-201", "PT-309")
    - other_text       (title block, notes, legal junk, etc.)

- Writes JSON files to: <pdf_folder>/__pdf_debug__/

Goal: let you see what the PDF actually gives you so you can decide
what metadata schema to build.
"""

import json
import re
from pathlib import Path

import fitz  # PyMuPDF


# ---------- helpers ----------

def ensure_out_dir(pdf_path: str) -> Path:
    p = Path(pdf_path)
    out = p.parent / "__pdf_debug__"
    out.mkdir(exist_ok=True)
    return out


def save_json(out_dir: Path, name: str, data):
    path = out_dir / name
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[+] Wrote {path}")
    return path


def classify_span(text: str) -> str:
    """
    Very rough classification just to separate things for inspection.
    Tweak this after you look at the output.
    """
    t = text.strip()

    if not t:
        return "empty"

    upper = t.upper()

    # View titles (you can extend this)
    if "WALK-IN CLOSET DETAIL" in upper or "WARDROBE DETAIL" in upper:
        return "view_title"
    if upper.startswith("SCALE:") and "DETAIL" in upper:
        return "view_title"

    # Component labels – all-uppercase, few spaces, not too long
    if upper == t and len(t) <= 40 and any(w in upper for w in [
        "SAFE", "DRAWER", "LEDGE", "HANG ROD", "IRON BOARD",
        "METAL LUGGAGE", "CLOSET", "UNIT"
    ]):
        return "component_label"

    # Dimension-ish: feet/inches (1'-6", 3'-8 3/4", 11", 2800, etc.)
    dim_like = bool(re.search(r"(\d+'\-\d+\"|\d+'\s*\-\s*\d+\s*\d*/\d+\"|\d+\"|\d+\.\d+|\d+'\-\d+)", t))
    just_numbers = bool(re.fullmatch(r"[0-9\-\s'/\.]+", t))
    if dim_like or just_numbers:
        return "dimension"

    # Codes like HD 214, WD-201, PT-309, MT-100, WC-206, etc.
    if re.fullmatch(r"[A-Z]{2,3}[- ]?\d{2,4}", upper):
        return "code"

    return "other_text"


def collect_page_data(page):
    raw = page.get_text("dict")
    spans = []
    for bi, block in enumerate(raw.get("blocks", [])):
        if block.get("type", 0) != 0:
            continue  # ignore non-text blocks

        for li, line in enumerate(block.get("lines", [])):
            for si, span in enumerate(line.get("spans", [])):
                text = span.get("text", "").strip()
                if not text:
                    continue

                bbox = list(span.get("bbox", []))  # [x0, y0, x1, y1]
                size = span.get("size", None)
                font = span.get("font", None)
                category = classify_span(text)

                spans.append({
                    "text": text,
                    "bbox": bbox,
                    "size": size,
                    "font": font,
                    "block_index": bi,
                    "line_index": li,
                    "span_index": si,
                    "category": category,
                })

    w, h = page.rect.width, page.rect.height
    return {
        "page_number": page.number,
        "page_width": w,
        "page_height": h,
        "spans": spans,
    }


def main():
    # TODO: point this at "Walk in Closet Detail.pdf"
    pdf_path = r"C:\\Users\\ayushkum\\Desktop\\Ayush\\Latest Details\\CLOSET 2\\Final Output\\Walk in Closet Detail.pdf"

    out_dir = ensure_out_dir(pdf_path)

    doc = fitz.open(pdf_path)
    print(f"Opened PDF: {pdf_path} ({len(doc)} pages)")

    index_summary = []

    for i, page in enumerate(doc): # type: ignore
        page_data = collect_page_data(page)
        filename = f"page_{i:02d}_text.json"
        save_json(out_dir, filename, page_data)

        # quick summary for that page
        cats = {}
        for s in page_data["spans"]:
            cats.setdefault(s["category"], 0)
            cats[s["category"]] += 1

        example_texts = [s["text"] for s in page_data["spans"][:40]]

        index_summary.append({
            "page": i,
            "num_spans": len(page_data["spans"]),
            "category_counts": cats,
            "examples": example_texts,
        })

    save_json(out_dir, "_index.json", index_summary)

    print("\nDone.")
    print(f"Check folder: {out_dir}")
    print("- _index.json          -> overview")
    print("- page_XX_text.json    -> full text + positions + category")


if __name__ == "__main__":
    main()
