#!/usr/bin/env python3
"""Lab 012: Multi-Region AWS — config validation and dry-run stub."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RegionConfig:
    name: str
    vpc_cidr: str
    is_primary: bool


@dataclass
class LabConfig:
    primary_region: str
    dr_region: str
    rto_minutes: int
    rpo_minutes: int
    budget_usd: int
    regions: list[RegionConfig]


REQUIRED_TAGS = {"lab": "lab-012", "auto_destroy": "true"}


def load_config(path: Path) -> LabConfig:
    data = json.loads(path.read_text())
    regions = [
        RegionConfig(r["name"], r["vpc_cidr"], r.get("is_primary", False))
        for r in data.get("regions", [])
    ]
    return LabConfig(
        primary_region=data["primary_region"],
        dr_region=data["dr_region"],
        rto_minutes=data.get("rto_minutes", 15),
        rpo_minutes=data.get("rpo_minutes", 5),
        budget_usd=data.get("budget_usd", 25),
        regions=regions,
    )


def validate_config(cfg: LabConfig) -> list[str]:
    errors: list[str] = []
    if cfg.primary_region == cfg.dr_region:
        errors.append("primary and DR region must differ")
    if cfg.budget_usd > 50:
        errors.append("budget_usd > 50 requires explicit approval for lab apply")
    if not cfg.regions:
        errors.append("at least one region config required")
    return errors


FAILOVER_STEPS = [
    "Verify Route 53 health check failure",
    "Check RDS replication lag",
    "Promote DR replica (if manual)",
    "Scale DR ECS service",
    "Validate application health",
]


def simulate_failover(dry_run: bool = True) -> list[dict[str, str | int]]:
    mode = "DRY-RUN" if dry_run else "EXEC"
    return [
        {"step": i, "action": action, "mode": mode}
        for i, action in enumerate(FAILOVER_STEPS, 1)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 012: Multi-Region AWS")
    parser.add_argument("--validate-config", action="store_true")
    parser.add_argument("--config", type=Path, default=Path("config/lab.json.example"))
    parser.add_argument("--simulate-failover", action="store_true")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--serve", action="store_true", help="Start API on :8102")
    parser.add_argument("--port", type=int, default=8102)
    args = parser.parse_args()

    if args.validate_config:
        cfg = load_config(args.config)
        errors = validate_config(cfg)
        if errors:
            print("VALIDATION FAILED:", errors)
            return 1
        print("VALIDATION OK:", cfg.primary_region, "->", cfg.dr_region)
        print("Required tags:", REQUIRED_TAGS)
        return 0

    if args.simulate_failover:
        for step in simulate_failover(dry_run=args.dry_run):
            print(f"{step['mode']} step {step['step']}: {step['action']}")
        return 0

    if args.serve:
        import uvicorn

        from .api import create_app

        uvicorn.run(create_app(), host="0.0.0.0", port=args.port)
        return 0

    print("Use --validate-config, --simulate-failover, or --serve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
