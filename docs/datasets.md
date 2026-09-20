# Dataset Documentation

This page is the public dataset documentation authority for the repository. It describes the recorded MRI segmentation data contracts at an aggregate level only. Raw research data, labels, posterior maps, predictions, folds, logs, private paths, and case-level tables are not distributed.

## Project and Data Purpose

The project develops an MRI segmentation workflow for organoid MRI. The private research data support preprocessing, GMM-derived intensity probability priors, nnU-Net v2 dataset construction, supervised binary segmentation, and aggregate development-run evaluation.

The public repository exposes the reusable engineering contracts: array normalization, optional denoising, GMM posterior handling, NIfTI geometry capture, label/geometry checks, nnU-Net dataset metadata planning, command planning, and aggregate reporting helpers. It does not contain the private data used by the recorded experiments.

## Data Domains

| Domain | Role in this public repository | Public status |
| --- | --- | --- |
| In-vitro organoid MRI | Primary development domain for the documented preprocessing, GMM-prior, and nnU-Net workflow. | Documented through aggregate counts, channel contracts, and de-identified figures only. |
| Phantom / controlled technical data | Used where relevant for technical validation and workflow development. | Not distributed; no separate public training claim is made. |
| Ex-vivo tissue | Supplementary extension/generalization material in the private project. | Not presented as approved combined training data here. |
| In-vivo imaging | Supplementary extension/generalization context in the private project. | Not presented as a trained public workflow target here. |

The repository remains focused on the organoid segmentation workflow. Other domains must not automatically inherit organoid-specific GMM component names, labels, or trained-model assumptions.

## MRI Data Characteristics

The reusable public contract starts from a caller-owned 3D NIfTI-like MRI volume with explicit spatial metadata. The private workflow used GRE/N4-derived MRI representations, including a segmentation-normalized MRI branch and a denoised GMM-preparation branch.

Important distinctions:

| Term | Meaning in this repository |
| --- | --- |
| Acquisition sequence | The original MRI acquisition family, kept private. |
| GRE/N4 representation | The earliest derived MRI representation documented as the public input contract. |
| Segmentation-normalized MRI | GRE/N4 followed by z-score and min-max normalization. |
| GMM-prepared MRI | GRE/N4 followed by optional NLM denoising, then z-score and min-max normalization. |
| GMM posterior map | A private derived probability volume for one ordered intensity component. |
| nnU-Net input channel | A normalized MRI channel or GMM-prior channel exported under an explicit dataset contract. |

The private organoid preprocessing universe contains 159 subject/session processing case units. Aggregate header inspection showed all are 3D NIfTI volumes. The common matrix shape is `128 x 100 x 70`; observed shapes were `128 x 100 x 70`, `168 x 100 x 70`, `128 x 100 x 80`, and `160 x 100 x 70`. Most had voxel spacing `1.0 x 1.0 x 1.0`; nine historical cases carried `0.05 x 0.05 x 0.05` spacing and are treated as metadata-sensitive historical cases in the private project. Compressed file sizes for the segmentation-normalized MRI branch ranged from about 2.9 MB to 4.0 MB, with a median of about 3.1 MB.

These values describe matrix dimensions, voxel spacing, and filesystem file size. They do not identify individual cases.

## Dataset Scale

| Count | Meaning |
| ---: | --- |
| 159 | Broader organoid-processing subject/session case units in the private preprocessing and GMM universe. |
| 64 | Supervised development cases used by Dataset101-105. |
| 8 x 8 | Private supervised development design corresponding to 64 subject/session case units. |
| 5 | Five-fold development evaluation for Dataset101-105. |

The `159` value is not described here as 159 different biological organoids. The public-safe term is subject/session processing case units.

## Data Representations

| Representation | Purpose | Used by | Public/private status |
| --- | --- | --- | --- |
| GRE/N4 image | Derived MRI input contract before normalization. | Public preprocessing interface. | Data private; contract public. |
| Segmentation-normalized MRI | Main MRI input channel. | Dataset101-105 channel 0. | Data private; transformation public. |
| GMM-prepared normalized MRI | Denoised branch used to fit GMM priors. | K3/K4/K5/K10 GMM workflows. | Data private; branch order public. |
| K3 posterior channels | Coarser controlled GMM prior comparison. | Dataset105. | Volumes private; channel contract public. |
| Direct K4 posterior channels | Main direct reference prior branch. | Dataset103. | Volumes private; channel contract public. |
| K5 posterior channels | Finer controlled GMM prior comparison. | Dataset104. | Volumes private; channel contract public. |
| Exploratory K10 components | Fine-grained intensity decomposition and reduction source. | Historical K10-to-K4 reductions. | Volumes private; role public. |
| Standard K10-to-K4 reduction | Original four-prior reduction from K10. | Dataset101. | Volumes private; aggregate summary public. |
| Sigma-rule K10-to-K4 reduction | Corrected four-prior reduction from K10. | Dataset102. | Volumes private; aggregate summary public. |
| Binary reference label | Supervised segmentation target. | Dataset101-105 labels. | Masks private; label contract public. |
| nnU-Net prediction | Validation prediction for development runs. | Aggregate evaluation and selected de-identified figures. | Volumes private; aggregate metrics public. |

