"""Prediction/reference checks used by the project QC workflow."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BinaryComparison:
    dice: float
    prediction_voxels: int
    reference_voxels: int
    false_positive_voxels: int
    false_negative_voxels: int


def compare_binary_volumes(
    prediction: np.ndarray, reference: np.ndarray
) -> BinaryComparison:
    pred = np.asarray(prediction).astype(bool)
    ref = np.asarray(reference).astype(bool)
    if pred.shape != ref.shape:
        raise ValueError("prediction and reference must have the same shape")
    intersection = int(np.count_nonzero(pred & ref))
    pred_count = int(pred.sum())
    ref_count = int(ref.sum())
    denominator = pred_count + ref_count
    dice = (2.0 * intersection / denominator) if denominator else 1.0
    return BinaryComparison(
        dice=dice,
        prediction_voxels=pred_count,
        reference_voxels=ref_count,
        false_positive_voxels=int(np.count_nonzero(pred & ~ref)),
        false_negative_voxels=int(np.count_nonzero(~pred & ref)),
    )


def summarize_prediction(
    prediction: np.ndarray, reference: np.ndarray
) -> dict[str, object]:
    """Return JSON-friendly binary comparison metrics."""
    return compare_binary_volumes(prediction, reference).__dict__.copy()
