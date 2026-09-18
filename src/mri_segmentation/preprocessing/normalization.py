"""Foreground-aware intensity normalization for three-dimensional arrays."""

from __future__ import annotations

import numpy as np


def _float_volume(data: np.ndarray) -> np.ndarray:
    array = np.asarray(data, dtype=np.float32)
    if array.ndim != 3:
        raise ValueError("expected a three-dimensional volume")
    if not np.isfinite(array).all():
        raise ValueError("input contains non-finite values")
    return array


def zscore_nonzero(data: np.ndarray) -> np.ndarray:
    """Z-score non-zero voxels while preserving zero-valued background."""
    array = _float_volume(data)
    mask = array != 0
    if not np.any(mask):
        raise ValueError("volume contains no non-zero voxels")
    values = array[mask]
    standard_deviation = float(np.std(values))
    if standard_deviation == 0:
        raise ValueError("non-zero voxels have zero standard deviation")

    output = np.zeros_like(array, dtype=np.float32)
    output[mask] = (array[mask] - float(np.mean(values))) / standard_deviation
    return output


def minmax_nonzero_to_m1p1(data: np.ndarray) -> np.ndarray:
    """Map non-zero values to [-1, 1] and represent background as -1.

    This preserves the reviewed preprocessing behavior: after z-scoring, values
    equal to zero are treated as background by this stage.
    """
    array = _float_volume(data)
    mask = array != 0
    if not np.any(mask):
        raise ValueError("volume contains no non-zero voxels")
    values = array[mask]
    minimum = float(np.min(values))
    maximum = float(np.max(values))
    if maximum == minimum:
        raise ValueError("non-zero voxels have zero intensity range")

    output = np.full_like(array, -1.0, dtype=np.float32)
    output[mask] = 2.0 * (array[mask] - minimum) / (maximum - minimum) - 1.0
    return output
