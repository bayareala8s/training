#!/usr/bin/env python3
"""Day-one environment check for students. Exits 0 if Python is usable; warns on optional tools."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_PY = (3, 10)


def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        out = (r.stdout or r.stderr or "").strip()
        line = out.splitlines()[0] if out else f"exit {r.returncode}"
        if r.returncode != 0 or "Traceback" in out:
            return False, line
        return True, line
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return False, f"not found ({exc.__class__.__name__})"


def main() -> int:
    print("BayLearn EIA — prerequisite check")
    print(f"Repo: {ROOT}")
    ok = True
    if sys.version_info < MIN_PY:
        print(f"FAIL  Python {sys.version.split()[0]} (need 3.10+)")
        ok = False
    else:
        print(f"OK    Python {sys.version.split()[0]}")

    for name, cmd in [
        ("terraform", ["terraform", "version"]),
        ("aws", ["aws", "--version"]),
    ]:
        path = shutil.which(name)
        if not path:
            print(f"WARN  {name} not on PATH — required before Lab 2")
            continue
        good, msg = run(cmd)
        print(f"{'OK   ' if good else 'WARN '} {name}: {msg}")

    try:
        import boto3  # noqa: F401

        print("OK    boto3 (validate_lab.py)")
    except ImportError:
        print("WARN  boto3 missing — pip install -r requirements.txt")

    start = ROOT / "scripts" / "start_course.sh"
    getting = ROOT / "GETTING_STARTED.md"
    if not start.exists() or not getting.exists():
        print("FAIL  Missing GETTING_STARTED.md or scripts/start_course.sh")
        ok = False
    else:
        print("OK    Getting started files present")

    print()
    print("Next: ./scripts/start_course.sh")
    print("      then http://localhost:8080/course-ui/")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
