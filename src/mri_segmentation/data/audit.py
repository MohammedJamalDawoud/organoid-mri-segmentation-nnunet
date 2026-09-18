"""Small audit summary helpers."""

from __future__ import annotations

from .inventory import FileInventory


def summarize_inventory(records: list[FileInventory]) -> dict[str, int]:
    """Return a transparent count and byte total."""
    return {
        "file_count": len(records),
        "total_bytes": sum(record.bytes for record in records),
    }
