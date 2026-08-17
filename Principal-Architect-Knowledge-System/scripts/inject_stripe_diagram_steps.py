#!/usr/bin/env python3
"""Inject numbered Mermaid labels and step-by-step explanation tables."""

from __future__ import annotations

import re
from pathlib import Path

from stripe_diagram_steps_data import DIAGRAM_STEPS, step_table_markdown

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "32-real-world-scenarios" / "stripe-payment-idempotency.md"

MERMAID_DIAGRAM_IDS = [
    "aws-deployment-context",
    "interview-aws-reference",
    "interview-timeout-sequence",
    "aws-whiteboard",
    "aws-sizing-5k",
    "sticky-routing",
    "c4-logical",
    "vpc-production-full",
    "pattern-a",
    "pattern-b",
    "state-machine",
    "data-aurora",
    "data-dynamodb",
    "request-path-sequence",
    "ambiguous-timeout-sequence",
    "webhook-sqs",
    "reconciliation",
    "client-spa",
    "authority-failover",
    "multi-region-dr",
    "single-region-multi-az",
    "single-region-az-failover",
    "multi-region-dr",
    "dr-failover-sequence",
    "active-passive-vs-aa",
    "dynamodb-global-antipattern",
    "active-active-sequence",
    "component-failover",
    "webhook-dr",
    "sweeper",
    "dr-game-day",
    "security-perimeter",
    "observability",
    "gantt-rollout",
    "test-environment",
    "production-readiness",
]

PNG_DIAGRAM_IDS = [
    "aws-deployment-context",
    "vpc-production-full",
    "pattern-a",
    "pattern-b",
    "data-aurora",
    "data-dynamodb",
    "request-path-sequence",
    "webhook-sqs",
    "reconciliation",
    "client-spa",
    "single-region-multi-az",
    "multi-region-dr",
    "active-passive-vs-aa",
    "webhook-dr",
    "security-perimeter",
    "observability",
    "sweeper",
    "dr-game-day",
]

PNG_FILES = [
    "01-end-to-end-overview.png",
    "02-vpc-production-full-stack.png",
    "03-pattern-a-merchant.png",
    "04-pattern-b-platform.png",
    "05-data-aurora-multi-az.png",
    "06-data-dynamodb-hybrid.png",
    "07-request-path-alb-ecs.png",
    "08-webhook-sqs-pipeline.png",
    "09-reconciliation-eventbridge.png",
    "10-client-cloudfront-spa.png",
    "11-single-region-multi-az.png",
    "12-multi-region-dr.png",
    "13-active-passive-vs-active-active.png",
    "14-webhook-dr-failover.png",
    "15-security-perimeter.png",
    "16-observability.png",
    "17-sweeper-lambda.png",
    "18-dr-game-day.png",
]


def _strip_existing_labels(line: str) -> str:
    """Remove existing |"N. ..."| edge labels for idempotent re-run."""
    return re.sub(r'\|"?[0-9]+[a-z]?\.\s[^"|]*"?\|', "", line)


def number_flowchart(body: str, diagram_id: str) -> str:
    steps = DIAGRAM_STEPS.get(diagram_id, [])
    if not steps:
        return body
    out: list[str] = []
    step_i = 0
    for line in body.splitlines():
        raw = _strip_existing_labels(line)
        if "-->" in raw and "subgraph" not in raw.lower() and step_i < len(steps):
            # chain: A --> B --> C
            if raw.count("-->") >= 1 and not raw.strip().startswith("%%"):
                num, action, _ = steps[step_i]
                label = f'|"{num}. {action}"|'
                if "-->" in raw and "|" not in raw:
                    parts = re.split(r"\s*-->\s*", raw, maxsplit=1)
                    if len(parts) == 2:
                        left, right = parts[0], parts[1]
                        indent = line[: len(line) - len(line.lstrip())]
                        line = f"{indent}{left.strip()} -->{label} {right.strip()}"
                        step_i += 1
        out.append(line)
    return "\n".join(out)


def number_sequence(body: str, diagram_id: str) -> str:
    steps = DIAGRAM_STEPS.get(diagram_id, [])
    if not steps:
        return body
    out: list[str] = []
    step_i = 0
    msg_re = re.compile(r"^(\s*)(\S+)\s*(->>|-->>)\s*([^:]+):\s*(.*)$")
    for line in body.splitlines():
        m = msg_re.match(line)
        if m and step_i < len(steps) and "Note over" not in line:
            indent, src, arrow, dst, msg = m.groups()
            msg = strip_existing_sequence_numbers(msg)
            if msg:
                num, action, _ = steps[step_i]
                line = f"{indent}{src}{arrow}{dst}: {num}. {action} — {msg.strip()}"
                step_i += 1
        out.append(line)
    return "\n".join(out)


