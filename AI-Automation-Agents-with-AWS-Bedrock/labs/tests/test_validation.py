import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.validation import validate_classification, validate_route


def test_valid_classification():
    ok, data, errs = validate_classification(
        {"label": "billing", "confidence": 0.9, "reason": "invoice mention"}
    )
    assert ok and data["valid"] and not errs


def test_invalid_enum():
    ok, data, errs = validate_classification(
        {"label": "invalid_label", "confidence": 0.9, "reason": "x"}
    )
    assert not ok and data["label"] == "unknown"


def test_invalid_json_type():
    ok, data, errs = validate_classification("not a dict")  # type: ignore
    assert not ok


def test_missing_confidence():
    ok, _, errs = validate_classification({"label": "billing", "reason": "x"})
    assert not ok and errs


def test_valid_route():
    ok, data, _ = validate_route(
        {"route": "team_engineering", "confidence": 0.8, "reason": "api error"}
    )
    assert ok and data["route"] == "team_engineering"
