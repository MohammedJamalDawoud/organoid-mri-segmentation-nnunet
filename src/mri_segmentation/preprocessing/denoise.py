"""Deterministic three-dimensional non-local-means denoising."""

from __future__ import annotations

import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma


def estimate_noise_sigma(data: np.ndarray) -> float:
    """Estimate scalar noise from a finite three-dimensional array."""
    array = np.asarray(data, dtype=np.float32)
    if array.ndim != 3:
        raise ValueError("expected a three-dimensional volume")
    if not np.isfinite(array).all():
        raise ValueError("input contains non-finite values")

    estimate = estimate_sigma(array, channel_axis=None)
    sigma = float(np.mean(np.asarray(estimate, dtype=np.float64)))
    if not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("noise estimate must be finite and positive")
    return sigma


def apply_nlm_denoise(
    data: np.ndarray,
    sigma: float | None = None,
    *,
    patch_size: int = 5,
    patch_distance: int = 6,
    h_factor: float = 0.8,
) -> np.ndarray:
    """Apply three-dimensional non-local-means denoising.

    The defaults retain the reviewed reference parameters. The function accepts
    arrays only and never discovers files or creates output directories.
    """
    array = np.asarray(data, dtype=np.float32)
    if array.ndim != 3:
        raise ValueError("expected a three-dimensional volume")
    if not np.isfinite(array).all():
        raise ValueError("input contains non-finite values")
    if patch_size < 1 or patch_distance < 1 or h_factor <= 0:
        raise ValueError("denoising parameters must be positive")

    resolved_sigma = estimate_noise_sigma(array) if sigma is None else float(sigma)
    if not np.isfinite(resolved_sigma) or resolved_sigma <= 0:
        raise ValueError("sigma must be finite and positive")

    output = denoise_nl_means(
        array,
        h=h_factor * resolved_sigma,
        sigma=resolved_sigma,
        fast_mode=True,
        patch_size=patch_size,
        patch_distance=patch_distance,
        preserve_range=True,
        channel_axis=None,
    )
    return np.asarray(output, dtype=np.float32)
