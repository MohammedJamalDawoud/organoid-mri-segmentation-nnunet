# Data policy

This repository is intentionally data-free with respect to the underlying MRI study.

Included:

- reusable Python implementation;
- data-free configuration examples;
- documentation and architecture diagrams;
- three curated, de-identified derived QC panels selected to explain the workflow.

Excluded:

- raw and derived NIfTI volumes;
- manual masks, labels, model weights, checkpoints, logs, and internal reports;
- subject, animal, case, institution, server, or collaborator identifiers;
- absolute local/network paths and credentials;
- the nnU-Net framework itself.

The curated QC panels are not a substitute for the research dataset and are not presented as a benchmark or performance result. The `.gitignore` provides prevention only; every future addition still requires review.
