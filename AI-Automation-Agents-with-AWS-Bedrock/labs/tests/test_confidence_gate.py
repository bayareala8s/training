import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.validation import apply_confidence_gate


def test_low_confidence_routes_to_human_review():
    data = {"route": "team_billing", "confidence": 0.3, "valid": True}
    out = apply_confidence_gate(data, threshold=0.65)
    assert out["route"] == "human_review"
    assert out.get("low_confidence") is True


def test_high_confidence_unchanged():
    data = {"route": "team_billing", "confidence": 0.9, "valid": True}
    out = apply_confidence_gate(data, threshold=0.65)
    assert out["route"] == "team_billing"
