"""Explicit label inspection and transformation utilities."""

from .inspection import LabelSummary, inspect_labels
from .transforms import binarize_labels

__all__ = ["LabelSummary", "binarize_labels", "inspect_labels"]
