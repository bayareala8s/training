#!/usr/bin/env python3
"""Hand-drawn BayPay architecture / stack teaching diagrams. No new AEJE-D catalog IDs."""
from __future__ import annotations

import shutil
import struct
import subprocess
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "diagrams" / "java" / "baypay"


def png_placeholder(path: Path, width: int = 1100, height: int = 520) -> None:
    raw = b"".join(b"\x00" + bytes((244, 247, 250)) * width for _ in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def rasterize(svg: Path, png: Path, height: int = 520) -> None:
    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        subprocess.run([rsvg, "-h", str(height), "-o", str(png), str(svg)], check=True)
        return
    ql = shutil.which("qlmanage")
    if ql:
        out = png.parent
        subprocess.run([ql, "-t", "-s", "1920", "-o", str(out), str(svg)], check=True, capture_output=True)
        thumb = out / f"{svg.name}.png"
        if thumb.exists():
            thumb.rename(png)
            return
    png_placeholder(png, 1100, height)


HEADER = """<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="520" viewBox="0 0 1100 520" role="img" aria-labelledby="t d">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#0a1f33"/></marker>
  <marker id="arrowTeal" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#0d8fad"/></marker>
</defs>
<rect width="100%" height="100%" fill="#f4f7fa"/>
<text id="t" x="36" y="34" font-family="Helvetica, Arial, sans-serif" font-size="20" fill="#0a1f33">{title}</text>
<text x="36" y="56" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0d8fad">{subtitle}</text>
<desc id="d">{desc}</desc>
"""

FOOTER = """<text x="36" y="506" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#5c6b7a">BayPay Financial Services is fictional. BayLearn AEJE. One process today; extract a module only when scale, store, or team forces it.</text>
</svg>
"""


def card(x: int, y: int, w: int, h: int, fill: str = "#ffffff", stroke: str = "#0d8fad") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def label(x: int, y: int, text: str, size: int = 13, fill: str = "#0a1f33", anchor: str = "middle") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="{size}" fill="{fill}">{text}</text>'
    )


def architecture_svg() -> str:
    return (
        HEADER.format(
            title="1. BayPay is a modular monolith — five Maven modules, one JVM.",
            subtitle="payment-service is the composition root. Posting and notify are in-process events, not extra HTTP hops.",
            desc="Merchants call payment-service. Inside one JVM: API, payment and refund use cases, posting worker, notification listener, and shared domain plus JPA. One database.",
        )
        + card(36, 90, 160, 150, "#e8f4f8")
        + label(116, 130, "Merchants")
        + label(116, 154, "Harbor Market", 12, "#5c6b7a")
        + label(116, 176, "Avery Chen", 12, "#5c6b7a")
        + label(116, 206, "HTTP :8080", 12, "#0d8fad")
        + '<line x1="196" y1="165" x2="248" y2="165" stroke="#0a1f33" stroke-width="2" marker-end="url(#arrow)"/>'
        + card(250, 78, 560, 360, "#ffffff", "#0a1f33")
        + label(530, 104, "payment-service  ·  one Spring Boot process", 15)
        + label(530, 126, "Java 21  ·  Spring Boot 3.5.5  ·  composition root", 12, "#5c6b7a")
        + card(270, 144, 250, 70)
        + label(395, 172, "API  /api/v1/payments", 13)
        + label(395, 194, "/api/v1/refunds  ·  OpenAPI", 12, "#5c6b7a")
        + card(540, 144, 250, 70)
        + label(665, 172, "PaymentApplicationService", 13)
        + label(665, 194, "RefundApplicationService", 12, "#5c6b7a")
        + card(270, 230, 250, 70, "#e8f4f8")
        + label(395, 258, "transaction-worker", 13)
        + label(395, 280, "in-process  ·  ledger post", 12, "#5c6b7a")
        + card(540, 230, 250, 70, "#e8f4f8")
        + label(665, 258, "notification-service", 13)
        + label(665, 280, "in-process  ·  email record", 12, "#5c6b7a")
        + card(270, 316, 520, 100, "#fff8e8", "#c47b00")
        + label(530, 348, "shared", 15)
        + label(530, 372, "Money  ·  Payment  ·  state machine  ·  idempotency", 12, "#5c6b7a")
        + label(530, 394, "Customer  ·  Account  ·  JPA repositories", 12, "#5c6b7a")
        + '<line x1="810" y1="255" x2="868" y2="255" stroke="#0a1f33" stroke-width="2" marker-end="url(#arrow)"/>'
        + card(870, 180, 194, 160, "#e8f4f8")
        + label(967, 230, "One database")
        + label(967, 256, "H2 local", 12, "#5c6b7a")
        + label(967, 278, "Postgres prod profile", 12, "#5c6b7a")
        + label(967, 308, "not five DBs", 12, "#0d8fad")
        + FOOTER
    )


