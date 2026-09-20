"""Command-line entry points for data-free demonstrations."""

from __future__ import annotations

import argparse
import json

import numpy as np

from .config import GMMConfig, PreprocessingConfig
from .gmm.fit import fit_intensity_gmm
from .gmm.posterior import validate_posteriors
from .gmm.support import build_support_mask
from .preprocessing.pipeline import preprocess_volume


def _synthetic_volume(seed: int) -> np.ndarray:
    """Create a deterministic synthetic array volume for the demonstration."""
    generator = np.random.default_rng(seed)
    output = np.zeros((24, 24, 24), dtype=np.float32)
    values = np.concatenate(
        (
            generator.normal(0.25, 0.03, size=1200),
            generator.normal(0.55, 0.04, size=1200),
            generator.normal(0.82, 0.03, size=1200),
        )
    ).astype(np.float32)
    output[4:19, 4:19, 4:20] = values.reshape(15, 15, 16)
    return output


def run_demo(seed: int, components: int) -> dict[str, object]:
    """Run the preprocessing and GMM pipeline entirely on a synthetic array."""
    if components < 2:
        raise ValueError("components must be at least two")
    volume = _synthetic_volume(seed)
    preprocessed = preprocess_volume(
        volume,
        config=PreprocessingConfig(denoise=False),
    )
    config = GMMConfig(
        seed=seed,
        fit_max_samples=20_000,
        baseline_n_init=1,
        support_min_fill_fraction=0.0,
    )
    support = build_support_mask(preprocessed.gmm_input, config=config)
    values = preprocessed.gmm_input[support.mask]
    result = fit_intensity_gmm(
        values,
        values,
        n_components=components,
        config=config,
    )
    validate_posteriors(result.posteriors)

    return {
        "mode": "synthetic_array_demo",
        "shape": list(volume.shape),
        "support_voxels": int(support.mask.sum()),
        "components": components,
        "means_ascending": [round(float(value), 6) for value in result.means],
        "posterior_row_sum_max_error": float(
            np.max(np.abs(result.posteriors.sum(axis=1) - 1.0))
        ),
        "converged": result.converged,
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="mri-segmentation",
        description="Data-free MRI segmentation engineering utilities.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    demo = subcommands.add_parser(
        "demo",
        help="run a deterministic synthetic-array preprocessing and GMM demo",
    )
    demo.add_argument("--seed", type=int, default=7)
    demo.add_argument("--components", type=int, default=3)
    return parser


def main(arguments: list[str] | None = None) -> None:
    """Run the CLI."""
    parser = build_parser()
    parsed = parser.parse_args(arguments)
    if parsed.command == "demo":
        print(json.dumps(run_demo(parsed.seed, parsed.components), indent=2))
