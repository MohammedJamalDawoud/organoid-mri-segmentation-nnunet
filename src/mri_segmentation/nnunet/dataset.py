"""Data-free nnU-Net dataset construction and validation plans."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping, Sequence
from .channels import ChannelSpec, default_channel_specs

@dataclass(frozen=True)
class DatasetCase:
    """A caller-owned case with source paths supplied at runtime."""
    case_id: str
    channels: Mapping[str, Path]
    label: Path | None = None


def _nifti(path: Path) -> bool:
    return path.name.endswith((".nii", ".nii.gz"))


def build_export_plan(
    cases: Sequence[DatasetCase],
    output_root: str | Path,
    specs: Sequence[ChannelSpec] | None = None,
) -> list[dict[str, str]]:
    """Plan nnU-Net filenames without copying or modifying source data."""
    specs = tuple(specs or default_channel_specs())
    if not cases:
        raise ValueError("at least one case is required")
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("case_id values must be unique")
    root = Path(output_root)
    plan: list[dict[str, str]] = []
    for case in cases:
        for spec in specs:
            source = Path(case.channels[spec.source_key])
            if not _nifti(source):
                raise ValueError(f"channel source is not NIfTI: {source}")
            target = root / "imagesTr" / f"{case.case_id}_{spec.index:04d}.nii.gz"
            plan.append({"case_id": case.case_id, "kind": "image", "channel": f"{spec.index:04d}", "source": str(source), "target": str(target)})
        if case.label is not None:
            label = Path(case.label)
            if not _nifti(label):
                raise ValueError(f"label source is not NIfTI: {label}")
            plan.append({"case_id": case.case_id, "kind": "label", "channel": "label", "source": str(label), "target": str(root / "labelsTr" / f"{case.case_id}.nii.gz")})
    return plan


def build_dataset_json(
    name: str,
    cases: Sequence[DatasetCase],
    specs: Sequence[ChannelSpec] | None = None,
    labels: Mapping[str, int] | None = None,
) -> dict[str, object]:
    """Create a nnU-Net v2 dataset metadata object from a runtime case list."""
    specs = tuple(specs or default_channel_specs())
    if not name or not name.strip():
        raise ValueError("name must be non-empty")
    return {
        "channel_names": {str(spec.index): spec.name for spec in specs},
        "labels": dict(labels or {"background": 0, "foreground": 1}),
        "numTraining": len(cases),
        "file_ending": ".nii.gz",
        "name": name,
    }


def write_dataset_json(path: str | Path, payload: Mapping[str, object], *, overwrite: bool = False) -> Path:
    """Write metadata with an explicit overwrite guard."""
    target = Path(path)
    if target.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing dataset metadata: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(dict(payload), indent=2) + "\n", encoding="utf-8")
    return target
