#!/usr/bin/env python3
"""Smoke runnable Java labs: compile stubs, run contract tests against solutions."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAVA_HOME = os.environ.get("JAVA_HOME", "/opt/homebrew/opt/openjdk@21")
MVNW = ROOT / "reference-apps/baypay/mvnw"
TF = Path("/opt/homebrew/bin/terraform")
JAVAC = Path(JAVA_HOME) / "bin" / "javac"

MODULES = ("BUILD-101", "BUILD-102", "FIX-103", "CHALLENGE-104", "BREAKFIX-201")

SOLUTION_OVERLAYS: dict[str, list[tuple[str, str]]] = {
    "BUILD-101": [
        ("solutions/BUILD-101/Money.java", "src/main/java/com/baypay/labs/build101/Money.java"),
        ("solutions/BUILD-101/PaymentStatus.java", "src/main/java/com/baypay/labs/build101/PaymentStatus.java"),
        ("solutions/BUILD-101/PaymentStateMachine.java", "src/main/java/com/baypay/labs/build101/PaymentStateMachine.java"),
        ("solutions/BUILD-101/Payment.java", "src/main/java/com/baypay/labs/build101/Payment.java"),
    ],
    "BUILD-102": [
        ("solutions/BUILD-102/PaymentValidator.java", "src/main/java/com/baypay/labs/build102/PaymentValidator.java"),
    ],
    "FIX-103": [
        ("solutions/FIX-103/CleanPaymentValidator.java", "src/main/java/com/baypay/labs/fix103/CleanPaymentValidator.java"),
    ],
    "CHALLENGE-104": [
        ("solutions/CHALLENGE-104/FasterPostingLoop.java", "src/main/java/com/baypay/labs/challenge104/FasterPostingLoop.java"),
    ],
    "BREAKFIX-201": [
        ("solutions/BREAKFIX-201/SafePaymentLedger.java", "src/main/java/com/baypay/labs/breakfix201/SafePaymentLedger.java"),
    ],
}

HARNESSES = [
    ROOT / "labs/LAB-701/starter/MemoryProbe.java",
    ROOT / "labs/LAB-702/starter/AllocationHarness.java",
    ROOT / "labs/LAB-703/starter/GcVisibleHarness.java",
    ROOT / "labs/FIX-103/starter/MessyPaymentValidator.java",
    ROOT / "labs/CHALLENGE-104/starter/NaivePostingLoop.java",
    ROOT / "labs/BREAKFIX-201/starter/UnsafePaymentLedger.java",
]

TF_DIRS = [
    ROOT / "solutions/BUILD-1101",
    ROOT / "solutions/BUILD-1201",
    ROOT / "solutions/BUILD-1202",
    ROOT / "infrastructure/terraform/baypay-ecs",
]


def run(name: str, cmd: list[str], cwd: Path | None = None) -> None:
    env = os.environ.copy()
    env["JAVA_HOME"] = JAVA_HOME
    env["PATH"] = f"{JAVA_HOME}/bin:{env.get('PATH', '')}"
    print(f"== {name} ==")
    proc = subprocess.run(cmd, cwd=str(cwd or ROOT), env=env, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"FAIL: {name} (exit {proc.returncode})")


def compile_stubs() -> None:
    run(
        "labs stub compile",
        [str(MVNW), "-f", str(ROOT / "labs/pom.xml"), "-q", "test-compile"],
    )


def overlay_and_test() -> None:
    work = Path(tempfile.mkdtemp(prefix="aeje-lab-smoke-"))
    try:
        shutil.copy2(ROOT / "labs/pom.xml", work / "pom.xml")
        for module in MODULES:
            src = ROOT / "labs" / module
            dest = work / module
            shutil.copytree(
                src,
                dest,
                ignore=shutil.ignore_patterns("target", "starter"),
            )
            for rel_src, rel_dest in SOLUTION_OVERLAYS[module]:
                shutil.copy2(ROOT / rel_src, dest / rel_dest)
        run(
            "labs solution contract tests",
            [str(MVNW), "-f", str(work / "pom.xml"), "-q", "test"],
            cwd=work,
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)


def compile_harnesses() -> None:
    out = Path(tempfile.mkdtemp(prefix="aeje-javac-"))
    try:
        for path in HARNESSES:
            run(
                f"javac {path.relative_to(ROOT)}",
                [str(JAVAC), "--release", "21", "-d", str(out), str(path)],
            )
    finally:
        shutil.rmtree(out, ignore_errors=True)


def terraform_validate() -> None:
    if not TF.exists():
        raise SystemExit("FAIL: terraform not found at /opt/homebrew/bin/terraform")
    for tf_dir in TF_DIRS:
        run(
            f"terraform init {tf_dir.relative_to(ROOT)}",
            [str(TF), "init", "-backend=false", "-input=false", "-no-color"],
            cwd=tf_dir,
        )
        run(
            f"terraform validate {tf_dir.relative_to(ROOT)}",
            [str(TF), "validate", "-no-color"],
            cwd=tf_dir,
        )


def reference_app_tests() -> None:
    run(
        "reference-apps/baypay ./mvnw test",
        [str(MVNW), "-q", "test"],
        cwd=ROOT / "reference-apps/baypay",
    )


def interview_smoke() -> None:
    run(
        "interview simulator AEJE-IQ-012",
        [sys.executable, str(ROOT / "interview-bank/simulator.py"), "--mode", "practice", "--id", "AEJE-IQ-012"],
    )


def main() -> int:
    if not MVNW.exists():
        raise SystemExit(f"FAIL: missing Maven wrapper at {MVNW}")
    if not JAVAC.exists():
        raise SystemExit(f"FAIL: javac not found under JAVA_HOME={JAVA_HOME}")
    compile_stubs()
    overlay_and_test()
    compile_harnesses()
    terraform_validate()
    reference_app_tests()
    interview_smoke()
    print("PASS runnable lab smoke")
    return 0


if __name__ == "__main__":
    sys.exit(main())
