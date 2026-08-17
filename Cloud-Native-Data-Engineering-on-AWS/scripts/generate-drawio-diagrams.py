#!/usr/bin/env python3
"""
Generate Draw.io (.drawio) architecture diagrams with AWS Architecture Icons (aws4 stencils).

Output: docs/diagrams/drawio/*.drawio
Run: python scripts/generate-drawio-diagrams.py
Then: ./scripts/export-drawio.sh
"""

from __future__ import annotations

import html
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "docs" / "diagrams" / "drawio"

# AWS4 resource icon styles (Draw.io built-in AWS 2021/2024 stencil set)
AWS4 = {
    "s3": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#7AA116;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;",
    "lambda": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#D86613;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;",
    "eventbridge": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#E7157B;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;",
    "glue": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#693CBF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue;",
    "athena": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#8C4FFF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.athena;",
    "step_functions": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#E7157B;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.step_functions;",
    "cloudwatch": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#E7157B;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;",
    "sns": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#E7157B;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;",
    "iam": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#DD344C;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management;",
    "kms": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#DD344C;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.key_management_service;",
    "catalog": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#693CBF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.glue_data_catalog;",
    "user": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.user;",
    "client": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.client;",
    "api": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#E7157B;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;",
    "sagemaker": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#01A88D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker;",
    "cost": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#01A88D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cost_explorer;",
    "terraform": "rounded=1;whiteSpace=wrap;html=1;fillColor=#5C4EE5;fontColor=#FFFFFF;strokeColor=#432DD7;fontSize=11;",
    "zone": "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_s3;strokeColor=#7AA116;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;",
    "account": "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;",
    "label": "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#666666;",
    "title": "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#232F3E;",
    "edge": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#232F3E;strokeWidth=1;fontSize=10;fontColor=#232F3E;",
}

ICON_SIZE = 60
GROUP_H = 200
GROUP_W = 280


@dataclass
class Node:
    id: str
    label: str
    icon: str
    x: int
    y: int
    w: int = ICON_SIZE
    h: int = ICON_SIZE
    parent: str | None = None


@dataclass
class Edge:
    src: str
    dst: str
    label: str = ""


@dataclass
class Diagram:
    filename: str
    title: str
    subtitle: str = ""
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    page_w: int = 1100
    page_h: int = 700