def stack_svg() -> str:
    return (
        HEADER.format(
            title="2. Same app, two runtimes — laptop H2, or student Fargate.",
            subtitle="Student AWS apply: public subnets + IGW + ALB. No NAT, no EKS, no RDS. Profile stays local (H2 in the task).",
            desc="Left: curl to localhost 8080 on Java 21 Spring Boot with H2. Right: merchants to ALB to Fargate 256/512 running the same image. Both use the modular monolith.",
        )
        + card(36, 80, 500, 390)
        + label(286, 110, "Local (default)", 16)
        + label(286, 132, "reference-apps/baypay  ·  ./mvnw spring-boot:run", 12, "#5c6b7a")
        + card(64, 154, 444, 42, "#e8f4f8")
        + label(286, 180, "curl / Swagger  →  localhost:8080", 13)
        + card(64, 210, 444, 42)
        + label(286, 236, "Spring Boot 3.5.5  ·  Java 21  ·  actuator", 13)
        + card(64, 266, 444, 42)
        + label(286, 292, "Five Maven modules in one process", 13)
        + card(64, 322, 444, 42, "#fff8e8", "#c47b00")
        + label(286, 348, "JPA  →  H2 mem  (MODE=PostgreSQL)", 13)
        + label(286, 390, "Health: /actuator/health/liveness", 12, "#5c6b7a")
        + label(286, 412, "Heap teaching: -Xmx must stay below the container limit", 12, "#5c6b7a")
        + label(286, 444, "Never set -Xmx equal to 512 MiB on the Fargate task", 12, "#b42318")
        + card(564, 80, 500, 390)
        + label(814, 110, "Student AWS (us-west-2)", 16)
        + label(814, 132, "BUILD-1101 extra credit  ·  destroy the same day", 12, "#5c6b7a")
        + card(592, 154, 444, 42, "#e8f4f8")
        + label(814, 180, "Merchants  →  ALB :80", 13)
        + card(592, 210, 444, 42)
        + label(814, 236, "ECS Fargate  0.25 vCPU / 512 MiB", 13)
        + card(592, 266, 444, 42)
        + label(814, 292, "Same image  ·  SPRING_PROFILES_ACTIVE=local", 13)
        + card(592, 322, 444, 42, "#fff8e8", "#c47b00")
        + label(814, 348, "H2 inside the task  ·  no RDS apply", 13)
        + label(814, 390, "Public subnets + Internet Gateway", 12, "#5c6b7a")
        + label(814, 412, "ECR baypay/payment-service:&lt;tag&gt;  (never :latest)", 12, "#5c6b7a")
        + label(814, 444, "Do not add NAT, EKS, or Multi-AZ RDS", 12, "#b42318")
        + FOOTER
    )


