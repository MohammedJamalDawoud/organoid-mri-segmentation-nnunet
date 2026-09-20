# Architecture

The public package is a focused extraction of the MRI segmentation engineering work. Dataset contracts and aggregate scale are documented in [Datasets](datasets.md). It exposes reusable array and metadata operations while leaving study-specific orchestration, data locations, and nnU-Net execution outside the repository.

## Module responsibilities

| Module | Responsibility | Boundary |
| --- | --- | --- |
| [io/nifti.py](../src/mri_segmentation/io/nifti.py) | Load/save NIfTI arrays with spatial metadata | Filesystem adapter |
| [preprocessing/](../src/mri_segmentation/preprocessing/) | Normalization, optional NLM denoising, pipeline order | Pure arrays plus caller-owned config |
| [gmm/](../src/mri_segmentation/gmm/) | Support masks, one-dimensional GMM fitting, posterior validation and volume reconstruction | Pure arrays |
| [labels/](../src/mri_segmentation/labels/) | Inspect label values and apply explicit caller-selected transforms | Pure arrays |
| [geometry/compatibility.py](../src/mri_segmentation/geometry/compatibility.py) | Compare shape, spacing, origin, direction and affine | Metadata only |
| [qc/](../src/mri_segmentation/qc/) | Build overlays and preflight checks | Pure arrays and metadata |
| [nnunet/](../src/mri_segmentation/nnunet/) | Channel contracts, dataset metadata, command planning and binary metrics | Integration boundary; [external nnU-Net v2 runtime](https://github.com/MIC-DKFZ/nnUNet) |
| [reporting/metrics.py](../src/mri_segmentation/reporting/metrics.py) | Aggregate scalar metrics using population standard deviation | Public-safe aggregate summaries |
| [cli.py](../src/mri_segmentation/cli.py) | Deterministic synthetic-array preprocessing/GMM demonstration | No research files |

## Data flow

1. The caller supplies an MRI array and preprocessing configuration.
2. The segmentation MRI branch applies z-score followed by min-max normalization.
3. The GMM branch optionally applies NLM denoising, then applies z-score followed by min-max normalization.
4. A support mask limits GMM fitting to relevant voxels.
5. The GMM returns components sorted by mean intensity; posterior columns use the same order.
6. Posterior vectors are reconstructed into volumes and checked for normalization.
7. Geometry and labels are checked before a caller constructs an nnU-Net dataset.
8. The nnU-Net layer generates reviewable metadata and commands; it does not run nnU-Net.
9. Aggregate metrics and qualitative figures document recorded experiments without exposing case-level material.

## Separation of concerns

Pure array operations are kept independent from file naming and path conventions. NIfTI I/O is the explicit filesystem edge. Dataset and command helpers accept caller-provided values rather than embedding server paths or dataset files. The reporting package accepts rows supplied by the caller and does not discover private result trees.

The original research runtime remains outside this repository. It includes study-specific orchestration, source inventories, full training/inference runs, private result tables, and internal QC packages. The public package documents the reusable contracts and selected de-identified evidence only.

## Public package structure

    src/mri_segmentation/
      io/
      preprocessing/
      gmm/
      labels/
      geometry/
      qc/
      nnunet/
      reporting/
      config.py
      cli.py

The privacy boundary is deliberate: no raw volumes, masks, prediction maps, weights, logs, internal paths, or case identifiers cross into the public tree.
