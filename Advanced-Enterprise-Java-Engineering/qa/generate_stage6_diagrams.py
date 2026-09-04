#!/usr/bin/env python3
"""Generate Stage 6 diagram sources, SVG, alt text, and PNG."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = [
    ("AEJE-D-038", "containers", "concept", 9, "L-9.1", 1, "OCI container layers",
     "flowchart LR\n  Base[JRE base] --> Deps[deps layer]\n  Deps --> App[app layer]\n  App --> Cfg[config / user]",
     ["base JRE", "deps", "app", "user/config"]),
    ("AEJE-D-039", "containers", "component", 9, "BUILD-901", 2, "BayPay container image",
     "flowchart LR\n  Build[JDK build stage] --> Jar[payment-service.jar]\n  Jar --> Runtime[JRE runtime]\n  Runtime --> Port[8080 non-root]",
     ["build stage", "JAR", "JRE runtime", "8080"]),
    ("AEJE-D-040", "containers", "security-trust-boundary", 9, "SECURITY-903", 3, "Container trust boundary",
     "flowchart TB\n  Img[image] --> User[non-root]\n  Img --> Sec[no secrets in layers]\n  Img --> Fs[read-only rootfs]\n  Host[host / kube] -.-> Img",
     ["image", "non-root", "no layer secrets", "host boundary"]),
    ("AEJE-D-041", "containers", "concept", 9, "L-9.6", 2, "Java resource sizing",
     "flowchart LR\n  Limit[cgroup limit] --> Heap[MaxRAMPercentage]\n  Limit --> Native[native headroom]\n  Heap -.->|not 100 percent| Kill[OOMKill]",
     ["cgroup", "heap percent", "native", "OOMKill risk"]),
    ("AEJE-D-042", "kubernetes", "concept", 10, "L-10.1", 1, "Pods, Deployments and ReplicaSets",
     "flowchart TB\n  D[Deployment] --> RS[ReplicaSet]\n  RS --> P1[Pod]\n  RS --> P2[Pod]\n  RS --> P3[Pod]",
     ["Deployment", "ReplicaSet", "Pods"]),
    ("AEJE-D-043", "openshift", "deployment", 10, "L-10.2", 2, "OpenShift Routes vs Ingress",
     "flowchart LR\n  Client --> Route[Route or Ingress]\n  Route --> Svc[Service payment-service]\n  Svc --> Pods[Pods 8080]",
     ["client", "Route or Ingress", "Service", "Pods"]),
    ("AEJE-D-044", "kubernetes", "incident", 10, "INCIDENT-1001", 3, "CrashLoopBackOff",
     "flowchart LR\n  Start[container start] --> Exit[Exit 1]\n  Exit --> CLB[CrashLoopBackOff]\n  Logs[app logs] --> Exit",
     ["start", "Exit 1", "CrashLoopBackOff"]),
    ("AEJE-D-045", "kubernetes", "incident", 10, "INCIDENT-1002", 3, "OOMKilled",
     "flowchart TB\n  Limit[512Mi limit] --> Xmx[-Xmx 512m]\n  Xmx --> Kill[OOMKilled]",
     ["memory limit", "Xmx equals limit", "OOMKilled"]),
    ("AEJE-D-046", "kubernetes", "incident", 10, "INCIDENT-1003", 3, "Readiness failure",
     "flowchart LR\n  Pod[Running] --> Probe[readiness fail]\n  Probe --> EP[Endpoints empty]\n  EP --> S503[Ingress 503]",
     ["Running", "not Ready", "no Endpoints", "503"]),
    ("AEJE-D-047", "kubernetes", "network", 10, "INCIDENT-1006", 3, "Service routing failure",
     "flowchart LR\n  Svc[selector app=payment] -.-> X[no match]\n  Dep[labels app=payment-service] -.-> X\n  X --> Empty[Endpoints empty]",
     ["Service selector", "Pod labels", "no match", "empty Endpoints"]),
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
