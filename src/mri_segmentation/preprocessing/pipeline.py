"""Composable preprocessing pipeline with explicit output contracts."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..config import PreprocessingConfig
from .denoise import apply_nlm_denoise
from .normalization import minmax_nonzero_to_m1p1, zscore_nonzero


@dataclass(frozen=True)
class PreprocessingResult:
    """Two reviewed preprocessing outputs for downstream consumers."""

    gmm_input: np.ndarray
    segmentation_input: np.ndarray


def preprocess_volume(
    data: np.ndarray,
    config: PreprocessingConfig | None = None,
) -> PreprocessingResult:
    """Create GMM and external-segmentation inputs from one MRI array.

    The GMM branch is denoise -> z-score -> min-max. The segmentation branch is
    z-score -> min-max. Bias correction is deliberately outside this package.
    """
    if config is None:
        config = PreprocessingConfig()

    array = np.asarray(data, dtype=np.float32)
    z_scored = zscore_nonzero(array)
    segmentation_input = minmax_nonzero_to_m1p1(z_scored)

    if config.denoise:
        denoised = apply_nlm_denoise(
            array,
            patch_size=config.patch_size,
            patch_distance=config.patch_distance,
            h_factor=config.h_factor,
        )
        gmm_input = minmax_nonzero_to_m1p1(zscore_nonzero(denoised))
    else:
        gmm_input = segmentation_input.copy()

    return PreprocessingResult(
        gmm_input=gmm_input,
        segmentation_input=segmentation_input,
    )
