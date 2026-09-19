# nnU-Net Experiments

## Verified dataset evolution

| Dataset | Role | MRI + prior channels | Verified prior strategy | Recorded status |
| --- | --- | ---: | --- | --- |
| Dataset101 | Baseline | 5 | K10-to-K4 soft probability priors | Dataset preparation baseline |
| Dataset102 | Corrected-prior prototype | 5 | K10-to-K4 sigma-rule priors | 5-epoch CPU prototype |
| Dataset103 | Reference comparison | 5 | Direct K4 posterior priors | 5-epoch CPU prototype |
| Dataset104 | Controlled comparison | 6 | Controlled K5 posterior channels | 5-epoch CPU prototype |
| Dataset105 | Controlled comparison | 4 | Controlled K3 posterior channels | 5-epoch CPU prototype |

Dataset101 and Dataset102 are not identical: Dataset101 is the original K10-to-K4 soft-prior baseline, while Dataset102 is the later sigma-rule-corrected prior version. Dataset103 changes the prior branch to direct K4 output while keeping the MRI and binary-label source contract. Dataset104 and Dataset105 are controlled K5 and K3 prior-channel comparisons against the Dataset103 source.

The public-safe schema is recorded in [dataset_channel_contracts.csv](results/dataset_channel_contracts.csv).

## Integration layer

The [nnU-Net module](../src/mri_segmentation/nnunet/) provides channel specifications, filename planning, dataset metadata generation, reviewable plan/train/predict commands, and binary prediction/reference metrics. nnU-Net v2 itself remains external. These helpers do not start planning, training, inference, or data export.

The module exposes `default_channel_specs()` and `direct_k4_channel_specs()`
for the documented Dataset103 reference contract, plus explicit
`controlled_k3_channel_specs()` and `controlled_k5_channel_specs()` factories
for Dataset105 and Dataset104. The posterior names preserve source-contract
labels and remain generic; the source experiments do not establish biological
meanings for individual components.

## Result authority

The current project contains only nnUNetTrainer_5epochs__nnUNetPlans__3d_fullres result trees for Dataset101–105. Therefore the published comparison is explicitly a 5-epoch CPU development comparison. It is recorded project-internal evidence, not final model performance or a generalization benchmark.

See [Results](results.md) for aggregate metrics and the documented Dataset102 warnings.

