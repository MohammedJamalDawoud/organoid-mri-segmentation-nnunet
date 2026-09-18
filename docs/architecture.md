# Architecture

```text
mri_segmentation/
├── io/             NIfTI arrays plus spatial metadata
├── preprocessing/  denoising and intensity normalization
├── gmm/            support mask, fit, posterior contract, volumes
├── labels/         label inspection and explicit transforms
├── geometry/       shape/spacing/origin/direction/affine checks
├── qc/             array-level overlay and preflight helpers
└── nnunet/         project-specific dataset/channel/command/QC glue
```

The `nnunet` layer is an integration boundary, not a copy of nnU-Net. It generalizes the project’s own channel mapping, `imagesTr`/`labelsTr` naming, dataset metadata, reviewed command plans, and prediction/reference metrics. Runtime paths are supplied by the caller.

The five documented inputs are:

- channel 0: normalized MRI;
- channel 1: GMM background prior;
- channel 2: GMM low-probability tissue prior;
- channel 3: GMM tissue prior;
- channel 4: GMM fluid prior.

The channel names describe the project data contract. They do not prove biological semantics for every component.
