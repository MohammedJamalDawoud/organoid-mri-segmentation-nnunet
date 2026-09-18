"""Caller-scoped NIfTI discovery."""

from __future__ import annotations

from pathlib import Path


def discover_nifti(root: str | Path) -> list[Path]:
    """Return sorted NIfTI paths below a caller-provided directory."""
    base = Path(root)
    if not base.is_dir():
        raise NotADirectoryError(base)
    paths = {path for pattern in ("*.nii", "*.nii.gz") for path in base.rglob(pattern)}
    return sorted(paths)
