"""Posterior probability contracts."""

from __future__ import annotations

import numpy as np


def validate_posteriors(posteriors: np.ndarray, *, tolerance: float = 1e-6) -> None:
    """Raise when posterior rows are not finite probabilities summing to one."""
    array = np.asarray(posteriors, dtype=np.float64)
    if array.ndim != 2 or array.shape[1] < 2:
        raise ValueError("posteriors must have shape (n_samples, n_components)")
    if not np.isfinite(array).all():
        raise ValueError("posteriors contain non-finite values")
    if np.any(array < -tolerance) or np.any(array > 1.0 + tolerance):
        raise ValueError("posteriors are outside the probability range")
    if not np.allclose(array.sum(axis=1), 1.0, atol=tolerance, rtol=0.0):
        raise ValueError("posterior rows must sum to one")


def hard_labels(posteriors: np.ndarray) -> np.ndarray:
    """Return zero-based ordered-component labels from validated posteriors."""
    validate_posteriors(posteriors)
    return np.argmax(posteriors, axis=1).astype(np.int64)
