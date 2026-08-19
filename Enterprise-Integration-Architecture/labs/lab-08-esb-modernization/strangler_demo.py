#!/usr/bin/env python3
"""Local strangler router for Lab 8 — no AWS required.

Balances and new digital flows leave the ESB. Settlement ISO stays on a
certified adapter until dual-run completes. Marketing email is not a bus map.
"""

from __future__ import annotations

ROUTES = {
    "GET /balances": "new_api",
    "ADDRESS_CHANGE": "event",
    "MARKETING_EMAIL": "retire_esb_use_events",
    "SETTLEMENT_FILE": "file_landing",
    "ISO20022_MQ": "keep_adapter",
    "WAREHOUSE_COMMAND": "queue",
    "COLLECTIONS_SAAS": "new_api",
    "REPORTING_JDBC": "retire_undocumented_p2p",
}


def route(intent: str) -> str:
    if intent not in ROUTES:
        raise KeyError(f"unknown flow: {intent}")
    return ROUTES[intent]


def dual_run_required(intent: str) -> bool:
    return intent in {"ISO20022_MQ", "SETTLEMENT_FILE"}


def main() -> None:
    assert route("GET /balances") == "new_api"
    assert route("ISO20022_MQ") == "keep_adapter"
    assert route("MARKETING_EMAIL") == "retire_esb_use_events"
    assert dual_run_required("ISO20022_MQ")
    assert not dual_run_required("GET /balances")
    print("PASS strangler_demo: balances on new API; ISO adapter kept; marketing off the bus.")


if __name__ == "__main__":
    main()