## Dataset101-105

The supervised development datasets use the same 64 private supervised cases unless stated otherwise by the private project evidence. The detailed channel names are recorded in [dataset_channel_contracts.csv](results/dataset_channel_contracts.csv).

| Dataset | Role | MRI input | Prior strategy | Channels | Label contract | Development cases | Recorded training status |
| --- | --- | --- | --- | ---: | --- | ---: | --- |
| Dataset101 | Baseline prototype | Normalized GRE/N4 MRI | Standard K10-to-K4 soft priors | 5 | background=0; foreground/organoid=1 | 64 | 5-epoch CPU prototype with warnings/review required |
| Dataset102 | Corrected-prior prototype | Normalized GRE/N4 MRI | Sigma-rule K10-to-K4 priors | 5 | background=0; foreground/organoid=1 | 64 | 5-epoch CPU prototype with warnings/review required |
| Dataset103 | Reference comparison | Normalized GRE/N4 MRI | Direct K4 priors | 5 | background=0; foreground/organoid=1 | 64 | 5-epoch CPU prototype |
| Dataset104 | Controlled comparison | Normalized GRE/N4 MRI | Controlled K5 posterior channels | 6 | background=0; foreground/organoid=1 | 64 | 5-epoch CPU prototype |
| Dataset105 | Controlled comparison | Normalized GRE/N4 MRI | Controlled K3 posterior channels | 4 | background=0; foreground/organoid=1 | 64 | 5-epoch CPU prototype |

No direct 11-channel K10 nnU-Net dataset is claimed. K10 was used as an exploratory decomposition and reduction source.

For the 5-channel exported supervised datasets, aggregate file counts are 320 image-channel files and 64 label files. Dataset104 has 384 image-channel files because it has six channels. Dataset105 has 256 image-channel files because it has four channels. In the exported 64-case development set, 315 of 320 Dataset103 image-channel files had shape `128 x 100 x 70`, and five had shape `128 x 100 x 80`; all had voxel spacing `1.0 x 1.0 x 1.0`.

## Label Contract

The public-safe supervised label contract is binary:

| Value | Meaning |
| ---: | --- |
| 0 | background |
| 1 | foreground/organoid |

The public repository does not distribute labels or masks. Any caller adapting the package must define and verify their own target semantics before building a supervised dataset.

## Training and Evaluation Design

Dataset101-105 are recorded five-fold, 5-epoch CPU development comparisons. They are project-internal engineering evidence, not final model performance, production accuracy, or an external generalization benchmark. Fold-level assignments, case-level metrics, images, labels, predictions, and logs remain private.

The public aggregate summaries are in [Results](results.md) and the CSV files under [docs/results](results/).

## Workflow Position

```text
private/raw acquisition
    -> private GRE/N4 preparation
    -> publicly documented normalization contract
    -> GMM probability priors
    -> geometry and label QC
    -> Dataset101-105 channel construction
    -> external nnU-Net v2
    -> prediction/reference evaluation
```

## What Is Not Distributed

This repository does not contain raw MRI, NIfTI research volumes, DICOM/NRRD/MHA research data, masks, posterior probability volumes, prediction volumes, model weights, checkpoints, private case-level CSV/TSV files, raw logs, internal paths, private reports, or private metadata inventories. See [Data policy](data-policy.md).

## Working With Caller-Owned Data

To reuse the package, a caller needs a compatible 3D MRI/NIfTI representation, explicit spatial metadata, caller-owned file paths, suitable labels for supervised export, an explicit GMM/channel selection, and an external nnU-Net v2 installation for planning, training, and inference.

An arbitrary MRI dataset must not automatically inherit the organoid-specific component semantics, channel labels, or target assumptions used by these recorded development datasets.
