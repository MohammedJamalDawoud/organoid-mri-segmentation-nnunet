"""Deterministic aggregation helpers for public-safe result tables."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def summarize_metric(values: Iterable[float]) -> dict[str, float | int]:
    """Return count, mean, population standard deviation, minimum and maximum."""
    ordered = sorted(float(value) for value in values)
    if not ordered:
        raise ValueError("values must contain at least one number")
    count = len(ordered)
    mean = sum(ordered) / count
    median = (
        ordered[count // 2]
        if count % 2
        else (ordered[count // 2 - 1] + ordered[count // 2]) / 2
    )
    variance = sum((value - mean) ** 2 for value in ordered) / count
    return {
        "count": count,
        "mean": mean,
        "median": median,
        "std": variance**0.5,
        "min": ordered[0],
        "max": ordered[-1],
    }


def compare_variants(
    rows: Iterable[Mapping[str, object]],
    group_key: str,
    metric_key: str,
) -> dict[str, dict[str, float | int]]:
    """Aggregate a scalar metric by a named experiment variant."""
    groups: dict[str, list[float]] = {}
    for row in rows:
        if group_key not in row or metric_key not in row:
            raise KeyError(f"row requires {group_key!r} and {metric_key!r}")
        group = str(row[group_key])
        groups.setdefault(group, []).append(float(row[metric_key]))
    return {group: summarize_metric(values) for group, values in sorted(groups.items())}
