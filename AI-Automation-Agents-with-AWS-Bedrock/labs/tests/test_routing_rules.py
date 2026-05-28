import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from week03.route_service import rules_route


def test_billing_rules_hit():
    result = rules_route("I was charged twice on my invoice")
    assert result is not None
    assert result["route"] == "team_billing"
    assert result["source"] == "rules"


def test_no_rules_match():
    assert rules_route("Hello there") is None
