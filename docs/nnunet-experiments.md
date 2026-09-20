# nnU-Net Experiments

## Verified dataset evolution

| Dataset | Role | MRI + prior channels | Verified prior strategy | Recorded status |
| --- | --- | ---: | --- | --- |
| Dataset101 | Baseline | 5 | K10-to-K4 soft probability priors | 5-epoch CPU prototype with warnings |
| Dataset102 | Corrected-prior prototype | 5 | K10-to-K4 sigma-rule priors | 5-epoch CPU prototype with warnings/review required |
| Dataset103 | Reference comparison | 5 | Direct K4 posterior priors | 5-epoch CPU prototype |
| Dataset104 | Controlled comparison | 6 | Controlled K5 posterior channels | 5-epoch CPU prototype |
| Dataset105 | Controlled comparison | 4 | Controlled K3 posterior channels | 5-epoch CPU prototype |

Dataset101 and Dataset102 are not identical: Dataset101 is the original K10-to-K4 soft-prior baseline, while Dataset102 is the later sigma-rule-corrected prior version. Dataset103 changes the prior branch to direct K4 output while keeping the MRI and binary-label source contract. Dataset104 and Dataset105 are controlled K5 and K3 prior-channel comparisons against the Dataset103 source.

The public-safe schema is recorded in [dataset_channel_contracts.csv](results/dataset_channel_contracts.csv), with detailed dataset context in [Datasets](datasets.md).

## Integration layer

The [nnU-Net module](../src/mri_segmentation/nnunet/) provides channel specifications, filename planning, dataset metadata generation, reviewable plan/train/predict commands, and binary prediction/reference metrics. nnU-Net v2 itself remains external. These helpers do not start planning, training, inference, or data export.

## Framework attribution

The segmentation framework used in the original project was the external nnU-Net v2 implementation maintained by the Medical Image Computing Division at DKFZ / MIC-DKFZ and the Helmholtz Imaging Applied Computer Vision Lab: [official repository](https://github.com/MIC-DKFZ/nnUNet). This repository provides project-specific preprocessing, GMM-prior/channel contracts, dataset integration, command planning, QC, and aggregate reporting; it does not redistribute nnU-Net source.

Citation: Isensee, F., Jaeger, P. F., Kohl, S. A. A., Petersen, J., & Maier-Hein, K. H. (2021). *nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation.* Nature Methods, 18(2), 203--211.

The module exposes `default_channel_specs()` and `direct_k4_channel_specs()`
for the documented Dataset103 reference contract, plus explicit
`controlled_k3_channel_specs()` and `controlled_k5_channel_specs()` factories
for Dataset105 and Dataset104. K3 and K5 posterior channels retain generic
intensity-component names. Dataset103 direct-K4 preserves the project-specific
semantic mapping used in that reviewed experiment: `background_1`,
`background_2_lowprob_uncertain`, `tissue`, and `fluid`. These names are
contract labels for that experiment, not universally valid biological
identities for arbitrary GMM components.

## Result authority

The current project contains only nnUNetTrainer_5epochs__nnUNetPlans__3d_fullres result trees for Dataset101-105. Therefore the published comparison is explicitly a 5-epoch CPU development comparison. It is recorded project-internal evidence, not final model performance or a generalization benchmark.

See [Results](results.md) for aggregate metrics and the documented Dataset102 warnings.
