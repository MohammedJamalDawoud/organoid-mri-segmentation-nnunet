"""Small structured provenance helpers without environment-specific paths."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def make_record(operation: str, parameters: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-serializable provenance record."""
    if not operation.strip():
        raise ValueError("operation must be non-empty")
    return {
        "operation": operation,
        "parameters": parameters,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