def path_svg() -> str:
    boxes = [
        ("POST", "Idempotency-Key"),
        ("Replay?", "200 same id"),
        ("Money +", "Authorizer"),
        ("State", "machine"),
        ("Post", "ledger"),
        ("Notify", "in-process"),
        ("201", "COMPLETED"),
    ]
    parts = [
        HEADER.format(
            title="3. Create-payment path — one transaction, then 201 COMPLETED.",
            subtitle="Same key + same body replays. Frozen account declines (422). Email is not on Payment (SOLID S).",
            desc="POST with Idempotency-Key hits replay check, Money and Authorizer, state machine, ledger post, in-process notify, then 201 COMPLETED.",
        )
    ]
    x = 36
    y = 160
    w, h, gap = 132, 110, 16
    for i, (top, bot) in enumerate(boxes):
        fill = "#e8f4f8" if i in (0, 6) else "#ffffff"
        stroke = "#0d7a4f" if i == 6 else "#0d8fad"
        parts.append(card(x, y, w, h, fill, stroke))
        parts.append(label(x + w // 2, y + 48, top, 14))
        parts.append(label(x + w // 2, y + 74, bot, 12, "#5c6b7a"))
        if i < len(boxes) - 1:
            parts.append(
                f'<line x1="{x + w}" y1="{y + h // 2}" x2="{x + w + gap - 4}" y2="{y + h // 2}" '
                f'stroke="#0a1f33" stroke-width="2" marker-end="url(#arrow)"/>'
            )
        x += w + gap
    parts.append(card(36, 300, 1028, 170))
    parts.append(label(550, 336, "What this path refuses", 15))
    parts.append(label(550, 368, "No setStatus on Payment  ·  transitions go through PaymentStateMachine", 13, "#5c6b7a"))
    parts.append(label(550, 394, "No email inside PaymentApplicationService  ·  NotificationListener observes completion", 13, "#5c6b7a"))
    parts.append(label(550, 420, "No card SDK constructed in the service  ·  PaymentAuthorizer is the SOLID D seam", 13, "#5c6b7a"))
    parts.append(label(550, 446, "Same Idempotency-Key + different body → 409  ·  missing key → 400", 13, "#5c6b7a"))
    parts.append(FOOTER)
    return "".join(parts)


def write_pair(stem: str, title: str, mermaid: str, alt: str, svg: str) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    (PACK / f"{stem}.source.md").write_text(
        f"# {title}\n\n- Maps to: reference-apps/baypay, GETTING_STARTED, Module 1\n- Complexity: 1\n\n```mermaid\n{mermaid}\n```\n",
        encoding="utf-8",
    )
    (PACK / f"{stem}.alt.md").write_text(alt.rstrip() + "\n", encoding="utf-8")
    svg_path = PACK / f"{stem}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    rasterize(svg_path, PACK / f"{stem}.png")


def main() -> None:
    write_pair(
        "modular-monolith",
        "BayPay picture 1 — Modular monolith",
        "flowchart LR\n  M[Merchants] --> API[payment-service JVM]\n  API --> Pay[payment + refund]\n  API --> W[transaction-worker in-process]\n  API --> N[notification in-process]\n  Pay --> S[shared domain + JPA]\n  W --> S\n  N --> S\n  S --> DB[(one database)]",
        "Diagram: Merchants call one payment-service JVM. Payment and refund use cases, an in-process posting worker, and an in-process notification listener sit on shared domain and JPA. One database. BayPay is fictional instruction.",
        architecture_svg(),
    )
    write_pair(
        "runtime-stack",
        "BayPay picture 2 — Local and student AWS stack",
        "flowchart TB\n  subgraph Local\n    C[curl localhost:8080] --> SB[Java 21 Spring Boot]\n    SB --> H2[(H2 mem)]\n  end\n  subgraph AWS[us-west-2 student]\n    A[ALB :80] --> F[Fargate 256/512]\n    F --> H2b[(H2 in task)]\n  end",
        "Diagram: Left, local curl to localhost 8080 on Java 21 Spring Boot with H2. Right, student AWS in us-west-2: ALB to Fargate 256 CPU 512 MiB running the same local profile. No NAT, EKS, or RDS. BayPay is fictional instruction.",
        stack_svg(),
    )
    write_pair(
        "payment-path",
        "BayPay picture 3 — Create-payment path",
        "flowchart LR\n  P[POST + key] --> R[replay or create]\n  R --> A[Money + Authorizer]\n  A --> SM[state machine]\n  SM --> L[ledger post]\n  L --> N[notify]\n  N --> C[201 COMPLETED]",
        "Diagram: Create payment flows POST with Idempotency-Key, replay check, Money and Authorizer, state machine, ledger post, in-process notify, then 201 COMPLETED. Frozen accounts decline. BayPay is fictional instruction.",
        path_svg(),
    )
    (PACK / "README.md").write_text(
        """# BayPay architecture and stack

Three teaching pictures for [reference-apps/baypay](../../../reference-apps/baypay/README.md). Not new AEJE-D catalog IDs. BayPay is fictional.

| # | File | What to see |
|---|---|---|
| 1 | [modular-monolith.svg](modular-monolith.svg) | Five Maven modules in one JVM. Posting and notify are in-process. One database. |
| 2 | [runtime-stack.svg](runtime-stack.svg) | Laptop (`localhost:8080` + H2) versus student Fargate in `us-west-2` (ALB, no NAT/RDS). |
| 3 | [payment-path.svg](payment-path.svg) | `POST /api/v1/payments` from Idempotency-Key to `201 COMPLETED`. |

Open the SVG (or the mermaid in `*.source.md`). PNG is a raster sibling for slides.

Read left to right: **who lives in the process → where it runs → what one create does.**
""",
        encoding="utf-8",
    )
    print("wrote BayPay architecture / stack visual pack")


if __name__ == "__main__":
    main()
