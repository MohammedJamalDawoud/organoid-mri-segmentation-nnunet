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
    return direct_k4_channel_specs()


def direct_k4_channel_specs() -> tuple[ChannelSpec, ...]:
    """Return the documented Dataset103 direct-K4 channel contract."""
    return (
        ChannelSpec(0, "normalized_mri", "mri"),
        ChannelSpec(1, "gmm_background_prior", "gmm_background"),
        ChannelSpec(2, "gmm_low_probability_tissue_prior", "gmm_lowprob_tissue"),
        ChannelSpec(3, "gmm_tissue_prior", "gmm_tissue"),
        ChannelSpec(4, "gmm_fluid_prior", "gmm_fluid"),
    )


def controlled_k5_channel_specs() -> tuple[ChannelSpec, ...]:
    """Return the documented Dataset104 controlled-K5 contract.

    Component names remain generic because posterior channels are not assigned
    biological identities by the source experiments.
    """
    return (
        ChannelSpec(0, "normalized_mri", "mri"),
        ChannelSpec(1, "gmm_component_1_prior", "gmm_component_1"),
        ChannelSpec(2, "gmm_component_2_prior", "gmm_component_2"),
        ChannelSpec(3, "gmm_component_3_prior", "gmm_component_3"),
        ChannelSpec(4, "gmm_component_4_prior", "gmm_component_4"),
        ChannelSpec(5, "gmm_component_5_prior", "gmm_component_5"),
    )


def controlled_k3_channel_specs() -> tuple[ChannelSpec, ...]:
    """Return the documented Dataset105 controlled-K3 contract."""
    return (
        ChannelSpec(0, "normalized_mri", "mri"),
        ChannelSpec(1, "gmm_component_1_prior", "gmm_component_1"),
        ChannelSpec(2, "gmm_component_2_prior", "gmm_component_2"),
        ChannelSpec(3, "gmm_component_3_prior", "gmm_component_3"),
    )
