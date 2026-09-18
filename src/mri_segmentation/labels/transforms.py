"""Caller-controlled label transformations."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from .inspection import inspect_labels


def binarize_labels(
    labels: np.ndarray,
    foreground_values: Iterable[int],
) -> np.ndarray:
    """Create a binary mask from explicitly supplied foreground label values."""
    values = tuple(int(value) for value in foreground_values)
    if not values:
        raise ValueError("foreground_values must not be empty")
    inspect_labels(labels)
    output = np.isin(np.asarray(labels), values).astype(np.uint8)
    return output
