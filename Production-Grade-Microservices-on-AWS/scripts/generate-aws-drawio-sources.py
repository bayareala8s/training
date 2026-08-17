#!/usr/bin/env python3
"""Generate editable draw.io sources using AWS Architecture Icons (mxgraph.aws4)."""

from __future__ import annotations

import html
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "docs" / "diagrams" / "aws-stencils" / "drawio"

AWS_ICON = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
    "strokeColor=#ffffff;strokeWidth=2;dashed=0;verticalLabelPosition=bottom;"
    "verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"
    "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};"
)

AWS_GROUP = (
    "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],"
    "[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;"
    "gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;"
    "pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;"
    "grIcon=mxgraph.aws4.{gr_icon};strokeColor=#248814;fillColor=none;verticalAlign=top;"
    "align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;"
)

EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#232F3E;fontSize=11;"


class DrawioBuilder:
    def __init__(self, page_w: int = 2200, page_h: int = 1400) -> None:
        self._next_id = 2
        self.cells: list[str] = []
        self.page_w = page_w
        self.page_h = page_h
        self.cell("0")
        self.cell("1", parent="0")

    def cell(self, cid: str, **attrs) -> str:
        parts = [f'<mxCell id="{cid}"']
        for key, val in attrs.items():
            if val is None:
                continue
            parts.append(f'{key}="{html.escape(str(val), quote=True)}"')
        if "style" not in attrs:
            parts.append('style=""')
        if "vertex" not in attrs and "edge" not in attrs:
            pass
        parts.append("/>")
        self.cells.append("".join(parts))
        return cid

    def nid(self) -> str:
        cid = str(self._next_id)
        self._next_id += 1
        return cid

    def icon(self, label: str, icon: str, x: int, y: int, parent: str = "1", w: int = 78, h: int = 78) -> str:
        cid = self.nid()
        geo = f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        self.cells.append(
            f'<mxCell id="{cid}" value="{html.escape(label)}" style="{AWS_ICON.format(icon=icon)}" '
            f'vertex="1" parent="{parent}">{geo}</mxCell>'
        )
        return cid

    def group(self, label: str, gr_icon: str, x: int, y: int, w: int, h: int, parent: str = "1") -> str:
        cid = self.nid()
        geo = f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        self.cells.append(
            f'<mxCell id="{cid}" value="{html.escape(label)}" style="{AWS_GROUP.format(gr_icon=gr_icon)}" '
            f'vertex="1" parent="{parent}">{geo}</mxCell>'
        )
        return cid

    def text(self, label: str, x: int, y: int, w: int, h: int, parent: str = "1", size: int = 11) -> str:
        cid = self.nid()
        style = f"text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;fontSize={size};"
        geo = f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        self.cells.append(
            f'<mxCell id="{cid}" value="{html.escape(label)}" style="{style}" '
            f'vertex="1" parent="{parent}">{geo}</mxCell>'
        )
        return cid

    def edge(self, src: str, dst: str, label: str = "", parent: str = "1", dashed: bool = False) -> None:
        cid = self.nid()
        style = EDGE + ("dashed=1;" if dashed else "")
        geo = '<mxGeometry relative="1" as="geometry"/>'
        val = html.escape(label) if label else ""
        self.cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{style}" edge="1" parent="{parent}" '
            f'source="{src}" target="{dst}">{geo}</mxCell>'
        )

    def build(self, diagram_name: str) -> str:
        diagram_id = str(uuid.uuid4())
        inner = "\n        ".join(self.cells)
        return f"""<mxfile host="app.diagrams.net" modified="2026-05-28T00:00:00.000Z" agent="course-generator" version="22.1.0" type="device">
  <diagram id="{diagram_id}" name="{html.escape(diagram_name)}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.page_w}" pageHeight="{self.page_h}" math="0" shadow="0">
      <root>
        {inner}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def vpc_ecs_deployment() -> str:
    b = DrawioBuilder(2400, 1600)
    region = b.group("AWS Region us-east-1", "group_region", 40, 40, 2320, 1520)
    vpc = b.group("VPC 10.0.0.0/16 (ms-course-dev-vpc)", "group_vpc", 40, 60, 2240, 1320, parent=region)
    pub = b.group("Public subnets · 2 AZs", "group_security_group", 60, 120, 1000, 420, parent=vpc)
    priv = b.group("Private subnets · 2 AZs", "group_security_group", 60, 580, 1400, 720, parent=vpc)

    users = b.icon("Users", "users", 80, 80, parent=region)
    igw = b.icon("Internet Gateway", "internet_gateway", 1180, 200, parent=vpc)
    alb = b.icon("Application Load Balancer\\nms-course-dev-alb", "application_load_balancer", 200, 220, parent=pub)
    nat = b.icon("NAT Gateway\\n(platform_active)", "nat_gateway", 700, 220, parent=pub)

    ecs_cluster = b.icon("Amazon ECS\\nms-course-dev-cluster", "elastic_container_service", 120, 120, parent=priv)
    usr = b.icon("user-service\\nFargate :8001", "fargate", 360, 100, parent=priv)
    prd = b.icon("product-service\\nFargate :8002", "fargate", 560, 100, parent=priv)
    ord_svc = b.icon("order-service\\nFargate :8003", "fargate", 360, 280, parent=priv)
    ntf = b.icon("notification-service\\nFargate :8004", "fargate", 560, 280, parent=priv)
    sd = b.icon("Cloud Map\\nms-course-dev.local", "cloud_map", 900, 180, parent=priv)

    ecr = b.icon("Amazon ECR\\n4 repositories", "elastic_container_registry", 1280, 140, parent=region)
    eb = b.icon("Amazon EventBridge\\nms-course-dev-bus", "eventbridge", 1280, 300, parent=region)
    ddb = b.icon("DynamoDB\\nms-course-dev-orders", "dynamodb", 1280, 460, parent=region)
    cw = b.icon("CloudWatch\\nLogs + metrics", "cloudwatch_2", 1500, 140, parent=region)
    sm = b.icon("Secrets Manager\\nJWT", "secrets_manager", 1500, 300, parent=region)
    exec_role = b.icon("IAM Execution Role\\nECR · logs", "identity_and_access_management_iam_role", 1500, 460, parent=region)
    task_role = b.icon("IAM Task Role\\nPutEvents · DynamoDB", "identity_and_access_management_iam_role", 1680, 460, parent=region)

    b.text(
        "Matches infrastructure/terraform/ · platform_active enables NAT + ALB + ECS tasks",
        60,
        1480,
        800,
        40,
        parent=region,
        size=12,
    )

    b.edge(users, igw, "HTTP :80", parent=region)
    b.edge(igw, alb, parent=vpc)
    b.edge(alb, usr, "/users · /auth", parent=vpc)
    b.edge(alb, prd, "/products", parent=vpc)
    b.edge(alb, ord_svc, "/orders", parent=vpc)
    b.edge(alb, ntf, "/events", parent=vpc)
    b.edge(ord_svc, prd, "GET /products", parent=vpc)
    b.edge(ord_svc, ntf, "POST /events", parent=vpc)
    b.edge(ord_svc, eb, "PutEvents", parent=region)
    b.edge(ord_svc, ddb, "orders table", parent=region, dashed=True)
    for task in (usr, prd, ord_svc, ntf):
        b.edge(task, nat, "egress via NAT", parent=vpc, dashed=True)
    b.edge(ecr, usr, "pull image", parent=region, dashed=True)
    b.edge(exec_role, ecs_cluster, parent=region, dashed=True)
    b.edge(task_role, ord_svc, parent=region, dashed=True)
    b.edge(sd, ord_svc, "DNS", parent=vpc, dashed=True)

    return b.build("10 VPC ECS Deployment (AWS Icons)")


def alb_routing() -> str:
    b = DrawioBuilder(1600, 900)
    client = b.icon("Client", "users", 80, 360)
    alb = b.icon("ALB Listener :80", "application_load_balancer", 320, 340)
    usr = b.icon("user-service TG\\n/users* /auth*", "elastic_container_service_container", 620, 120)
    prd = b.icon("product-service TG\\n/products*", "elastic_container_service_container", 620, 280)
    ord_svc = b.icon("order-service TG\\n/orders*", "elastic_container_service_container", 620, 440)
    ntf = b.icon("notification-service TG\\n/events*", "elastic_container_service_container", 620, 600)
    deflt = b.text("Default: Course welcome (200)", 620, 760, 280, 50)

    b.edge(client, alb)
    b.edge(alb, usr, "priority 10")
    b.edge(alb, prd, "priority 11")
    b.edge(alb, ord_svc, "priority 12")
    b.edge(alb, ntf, "priority 13")
    b.edge(alb, deflt, "default")
    return b.build("10 ALB Path Routing (AWS Icons)")


def eventbridge_flow() -> str:
    b = DrawioBuilder(1400, 700)
    order = b.icon("order-service\\nPutEvents", "elastic_container_service_container", 80, 280)
    bus = b.icon("EventBridge\\nCustom bus", "eventbridge", 420, 280)
    notify = b.icon("notification-service\\n/events consumer", "elastic_container_service_container", 760, 180)
    logs = b.icon("CloudWatch Logs\\naudit target", "cloudwatch_2", 760, 400)
    b.text("detail-type: OrderPlaced\\ncontracts/events/order-placed.json", 400, 80, 360, 60)
    b.edge(order, bus, "PutEvents")
    b.edge(bus, notify, "rule → HTTP")
    b.edge(bus, logs, "rule → logs")
    return b.build("09 EventBridge Flow (AWS Icons)")


SOURCES = [
    ("10-vpc-ecs-deployment-detail.drawio", vpc_ecs_deployment),
    ("10-alb-path-routing-detail.drawio", alb_routing),
    ("09-eventbridge-order-flow.drawio", eventbridge_flow),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in SOURCES:
        path = OUT / filename
        path.write_text(builder(), encoding="utf-8")
        print(f"  {path.relative_to(REPO_ROOT)}")
    print(f"\nWrote {len(SOURCES)} draw.io sources. Open in https://app.diagrams.net (AWS 2024 library).")
    print("Export: ./scripts/export-aws-drawio.sh (requires drawio CLI or Docker)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
