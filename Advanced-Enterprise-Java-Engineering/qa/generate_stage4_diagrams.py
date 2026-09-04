#!/usr/bin/env python3
"""Generate Stage 4 diagram sources, SVG, alt text, and PNG."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = [
    ("AEJE-D-018", "websphere", "concept", 5, "L-5.1", 1, "WebSphere ND cell, DMGR, node, server",
     "flowchart TB\n  DMGR[dmgr-east] --> NA1[nodeagent-pay-1]\n  DMGR --> NA2[nodeagent-pay-2]\n  NA1 --> Pay1[Pay1]\n  NA2 --> Pay2[Pay2]\n  NA2 --> Pay3[Pay3]",
     ["dmgr-east", "node agents", "Pay1", "Pay2", "Pay3"]),
    ("AEJE-D-019", "websphere", "deployment", 5, "ARCHITECT-501", 3, "BayPay WebSphere ND current state",
     "flowchart LR\n  IHS[ihs-east] --> PC[PaymentCluster]\n  IHS --> RC[RefundCluster]\n  PC --> BUS[BayPayBus]\n  RC --> BUS\n  BUS --> DB[(baypay DB)]",
     ["ihs-east", "PaymentCluster", "RefundCluster", "BayPayBus", "database"]),
    ("AEJE-D-020", "websphere", "component", 5, "L-5.3", 2, "JDBC, JNDI and JMS",
     "flowchart TB\n  App[payment.ear] --> JNDI[JNDI]\n  JNDI --> JDBC[jdbc/baypay]\n  JNDI --> JMS[jms/paymentEvents]\n  JDBC --> DB[(PostgreSQL)]\n  JMS --> BUS[SIBus BayPayBus]",
     ["JNDI", "jdbc/baypay", "jms/paymentEvents", "BayPayBus"]),
    ("AEJE-D-021", "websphere", "incident", 5, "INCIDENT-502", 3, "Cluster members stop processing",
     "flowchart LR\n  IHS[ihs-east TCP-up] --> Pay1[Pay1 serving]\n  IHS --> Pay2[Pay2 hung]\n  IHS --> Pay3[Pay3 hung]",
     ["IHS plugin", "Pay1 serving", "Pay2 hung", "Pay3 hung"]),
    ("AEJE-D-022", "websphere", "incident", 5, "INCIDENT-504", 3, "Deployment failure",
     "flowchart TB\n  DMGR[dmgr-east install 4.12] --> Sync[node sync]\n  Sync --> Pay1[Pay1 4.12]\n  Sync --> Stuck[nodeagent-pay-2 down]\n  Stuck --> Old[Pay2/Pay3 4.11]",
     ["install 4.12", "Pay1 new", "nodeagent down", "Pay2/Pay3 old"]),
    ("AEJE-D-023", "liberty", "current-state-target-state", 6, "L-6.1", 2, "Traditional WebSphere vs Liberty",
     "flowchart LR\n  ND[BayPayCell ND] -->|modernize| LIB[Liberty server.xml]\n  ND -.->|do not grow| X[No new cell]\n  LIB --> WAR[payment WAR]",
     ["BayPayCell source", "Liberty target", "no new ND cell"]),
    ("AEJE-D-024", "liberty", "component", 6, "L-6.2", 2, "Liberty features and server.xml",
     "flowchart TB\n  XML[server.xml] --> FM[featureManager]\n  FM --> S[servlet-6.0]\n  FM --> J[jdbc-4.3 jndi-1.0]\n  XML --> DS[jdbc/baypay-payment]\n  XML --> WAR[webApplication]",
     ["featureManager", "servlet-6.0", "jdbc-4.3", "isolated DataSource"]),
    ("AEJE-D-025", "liberty", "modernization", 6, "MODERNIZE-602", 3, "BayPay Liberty adaptation",
     "flowchart LR\n  EAR[payment.ear on ND] --> WAR[payment-service.war]\n  WAR --> LIB[Liberty]\n  LIB --> DS[jdbc/baypay-payment]",
     ["ear to war", "Liberty", "isolated jdbc/baypay-payment"]),
    ("AEJE-D-026", "liberty", "modernization", 6, "MODERNIZE-603", 3, "Configuration externalization",
     "flowchart LR\n  ENV[server.env BAYPAY_DB_*] --> XML[server.xml variables]\n  XML --> DS[DataSource]\n  GIT[git] -.->|no password| XML",
     ["server.env", "variables", "no password in git"]),
    ("AEJE-D-027", "liberty", "modernization", 6, "ARCHITECT-604", 4, "Migration waves and rollback",
     "flowchart LR\n  W0[Wave 0 inventory] --> W1[Wave 1 Refund Liberty]\n  W1 --> W2[Wave 2 Payment canary]\n  W2 --> W3[Wave 3 decommission ND]\n  W2 -.->|rollback| PC[PaymentCluster]",
     ["Wave 0", "Wave 1 refund", "Wave 2 canary", "Wave 3 exit", "rollback to ND"]),
]


def svg_box_flow(did: str, title: str, boxes: list[str]) -> str:
    w, h = 960, 420
    gap = 20
    bw = min(170, (w - 80 - gap * (len(boxes) - 1)) // max(len(boxes), 1))
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
            f'<text x="{x + bw/2}" y="{y + 42}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">{label}</text>'
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
