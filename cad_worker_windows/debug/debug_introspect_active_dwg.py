"""
Debug script to introspect the CURRENTLY OPEN drawing in AutoCAD.

What it does:
- Connects to the active AutoCAD document (assumes DWG is already open).
- Extracts:
    - Layers
    - Block references (counts + a sample of instances)
    - Text (TEXT + MTEXT)
    - Aligned dimensions
- Attempts to export a PNG raster of the current view (using PNGOUT).
- Writes everything into separate JSON files under:
    <dwg_folder>/__debug_metadata__/

Usage:
- Open a DWG in AutoCAD.
- Run this script with the same Windows user that has AutoCAD open.
"""

import json
import time
from collections import Counter
from pathlib import Path


from pyautocad import Autocad

def ensure_out_dir(doc_path: str) -> Path:
    """Checks whether DWG file path exist and creates a folder named __debug_metadata__ in parent folder to save json files and raster image.

    Args:
        doc_path (str): Path to DWG document

    Returns:
        Path: Path to the output directory where extracted stuff would be saved.
    """
    dwg_path = Path(doc_path)
    if not dwg_path.exists():
        raise RuntimeError(f"DWG path does not exist: {dwg_path}")
    
    out_dir = dwg_path.parent / "__debug_metadata__"
    out_dir.mkdir(exist_ok=True)
    return out_dir

def save_json(out_dir: Path, name: str, data: dict) -> Path:
    """Save data in a json file.

    Args:
        out_dir (Path): Path where the json file will be saved
        name (str): Name of the json file
        data (dict): Extracted data which is to be saved.

    Returns:
        Path: Path to the saved json file
    """
    path = out_dir / f"{name}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[+] Wrote {name}.json -> {path}")
    return path

def collect_layers(acad: Autocad) -> dict:
    """Extracts layer information from the DWG file.

    Args:
        acad (Autocad): The Autocad instance

    Returns:
        dict: The extracted layer information.
    """
    layers = []
    for layer in acad.doc.Layers:
        layers.append(
            {
                "name": layer.Name,
                "color": layer.Color,
                "lineweight": layer.Lineweight,
            }
        )
    return {"layers": layers}

def collect_blocks(acad: Autocad) -> dict:
    """Extracts block information from the DWG file.

    Args:
        acad (Autocad): The Autocad instance

    Returns:
        dict: The extracted block information.
    """
    counts = Counter()
    instances = []

    for ent in acad.iter_objects("AcDbBlockReference"):
        name = ent.Name
        layer = ent.Layer
        counts[(name, layer)] += 1

        if len(instances) < 300:
            try:
                ip = ent.InsertionPoint
                pos = {"x": ip[0], "y": ip[1], "Z": ip[2] if ip is not None else None}
            except Exception:
                pos = None
            instances.append(
                {
                    "name": name,
                    "layer": layer,
                    "position": pos,
                }
            )
    
    counts_list = [
        {
            "name": n,
            "layer": l,
            "count": c
        }
        for (n, l), c in counts.items()
    ]

    return {
        "block_counts": counts_list,
        "block_instances_sample": instances,
    }

def collect_text(acad: Autocad) -> dict:
    """Extracts text information from the DWG file.

    Args:
        acad (Autocad): The Autocad instance

    Returns:
        dict: The extracted text information.
    """
    texts = []

    # * Simple TEXT
    for ent in acad.iter_objects("AcDbText"):
        try:
            txt = ent.TextString
        except Exception:
            txt = None
        
        texts.append(
            {
                "type": "TEXT",
                "layer": ent.Layer,
                "text": txt,
            }
        )
    
    # * MTEXT
    for ent in acad.iter_objects("AcDbMText"):
        try:
            txt = ent.Contents
        except Exception:
            txt = None
        
        texts.append(
            {
                "type": "MTEXT",
                "layer": ent.Layer,
                "text": txt,
            }
        )
    
    return {"texts": texts}

def collect_dimensions(acad: Autocad) -> dict:
    """Extracts dimensions information from the DWG file.

    Args:
        acad (Autocad): The Autocad instance

    Returns:
        dict: The extracted dimensions information.
    """
    dims = []

    for ent in acad.iter_objects("AcDbAlignedDimension"):
        try:
            val = ent.Measurement
        except:
            val = None
        
        dims.append(
            {
                "type": "AlignedDimension",
                "layer": ent.Layer,
                "measurement": val,
            }
        )
    
    return {"dimensions": dims}

def export_raster_png(acad: Autocad, out_dir: Path) -> Path | None:
    """Tries to export a PNG of the current view using PNGOUT.

    Args:
        acad (Autocad): The Autocad instance
        out_dir (Path): Path to the folder where the rasterized png to be saved.

    Returns:
        Path | None: Path to the saved png or None if things fail.
    """
    png_path = out_dir / "debug_view.png"
    cmd = f'_PNGOUT\n"{str(png_path)}"\n\n'

    print(f"[*] Sending PNGOUT command to AutoCAD...")
    acad.doc.SendCommand(cmd)

    time.sleep(10)

    if png_path.exists():
        print(f"[+] PNG exported -> {png_path}")
        return png_path
    
    print("[!] PNG file not found after PNGOUT. You may need to adjust the command or run manually once.")
    return None

def main():
    acad = Autocad(create_if_not_exists=False)
    doc = acad.doc

    print(f"Connected to AutoCAD document: {doc.Name}")
    doc_path = doc.FullName
    print(f"Full path: {doc_path}")

    out_dir = ensure_out_dir(doc_path)
    print(f"Output dir: {out_dir}")

    # 1) Layers
    layers_data = collect_layers(acad)
    save_json(out_dir, "layers", layers_data)

    # 2) Blocks
    blocks_data = collect_blocks(acad)
    save_json(out_dir, "blocks", blocks_data)

    # 3) Text / MText
    text_data = collect_text(acad)
    save_json(out_dir, "texts", text_data)

    # 4) Dimensions
    dim_data = collect_dimensions(acad)
    save_json(out_dir, "dimensions", dim_data)

    # 5) Try to export a PNG of the current view
    export_raster_png(acad, out_dir)

    # 6) Optionally, a small summary JSON that cross-links stuff
    summary = {
        "doc_name": doc.Name,
        "doc_path": doc.FullName,
        "outputs": {
            "layers_json": str((out_dir / "layers.json").resolve()),
            "blocks_json": str((out_dir / "blocks.json").resolve()),
            "texts_json": str((out_dir / "texts.json").resolve()),
            "dimensions_json": str((out_dir / "dimensions.json").resolve()),
            "png": str((out_dir / "debug_view.png").resolve()),
        },
    }
    save_json(out_dir, "summary", summary)

    print("\nDone. Open the JSON files in __debug_metadata__ and decide:")
    print("- Which blocks/layers matter")
    print("- How messy text is")
    print("- Whether dimensions are usable")
    print("- Whether PNGOUT gives a decent raster to feed CLIP")


## ----------- DRIVER CODE -----------------------
if __name__ == "__main__":
    main()