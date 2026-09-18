# Workflow

The implementation follows the project’s engineering sequence:

1. Load a caller-provided NIfTI image while retaining shape, affine, spacing, origin, and direction metadata.
2. Prepare a modeling input using the documented optional denoising and nonzero-voxel normalization order.
3. Build a support mask so intensity modeling is not dominated by empty borders.
4. Fit a one-dimensional GMM, reorder posterior columns by mean intensity, and reconstruct probability volumes in the original grid.
5. Inspect labels explicitly and compare image/mask geometry before any dataset export. No silent resampling is performed.
6. Build an nnU-Net v2 export plan for the normalized image, GMM prior channels, and label. The plan is reviewable and does not copy files.
7. Generate dataset metadata and reviewable external nnU-Net commands.
8. Compare binary predictions and references with the same geometry-aware QC mindset used during dataset preparation.

The public package intentionally separates reusable computation from caller-owned paths and execution decisions.
