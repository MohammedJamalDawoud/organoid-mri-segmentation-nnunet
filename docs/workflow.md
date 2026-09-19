# Workflow

## 1. MRI input and spatial metadata

The caller supplies an MRI volume and, when using file integration, a NIfTI path. [nifti.py](../src/mri_segmentation/io/nifti.py) keeps the voxel array separate from shape, spacing, origin, direction, and affine metadata. This makes later geometry checks explicit.

## 2. GRE/N4 preparation contract

The research workflow uses a GRE/N4-derived MRI representation before normalization. The public package treats that representation as an input contract; it does not bundle the private bias-correction runtime. This keeps upstream preparation separate from reusable array code.

## 3. Normalization and optional denoising

[normalization.py](../src/mri_segmentation/preprocessing/normalization.py) implements the documented z-score and min-max operations. [denoise.py](../src/mri_segmentation/preprocessing/denoise.py) contains the optional 3D NLM branch. [pipeline.py](../src/mri_segmentation/preprocessing/pipeline.py) returns two explicit outputs: the segmentation MRI branch is z-score followed by min-max, while the GMM branch optionally denoises first and then applies z-score followed by min-max.

## 4. Support mask and GMM branch

[support.py](../src/mri_segmentation/gmm/support.py) selects the fitting region. [fit.py](../src/mri_segmentation/gmm/fit.py) fits a one-dimensional GMM with deterministic sampling and sorts components by ascending mean intensity. [posterior.py](../src/mri_segmentation/gmm/posterior.py) validates row sums, and [volumes.py](../src/mri_segmentation/gmm/volumes.py) reconstructs posterior and hard-label volumes.

The reason for stable ordering is contract integrity: channel 1 must refer to the same ordered component definition as the corresponding fitted statistics and reconstructed volume.

## 5. Label and geometry QC

[inspection.py](../src/mri_segmentation/labels/inspection.py) reports label values without silently changing them. [transforms.py](../src/mri_segmentation/labels/transforms.py) requires an explicit caller-selected transform. [compatibility.py](../src/mri_segmentation/geometry/compatibility.py) compares spatial metadata and rejects mismatches rather than silently resampling.

## 6. nnU-Net dataset branch

[channels.py](../src/mri_segmentation/nnunet/channels.py) defines the normalized MRI plus prior-channel contract. [dataset.py](../src/mri_segmentation/nnunet/dataset.py) plans filenames and dataset metadata without copying data. [commands.py](../src/mri_segmentation/nnunet/commands.py) returns reviewable external commands. No training or inference is started by the package.

The runtime itself is external: the original workflow used [nnU-Net v2](https://github.com/MIC-DKFZ/nnUNet) for planning, training, and inference, while this repository provides the project-specific contracts and command planning around it.

## 7. Evaluation branch

[qc.py](../src/mri_segmentation/nnunet/qc.py) computes binary prediction/reference metrics. [reporting/metrics.py](../src/mri_segmentation/reporting/metrics.py) summarizes scalar values with population standard deviation. The public result tables contain aggregate values from recorded 5-epoch CPU development comparisons; private per-case tables remain excluded.

## 8. Why the branches are separate

Preprocessing creates a consistent intensity representation. The GMM branch adds interpretable probability priors. Geometry and label checks protect the dataset contract. The nnU-Net branch consumes the resulting channel specification, while the evaluation branch combines overlap metrics with qualitative overlays and volume agreement.

