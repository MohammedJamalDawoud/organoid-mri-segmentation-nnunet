"""Channel contracts for multi-input nnU-Net datasets.

The project used a normalized GRE/MGE image plus GMM-derived probability
channels. These names describe the data contract without assigning biological
meaning to an individual GMM component beyond its documented prior role.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ChannelSpec:
    """One nnU-Net channel and its public semantic name."""
    index: int
    name: str
    source_key: str


def default_channel_specs() -> tuple[ChannelSpec, ...]:
    """Return the five-channel contract used by the documented workflow."""
    return (
        ChannelSpec(0, "normalized_mri", "mri"),
        ChannelSpec(1, "gmm_background_prior", "gmm_background"),
        ChannelSpec(2, "gmm_low_probability_tissue_prior", "gmm_lowprob_tissue"),
        ChannelSpec(3, "gmm_tissue_prior", "gmm_tissue"),
        ChannelSpec(4, "gmm_fluid_prior", "gmm_fluid"),
    )