class DrawioBuilder:
    def __init__(self, diagram: Diagram):
        self.d = diagram
        self.cells: list[str] = []
        self._id = 2

    def _next_id(self) -> str:
        cid = str(self._id)
        self._id += 1
        return cid

    def _style(self, icon: str) -> str:
        return AWS4.get(icon, AWS4["label"])

    def build(self) -> str:
        d = self.d
        title_id = self._next_id()
        self.cells.append(
            f'<mxCell id="{title_id}" value="{html.escape(d.title)}" style="{AWS4["title"]}" '
            f'vertex="1" parent="1"><mxGeometry x="40" y="20" width="900" height="30" as="geometry"/></mxCell>'
        )
        if d.subtitle:
            sub_id = self._next_id()
            self.cells.append(
                f'<mxCell id="{sub_id}" value="{html.escape(d.subtitle)}" style="{AWS4["label"]}" '
                f'vertex="1" parent="1"><mxGeometry x="40" y="48" width="900" height="20" as="geometry"/></mxCell>'
            )

        id_map: dict[str, str] = {}
        for node in d.nodes:
            cid = self._next_id()
            id_map[node.id] = cid
            parent = "1" if node.parent is None else id_map[node.parent]
            style = self._style(node.icon)
            self.cells.append(
                f'<mxCell id="{cid}" value="{html.escape(node.label)}" style="{style}" '
                f'vertex="1" parent="{parent}">'
                f'<mxGeometry x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" as="geometry"/>'
                f"</mxCell>"
            )

        for edge in d.edges:
            eid = self._next_id()
            src = id_map[edge.src]
            dst = id_map[edge.dst]
            lbl = html.escape(edge.label)
            self.cells.append(
                f'<mxCell id="{eid}" value="{lbl}" style="{AWS4["edge"]}" edge="1" '
                f'parent="1" source="{src}" target="{dst}">'
                f'<mxGeometry relative="1" as="geometry"/></mxCell>'
            )

        body = "\n        ".join(self.cells)
        diagram_id = str(uuid.uuid4())
        return f"""<mxfile host="app.diagrams.net" agent="CNDE-Course-Generator" version="24.0.0">
  <diagram id="{diagram_id}" name="{html.escape(d.title)}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{d.page_w}" pageHeight="{d.page_h}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""


def _lab(name: str, title: str, subtitle: str, nodes: list, edges: list, **kw) -> Diagram:
    return Diagram(filename=name, title=title, subtitle=subtitle, nodes=nodes, edges=edges, **kw)


# ---------------------------------------------------------------------------
# Diagram definitions (26 labs + platform + capstone)
# ---------------------------------------------------------------------------
DIAGRAMS: list[Diagram] = [
    _lab(
        "lab-1.1-build-s3-data-lake",
        "Lab 1.1 — Build S3 Data Lake",
        "Terraform deploys encrypted S3 bucket with medallion zones",
        [
            Node("tf", "Terraform", "terraform", 80, 140, 120, 50),
            Node("acct", "AWS Account", "account", 280, 100, 520, 320),
            Node("s3", "Amazon S3\nData Lake", "s3", 40, 50, ICON_SIZE, ICON_SIZE, "acct"),
            Node("enc", "SSE + Versioning", "label", 140, 50, 100, 30, "acct"),
            Node("life", "Lifecycle Rules", "label", 140, 90, 100, 30, "acct"),
        ],
        [Edge("tf", "acct", "terraform apply"), Edge("tf", "s3", "creates")],
    ),
    _lab(
        "lab-1.2-data-lake-zones",
        "Lab 1.2 — Data Lake Zones",
        "Medallion architecture: raw → cleaned → curated",
        [
            Node("bucket", "S3 Data Lake", "zone", 60, 120, 680, 280),
            Node("raw", "raw/\nBronze", "s3", 30, 50, 90, 70, "bucket"),
            Node("clean", "cleaned/\nSilver", "s3", 150, 50, 90, 70, "bucket"),
            Node("cur", "curated/\nGold", "s3", 270, 50, 90, 70, "bucket"),
            Node("qua", "quarantine/", "s3", 390, 50, 90, 70, "bucket"),
            Node("meta", "metadata/", "s3", 510, 50, 90, 70, "bucket"),
            Node("orders", "raw/retail/orders\nyear=/month=/day=", "label", 30, 160, 200, 40),
        ],
        [
            Edge("raw", "clean", "Glue ETL"),
            Edge("clean", "cur", "Modeling"),
        ],
    ),
    _lab(
        "lab-2.1-lambda-ingestion",
        "Lab 2.1 — Lambda Ingestion",
        "JSON records → Lambda → S3 raw zone (idempotent keys)",
        [
            Node("cli", "AWS CLI / API", "client", 60, 180),
            Node("lam", "AWS Lambda\nfile-ingest", "lambda", 220, 170),
            Node("iam", "IAM Role", "iam", 220, 290),
            Node("s3", "Amazon S3\nraw/", "s3", 420, 170),
            Node("cw", "CloudWatch\nLogs", "cloudwatch", 420, 290),
        ],
        [
            Edge("cli", "lam", "Invoke"),
            Edge("lam", "iam", "assumes"),
            Edge("lam", "s3", "PutObject"),
            Edge("lam", "cw", "logs"),
        ],
    ),
    _lab(
        "lab-2.2-eventbridge-automation",
        "Lab 2.2 — EventBridge Automation",
        "Scheduled API ingestion with watermarks",
        [
            Node("eb", "EventBridge\nSchedule", "eventbridge", 80, 180),
            Node("lam", "Lambda\nscheduled-ingest", "lambda", 280, 180),
            Node("api", "External API", "api", 80, 320),
            Node("s3", "S3 raw/", "s3", 480, 180),
            Node("wm", "metadata/watermarks/", "s3", 480, 300),
        ],
        [
            Edge("eb", "lam", "trigger"),
            Edge("api", "lam", "HTTP GET"),
            Edge("lam", "s3", "PutObject"),
            Edge("lam", "wm", "update watermark"),
        ],
    ),
    _lab(
        "lab-2.3-s3-event-processing",
        "Lab 2.3 — S3 Event Processing",
        "incoming/ → promote to raw/ or quarantine/",
        [
            Node("upload", "File Upload", "user", 60, 200),
            Node("inc", "S3 incoming/", "s3", 220, 190),
            Node("ev", "S3 Event\nNotification", "eventbridge", 380, 190),
            Node("lam", "Lambda\ns3-event-ingest", "lambda", 540, 190),
            Node("raw", "raw/", "s3", 720, 140),
            Node("qua", "quarantine/", "s3", 720, 260),
        ],
        [
            Edge("upload", "inc", "upload"),
            Edge("inc", "ev", "ObjectCreated"),
            Edge("ev", "lam", "invoke"),
            Edge("lam", "raw", "promote"),
            Edge("lam", "qua", "on failure"),
        ],
    ),
    _lab(
        "lab-3.1-etl-raw-to-cleaned",
        "Lab 3.1 — Glue ETL Raw → Cleaned",
        "PySpark transforms CSV to Parquet",
        [
            Node("raw", "S3 raw/\nCSV orders", "s3", 80, 190),
            Node("glue", "AWS Glue\nETL Job", "glue", 300, 180),
            Node("script", "glue/scripts/\nglue_etl_job.py", "s3", 300, 300),
            Node("clean", "S3 cleaned/\nParquet", "s3", 520, 190),
            Node("logs", "CloudWatch\nLogs", "cloudwatch", 520, 300),
        ],
        [
            Edge("raw", "glue", "read CSV"),
            Edge("script", "glue", "script"),
            Edge("glue", "clean", "write Parquet"),
            Edge("glue", "logs", "metrics"),
        ],
    ),
    _lab(
        "lab-3.2-glue-crawlers",
        "Lab 3.2 — Glue Crawlers & Catalog",
        "Auto-discover schema → Athena queries",
        [
            Node("clean", "S3 cleaned/", "s3", 80, 200),
            Node("crawler", "Glue Crawler", "glue", 280, 190),
            Node("cat", "Glue Data\nCatalog", "catalog", 480, 190),
            Node("ath", "Amazon Athena", "athena", 680, 190),
            Node("analyst", "Analyst", "user", 680, 310),
        ],
        [
            Edge("clean", "crawler", "scan"),
            Edge("crawler", "cat", "register tables"),
            Edge("cat", "ath", "SQL"),
            Edge("ath", "analyst", "results"),
        ],
    ),
    _lab(
        "lab-3.3-etl-optimization",
        "Lab 3.3 — ETL Optimization",
        "Partitioning, Parquet, worker tuning",
        [
            Node("before", "Before\nCSV full scan", "label", 60, 180, 140, 50),
            Node("glue", "Optimized\nGlue Job", "glue", 280, 170),
            Node("after", "After\nPartitioned Parquet", "label", 500, 180, 140, 50),
            Node("tune", "coalesce + AQE\nSnappy compression", "label", 280, 300, 180, 50),
        ],
        [
            Edge("before", "glue", "transform"),
            Edge("glue", "after", "optimized write"),
            Edge("tune", "glue", "config"),
        ],
    ),
    _lab(
        "lab-4.1-quality-framework",
        "Lab 4.1 — Data Quality Framework",
        "Rule engine routes pass vs quarantine",
        [
            Node("in", "Input Records\nJSON/CSV", "client", 60, 190),
            Node("rules", "orders_rules.json", "label", 200, 100, 120, 40),
            Node("runner", "quality_runner.py\nRuleEngine", "lambda", 220, 180),
            Node("pass", "passed_records.json", "s3", 440, 140),
            Node("fail", "quarantined_records.json", "s3", 440, 260),
        ],
        [
            Edge("in", "runner", "validate"),
            Edge("rules", "runner", "rules"),
            Edge("runner", "pass", "pass"),
            Edge("runner", "fail", "quarantine"),
        ],
    ),
    _lab(
        "lab-4.2-validation-automation",
        "Lab 4.2 — Validation Automation",
        "Quality checks in ingestion/ETL pipeline",
        [
            Node("lam", "Lambda Ingestion", "lambda", 80, 190),
            Node("val", "Validation\nLambda", "lambda", 280, 190),
            Node("glue", "Glue ETL", "glue", 480, 190),
            Node("cw", "CloudWatch\nMetrics", "cloudwatch", 280, 310),
            Node("sns", "SNS Alert", "sns", 480, 310),
        ],
        [
            Edge("lam", "val", "pre-check"),
            Edge("val", "glue", "on pass"),
            Edge("val", "cw", "pass rate"),
            Edge("cw", "sns", "SLO breach"),
        ],
    ),
    _lab(
        "lab-4.3-quarantine-zone",
        "Lab 4.3 — Quarantine Zone",
        "Bad records isolated for steward review",
        [
            Node("etl", "ETL Pipeline", "glue", 80, 190),
            Node("qua", "S3 quarantine/\nretail/orders/", "s3", 300, 180),
            Node("manifest", "manifest.json\n+ error reason", "label", 300, 300, 140, 40),
            Node("steward", "Data Steward", "user", 520, 190),
            Node("replay", "Replay to\nraw/ after fix", "s3", 700, 190),
        ],
        [
            Edge("etl", "qua", "failed records"),
            Edge("qua", "manifest", "metadata"),
            Edge("steward", "qua", "review"),
            Edge("steward", "replay", "re-ingest"),
        ],
    ),
    _lab(
        "lab-5.1-star-schema",
        "Lab 5.1 — Star Schema",
        "dim_customer, dim_product, fact_orders",
        [
            Node("clean", "cleaned/\norders", "s3", 80, 200),
            Node("dc", "dim_customer", "athena", 300, 100),
            Node("dp", "dim_product", "athena", 300, 200),
            Node("fo", "fact_orders", "athena", 300, 300),
            Node("cur", "curated/\nretail/", "s3", 520, 200),
            Node("ath", "Amazon Athena", "athena", 720, 200),
        ],
        [
            Edge("clean", "dc", "load"),
            Edge("clean", "dp", "load"),
            Edge("clean", "fo", "load"),
            Edge("fo", "cur", "publish"),
            Edge("cur", "ath", "query"),
        ],
        page_w=900,
    ),
    _lab(
        "lab-5.2-athena-optimization",
        "Lab 5.2 — Athena Optimization",
        "Partition pruning & column projection",
        [
            Node("bad", "Full table scan\nSELECT *", "label", 60, 180, 150, 50),
            Node("good", "Optimized\npartition filter", "label", 60, 280, 150, 50),
            Node("ath", "Amazon Athena", "athena", 280, 220),
            Node("s3", "S3 Parquet\npartitioned", "s3", 480, 220),
            Node("save", "Lower cost\nfaster queries", "label", 680, 220, 120, 50),
        ],
        [
            Edge("bad", "ath", "avoid"),
            Edge("good", "ath", "prefer"),
            Edge("ath", "s3", "scan partitions"),
            Edge("ath", "save", "result"),
        ],
    ),
    _lab(
        "lab-5.3-cost-efficient-queries",
        "Lab 5.3 — Cost-Efficient Queries",
        "Summary tables, views, workgroup limits",
        [
            Node("fact", "fact_orders", "athena", 80, 190),
            Node("sum", "Summary Tables", "athena", 300, 140),
            Node("view", "Analyst Views", "athena", 300, 240),
            Node("wg", "Athena Workgroup\nscan limit", "athena", 520, 190),
            Node("dash", "Dashboards", "client", 720, 190),
        ],
        [
            Edge("fact", "sum", "pre-aggregate"),
            Edge("sum", "view", "expose"),
            Edge("view", "wg", "govern"),
            Edge("wg", "dash", "query"),
        ],
    ),
    _lab(
        "lab-6.1-step-functions-etl",
        "Lab 6.1 — Step Functions ETL",
        "Orchestrate Glue + quality validation",
        [
            Node("sfn", "Step Functions\ndaily-etl", "step_functions", 80, 190),
            Node("glue", "Glue ETL Job", "glue", 300, 140),
            Node("val", "Quality\nLambda", "lambda", 300, 260),
            Node("s3", "S3 Data Lake", "s3", 520, 190),
            Node("ok", "Success", "label", 720, 140, 80, 40),
        ],
        [
            Edge("sfn", "glue", "startJobRun.sync"),
            Edge("sfn", "val", "quality check"),
            Edge("glue", "s3", "write"),
            Edge("val", "ok", "pass_rate ≥ 99.9%"),
        ],
    ),
    _lab(
        "lab-6.2-retry-error-branching",
        "Lab 6.2 — Retry & Error Branching",
        "Retry policies and Catch states",
        [
            Node("sfn", "Step Functions", "step_functions", 80, 200),
            Node("task", "Glue Task", "glue", 280, 200),
            Node("retry", "Retry\n3x backoff", "label", 280, 320, 100, 40),
            Node("catch", "Catch\nStates.ALL", "label", 480, 200, 100, 40),
            Node("fail", "Fail State", "label", 660, 200, 80, 40),
        ],
        [
            Edge("sfn", "task", "invoke"),
            Edge("task", "retry", "on error"),
            Edge("task", "catch", "exhausted"),
            Edge("catch", "fail", "route"),
        ],
    ),
    _lab(
        "lab-6.3-sns-failure-handling",
        "Lab 6.3 — SNS Failure Handling",
        "Pipeline failures → SNS notifications",
        [
            Node("sfn", "Step Functions", "step_functions", 80, 200),
            Node("fail", "Pipeline\nFailed", "label", 280, 200, 100, 40),
            Node("sns", "Amazon SNS\ncritical topic", "sns", 480, 200),
            Node("email", "Email / Slack", "client", 680, 160),
            Node("ops", "On-Call Engineer", "user", 680, 260),
        ],
        [
            Edge("sfn", "fail", "Catch"),
            Edge("fail", "sns", "Publish"),
            Edge("sns", "email", "notify"),
            Edge("sns", "ops", "alert"),
        ],
    ),
    _lab(
        "lab-7.1-kms-bucket-policies",
        "Lab 7.1 — KMS & Bucket Policies",
        "Encryption at rest with SSE-KMS",
        [
            Node("kms", "AWS KMS\nCMK", "kms", 80, 190),
            Node("s3", "S3 Data Lake", "s3", 280, 190),
            Node("pol", "Bucket Policy\nDeny unencrypted", "iam", 480, 190),
            Node("user", "Authorized\nIAM User", "user", 680, 140),
            Node("deny", "Denied\nRequest", "label", 680, 260, 100, 40),
        ],
        [
            Edge("kms", "s3", "encrypt"),
            Edge("pol", "s3", "enforce"),
            Edge("user", "s3", "allowed"),
            Edge("deny", "pol", "blocked"),
        ],
    ),
    _lab(
        "lab-7.2-iam-rbac-data-zones",
        "Lab 7.2 — IAM RBAC Data Zones",
        "Role-based access per medallion zone",
        [
            Node("eng", "Data Engineer\nRole", "iam", 80, 120),
            Node("ana", "Analyst\nRole", "iam", 80, 220),
            Node("stw", "Steward\nRole", "iam", 80, 320),
            Node("raw", "raw/", "s3", 300, 120),
            Node("clean", "cleaned/", "s3", 480, 120),
            Node("cur", "curated/", "s3", 660, 120),
            Node("qua", "quarantine/", "s3", 480, 260),
        ],
        [
            Edge("eng", "raw", "read/write"),
            Edge("eng", "clean", "read/write"),
            Edge("ana", "cur", "read only"),
            Edge("stw", "qua", "read/replay"),
        ],
    ),
    _lab(
        "lab-7.3-governance-audit",
        "Lab 7.3 — Governance Audit",
        "Compliance validation and audit reports",
        [
            Node("s3", "S3 Data Lake", "s3", 80, 200),
            Node("iam", "IAM Policies", "iam", 280, 140),
            Node("kms", "KMS Keys", "kms", 280, 260),
            Node("trail", "CloudTrail\nAudit Logs", "cloudwatch", 480, 200),
            Node("report", "Audit Report", "client", 680, 200),
        ],
        [
            Edge("s3", "trail", "API calls"),
            Edge("iam", "trail", "access events"),
            Edge("kms", "trail", "key usage"),
            Edge("trail", "report", "evidence"),
        ],
    ),
    _lab(
        "lab-8.1-cloudwatch-dashboards",
        "Lab 8.1 — CloudWatch Dashboards",
        "ETL pipeline observability",
        [
            Node("glue", "Glue Jobs", "glue", 80, 190),
            Node("lam", "Lambda", "lambda", 80, 290),
            Node("cw", "CloudWatch\nDashboard", "cloudwatch", 300, 220),
            Node("met", "Custom Metrics\nCNDE/DataQuality", "cloudwatch", 300, 360),
            Node("ops", "Operations\nTeam", "user", 560, 220),
        ],
        [
            Edge("glue", "cw", "metrics"),
            Edge("lam", "cw", "errors"),
            Edge("met", "cw", "widgets"),
            Edge("cw", "ops", "monitor"),
        ],
    ),
    _lab(
        "lab-8.2-sns-alerts",
        "Lab 8.2 — SNS Alerts",
        "CloudWatch alarms → SNS → notifications",
        [
            Node("alarm", "CloudWatch\nAlarms", "cloudwatch", 80, 200),
            Node("crit", "SNS Critical", "sns", 300, 140),
            Node("warn", "SNS Warning", "sns", 300, 260),
            Node("email", "Email", "client", 520, 140),
            Node("slack", "Slack / PagerDuty", "client", 520, 260),
        ],
        [
            Edge("alarm", "crit", "threshold breach"),
            Edge("alarm", "warn", "degraded"),
            Edge("crit", "email", "page"),
            Edge("warn", "slack", "notify"),
        ],
    ),
    _lab(
        "lab-8.3-cost-reporting",
        "Lab 8.3 — Cost Reporting",
        "Tags, Cost Explorer, budgets",
        [
            Node("res", "AWS Resources\ncnde-dev-*", "account", 80, 180, 200, 120),
            Node("tags", "Cost Allocation\nTags", "label", 320, 160, 120, 40),
            Node("ce", "Cost Explorer", "cost", 320, 230),
            Node("budget", "AWS Budgets\n$20 alert", "cost", 520, 200),
            Node("fin", "Finance / Ops", "user", 720, 200),
        ],
        [
            Edge("res", "tags", "tagged"),
            Edge("tags", "ce", "report"),
            Edge("ce", "budget", "track"),
            Edge("budget", "fin", "review"),
        ],
    ),
    _lab(
        "lab-9.1-ml-dataset-prep",
        "Lab 9.1 — ML Dataset Preparation",
        "Point-in-time features from curated data",
        [
            Node("cur", "curated/\norders", "s3", 80, 200),
            Node("prep", "prepare_ml_dataset.py", "lambda", 280, 190),
            Node("train", "ml/training/\ntrain.parquet", "s3", 480, 140),
            Node("val", "ml/training/\nval.parquet", "s3", 480, 260),
            Node("sm", "SageMaker\n(optional)", "sagemaker", 680, 200),
        ],
        [
            Edge("cur", "prep", "features"),
            Edge("prep", "train", "split"),
            Edge("prep", "val", "split"),
            Edge("train", "sm", "train model"),
        ],
    ),
    _lab(
        "lab-9.2-feature-store-pipeline",
        "Lab 9.2 — Feature Store Pipeline",
        "Offline feature pipeline with registry",
        [
            Node("cur", "curated data", "s3", 80, 200),
            Node("pipe", "feature_pipeline.py", "glue", 280, 190),
            Node("reg", "feature_registry.json", "catalog", 280, 310),
            Node("feat", "ml/features/\noffline store", "s3", 480, 200),
            Node("ml", "ML Training", "sagemaker", 680, 200),
        ],
        [
            Edge("cur", "pipe", "transform"),
            Edge("reg", "pipe", "schema"),
            Edge("pipe", "feat", "write"),
            Edge("feat", "ml", "consume"),
        ],
    ),
    _lab(
        "lab-9.3-ai-data-quality",
        "Lab 9.3 — AI Data Quality",
        "PSI drift, leakage, label balance checks",
        [
            Node("ml", "ML Dataset", "s3", 80, 200),
            Node("val", "ai_quality_validator.py", "lambda", 280, 190),
            Node("rules", "ai_quality_rules.json", "label", 280, 310, 140, 40),
            Node("pass", "Training Ready", "label", 480, 140, 100, 40),
            Node("fail", "Block Training", "label", 480, 260, 100, 40),
        ],
        [
            Edge("ml", "val", "validate"),
            Edge("rules", "val", "rules"),
            Edge("val", "pass", "OK"),
            Edge("val", "fail", "drift/leakage"),
        ],
    ),
    _lab(
        "course-platform-overview",
        "CNDE Course — Platform Overview",
        "End-to-end cloud-native data platform (Modules 1–10)",
        [
            Node("acct", "AWS Cloud", "account", 40, 80, 900, 420),
            Node("src", "Data Sources", "client", 60, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("ing", "Lambda + EventBridge", "lambda", 180, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("s3", "S3 Data Lake", "zone", 300, 30, 200, 100, "acct"),
            Node("glue", "Glue ETL", "glue", 540, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("dq", "Data Quality", "lambda", 660, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("ath", "Athena", "athena", 540, 160, ICON_SIZE, ICON_SIZE, "acct"),
            Node("sfn", "Step Functions", "step_functions", 660, 160, ICON_SIZE, ICON_SIZE, "acct"),
            Node("sec", "IAM + KMS", "iam", 60, 180, ICON_SIZE, ICON_SIZE, "acct"),
            Node("mon", "CloudWatch + SNS", "cloudwatch", 180, 180, ICON_SIZE, ICON_SIZE, "acct"),
            Node("ml", "ML Features", "sagemaker", 300, 180, ICON_SIZE, ICON_SIZE, "acct"),
        ],
        [
            Edge("src", "ing", "ingest"),
            Edge("ing", "s3", "raw"),
            Edge("s3", "glue", "ETL"),
            Edge("glue", "dq", "validate"),
            Edge("glue", "ath", "query"),
            Edge("sfn", "glue", "orchestrate"),
        ],
        page_w=1000,
        page_h=550,
    ),
    _lab(
        "capstone-banking",
        "Capstone — Banking Regulatory Platform",
        "Financial reporting with audit trails",
        [
            Node("fin", "Core Banking\nFeeds", "client", 60, 200),
            Node("ing", "Lambda Ingestion", "lambda", 220, 190),
            Node("s3", "S3 Data Lake", "zone", 380, 120, 240, 160),
            Node("glue", "Glue ETL", "glue", 660, 190),
            Node("rep", "Regulatory\nReports", "athena", 820, 190),
        ],
        [
            Edge("fin", "ing", "settlements"),
            Edge("ing", "s3", "raw"),
            Edge("s3", "glue", "transform"),
            Edge("glue", "rep", "compliance"),
        ],
    ),
    _lab(
        "capstone-healthcare",
        "Capstone — Healthcare Analytics",
        "HIPAA-aware patient analytics",
        [
            Node("ehr", "EHR / HL7", "client", 60, 200),
            Node("ing", "Secure Ingestion", "lambda", 220, 190),
            Node("kms", "KMS Encryption", "kms", 380, 100),
            Node("s3", "S3 Lake\nPHI protected", "zone", 380, 180, 200, 140),
            Node("ath", "De-identified\nAnalytics", "athena", 640, 190),
        ],
        [
            Edge("ehr", "ing", "ingest"),
            Edge("kms", "s3", "encrypt"),
            Edge("ing", "s3", "raw"),
            Edge("s3", "ath", "masked query"),
        ],
    ),
    _lab(
        "capstone-ecommerce",
        "Capstone — E-Commerce Lakehouse",
        "Customer & sales analytics",
        [
            Node("web", "Web + Mobile\nEvents", "client", 60, 200),
            Node("eb", "EventBridge", "eventbridge", 220, 190),
            Node("s3", "S3 Lakehouse", "zone", 400, 130, 220, 150),
            Node("star", "Star Schema\ncurated/", "athena", 660, 140),
            Node("dash", "QuickSight\nDashboards", "client", 660, 260),
        ],
        [
            Edge("web", "eb", "events"),
            Edge("eb", "s3", "raw"),
            Edge("s3", "star", "model"),
            Edge("star", "dash", "BI"),
        ],
    ),
    _lab(
        "capstone-enterprise",
        "Capstone — Enterprise Data Platform",
        "Complete cloud-native data engineering platform",
        [
            Node("acct", "Enterprise AWS", "account", 40, 80, 820, 380),
            Node("ing", "Ingestion Layer", "lambda", 60, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("lake", "Medallion Lake", "zone", 180, 30, 180, 100, "acct"),
            Node("etl", "Glue ETL", "glue", 400, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("dq", "Quality + Quarantine", "lambda", 520, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("sfn", "Step Functions", "step_functions", 640, 40, ICON_SIZE, ICON_SIZE, "acct"),
            Node("sec", "Security + Governance", "iam", 60, 200, ICON_SIZE, ICON_SIZE, "acct"),
            Node("ops", "Monitoring + Cost", "cloudwatch", 200, 200, ICON_SIZE, ICON_SIZE, "acct"),
            Node("ai", "AI-Ready Data", "sagemaker", 400, 200, ICON_SIZE, ICON_SIZE, "acct"),
        ],
        [
            Edge("ing", "lake", "raw"),
            Edge("lake", "etl", "transform"),
            Edge("etl", "dq", "validate"),
            Edge("sfn", "etl", "orchestrate"),
        ],
        page_w=920,
        page_h=520,
    ),
]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for spec in DIAGRAMS:
        xml = DrawioBuilder(spec).build()
        path = OUT_DIR / f"{spec.filename}.drawio"
        path.write_text(xml, encoding="utf-8")
        manifest.append({"file": spec.filename, "title": spec.title, "path": str(path.relative_to(REPO))})
        print(f"Created {path.relative_to(REPO)}")

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n{len(DIAGRAMS)} Draw.io files → {OUT_DIR.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
