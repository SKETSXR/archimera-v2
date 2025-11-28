#backend/storage/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from backend.db.view_models import ViewFiles
from fastapi import UploadFile


class StorageBackend(ABC):
    @abstractmethod
    def save_view_files(
        self,
        asset_id: str,
        view_id: str,
        sketch: Optional[UploadFile],
        cad: Optional[UploadFile],
    ) -> ViewFiles:
        """
        Save sketch and CAD files for a specific view and return a ViewFiles
        object pointing to relative paths.
        """
        raise NotImplementedError
