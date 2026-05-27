#!/usr/bin/env python3
"""Generate draw.io stencil files with AWS Architecture Icons for course modules."""

from __future__ import annotations

import html
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "diagrams"

# mxgraph.aws4 resourceIcon resIcon values
AWS = {
    "transfer": ("mxgraph.aws4.transfer", "AWS Transfer Family"),
    "s3": ("mxgraph.aws4.s3", "Amazon S3"),
    "lambda": ("mxgraph.aws4.lambda", "AWS Lambda"),
    "sfn": ("mxgraph.aws4.step_functions", "AWS Step Functions"),
    "cognito": ("mxgraph.aws4.cognito", "Amazon Cognito"),
    "apigw": ("mxgraph.aws4.api_gateway", "Amazon API Gateway"),
    "ddb": ("mxgraph.aws4.dynamodb", "Amazon DynamoDB"),
    "kms": ("mxgraph.aws4.key_management_service", "AWS KMS"),
    "cw": ("mxgraph.aws4.cloudwatch", "Amazon CloudWatch"),
    "sns": ("mxgraph.aws4.sns", "Amazon SNS"),
    "ecs": ("mxgraph.aws4.ecs", "Amazon ECS"),
    "ecr": ("mxgraph.aws4.ecr", "Amazon ECR"),
    "vpc": ("mxgraph.aws4.vpc", "Amazon VPC"),
    "secrets": ("mxgraph.aws4.secrets_manager", "AWS Secrets Manager"),
    "user": ("mxgraph.aws4.user", "Partner / User"),
}

STYLE_ICON = (
    "outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
    "strokeColor=#ffffff;fillColor=#232F3D;dashed=0;verticalLabelPosition=bottom;"
    "verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
    "pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon={res};"
)
STYLE_ARROW = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;strokeColor=#232F3E;strokeWidth=2;fontSize=10;"
)
STYLE_GROUP = (
    "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#232F3E;"
    "verticalAlign=top;fontStyle=1;fontSize=12;dashed=1;"
)


def icon_cell(cid: str, key: str, x: int, y: int, parent: str = "1", w: int = 78, h: int = 78) -> str:
    res, label = AWS[key]
    style = STYLE_ICON.format(res=res)
    val = html.escape(label)
    return f"""        <mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="{parent}">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>"""


def arrow(cid: str, src: str, tgt: str, label: str = "", parent: str = "1") -> str:
    lbl = html.escape(label) if label else ""
    return f"""        <mxCell id="{cid}" value="{lbl}" style="{STYLE_ARROW}" edge="1" parent="{parent}" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>"""


def group_cell(cid: str, label: str, x: int, y: int, w: int, h: int, parent: str = "1") -> str:
    return f"""        <mxCell id="{cid}" value="{html.escape(label)}" style="{STYLE_GROUP}" vertex="1" parent="{parent}">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>"""


def wrap_diagram(name: str, diagram_id: str, body: str) -> str:
    return f"""  <diagram id="{diagram_id}" name="{html.escape(name)}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>"""


def write_mxfile(path: Path, title: str, pages: list[tuple[str, str, str]]) -> None:
    diagrams = "\n".join(wrap_diagram(n, did, b) for n, did, b in pages)
    content = f"""<mxfile host="app.diagrams.net" modified="2026-05-27T00:00:00.000Z" agent="BayLearn-Course" version="22.1.0" type="device">
{diagrams}
</mxfile>
"""
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(REPO)}")


def page_week01() -> str:
    g = group_cell("g1", "Module 1 — Transfer edge + S3 landing", 40, 40, 720, 320)
    cells = [
        g,
        icon_cell("p1", "user", 80, 120, "g1"),
        icon_cell("tf1", "transfer", 240, 120, "g1"),
        icon_cell("s3_1", "s3", 440, 120, "g1"),
        icon_cell("l1", "lambda", 600, 120, "g1", 78, 78),
        arrow("e1", "p1", "tf1", "SFTP", "g1"),
        arrow("e2", "tf1", "s3_1", "PutObject", "g1"),
        arrow("e3", "s3_1", "l1", "Week 3+", "g1"),
    ]
    return "\n".join(cells)


