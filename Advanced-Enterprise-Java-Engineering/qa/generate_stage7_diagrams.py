#!/usr/bin/env python3
"""Generate Stage 7 diagram sources, SVG, alt text, and PNG."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIAGRAMS = [
    ("AEJE-D-048", "aws", "deployment", 11, "BUILD-1101", 3, "ECR and ECS/Fargate BayPay",
     "flowchart LR\n  ECR[ECR image] --> Task[Fargate task 8080]\n  Task --> ALB[ALB]\n  Client --> ALB",
     ["ECR", "Fargate 8080", "ALB", "client"]),
    ("AEJE-D-049", "aws", "executive", 11, "ARCHITECT-1102", 4, "ECS vs EKS vs OpenShift",
     "flowchart LR\n  ECS[ECS Fargate] --- EKS[EKS]\n  EKS --- OCP[OpenShift]\n  Pay[payment-service] --> ECS",
     ["ECS Fargate", "EKS", "OpenShift", "payment-service"]),
    ("AEJE-D-050", "aws", "security-trust-boundary", 11, "SECURITY-1103", 3, "IAM, Secrets Manager and KMS",
     "flowchart TB\n  Exec[execution role] --> SM[Secrets Manager]\n  SM --> KMS[KMS]\n  Task[task role] --> App[app AWS APIs]",
     ["execution role", "Secrets Manager", "KMS", "task role"]),
    ("AEJE-D-051", "aws", "incident", 11, "INCIDENT-1104", 3, "Unhealthy ALB target",
     "flowchart LR\n  Task[ECS RUNNING] --> HC[ALB health / 404]\n  HC --> Un[unhealthy]\n  Un --> S503[502/503]",
     ["task RUNNING", "health 404", "unhealthy", "503"]),
    ("AEJE-D-052", "aws", "concept", 11, "COST-1105", 2, "Cost optimization levers",
     "flowchart LR\n  Idle[idle ALB] --> Stop[destroy after lab]\n  Size[Fargate size] --> Right[right-size]\n  Nat[NAT / EKS] --> Avoid[avoid in 90 min]",
     ["idle ALB", "Fargate size", "no NAT/EKS"]),
    ("AEJE-D-053", "aws", "network", 11, "L-11.4", 2, "ALB, NLB and Route 53",
     "flowchart LR\n  R53[Route 53] --> ALB[ALB HTTP]\n  ALB --> TG[target 8080]\n  NLB[NLB] -.-> TG",
     ["Route 53", "ALB", "target 8080", "NLB optional"]),
    ("AEJE-D-054", "devops", "concept", 12, "L-12.1", 1, "Git and CI flow",
     "flowchart LR\n  PR[pull request] --> CI[mvn test]\n  CI --> Img[image tag SHA]\n  Img --> Deploy[deploy]",
     ["PR", "CI test", "image SHA", "deploy"]),
    ("AEJE-D-055", "devops", "component", 12, "BUILD-1202", 2, "Reusable Terraform modules",
     "flowchart TB\n  Root[root module] --> ECR[module ecr]\n  Root --> ECS[module ecs_service]",
     ["root", "module ecr", "module ecs_service"]),
    ("AEJE-D-056", "devops", "component", 12, "BUILD-1204", 3, "CI/CD pipeline",
     "flowchart LR\n  Push[git push] --> Test[Java 21 tests]\n  Test --> Build[image]\n  Build --> ECR[ECR SHA]",
     ["push", "tests", "image", "ECR"]),
    ("AEJE-D-057", "devops", "incident", 12, "INCIDENT-1205", 3, "Failed deployment and rollback",
     "flowchart LR\n  Bad[new tag unhealthy] --> CB[circuit breaker]\n  CB --> Old[last healthy 3.8.0]",
     ["bad tag", "circuit breaker", "rollback"]),
    ("AEJE-D-058", "devops", "deployment", 12, "BUILD-1203", 2, "Ansible configuration automation",
     "flowchart LR\n  Vars[group_vars] --> Play[playbook]\n  Play --> Env[server.env template]",
     ["vars", "playbook", "env template"]),
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
