"""Array-only QC overlay generation."""

from __future__ import annotations

import numpy as np


def make_overlay(
    image_slice: np.ndarray,
    mask_slice: np.ndarray,
    *,
    alpha: float = 0.45,
) -> np.ndarray:
    """Return an RGB overlay without writing figures or assigning semantics."""
    image = np.asarray(image_slice, dtype=np.float32)
    mask = np.asarray(mask_slice, dtype=bool)
    if image.ndim != 2 or mask.ndim != 2 or image.shape != mask.shape:
        raise ValueError("image_slice and mask_slice must be matching 2D arrays")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be between zero and one")

    minimum = float(np.min(image))
    maximum = float(np.max(image))
    if maximum == minimum:
        normalized = np.zeros_like(image)
    else:
        normalized = (image - minimum) / (maximum - minimum)
    rgb = np.repeat(normalized[..., None], repeats=3, axis=2)
    rgb[mask, 0] = (1.0 - alpha) * rgb[mask, 0] + alpha
    rgb[mask, 1] *= 1.0 - alpha
    rgb[mask, 2] *= 1.0 - alpha
    return np.clip(rgb, 0.0, 1.0).astype(np.float32)
