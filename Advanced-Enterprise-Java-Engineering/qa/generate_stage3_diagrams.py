#!/usr/bin/env python3
"""Generate Stage 3 diagram sources, SVG, alt text, and PNG."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = [
    ("AEJE-D-001", "java", "concept", 1, "L-1.1", 1, "Modern Java, JDK and JVM stack",
     "flowchart TB\n  JDK[JDK 21 toolchain] --> Bytecode[Class files]\n  Bytecode --> JVM[HotSpot JVM]\n  JVM --> Heap[Heap]\n  JVM --> Threads[Threads]\n  App[BayPay payment-service] --> JDK",
     ["JDK 21", "bytecode", "HotSpot", "BayPay"]),
    ("AEJE-D-002", "java", "concept", 1, "L-1.2", 1, "SOLID and immutability",
     "flowchart LR\n  Cmd[Payment command] --> Money[Money value]\n  Money --> Payment[Payment entity]\n  Payment --> SM[State machine]",
     ["immutable Money", "Payment", "state machine"]),
    ("AEJE-D-003", "java", "component", 1, "BUILD-101", 2, "BayPay transaction domain model",
     "flowchart TB\n  Customer --> Account\n  Account --> Payment\n  Payment --> Ledger[LedgerTransaction]\n  Payment --> Refund\n  Ledger --> TE[TransactionEvent]\n  Payment --> Audit[AuditEvent]",
     ["Customer", "Account", "Payment", "Refund", "LedgerTransaction"]),
    ("AEJE-D-004", "java", "sequence", 1, "BUILD-102", 2, "Payment validation flow",
     "sequenceDiagram\n  Client->>API: POST payment\n  API->>Val: validate amount currency account\n  Val-->>API: ok or decline\n  API-->>Client: 201 COMPLETED or 422 DECLINED",
     ["validate", "DECLINED", "COMPLETED"]),
    ("AEJE-D-005", "java", "concept", 2, "L-2.1", 1, "Java memory visibility",
     "flowchart LR\n  T1[Worker thread] -->|write| Main[Main memory]\n  T2[Worker thread] -->|stale read without happens-before| Cache[CPU cache]",
     ["happens-before", "worker threads", "main memory"]),
    ("AEJE-D-006", "java", "incident", 2, "BREAKFIX-201", 3, "Duplicate payment race",
     "flowchart TB\n  A[Two POSTs same invoice] --> R[Race on ledger map]\n  R --> Dup[Two COMPLETED posts]",
     ["race", "duplicate COMPLETED"]),
    ("AEJE-D-007", "java", "incident", 2, "INCIDENT-202", 3, "Deadlocked payment workers",
     "flowchart LR\n  PW[Payment worker] --> L1[Lock A]\n  RW[Refund worker] --> L2[Lock B]\n  PW -.-> L2\n  RW -.-> L1",
     ["two workers", "two locks", "wait cycle"]),
    ("AEJE-D-008", "java", "component", 2, "ARCHITECT-203", 3, "Safe concurrent payment processing",
     "flowchart TB\n  In[Authorize] --> Q[Single writer or striped lock]\n  Q --> Ledger[Ledger]\n  In --> Idem[Idempotency store]",
     ["idempotency store", "single writer or striped lock"]),
    ("AEJE-D-009", "spring", "concept", 3, "L-3.1", 1, "Spring IoC container",
     "flowchart TB\n  Ctx[ApplicationContext] --> Ctrl[PaymentController]\n  Ctx --> Svc[PaymentApplicationService]\n  Ctx --> Repo[PaymentRepository]",
     ["ApplicationContext", "constructor injection"]),
    ("AEJE-D-010", "spring", "request-flow", 3, "BUILD-301", 2, "Payment REST API request flow",
     "sequenceDiagram\n  Client->>Ctrl: POST /api/v1/payments + Idempotency-Key\n  Ctrl->>Svc: create\n  Svc->>Post: postAuthorized\n  Svc-->>Ctrl: Payment COMPLETED\n  Ctrl-->>Client: 201",
     ["Idempotency-Key", "POST payments", "201"]),
    ("AEJE-D-011", "spring", "sequence", 3, "L-3.4", 2, "JPA transaction boundary",
     "sequenceDiagram\n  Svc->>Tx: @Transactional begin\n  Tx->>DB: persist Payment\n  Tx->>DB: persist Ledger\n  Tx->>Tx: commit",
     ["one transaction", "payment and ledger"]),
    ("AEJE-D-012", "spring", "component", 3, "BUILD-305", 2, "Actuator health and readiness",
     "flowchart LR\n  K8s[Probe] --> Live[/actuator/health/liveness]\n  K8s --> Ready[/actuator/health/readiness]\n  Ready --> DB[DataSource health]",
     ["liveness", "readiness", "DataSource"]),
    ("AEJE-D-013", "spring", "incident", 3, "FIX-304", 3, "Transaction rollback bug",
     "flowchart TB\n  Refund[Refund API] --> Catch[Exception swallowed]\n  Catch --> Pay[Payment marked refunded]\n  Catch --> Gap[Ledger row missing]",
     ["refund", "ledger missing", "exception path"]),
    ("AEJE-D-014", "java", "concept", 4, "L-4.1", 1, "Servlet and Jakarta EE model",
     "flowchart LR\n  HTTP --> Servlet[Jakarta Servlet]\n  Servlet --> Spring[DispatcherServlet]\n  Spring --> Ctrl[RestController]",
     ["Servlet", "DispatcherServlet", "RestController"]),
    ("AEJE-D-015", "java", "concept", 4, "ARCHITECT-401", 2, "Spring to Jakarta mapping",
     "flowchart TB\n  DI[Spring DI] --- CDI[CDI]\n  Tx[@Transactional] --- JTA[JTA]\n  JPA[Spring Data JPA] --- EM[EntityManager]\n  Rest[RestController] --- JAX[JAX-RS]",
     ["DI to CDI", "Transactional to JTA", "JPA to EntityManager"]),
    ("AEJE-D-016", "java", "incident", 4, "INCIDENT-402", 3, "Connection pool exhaustion",
     "flowchart LR\n  App[BayPay workers] --> Pool[JDBC pool 50/50]\n  Pool --> Wait[Waiters / timeout]\n  Pool --> DB[(PostgreSQL)]",
     ["pool exhausted", "waiters", "database"]),
    ("AEJE-D-017", "java", "incident", 4, "INCIDENT-403", 3, "Transaction boundary failure",
     "flowchart TB\n  Tx1[Payment TX commits]\n  Tx2[Ledger write not enlisted]\n  Tx1 --> PayOK[Payment COMPLETED]\n  Tx2 --> Missing[No ledger row]",
     ["payment committed", "ledger not enlisted"]),
]


def svg_box_flow(did: str, title: str, boxes: list[str]) -> str:
    w, h = 960, 420
    gap = 24
    bw = min(200, (w - 80 - gap * (len(boxes) - 1)) // max(len(boxes), 1))
    y = 180
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">',
        f'<title id="t">{did}: {title}</title>',
        f'<desc id="d">{title}</desc>',
        '<rect width="100%" height="100%" fill="#f4f7fa"/>',
        f'<text x="40" y="48" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#0a1f33">{did}</text>',
        f'<text x="40" y="78" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="#0d8fad">{title}</text>',
        '<text x="40" y="400" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#5c6b7a">BayPay Financial Services is fictional. BayLearn AEJE.</text>',
    ]
    x = 40
    for i, label in enumerate(boxes):
        parts.append(
            f'<rect x="{x}" y="{y}" width="{bw}" height="72" rx="6" fill="#ffffff" stroke="#0d8fad" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x + bw/2}" y="{y + 42}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">{label}</text>'
        )
        if i < len(boxes) - 1:
            x2 = x + bw + gap
            parts.append(
                f'<line x1="{x + bw}" y1="{y + 36}" x2="{x2}" y2="{y + 36}" stroke="#0a1f33" stroke-width="2" marker-end="url(#arrow)"/>'
            )
        x += bw + gap
    parts.insert(
        4,
        '<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#0a1f33"/></marker></defs>',
    )
    parts.append("</svg>")
    return "\n".join(parts)


def write_png(path: Path, width: int, height: int, rgb: tuple[int, int, int]) -> None:
    """Solid PNG so the asset pipeline has a raster sibling (presentation SVG is canonical)."""
    raw = b"".join(b"\x00" + bytes(rgb) * width for _ in range(height))
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> None:
    for did, folder, dtype, module, maps, cx, title, mermaid, boxes in DIAGRAMS:
        d = ROOT / "diagrams" / folder
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{did}.source.md").write_text(
            f"# {did} — {title}\n\n"
            f"- Type: {dtype}\n- Module: {module}\n- Maps to: {maps}\n- Complexity: {cx}\n\n"
            f"```mermaid\n{mermaid}\n```\n",
            encoding="utf-8",
        )
        (d / f"{did}.alt.md").write_text(
            f"Diagram {did}: {title}. Left-to-right labeled boxes: "
            + ", ".join(boxes)
            + ". BayPay is a fictional payment platform used for instruction.\n",
            encoding="utf-8",
        )
        (d / f"{did}.svg").write_text(svg_box_flow(did, title, boxes), encoding="utf-8")
        write_png(d / f"{did}.png", 960, 420, (244, 247, 250))
        print(did)
    print("wrote", len(DIAGRAMS), "diagrams")


if __name__ == "__main__":
    main()
