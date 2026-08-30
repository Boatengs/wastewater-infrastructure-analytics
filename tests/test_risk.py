import pytest

from wastewater_infrastructure_analytics import classify_risk, risk_priority_number


def test_risk_priority_number_default_multiplier() -> None:
    assert risk_priority_number(4, 5) == 20.0


def test_risk_priority_number_criticality_multiplier() -> None:
    assert risk_priority_number(3, 4, 1.25) == 15.0


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (1, "low"),
        (6, "moderate"),
        (12, "high"),
        (20, "very_high"),
    ],
)
def test_classify_risk(score: float, expected: str) -> None:
    assert classify_risk(score) == expected


def test_invalid_ordinal_score_rejected() -> None:
    with pytest.raises(ValueError):
        risk_priority_number(0, 4)


def test_nonpositive_criticality_rejected() -> None:
    with pytest.raises(ValueError):
        risk_priority_number(3, 4, 0)