def page_week02() -> str:
    g = group_cell("g2", "Module 2 — Security layers", 40, 40, 900, 340)
    cells = [
        g,
        icon_cell("kms", "kms", 80, 130, "g2"),
        icon_cell("iam", "lambda", 220, 130, "g2"),  # proxy for IAM role
        icon_cell("s3_2", "s3", 380, 130, "g2"),
        icon_cell("cw2", "cw", 540, 130, "g2"),
        icon_cell("tf2", "transfer", 700, 130, "g2"),
        arrow("e4", "kms", "s3_2", "SSE-KMS", "g2"),
        arrow("e5", "tf2", "s3_2", "scoped IAM", "g2"),
        arrow("e6", "s3_2", "cw2", "logs", "g2"),
    ]
    return "\n".join(cells)


def page_week03() -> str:
    g = group_cell("g3", "Module 3 — S3 event processor", 40, 40, 820, 300)
    cells = [
        g,
        icon_cell("s3_in", "s3", 80, 120, "g3"),
        icon_cell("lam3", "lambda", 300, 120, "g3"),
        icon_cell("s3_proc", "s3", 520, 120, "g3"),
        icon_cell("ddb3", "ddb", 300, 240, "g3"),
        arrow("e7", "s3_in", "lam3", "ObjectCreated", "g3"),
        arrow("e8", "lam3", "s3_proc", "valid → processing/", "g3"),
        arrow("e9", "lam3", "ddb3", "idempotency", "g3"),
    ]
    return "\n".join(cells)


def page_week04() -> str:
    g = group_cell("g4", "Module 4 — Step Functions workflow", 40, 40, 900, 320)
    cells = [
        g,
        icon_cell("sfn4", "sfn", 120, 120, "g4"),
        icon_cell("lv", "lambda", 300, 80, "g4"),
        icon_cell("lc", "lambda", 300, 180, "g4"),
        icon_cell("sns4", "sns", 520, 120, "g4"),
        icon_cell("s3_4", "s3", 680, 120, "g4"),
        arrow("e10", "sfn4", "lv", "Validate", "g4"),
        arrow("e11", "sfn4", "lc", "Copy", "g4"),
        arrow("e12", "sfn4", "sns4", "Notify", "g4"),
        arrow("e13", "lc", "s3_4", "", "g4"),
    ]
    return "\n".join(cells)


def page_week05() -> str:
    g = group_cell("g5", "Module 5 — Server vs connector", 40, 40, 900, 360)
    cells = [
        g,
        icon_cell("srv", "transfer", 100, 100, "g5"),
        icon_cell("con", "transfer", 100, 220, "g5"),
        icon_cell("s3a", "s3", 320, 100, "g5"),
        icon_cell("s3b", "s3", 320, 220, "g5"),
        icon_cell("sec", "secrets", 520, 220, "g5"),
        icon_cell("pt", "user", 700, 160, "g5"),
        arrow("e14", "pt", "srv", "inbound SFTP", "g5"),
        arrow("e15", "srv", "s3a", "", "g5"),
        arrow("e16", "s3b", "con", "StartFileTransfer", "g5"),
        arrow("e17", "con", "pt", "outbound SFTP", "g5"),
        arrow("e18", "con", "sec", "credentials", "g5"),
    ]
    return "\n".join(cells)


def page_week06() -> str:
    g = group_cell("g6", "Module 6 — Self-serve API", 40, 40, 1000, 360)
    cells = [
        g,
        icon_cell("u6", "user", 60, 140, "g6"),
        icon_cell("cog", "cognito", 180, 140, "g6"),
        icon_cell("api", "apigw", 320, 140, "g6"),
        icon_cell("lap", "lambda", 480, 140, "g6"),
        icon_cell("ddb6", "ddb", 640, 80, "g6"),
        icon_cell("sfn6", "sfn", 640, 200, "g6"),
        icon_cell("s3_6", "s3", 820, 140, "g6"),
        arrow("e19", "u6", "cog", "login", "g6"),
        arrow("e20", "cog", "api", "JWT", "g6"),
        arrow("e21", "api", "lap", "", "g6"),
        arrow("e22", "lap", "ddb6", "CRUD", "g6"),
        arrow("e23", "lap", "sfn6", "POST /jobs", "g6"),
        arrow("e24", "sfn6", "s3_6", "", "g6"),
    ]
    return "\n".join(cells)


