#!/usr/bin/env python3
"""Generate Stage 5 diagram sources, SVG, alt text, and PNG."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = [
    ("AEJE-D-028", "jvm", "concept", 7, "L-7.1", 1, "Heap, stacks, metaspace and native memory",
     "flowchart LR\n  P[payment-service process] --> H[Heap]\n  P --> S[Thread stacks]\n  P --> M[Metaspace]\n  P --> N[Native / NMT]",
     ["process RSS", "heap", "stacks", "metaspace", "native"]),
    ("AEJE-D-029", "jvm", "concept", 7, "L-7.2", 2, "Class loading and JIT",
     "flowchart LR\n  CL[Class loader] --> Meta[Metaspace]\n  Byte[Bytecode] --> C1[C1]\n  C1 --> C2[C2]\n  C2 --> Code[Code cache]",
     ["class loader", "metaspace", "C1", "C2", "code cache"]),
    ("AEJE-D-030", "jvm", "concept", 7, "L-7.4", 2, "Garbage collection",
     "flowchart TB\n  Alloc[Allocation / TLAB] --> Young[Young]\n  Young --> Old[Old]\n  Young --> GC[Young GC]\n  Old --> Mixed[Mixed / old GC]",
     ["allocation", "young", "old", "GC pauses"]),
    ("AEJE-D-031", "jvm", "concept", 7, "L-7.6", 3, "JVM in containers",
     "flowchart LR\n  Cgroup[cgroup memory] --> Heap[-Xmx / MaxRAMPercentage]\n  Cgroup --> Native[native + stacks]\n  Heap -.->|never 100 percent| Kill[OOMKill risk]",
     ["cgroup limit", "heap percent", "native headroom", "OOMKill risk"]),
    ("AEJE-D-032", "jvm", "troubleshooting-decision-tree", 8, "L-8.1", 3, "Thread-dump decision tree",
     "flowchart TB\n  Dump[Thread.print] --> R[many RUNNABLE]\n  Dump --> B[BLOCKED cycle]\n  Dump --> W[WAITING on pool]\n  R --> CPU[CPU incident]\n  B --> DL[deadlock]\n  W --> Starve[starvation]",
     ["thread dump", "RUNNABLE", "deadlock", "WAITING"]),
    ("AEJE-D-033", "jvm", "incident", 8, "INCIDENT-801", 3, "CPU 98 percent",
     "flowchart LR\n  LB[load balancer] --> E2[pay-prod-east-2 CPU 98]\n  LB --> E1[east-1 healthy]\n  E2 --> Threads[RUNNABLE hot frames]",
     ["east-2 high CPU", "east-1 healthy", "RUNNABLE frames"]),
    ("AEJE-D-034", "jvm", "incident", 8, "INCIDENT-802", 3, "Memory leak",
     "flowchart TB\n  Traffic[retries] --> Map[growing in-memory map]\n  Map --> Old[old gen up only]\n  Old --> Hist[one type dominates histogram]",
     ["retries", "growing map", "old gen", "histogram"]),
    ("AEJE-D-035", "jvm", "incident", 8, "INCIDENT-803", 3, "Deadlock",
     "flowchart LR\n  T1[payment thread] --> L1[lock A]\n  T2[job thread] --> L2[lock B]\n  T1 -.-> L2\n  T2 -.-> L1",
     ["two threads", "two locks", "wait cycle"]),
    ("AEJE-D-036", "jvm", "incident", 8, "INCIDENT-804", 3, "Thread-pool exhaustion",
     "flowchart LR\n  HTTP[Tomcat 200/200] --> Wait[WAITING]\n  Wait --> Down[downstream client pool]\n  DB[Hikari idle] -.-> HTTP",
     ["HTTP pool full", "WAITING", "downstream", "JDBC idle"]),
    ("AEJE-D-037", "jvm", "incident", 8, "INCIDENT-806", 3, "Container OOM",
     "flowchart TB\n  Limit[cgroup 512Mi] --> Xmx[-Xmx 512m]\n  Xmx --> RSS[RSS + native]\n  RSS --> Kill[OOMKilled]",
     ["512Mi limit", "Xmx equals limit", "RSS plus native", "OOMKilled"]),
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
