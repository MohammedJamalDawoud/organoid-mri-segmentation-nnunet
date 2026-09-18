"""Command planners for an installed nnU-Net v2 environment.

These helpers return commands for a caller to review. They never invoke
training, planning, preprocessing, or prediction themselves.
"""

def plan_preprocess(dataset_id: int, *, verify_integrity: bool = True) -> list[str]:
    command = ["nnUNetv2_plan_and_preprocess", "-d", str(dataset_id), "--verify_dataset_integrity"]
    if not verify_integrity:
        command.pop()
    return command


def plan_train(dataset_id: int, configuration: str, fold: int, *, trainer: str = "nnUNetTrainer") -> list[str]:
    if fold < 0:
        raise ValueError("fold must be non-negative")
    return ["nnUNetv2_train", str(dataset_id), configuration, str(fold), "-tr", trainer]


def plan_predict(dataset_id: int, configuration: str, *, input_dir: str, output_dir: str, fold: int | str = "all", trainer: str = "nnUNetTrainer") -> list[str]:
    return ["nnUNetv2_predict", "-d", str(dataset_id), "-c", configuration, "-i", input_dir, "-o", output_dir, "-f", str(fold), "-tr", trainer]
