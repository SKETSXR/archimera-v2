#backend/storage/filesystem.py
from __future__ import annotations
from pathlib import Path
from typing import Optional

from backend.db.common_models import FileRef
from backend.db.view_models import ViewFiles
from fastapi import UploadFile
from backend.storage.base import StorageBackend


class FileSystemStorage(StorageBackend):
    """
    Save files under FILE_BASE_DIR following the agreed layout:

        raw/sketch/{asset_id}/{view_id}.{ext}
        raw/cad/{asset_id}/{view_id}.dwg
    """
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir).resolve()
    
    def _ensure_dir(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
    
    def _save_upload(self, rel_path: str, upload: UploadFile) -> FileRef:
        abs_path = self.base_dir / rel_path
        self._ensure_dir(abs_path)

        with abs_path.open("wb") as f:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
        
        size_bytes = abs_path.stat().st_size
        content_type = upload.content_type or "application/octet-stream"

        return FileRef(
            rel_path=rel_path.replace("\\", "/"),
            content_type=content_type,
            size_bytes=size_bytes,
        )
    
    def save_view_files(
            self,
            asset_id: str,
            view_id: str,
            sketch: Optional[UploadFile],
            cad: Optional[UploadFile],
    ) -> ViewFiles:
        files = ViewFiles()
        
        if sketch is not None:
            ext = Path(sketch.filename or "").suffix or ".png"
            rel_path = f"raw/sketch/{asset_id}/{view_id}{ext}"
            files.sketch = self._save_upload(rel_path, sketch)
        
        if cad is not None:
            rel_path = f"raw/cad/{asset_id}/{view_id}.dwg"
            files.cad = self._save_upload(rel_path, cad)
        
        return files
