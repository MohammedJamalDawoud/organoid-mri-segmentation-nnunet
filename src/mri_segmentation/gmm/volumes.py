"""Probability-volume reconstruction utilities."""

from __future__ import annotations

import numpy as np

from .posterior import validate_posteriors


def reconstruct_probability_volume(
    support_mask: np.ndarray,
    posteriors: np.ndarray,
    component_index: int,
) -> np.ndarray:
    """Place one ordered posterior channel into a full volume."""
    mask = np.asarray(support_mask, dtype=bool)
    validate_posteriors(posteriors)
    if mask.ndim != 3:
        raise ValueError("support_mask must be three-dimensional")
    if mask.sum() != posteriors.shape[0]:
        raise ValueError("support voxel count does not match posterior rows")
    if not 0 <= component_index < posteriors.shape[1]:
        raise ValueError("component_index is out of range")

    output = np.zeros(mask.shape, dtype=np.float32)
    output[mask] = posteriors[:, component_index].astype(np.float32)
    return output


def reconstruct_hard_labels(
    support_mask: np.ndarray,
    ordered_labels: np.ndarray,
) -> np.ndarray:
    """Place zero-based labels into a volume, reserving zero for outside support."""
    mask = np.asarray(support_mask, dtype=bool)
    labels = np.asarray(ordered_labels, dtype=np.int64).reshape(-1)
    if mask.ndim != 3 or labels.size != mask.sum():
        raise ValueError("labels must correspond exactly to support voxels")
    if np.any(labels < 0):
        raise ValueError("labels must be non-negative")

    output = np.zeros(mask.shape, dtype=np.uint16)
    output[mask] = (labels + 1).astype(np.uint16)
    return output
