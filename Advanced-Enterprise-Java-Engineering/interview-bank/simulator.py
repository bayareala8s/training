#!/usr/bin/env python3
"""Phase A interview simulator: print prompts from questions.json. No network."""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANK = ROOT / "questions.json"


def load() -> list[dict]:
    if not BANK.exists():
        sys.stderr.write("questions.json not assembled yet. Merge domains first.\n")
        sys.exit(2)
    data = json.loads(BANK.read_text())
    return data if isinstance(data, list) else data.get("questions", [])


def show(q: dict, reveal: bool) -> None:
    print(f"{q['id']}  [{q['domain']}]  {q.get('difficulty', '')}")
    print(q["question"])
    print("Follow-ups:")
    for fu in q.get("followUps", []):
        print(f"  - {fu}")
    if reveal:
        print("\n--- reveal (instructor / self-check) ---")
        for key in ("engineerAnswer", "seniorAnswer", "staffAnswer", "principalAnswer"):
            if q.get(key):
                print(f"\n{key}:\n{q[key]}")
        print("\nCommon mistakes:", "; ".join(q.get("commonMistakes", [])))
        print("\nRubric:\n", q.get("scoreRubric", ""))
    else:
        print("\n(Write your answer. Re-run with --reveal after you stop talking.)")


def main() -> int:
    p = argparse.ArgumentParser(description="AEJE Phase A interview simulator")
    p.add_argument("--mode", choices=["practice", "rapid-fire", "timed-interview"], default="practice")
    p.add_argument("--domain", default="")
    p.add_argument("--id", default="")
    p.add_argument("--count", type=int, default=8)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--reveal", action="store_true")
    args = p.parse_args()
    qs = load()
    if args.id:
        match = [q for q in qs if q["id"] == args.id]
        if not match:
            sys.stderr.write(f"unknown id {args.id}\n")
            return 1
        show(match[0], args.reveal)
        return 0
    pool = [q for q in qs if not args.domain or q["domain"] == args.domain]
    if not pool:
        sys.stderr.write("empty pool\n")
        return 1
    rng = random.Random(args.seed)
    if args.mode == "rapid-fire":
        pick = rng.sample(pool, k=min(args.count, len(pool)))
        print(f"Rapid fire: {len(pick)} items. 60–90 seconds each. No reveal.\n")
        for i, q in enumerate(pick, 1):
            print(f"--- {i}/{len(pick)} ---")
            show(q, False)
            print()
        return 0
    q = rng.choice(pool)
    if args.mode == "timed-interview":
        print("Timed interview: 8 minutes. Start your clock.\n")
    show(q, args.reveal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
