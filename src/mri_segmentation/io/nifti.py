"""NIfTI I/O with explicit geometry capture."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import nibabel as nib
import numpy as np

if TYPE_CHECKING:
    from ..geometry.compatibility import Geometry


@dataclass(frozen=True)
class NiftiVolume:
    """An image array with the geometry required for compatibility checks."""

    data: np.ndarray
    affine: np.ndarray
    spacing: tuple[float, ...]
    shape: tuple[int, ...]
    header: nib.Nifti1Header

    def to_geometry(self) -> Geometry:
        """Convert captured NIfTI metadata into the package geometry contract."""
        from ..geometry.compatibility import Geometry

        spatial = self.affine[:3, :3]
        spacing = np.asarray(self.spacing[:3], dtype=np.float64)
        if self.data.ndim != 3 or np.any(spacing <= 0):
            raise ValueError(
                "expected a three-dimensional volume with positive spacing"
            )
        direction = spatial / spacing[np.newaxis, :]
        return Geometry(
            shape=self.shape,
            spacing=tuple(float(value) for value in spacing),
            origin=tuple(float(value) for value in self.affine[:3, 3]),
            direction=tuple(float(value) for value in direction.ravel()),
            affine=self.affine.copy(),
        )


def load_nifti(path: str | Path) -> NiftiVolume:
    """Load a NIfTI volume without changing source data."""
    resolved = Path(path)
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    image = nib.load(str(resolved))
    data = image.get_fdata(dtype=np.float32)
    if data.ndim != 3:
        raise ValueError("expected a three-dimensional NIfTI volume")
    if not np.isfinite(data).all():
        raise ValueError("NIfTI volume contains non-finite values")
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
    output = np.asarray(data)
    if output.shape != reference.shape:
        raise ValueError(
            f"derived output shape {output.shape} does not match reference {reference.shape}"
        )
    if not np.isfinite(output).all():
        raise ValueError("derived output contains non-finite values")
    destination.parent.mkdir(parents=True, exist_ok=True)
    header = reference.header.copy()
    header.set_data_dtype(dtype)
    image = nib.Nifti1Image(
        output.astype(dtype),
        reference.affine,
        header=header,
    )
    nib.save(image, str(destination))
