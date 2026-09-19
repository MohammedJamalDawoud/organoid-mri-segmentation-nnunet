"""Support-mask construction without anatomical interpretation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import ndimage

from ..config import GMMConfig


@dataclass(frozen=True)
class SupportMaskResult:
    """A support mask and auditable summary statistics."""

    mask: np.ndarray
    statistics: dict[str, float | int | bool | str]


def build_support_mask(
    data: np.ndarray,
    config: GMMConfig | None = None,
) -> SupportMaskResult:
    """Exclude border-connected low-intensity space from a volume.

    The threshold and fallback retain the reviewed reference mechanics. This
    function does not interpret the retained voxels as a biological structure.
    """
    if config is None:
        config = GMMConfig()

    array = np.asarray(data, dtype=np.float32)
    if array.ndim != 3:
        raise ValueError("expected a three-dimensional volume")
    if not np.isfinite(array).all():
        raise ValueError("support input contains non-finite values")

    finite = np.isfinite(array)
    low = finite & (array <= config.support_low_threshold)
    border_seed = np.zeros_like(low, dtype=bool)
    border_seed[0, :, :] = low[0, :, :]
    border_seed[-1, :, :] = low[-1, :, :]
    border_seed[:, 0, :] = low[:, 0, :]
    border_seed[:, -1, :] = low[:, -1, :]
    border_seed[:, :, 0] = low[:, :, 0]
    border_seed[:, :, -1] = low[:, :, -1]

    outside = ndimage.binary_propagation(border_seed, mask=low)
    support = finite & ~outside
    fraction = float(np.mean(support))
    fallback_used = False
    if fraction < config.support_min_fill_fraction:
        support = finite.copy()
        fraction = float(np.mean(support))
        fallback_used = True
    if not np.any(support):
        raise ValueError("support mask is empty")

    return SupportMaskResult(
        mask=support,
        statistics={
            "strategy": "border_connected_low_intensity_exclusion",
            "support_low_threshold": config.support_low_threshold,
            "support_min_fill_fraction": config.support_min_fill_fraction,
            "finite_voxels": int(finite.sum()),
            "low_candidate_voxels": int(low.sum()),
            "outside_mask_voxels": int(outside.sum()),
            "support_voxels": int(support.sum()),
            "support_fraction": fraction,
            "fallback_to_finite_mask": fallback_used,
        },
    )
