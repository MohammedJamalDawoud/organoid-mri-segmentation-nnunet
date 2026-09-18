"""NIfTI I/O with explicit geometry capture."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import nibabel as nib
import numpy as np


@dataclass(frozen=True)
class NiftiVolume:
    """An image array with the geometry required for compatibility checks."""

    data: np.ndarray
    affine: np.ndarray
    spacing: tuple[float, ...]
    shape: tuple[int, ...]
    header: nib.Nifti1Header


def load_nifti(path: str | Path) -> NiftiVolume:
    """Load a NIfTI volume without changing source data."""
    resolved = Path(path)
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    image = nib.load(str(resolved))
    data = image.get_fdata(dtype=np.float32)
    return NiftiVolume(
        data=data,
        affine=np.asarray(image.affine, dtype=np.float64),
        spacing=tuple(float(value) for value in image.header.get_zooms()[: data.ndim]),
        shape=tuple(int(value) for value in data.shape),
        header=image.header.copy(),
    )


def save_nifti_like(
    path: str | Path,
    data: np.ndarray,
    reference: NiftiVolume,
    *,
    dtype: np.dtype = np.float32,
) -> None:
    """Save derived data using a caller-provided reference geometry."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    header = reference.header.copy()
    header.set_data_dtype(dtype)
    image = nib.Nifti1Image(
        np.asarray(data, dtype=dtype),
        reference.affine,
        header=header,
    )
    nib.save(image, str(destination))