def page_week07() -> str:
    g = group_cell("g7", "Module 7 — Observability", 40, 40, 900, 320)
    cells = [
        g,
        icon_cell("tf7", "transfer", 80, 120, "g7"),
        icon_cell("l7", "lambda", 220, 120, "g7"),
        icon_cell("sfn7", "sfn", 360, 120, "g7"),
        icon_cell("cw7", "cw", 520, 120, "g7"),
        icon_cell("sns7", "sns", 680, 120, "g7"),
        arrow("e25", "tf7", "cw7", "metrics", "g7"),
        arrow("e26", "l7", "cw7", "logs", "g7"),
        arrow("e27", "sfn7", "cw7", "", "g7"),
        arrow("e28", "cw7", "sns7", "alarms", "g7"),
    ]
    return "\n".join(cells)


def page_week08() -> str:
    return page_lab_stack()


def page_week09() -> str:
    g = group_cell("g9", "Module 9 — ECS Fargate large files", 40, 40, 950, 380)
    cells = [
        g,
        icon_cell("s3in9", "s3", 80, 140, "g9"),
        icon_cell("disp9", "lambda", 260, 140, "g9"),
        icon_cell("ecs9", "ecs", 440, 140, "g9"),
        icon_cell("ecr9", "ecr", 440, 260, "g9"),
        icon_cell("vpc9", "vpc", 620, 140, "g9"),
        icon_cell("s3out9", "s3", 800, 140, "g9"),
        icon_cell("cw9", "cw", 620, 260, "g9"),
        arrow("e29", "s3in9", "disp9", "ObjectCreated", "g9"),
        arrow("e30", "disp9", "ecs9", "RunTask", "g9"),
        arrow("e31", "ecr9", "ecs9", "image", "g9"),
        arrow("e32", "ecs9", "s3out9", "manifest", "g9"),
        arrow("e33", "ecs9", "cw9", "logs", "g9"),
    ]
    return "\n".join(cells)


def page_lab_stack() -> str:
    g = group_cell("g0", "BayLearn MFT Lab Stack (Terraform)", 20, 20, 1100, 520)
    cells = [
        g,
        icon_cell("t0", "transfer", 40, 80, "g0"),
        icon_cell("c0", "transfer", 40, 200, "g0"),
        icon_cell("s0", "s3", 240, 140, "g0"),
        icon_cell("k0", "kms", 240, 280, "g0"),
        icon_cell("p0", "lambda", 440, 80, "g0"),
        icon_cell("w0", "sfn", 440, 200, "g0"),
        icon_cell("a0", "apigw", 640, 80, "g0"),
        icon_cell("g0c", "cognito", 640, 200, "g0"),
        icon_cell("d0", "ddb", 800, 80, "g0"),
        icon_cell("e0", "ecs", 800, 200, "g0"),
        icon_cell("v0", "vpc", 960, 200, "g0"),
        arrow("a0a", "t0", "s0", "", "g0"),
        arrow("a0b", "s0", "p0", "inbound/", "g0"),
        arrow("a0c", "p0", "w0", "", "g0"),
        arrow("a0d", "a0", "g0c", "", "g0"),
        arrow("a0e", "s0", "e0", "large/inbound/", "g0"),
        arrow("a0f", "e0", "v0", "", "g0"),
    ]
    return "\n".join(cells)


FILES = [
    ("week-01-transfer-edge.drawio", [("1. Transfer + S3", "w01", page_week01())]),
    ("week-02-security-governance.drawio", [("2. Security layers", "w02", page_week02())]),
    ("week-03-event-driven.drawio", [("3. Event processor", "w03", page_week03())]),
    ("week-04-step-functions.drawio", [("4. Step Functions", "w04", page_week04())]),
    ("week-05-connectors.drawio", [("5. Connectors", "w05", page_week05())]),
    ("week-06-self-serve-api.drawio", [("6. Self-serve API", "w06", page_week06())]),
    ("week-07-observability.drawio", [("7. Observability", "w07", page_week07())]),
    ("week-08-capstone-platform.drawio", [("8. Full platform", "w08", page_lab_stack())]),
    ("week-09-ecs-fargate.drawio", [("9. ECS Fargate", "w09", page_week09())]),
    ("lab-stack-reference.drawio", [("Lab stack", "lab", page_lab_stack())]),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, pages in FILES:
        write_mxfile(OUT / filename, filename, pages)


if __name__ == "__main__":
    main()
