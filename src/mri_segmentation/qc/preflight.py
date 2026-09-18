"""Data-independent preflight checks."""

from __future__ import annotations

import numpy as np


def validate_volume_contract(
    data: np.ndarray,
    *,
    require_finite: bool = True,
    require_three_dimensions: bool = True,
) -> None:
    """Raise for invalid array contracts before downstream processing."""
    array = np.asarray(data)
    if require_three_dimensions and array.ndim != 3:
        raise ValueError("expected a three-dimensional volume")
    if require_finite and not np.isfinite(array).all():
        raise ValueError("volume contains non-finite values")
