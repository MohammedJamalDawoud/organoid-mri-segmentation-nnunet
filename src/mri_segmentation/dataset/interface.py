"""A small validated manifest for an external nnU-Net workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatasetCase:
    """A generic dataset-interface record without invoking nnU-Net."""

    case_id: str
    image_path: Path
    label_path: Path | None = None


def _is_nifti_path(path: Path) -> bool:
    return path.name.endswith((".nii", ".nii.gz"))


def validate_dataset_cases(
    cases: list[DatasetCase],
    *,
    require_labels: bool = False,
) -> None:
    """Validate identifiers and paths without copying data or running nnU-Net."""
    if not cases:
        raise ValueError("at least one case is required")
    identifiers = [case.case_id for case in cases]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("case identifiers must be unique")

    for case in cases:
        if not case.case_id or any(character.isspace() for character in case.case_id):
            raise ValueError("case identifiers must be non-empty and whitespace-free")
        if not _is_nifti_path(case.image_path):
            raise ValueError("image_path must have a NIfTI suffix")
        if require_labels and case.label_path is None:
            raise ValueError("labels are required for every case")
        if case.label_path is not None and not _is_nifti_path(case.label_path):
            raise ValueError("label_path must have a NIfTI suffix")
