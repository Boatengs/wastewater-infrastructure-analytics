"""Core wastewater asset risk-scoring helpers."""

from __future__ import annotations

from numbers import Real


def _validate_score(name: str, value: Real) -> float:
    """Validate a 1–5 ordinal score and return it as a float."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a numeric value between 1 and 5")

    score = float(value)
    if not 1 <= score <= 5:
        raise ValueError(f"{name} must be between 1 and 5; received {value!r}")
    return score


def risk_priority_number(
    likelihood_of_failure: Real,
    consequence_of_failure: Real,
    criticality_multiplier: Real = 1.0,
) -> float:
    """Calculate a transparent asset risk priority number.

    Parameters
    ----------
    likelihood_of_failure:
        Ordinal likelihood-of-failure score from 1 (low) to 5 (high).
    consequence_of_failure:
        Ordinal consequence-of-failure score from 1 (low) to 5 (high).
    criticality_multiplier:
        Positive multiplier used to reflect local service, environmental,
        regulatory, or operational criticality. Defaults to 1.0.

    Returns
    -------
    float
        ``likelihood_of_failure * consequence_of_failure * criticality_multiplier``.
    """
    lof = _validate_score("likelihood_of_failure", likelihood_of_failure)
    cof = _validate_score("consequence_of_failure", consequence_of_failure)

    if isinstance(criticality_multiplier, bool) or not isinstance(criticality_multiplier, Real):
        raise TypeError("criticality_multiplier must be a positive numeric value")

    criticality = float(criticality_multiplier)
    if criticality <= 0:
        raise ValueError("criticality_multiplier must be greater than 0")

    return lof * cof * criticality


def classify_risk(risk_score: Real) -> str:
    """Convert a baseline risk score into a simple decision-support category.

    The thresholds assume the default 1–5 LoF and CoF scales with a 1.0
    criticality multiplier. Utilities should recalibrate these thresholds when
    local risk tolerance or criticality multipliers materially change the scale.
    """
    if isinstance(risk_score, bool) or not isinstance(risk_score, Real):
        raise TypeError("risk_score must be numeric")

    score = float(risk_score)
    if score < 0:
        raise ValueError("risk_score cannot be negative")
    if score >= 20:
        return "very_high"
    if score >= 12:
        return "high"
    if score >= 6:
        return "moderate"
    return "low"
