#backend/tools/validate_nas_mount.py
from __future__ import annotations
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import traceback
from typing import NoReturn

from core.config import settings


def _fail(msg: str, exit_code: int = 1) -> NoReturn:
    print(f"[ERROR] {msg}")
    sys.exit(exit_code)


def main() -> None:
    print("=== NAS Validation Script (backend container) ===")

    # 1. Resolve FILE_BASE_DIR from settings
    raw_base_dir = settings.file_base_dir
    base_dir = Path(raw_base_dir).resolve()

    print(f"[INFO] FILE_BASE_DIR from settings: {raw_base_dir}")
    print(f"[INFO] Resolved absolute path: {base_dir}")

    # 2. Basic existence check
    if not base_dir.exists():
        _fail(
            f"Base directory does not exist: {base_dir}. "
            "Check your Docker bind/volume mount configuration."
        )
    
    if not base_dir.is_dir():
        _fail(
            f"Base path is not a directory: {base_dir}. "
            "Something is very wrong with the mount."
        )
    
    # 3. Permission checks (read/write/execute)
    mode = 0
    for flag, name in ((os.R_OK, "R"), (os.W_OK, "W"), (os.X_OK, "X")):
        has_perm = os.access(base_dir, flag)
        mode |= flag if has_perm else 0
        print(f"[INFO] Permission {name}: {'YES' if has_perm else 'NO'}")
    
    if not os.access(base_dir, os.R_OK | os.W_OK | os.X_OK):
        _fail(
            "Backend container does not have full R/W/X permissions on FILE_BASE_DIR. "
            "Check NAS share permissions and Docker mount options."
        )
    
    # 4. Try writing + reading a file
    test_dir = base_dir / "_archimera_nas_test"
    test_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat() + "Z"
    test_file = test_dir / "nas_write_test.txt"
    content = f"NAS test from backend container at {timestamp}\n"

    print(f"[INFO] Writing test file: {test_file}")

    try:
        with test_file.open("w", encoding="utf-8") as f:
            f.write(content)
    except Exception as exc:
        _fail(f"Failed to WRITE test file: {exc}")
    
    try:
        with test_file.open("r", encoding="utf-8") as f:
            readback = f.read()
    except Exception as exc:
        _fail(f"Failed to READ test file: {exc}")
    
    if readback != content:
        _fail("Read-back content does not match written content. IO corruption or buffering issue?")
    
    print("[OK] Write + read test succeeded.")

    # 5. Try listing some entries in base_dir (helps sanity check)
    try:
        entries = list(base_dir.iterdir())
        print(f"[INFO] Listing up to 10 entries in {base_dir}:")
        for p in entries[:10]:
            type_str = "DIR " if p.is_dir() else "FILE"
            print(f" - [{type_str}] {p.name}")
        if len(entries) == 0:
            print("[INFO] Directory is empty. That's fine as long as mounts are correct.")
    except Exception as exc:
        print(f"[WARN] Failed to list contents of {base_dir}: {exc}")
    
    # 6. Disk usage info
    try:
        total, used, free = shutil.disk_usage(base_dir)
        gb = 1024 ** 3
        print(
            "[INFO] Disk usage for FILE_BASE_DIR:\n"
            f"      Total: {total // gb} GiB\n"
            f"      Used : {used // gb} GiB\n"
            f"      Free : {free // gb} GiB\n"
        )
    except Exception as exc:
        print(f"[WARN] Could not get disk usage info: {exc}")
    
    print("=== NAS validation completed successfully. ===")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        print("[FATAL] Unhandled exception in NAS validation script:")
        traceback.print_exc()
        sys.exit(1)
