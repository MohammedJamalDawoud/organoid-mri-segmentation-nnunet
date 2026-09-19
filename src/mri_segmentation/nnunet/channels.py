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
        ChannelSpec(1, "direct_k4_background_1_prior", "direct_k4_background_1"),
        ChannelSpec(
            2,
            "direct_k4_background_2_lowprob_uncertain_prior",
            "direct_k4_background_2_lowprob_uncertain",
        ),
        ChannelSpec(3, "direct_k4_tissue_prior", "direct_k4_tissue"),
        ChannelSpec(4, "direct_k4_fluid_prior", "direct_k4_fluid"),
    )


def controlled_k5_channel_specs() -> tuple[ChannelSpec, ...]:
    """Return the documented Dataset104 controlled-K5 contract.

    Component names remain generic because posterior channels are not assigned
    biological identities by the source experiments.
    """
    return (
        ChannelSpec(0, "normalized_mri", "mri"),
        ChannelSpec(
            1, "controlled_k5_component_01_prior", "controlled_k5_component_01"
        ),
        ChannelSpec(
            2, "controlled_k5_component_02_prior", "controlled_k5_component_02"
        ),
        ChannelSpec(
            3, "controlled_k5_component_03_prior", "controlled_k5_component_03"
        ),
        ChannelSpec(
            4, "controlled_k5_component_04_prior", "controlled_k5_component_04"
        ),
        ChannelSpec(
            5, "controlled_k5_component_05_prior", "controlled_k5_component_05"
        ),
    )


def controlled_k3_channel_specs() -> tuple[ChannelSpec, ...]:
    """Return the documented Dataset105 controlled-K3 contract."""
    return (
        ChannelSpec(0, "normalized_mri", "mri"),
        ChannelSpec(
            1, "controlled_k3_component_01_prior", "controlled_k3_component_01"
        ),
        ChannelSpec(
            2, "controlled_k3_component_02_prior", "controlled_k3_component_02"
        ),
        ChannelSpec(
            3, "controlled_k3_component_03_prior", "controlled_k3_component_03"
        ),
    )
