"""Explicit image-geometry compatibility checks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Geometry:
    """Shape, spacing, origin, direction, and affine metadata."""

    shape: tuple[int, ...]
    spacing: tuple[float, ...]
    origin: tuple[float, ...]
    direction: tuple[float, ...]
    affine: np.ndarray | None = None


@dataclass(frozen=True)
class GeometryComparison:
    """Field-level compatibility result without applying any correction."""

    shape_match: bool
    spacing_match: bool
    origin_match: bool
    direction_match: bool
    affine_match: bool | None

    @property
    def matches(self) -> bool:
        affine_ok = self.affine_match is not False
        return all(
            (
                self.shape_match,
                self.spacing_match,
                self.origin_match,
                self.direction_match,
                affine_ok,
            )
        )


def compare_geometry(
    image: Geometry,
    label: Geometry,
    *,
    tolerance: float = 1e-5,
) -> GeometryComparison:
    """Compare geometry fields and never resample or modify an input."""
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    affine_match: bool | None
    if image.affine is None or label.affine is None:
        affine_match = None
    else:
        affine_match = bool(
            np.allclose(image.affine, label.affine, atol=tolerance, rtol=0.0)
        )

    return GeometryComparison(
        shape_match=image.shape == label.shape,
        spacing_match=bool(
            np.allclose(image.spacing, label.spacing, atol=tolerance, rtol=0.0)
        ),
        origin_match=bool(
            np.allclose(image.origin, label.origin, atol=tolerance, rtol=0.0)
        ),
        direction_match=bool(
            np.allclose(image.direction, label.direction, atol=tolerance, rtol=0.0)
        ),
        affine_match=affine_match,
    )
