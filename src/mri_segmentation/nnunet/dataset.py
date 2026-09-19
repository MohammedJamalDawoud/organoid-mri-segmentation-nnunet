"""Data-free nnU-Net dataset construction and validation plans."""

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from .channels import ChannelSpec, default_channel_specs


@dataclass(frozen=True)
class DatasetCase:
    """A caller-owned case with source paths supplied at runtime."""

    case_id: str
    channels: Mapping[str, Path]
    label: Path | None = None


def _nifti(path: Path) -> bool:
    return path.name.endswith((".nii", ".nii.gz"))


def _validate_specs(specs: Sequence[ChannelSpec]) -> tuple[ChannelSpec, ...]:
    normalized = tuple(specs)
    if not normalized:
        raise ValueError("at least one channel specification is required")
    if len({spec.index for spec in normalized}) != len(normalized):
        raise ValueError("channel indices must be unique")
    if len({spec.source_key for spec in normalized}) != len(normalized):
        raise ValueError("channel source keys must be unique")
    if tuple(sorted(spec.index for spec in normalized)) != tuple(
        range(len(normalized))
    ):
        raise ValueError("channel indices must be contiguous and start at zero")
    return normalized


def build_export_plan(
    cases: Sequence[DatasetCase],
    output_root: str | Path,
    specs: Sequence[ChannelSpec] | None = None,
) -> list[dict[str, str]]:
    """Plan nnU-Net filenames without copying or modifying source data."""
    specs = _validate_specs(specs or default_channel_specs())
    if not cases:
        raise ValueError("at least one case is required")
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("case_id values must be unique")
    root = Path(output_root)
    plan: list[dict[str, str]] = []
    for case in cases:
        for spec in specs:
            if spec.source_key not in case.channels:
                raise ValueError(
                    f"case {case.case_id} is missing channel source {spec.source_key}"
                )
            source = Path(case.channels[spec.source_key])
            if not _nifti(source):
                raise ValueError(f"channel source is not NIfTI: {source}")
            if not source.is_file():
                raise FileNotFoundError(source)
            target = root / "imagesTr" / f"{case.case_id}_{spec.index:04d}.nii.gz"
            plan.append(
                {
                    "case_id": case.case_id,
                    "kind": "image",
                    "channel": f"{spec.index:04d}",
                    "source": str(source),
                    "target": str(target),
                }
            )
        if case.label is not None:
            label = Path(case.label)
            if not _nifti(label):
                raise ValueError(f"label source is not NIfTI: {label}")
            if not label.is_file():
                raise FileNotFoundError(label)
            plan.append(
                {
                    "case_id": case.case_id,
                    "kind": "label",
                    "channel": "label",
                    "source": str(label),
                    "target": str(root / "labelsTr" / f"{case.case_id}.nii.gz"),
                }
            )
    return plan


def build_dataset_json(
    name: str,
    cases: Sequence[DatasetCase],
    specs: Sequence[ChannelSpec] | None = None,
    labels: Mapping[str, int] | None = None,
) -> dict[str, object]:
    """Create a nnU-Net v2 dataset metadata object from a runtime case list."""
    specs = _validate_specs(specs or default_channel_specs())
    if not name or not name.strip():
        raise ValueError("name must be non-empty")
    if not cases:
        raise ValueError("at least one case is required")
    label_map = dict(labels or {"background": 0, "foreground": 1})
    if not label_map or set(label_map.values()) != set(range(len(label_map))):
        raise ValueError("labels must use contiguous integer values starting at zero")
    return {
        "channel_names": {str(spec.index): spec.name for spec in specs},
        "labels": label_map,
        "numTraining": len(cases),
        "file_ending": ".nii.gz",
        "name": name,
    }


def write_dataset_json(
    path: str | Path, payload: Mapping[str, object], *, overwrite: bool = False
) -> Path:
    """Write metadata with an explicit overwrite guard."""
    target = Path(path)
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"refusing to overwrite existing dataset metadata: {target}"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(dict(payload), indent=2) + "\n", encoding="utf-8")
    return target
