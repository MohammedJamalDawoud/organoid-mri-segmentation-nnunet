"""Label-value inspection without semantic inference."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LabelSummary:
    """Observed label properties; it does not claim anatomical meaning."""

    values: tuple[int, ...]
    foreground_voxels: int
    non_empty: bool
    integral: bool


def inspect_labels(data: np.ndarray) -> LabelSummary:
    """Inspect values and non-emptiness of a three-dimensional label array."""
    array = np.asarray(data)
    if array.ndim != 3:
        raise ValueError("expected a three-dimensional label volume")
    if not np.isfinite(array).all():
        raise ValueError("labels contain non-finite values")
    integral = bool(np.allclose(array, np.rint(array)))
    if not integral:
        raise ValueError("labels must contain integral values")

    integer_labels = np.rint(array).astype(np.int64)
    values = tuple(int(value) for value in np.unique(integer_labels))
    foreground = int(np.count_nonzero(integer_labels))
    return LabelSummary(
        values=values,
        foreground_voxels=foreground,
        non_empty=foreground > 0,
        integral=integral,
    )
