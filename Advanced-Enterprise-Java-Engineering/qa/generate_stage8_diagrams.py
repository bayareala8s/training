#!/usr/bin/env python3
"""Generate Stage 8 diagram sources, SVG, alt text, and PNG."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = [
    (
        "AEJE-D-059",
        "observability",
        "concept",
        13,
        "L-13.1",
        1,
        "Logs, metrics and traces",
        "flowchart LR\n  Log[JSON logs] --> Corr[correlationId]\n  Met[metrics] --> Prom[Prometheus]\n  Tr[traceparent] --> Span[spans]",
        ["JSON logs", "metrics", "traces", "correlationId"],
    ),
    (
        "AEJE-D-060",
        "observability",
        "concept",
        13,
        "L-13.2",
        2,
        "RED, USE, SLI and SLO",
        "flowchart LR\n  RED[RED rate errors duration] --> SLI[SLI]\n  USE[USE heap Hikari threads] --> Sat[saturation]\n  SLI --> SLO[SLO 99.9 percent]",
        ["RED", "USE", "SLI", "SLO 99.9%"],
    ),
    (
        "AEJE-D-061",
        "observability",
        "component",
        13,
        "BUILD-1300",
        3,
        "BayPay operations dashboard",
        "flowchart TB\n  Rate[POST rate] --> Dash[ops dashboard]\n  P99[P99 duration] --> Dash\n  Burn[SLO burn] --> Dash\n  Hikari[Hikari pending] --> Dash",
        ["rate", "P99", "SLO burn", "Hikari"],
    ),
    (
        "AEJE-D-062",
        "observability",
        "incident",
        13,
        "INCIDENT-1301",
        3,
        "Throughput collapse and P99 spike",
        "flowchart LR\n  Rel[new release] --> Red[rate down]\n  Red --> P99[P99 up]\n  P99 --> Gate[gated evidence]",
        ["release", "rate down", "P99 up", "gates"],
    ),
    (
        "AEJE-D-063",
        "security",
        "security-trust-boundary",
        14,
        "L-14.1",
        2,
        "TLS and PKI trust boundary",
        "flowchart LR\n  Merch[merchant TLS] --> Edge[ALB / edge cert]\n  Edge --> Task[task HTTP 8080]\n  CA[public CA / ACM] --> Edge",
        ["merchant TLS", "edge cert", "task 8080", "ACM/CA"],
    ),
    (
        "AEJE-D-064",
        "security",
        "deployment",
        14,
        "ARCHITECT-1401",
        4,
        "99.99 percent HA failure domains",
        "flowchart TB\n  Task[task] --> AZ[AZ]\n  AZ --> LB[load balancer]\n  LB --> Reg[region]\n  Id[identity / TLS] --> LB",
        ["task", "AZ", "load balancer", "region"],
    ),
    (
        "AEJE-D-065",
        "security",
        "incident",
        14,
        "INCIDENT-1402",
        3,
        "Certificate expiration",
        "flowchart LR\n  Merch[merchant HTTPS] --> HS[handshake fail]\n  Task[task RUNNING 8080] --> OK[HTTP OK inside]\n  HS --> Gate[gated TLS evidence]",
        ["HTTPS fail", "task healthy", "gates"],
    ),
    (
        "AEJE-D-066",
        "security",
        "executive",
        14,
        "DR-1403",
        4,
        "Regional DR, RTO and RPO",
        "flowchart LR\n  West[us-west-2 gone] --> RPO[RPO payment vs report]\n  RPO --> East[paper us-east-1]\n  East --> RTO[RTO to take POSTs]",
        ["west gone", "RPO", "east paper", "RTO"],
    ),
    (
        "AEJE-D-067",
        "security",
        "security-trust-boundary",
        14,
        "SECURITY-1404",
        4,
        "BayPay threat model",
        "flowchart TB\n  API[POST payments] --> Idk[Idempotency-Key]\n  API --> Frz[frozen account]\n  API --> Sec[secrets / TLS]",
        ["payments API", "idempotency", "frozen account", "secrets/TLS"],
    ),
]


def svg_box_flow(did: str, title: str, boxes: list[str]) -> str:
    w, h = 960, 420
    gap = 20
    bw = min(180, (w - 80 - gap * (len(boxes) - 1)) // max(len(boxes), 1))
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