def number_state_diagram(body: str, diagram_id: str) -> str:
    steps = DIAGRAM_STEPS.get(diagram_id, [])
    if not steps:
        return body
    out: list[str] = []
    step_i = 0
    trans_re = re.compile(r"^(\s*)(\S+)\s*-->\s*(\S+):\s*(.*)$")
    for line in body.splitlines():
        m = trans_re.match(line)
        if m and step_i < len(steps) and m.group(2) != "[*]":
            indent, src, dst, lbl = m.groups()
            num, action, _ = steps[step_i]
            line = f'{indent}{src} --> {dst}: {num}. {action}'
            step_i += 1
        out.append(line)
    return "\n".join(out)


def number_mermaid_body(body: str, diagram_id: str) -> str:
    body = body.strip()
    if body.lstrip().startswith("sequenceDiagram"):
        result = number_sequence(body + "\n", diagram_id)
    elif body.lstrip().startswith("stateDiagram"):
        result = number_state_diagram(body + "\n", diagram_id)
    else:
        result = number_flowchart(body + "\n", diagram_id)
    return result if result.endswith("\n") else result + "\n"


STEP_TABLE_BLOCK = (
    r"\*\*Step-by-step flow:\*\*\n\n"
    r"\| Step \| Action \| Explanation \|\n"
    r"\|[-| ]+\|\n"
    r"(?:\|[^\n]+\|\n)+"
)


def strip_step_tables_after_mermaid(text: str) -> str:
    pattern = re.compile(
        rf"(```mermaid\n.*?```)\n+(?:{STEP_TABLE_BLOCK})+",
        re.DOTALL,
    )
    return pattern.sub(r"\1\n\n", text)


def dedupe_consecutive_step_tables(text: str) -> str:
    while True:
        updated = re.sub(
            rf"({STEP_TABLE_BLOCK})\s+\1",
            r"\1",
            text,
            flags=re.DOTALL,
        )
        if updated == text:
            return text
        text = updated


def strip_existing_sequence_numbers(msg: str) -> str:
    msg = re.sub(r"^\d+\.\s*[^—]+—\s*", "", msg.strip())
    return re.sub(r"^\d+\.\s*", "", msg.strip())


def inject_mermaid(text: str) -> str:
    text = strip_step_tables_after_mermaid(text)
    text = dedupe_consecutive_step_tables(text)
    pattern = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
    idx = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal idx
        if idx >= len(MERMAID_DIAGRAM_IDS):
            return match.group(0)
        diagram_id = MERMAID_DIAGRAM_IDS[idx]
        idx += 1
        body = number_mermaid_body(match.group(1), diagram_id)
        table = step_table_markdown(diagram_id)
        return f"```mermaid\n{body}```\n{table}"

    return pattern.sub(replacer, text)


def inject_png_sections(text: str) -> str:
    for diagram_id, png_file in zip(PNG_DIAGRAM_IDS, PNG_FILES):
        table = step_table_markdown(diagram_id)
        if not table:
            continue
        text = re.sub(
            rf"(!\[[^\]]*\]\(/img/aws-architecture/stripe-payment-idempotency/{re.escape(png_file)}\)\n)"
            rf"(?:\*Figure:[^\n]*\n\n)?"
            rf"(?:{STEP_TABLE_BLOCK})+",
            r"\1",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            rf"(!\[[^\]]*\]\(/img/aws-architecture/stripe-payment-idempotency/{re.escape(png_file)}\)\n)",
            rf"\1{table}",
            text,
            count=1,
        )
    return text


def add_convention_note(text: str) -> str:
    note = (
        "> **Diagram convention:** Arrows and messages are labeled **1, 2, 3…** "
        "to show processing order. Each diagram is followed by a **Step-by-step flow** table "
        "explaining every numbered step.\n\n"
    )
    marker = "# Scenario: Stripe Payment Idempotency\n\n"
    if note not in text and marker in text:
        text = text.replace(marker, marker + note)
    return text


def repair_mermaid_fences(text: str) -> str:
    """Fix closing ``` merged onto last diagram line (idempotent repair)."""
    return re.sub(
        r"([^`\n]+)```\n+(\s*\*\*Step-by-step flow:\*\*)",
        r"\1\n```\n\n\2",
        text,
    )


def main() -> int:
    text = DOC.read_text(encoding="utf-8")
    text = repair_mermaid_fences(text)
    text = dedupe_consecutive_step_tables(text)
    text = add_convention_note(text)
    text = inject_mermaid(text)
    text = inject_png_sections(text)
    text = dedupe_consecutive_step_tables(text)
    DOC.write_text(text, encoding="utf-8")
    print(f"Updated {DOC.relative_to(ROOT)}")
    print(f"  Numbered + explained {len(MERMAID_DIAGRAM_IDS)} Mermaid diagrams")
    print(f"  Step tables for {len(PNG_DIAGRAM_IDS)} PNG exports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
