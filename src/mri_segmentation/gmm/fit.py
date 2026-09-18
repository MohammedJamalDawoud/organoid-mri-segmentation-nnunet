"""Deterministic one-dimensional GMM fitting with stable component ordering."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.mixture import GaussianMixture

from ..config import GMMConfig


@dataclass(frozen=True)
class GMMFitResult:
    """Model statistics and posterior columns in ascending mean-intensity order."""

    means: np.ndarray
    standard_deviations: np.ndarray
    weights: np.ndarray
    posteriors: np.ndarray
    hard_labels: np.ndarray
    converged: bool
    iterations: int
    lower_bound: float
    fit_sample_size: int


def deterministic_subsample(
    values: np.ndarray,
    maximum_samples: int,
    seed: int,
) -> np.ndarray:
    """Return all values or a deterministic sample without replacement."""
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    if maximum_samples < 1:
        raise ValueError("maximum_samples must be positive")
    if array.size <= maximum_samples:
        return array
    generator = np.random.default_rng(seed)
    indices = generator.choice(array.size, size=maximum_samples, replace=False)
    return array[np.sort(indices)]


def fit_intensity_gmm(
    values_for_fit: np.ndarray,
    values_for_prediction: np.ndarray,
    n_components: int,
    config: GMMConfig | None = None,
) -> GMMFitResult:
    """Fit a 1D GMM and reorder posterior channels by ascending component mean."""
    if config is None:
        config = GMMConfig()

    fit_values = np.asarray(values_for_fit, dtype=np.float64).reshape(-1)
    predict_values = np.asarray(values_for_prediction, dtype=np.float64).reshape(-1)
    if n_components < 2:
        raise ValueError("n_components must be at least two")
    if fit_values.size < n_components:
        raise ValueError("fewer fit values than requested components")
    if not np.isfinite(fit_values).all() or not np.isfinite(predict_values).all():
        raise ValueError("GMM values must be finite")

    sample = deterministic_subsample(
        fit_values,
        maximum_samples=config.fit_max_samples,
        seed=config.seed,
    )
    model = GaussianMixture(
        n_components=n_components,
        covariance_type=config.covariance_type,
        random_state=config.seed,
        max_iter=config.max_iter,
        tol=config.tolerance,
        reg_covar=config.regularization,
        n_init=config.baseline_n_init,
        init_params="kmeans",
    )
    model.fit(sample.reshape(-1, 1))
    unsorted_posteriors = model.predict_proba(predict_values.reshape(-1, 1))

    order = np.argsort(model.means_.reshape(-1))
    means = model.means_.reshape(-1)[order]
    weights = model.weights_.reshape(-1)[order]
    covariance = np.asarray(model.covariances_).reshape(-1)[order]
    standard_deviations = np.sqrt(covariance)
    posteriors = unsorted_posteriors[:, order]
    hard_labels = np.argmax(posteriors, axis=1)

    return GMMFitResult(
        means=means.astype(np.float64),
        standard_deviations=standard_deviations.astype(np.float64),
        weights=weights.astype(np.float64),
        posteriors=posteriors.astype(np.float64),
        hard_labels=hard_labels.astype(np.int64),
        converged=bool(model.converged_),
        iterations=int(model.n_iter_),
        lower_bound=float(model.lower_bound_),
        fit_sample_size=int(sample.size),
    )
