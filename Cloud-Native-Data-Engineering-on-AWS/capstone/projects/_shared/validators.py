#!/usr/bin/env python3
"""Declarative data validation library for Lab 4.1."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


ValidatorFn = Callable[[Any, dict[str, Any]], tuple[bool, str | None]]


@dataclass
class Violation:
    """Single rule violation for a record."""

    rule: str
    field: str
    message: str
    severity: str
    actual_value: Any = None


@dataclass
class ValidationResult:
    """Outcome of validating one record."""

    record: dict[str, Any]
    violations: list[Violation] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(v.severity == "error" for v in self.violations)

    @property
    def has_warnings(self) -> bool:
        return any(v.severity == "warning" for v in self.violations)


def validate_not_null(value: Any, params: dict[str, Any]) -> tuple[bool, str | None]:
    if value is None:
        return False, "value is null"
    if isinstance(value, str) and value.strip() == "":
        return False, "value is empty"
    return True, None


def validate_range(value: Any, params: dict[str, Any]) -> tuple[bool, str | None]:
    if value is None:
        return False, "value is null"

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return False, f"value '{value}' is not numeric"

    min_val = params.get("min")
    max_val = params.get("max")

    if min_val is not None and numeric < float(min_val):
        return False, f"value {numeric} below minimum {min_val}"
    if max_val is not None and numeric > float(max_val):
        return False, f"value {numeric} above maximum {max_val}"
    return True, None


def validate_enum(value: Any, params: dict[str, Any]) -> tuple[bool, str | None]:
    allowed = params.get("values", [])
    if not allowed:
        return False, "enum rule missing 'values' parameter"

    if value is None:
        return False, "value is null"
    if value not in allowed:
        return False, f"value '{value}' not in {allowed}"
    return True, None


def validate_regex(value: Any, params: dict[str, Any]) -> tuple[bool, str | None]:
    pattern = params.get("pattern")
    if not pattern:
        return False, "regex rule missing 'pattern' parameter"

    if value is None:
        return False, "value is null"

    text = str(value)
    if not re.match(pattern, text):
        return False, f"value '{text}' does not match pattern"
    return True, None


VALIDATORS: dict[str, ValidatorFn] = {
    "not_null": validate_not_null,
    "range": validate_range,
    "enum": validate_enum,
    "regex": validate_regex,
}


@dataclass
class RuleDefinition:
    name: str
    field: str
    type: str
    severity: str = "error"
    message: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


class RuleEngine:
    """Loads JSON rule definitions and validates records."""

    def __init__(self, rules_path: str | Path):
        path = Path(rules_path)
        with path.open(encoding="utf-8") as f:
            config = json.load(f)

        self.dataset = config.get("dataset", "unknown")
        self.version = config.get("version", "1.0")
        self.rules: list[RuleDefinition] = []

        for rule in config.get("rules", []):
            rule_type = rule.get("type")
            if rule_type not in VALIDATORS:
                raise ValueError(f"Unsupported rule type: {rule_type}")

            self.rules.append(
                RuleDefinition(
                    name=rule["name"],
                    field=rule["field"],
                    type=rule_type,
                    severity=rule.get("severity", "error"),
                    message=rule.get("message"),
                    params=rule.get("params", {}),
                )
            )

    def validate_record(self, record: dict[str, Any]) -> ValidationResult:
        violations: list[Violation] = []

        for rule in self.rules:
            validator = VALIDATORS[rule.type]
            value = record.get(rule.field)
            passed, detail = validator(value, rule.params)

            if not passed:
                message = rule.message or detail or f"Rule {rule.name} failed"
                violations.append(
                    Violation(
                        rule=rule.name,
                        field=rule.field,
                        message=message,
                        severity=rule.severity,
                        actual_value=value,
                    )
                )

        return ValidationResult(record=record, violations=violations)

    def validate_batch(
        self, records: list[dict[str, Any]]
    ) -> list[ValidationResult]:
        return [self.validate_record(record) for record in records]
