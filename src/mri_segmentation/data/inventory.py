"""Minimal source-file inventory without data-content interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .discovery import discover_nifti


@dataclass(frozen=True)
class FileInventory:
    """Filesystem-level inventory record."""

    path: Path
    bytes: int


def inventory_nifti(root: str | Path) -> list[FileInventory]:
    """Record paths and byte sizes of caller-selected NIfTI files."""
    return [
        FileInventory(path=path, bytes=path.stat().st_size)
        for path in discover_nifti(root)
    ]
