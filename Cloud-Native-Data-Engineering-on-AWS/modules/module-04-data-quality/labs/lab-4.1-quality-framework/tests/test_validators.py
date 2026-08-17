"""Unit tests for Lab 4.1 validation framework."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from validators import RuleEngine, validate_enum, validate_not_null, validate_range  # noqa: E402

RULES = Path(__file__).resolve().parents[1] / "rules" / "orders_rules.json"


def test_not_null_rejects_empty_string():
    ok, _ = validate_not_null("", {})
    assert ok is False


def test_range_accepts_value_in_bounds():
    ok, _ = validate_range(50.0, {"min": 0.01, "max": 50000})
    assert ok is True


def test_range_rejects_negative():
    ok, msg = validate_range(-1, {"min": 0, "max": 100})
    assert ok is False
    assert msg is not None


def test_enum_rejects_invalid_status():
    ok, _ = validate_enum("invalid", {"values": ["pending", "shipped"]})
    assert ok is False


def test_rule_engine_passes_valid_order():
    engine = RuleEngine(RULES)
    record = {
        "order_id": "ORD-1",
        "order_amount": 25.0,
        "status": "pending",
        "customer_email": "user@example.com",
    }
    result = engine.validate_record(record)
    assert result.has_errors is False


def test_rule_engine_quarantines_bad_order():
    engine = RuleEngine(RULES)
    record = {
        "order_id": "ORD-2",
        "order_amount": -5,
        "status": "invalid",
        "customer_email": "bad@",
    }
    result = engine.validate_record(record)
    assert result.has_errors is True
    assert any(v.field == "order_amount" for v in result.violations)
