#!/usr/bin/env python3
"""Orchestrate Stage 14 checkers, Java tests, Terraform validate, interview smoke."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAVA_HOME = os.environ.get("JAVA_HOME", "/opt/homebrew/opt/openjdk@21")
TF = "/opt/homebrew/bin/terraform"
TF_DIRS = [
    ROOT / "solutions/BUILD-1101",
    ROOT / "solutions/BUILD-1201",
    ROOT / "solutions/BUILD-1202",
    ROOT / "infrastructure/terraform/baypay-ecs",
]
_K8S_PARSE = r"""
from pathlib import Path
import sys
import yaml
root = Path("infrastructure/kubernetes")
issues = []
for path in sorted(root.rglob("*.yaml")):
    docs = list(yaml.safe_load_all(path.read_text()) or [])
    if not docs:
        issues.append(f"{path} empty")
        continue
    for i, doc in enumerate(docs):
        if not isinstance(doc, dict):
            issues.append(f"{path} doc {i} not a mapping")
            continue
        if not doc.get("apiVersion") or not doc.get("kind"):
            issues.append(f"{path} doc {i} missing apiVersion/kind")
if issues:
    print("FAIL")
    for issue in issues:
        print("-", issue)
    sys.exit(1)
n = len(list(root.rglob("*.yaml")))
print("PASS k8s yaml parse (%s files)" % n)
"""

CHECKERS = [
    "qa/check_stage3.py",
    "qa/check_stage4.py",
    "qa/check_stage5.py",
    "qa/check_stage6.py",
    "qa/check_stage7.py",
    "qa/check_stage8.py",
    "qa/check_stage9.py",
    "qa/check_stage10.py",
    "qa/check_stage11.py",
    "qa/check_diagram_library.py",
    "qa/check_paks_links.py",
    "qa/check_stage14.py",
]


def run(name: str, cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> dict:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        env=merged,
        text=True,
        capture_output=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    print(f"== {name} exit={proc.returncode} ==")
    if out.strip():
        print(out.strip()[-4000:])
    return {
        "name": name,
        "exit": proc.returncode,
        "ok": proc.returncode == 0,
        "tail": out[-2000:],
    }


def main() -> int:
    results: list[dict] = []
    for rel in CHECKERS:
        results.append(run(rel, [sys.executable, str(ROOT / rel)]))

    results.append(
        run(
            "mvn test",
            ["./mvnw", "-q", "test"],
            cwd=ROOT / "reference-apps/baypay",
            env={"JAVA_HOME": JAVA_HOME},
        )
    )

    for tf_dir in TF_DIRS:
        init = run(
            f"terraform init {tf_dir.relative_to(ROOT)}",
            [TF, "init", "-backend=false", "-input=false", "-no-color"],
            cwd=tf_dir,
        )
        results.append(init)
        if init["ok"]:
            results.append(
                run(
                    f"terraform validate {tf_dir.relative_to(ROOT)}",
                    [TF, "validate", "-no-color"],
                    cwd=tf_dir,
                )
            )

    results.append(
        run(
            "k8s yaml parse",
            [sys.executable, "-c", _K8S_PARSE],
        )
    )

    results.append(
        run(
            "interview simulator smoke",
            [
                sys.executable,
                str(ROOT / "interview-bank/simulator.py"),
                "--mode",
                "practice",
                "--id",
                "AEJE-IQ-012",
            ],
        )
    )

    out_path = ROOT / "qa/stage14-results.json"
    out_path.write_text(json.dumps(results, indent=2) + "\n")
    failed = [r for r in results if not r["ok"]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    if failed:
        print("FAILED:")
        for r in failed:
            print("-", r["name"])
        return 1
    print("PASS Stage 14 full suite")
    return 0


if __name__ == "__main__":
    sys.exit(main())
