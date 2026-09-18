"""Configuration objects with explicit, data-independent defaults."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PreprocessingConfig:
    """Parameters for the array-only preprocessing pipeline."""

    denoise: bool = True
    patch_size: int = 5
    patch_distance: int = 6
    h_factor: float = 0.8


@dataclass(frozen=True)
class GMMConfig:
    """Parameters preserved from the reviewed reference GMM implementation."""

    seed: int = 20260730
    fit_max_samples: int = 400_000
    support_low_threshold: float = -0.99
    support_min_fill_fraction: float = 0.60
    covariance_type: str = "full"
    max_iter: int = 300
    tolerance: float = 1e-4
    regularization: float = 1e-6
    baseline_n_init: int = 5
