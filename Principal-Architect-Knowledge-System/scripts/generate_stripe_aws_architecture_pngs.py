#!/usr/bin/env python3
"""Generate AWS Architecture Icons-style PNG exports with numbered step flows."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Allow import when run as script from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import Aurora, Dynamodb
from diagrams.aws.integration import Eventbridge, SNS, SQS
from diagrams.aws.management import Cloudtrail, Cloudwatch, CloudwatchLogs, SystemsManagerParameterStore
from diagrams.aws.network import ALB, CloudFront, NATGateway, Route53
from diagrams.aws.security import IAM, KMS, SecretsManager, Shield, WAF
from diagrams.aws.storage import S3
from diagrams.generic.device import Mobile
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet

from stripe_diagram_steps_data import DIAGRAM_STEPS, edge_label

ROOT = Path(__file__).resolve().parent.parent
OUT_STATIC = ROOT / "static" / "img" / "aws-architecture" / "stripe-payment-idempotency"
OUT_GENERATED = ROOT / "diagrams" / "generated" / "stripe-payment-idempotency"

GRAPH_ATTR = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "spline",
    "nodesep": "0.9",
    "ranksep": "1.1",
}
NODE_ATTR = {"fontsize": "11"}
EDGE_ATTR = {"fontsize": "10", "fontcolor": "#232F3E"}


def L(diagram_id: str, step: str) -> str:
    for num, action, _ in DIAGRAM_STEPS[diagram_id]:
        if num == step:
            return edge_label(num, action)
    return step


def _stripe_node():
    return Internet("Stripe API\n+ Webhooks\n(Idempotency-Key)")


def diagram_01_end_to_end() -> None:
    did = "aws-deployment-context"
    with Diagram(
        "01 — End-to-End AWS Stack (numbered flow)",
        filename=str(OUT_GENERATED / "01-end-to-end-overview"),
        show=False,
        direction="TB",
        graph_attr=GRAPH_ATTR,
        node_attr=NODE_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        users = Users("Web + Mobile Clients")
        stripe = _stripe_node()
        with Cluster("AWS Edge"):
            cf, waf, r53 = CloudFront("CloudFront"), WAF("AWS WAF"), Route53("Route 53")
        with Cluster("VPC — Payment Tier"):
            alb = ALB("Application Load Balancer")
            api = ECS("ECS Fargate\ncheckout-api")
            wh = Lambda("Webhook worker")
            sweeper = Lambda("Idempotency sweeper")
            aurora = Aurora("Aurora PostgreSQL")
            sqs = SQS("SQS webhook queue")
            sm = SecretsManager("Secrets Manager")
            ssm = SystemsManagerParameterStore("SSM fail_closed")
            cw = Cloudwatch("CloudWatch")
            rec = Lambda("Reconciliation")

        users >> Edge(label=L(did, "1")) >> cf
        users >> Edge(label=L(did, "2")) >> r53
        cf >> Edge(label=L(did, "2")) >> waf >> alb
        r53 >> alb
        alb >> Edge(label=L(did, "3")) >> api
        api >> Edge(label=L(did, "4")) >> aurora
        api >> Edge(label=L(did, "5")) >> sm
        api >> Edge(label=L(did, "6")) >> stripe
        stripe >> Edge(label=L(did, "7")) >> wh >> Edge(label=L(did, "8")) >> sqs >> wh >> aurora
        sweeper >> Edge(label=L(did, "9")) >> aurora
        sweeper >> stripe
        rec >> Edge(label=L(did, "10")) >> aurora
        rec >> stripe
        api >> Edge(label=L(did, "11")) >> cw
        api >> ssm


def diagram_02_vpc_production() -> None:
    did = "vpc-production-full"
    with Diagram(
        "02 — VPC Production Stack (numbered flow)",
        filename=str(OUT_GENERATED / "02-vpc-production-full-stack"),
        show=False,
        direction="TB",
        graph_attr=GRAPH_ATTR,
        node_attr=NODE_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        users, stripe = Users("Clients"), _stripe_node()
        cf, waf, r53 = CloudFront("CloudFront"), WAF("WAF"), Route53("Route 53")
        alb = ALB("ALB")
        ecs = ECS("ECS checkout-api")
        aurora_w = Aurora("Aurora WRITER")
        aurora_r = Aurora("Aurora READER")
        nata, natb = NATGateway("NAT AZ-a"), NATGateway("NAT AZ-b")
        sqs = SQS("SQS")
        eb = Eventbridge("EventBridge")
        lrec = Lambda("Reconciliation")
        sweeper = Lambda("Sweeper")
        sm = SecretsManager("Secrets Manager")

        users >> Edge(label=L(did, "1")) >> cf >> waf >> alb
        users >> r53 >> alb
        alb >> Edge(label=L(did, "2")) >> ecs
        ecs >> Edge(label=L(did, "3")) >> aurora_w
        ecs >> Edge(label=L(did, "4")) >> sm
        ecs >> Edge(label=L(did, "5")) >> nata >> stripe
        ecs >> natb >> stripe
        stripe >> Edge(label=L(did, "6")) >> sqs >> ecs
        sweeper >> Edge(label=L(did, "7")) >> aurora_w
        eb >> Edge(label=L(did, "8")) >> lrec >> aurora_w
        aurora_w >> Edge(label=L(did, "9")) >> aurora_r


def diagram_03_pattern_a() -> None:
    did = "pattern-a"
    with Diagram(
        "03 — Pattern A (numbered flow)",
        filename=str(OUT_GENERATED / "03-pattern-a-merchant"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        fe, api, db = CloudFront("CloudFront+S3"), ECS("checkout-api"), Aurora("Aurora")
        stripe = _stripe_node()
        fe >> Edge(label=L(did, "1")) >> api >> Edge(label=L(did, "2")) >> db
        api >> Edge(label=L(did, "3")) >> db
        api >> Edge(label=L(did, "4")) >> stripe
        stripe >> Edge(label=L(did, "5")) >> api


def diagram_04_pattern_b() -> None:
    did = "pattern-b"
    with Diagram(
        "04 — Pattern B (numbered flow)",
        filename=str(OUT_GENERATED / "04-pattern-b-platform"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        svc = ECS("Internal services")
        alb, pay = ALB("ALB"), ECS("Payment API")
        idem, led = Dynamodb("Dedup store"), Aurora("Ledger")
        stripe = _stripe_node()
        svc >> Edge(label=L(did, "1")) >> alb >> Edge(label=L(did, "2")) >> pay
        pay >> Edge(label=L(did, "3")) >> idem >> Edge(label=L(did, "4")) >> led
        pay >> Edge(label=L(did, "5")) >> stripe


def diagram_05_data_aurora() -> None:
    did = "data-aurora"
    with Diagram(
        "05 — Aurora Data Layer (numbered flow)",
        filename=str(OUT_GENERATED / "05-data-aurora-multi-az"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        ecs = ECS("ECS Checkout Tasks")
        writer = Aurora("Aurora WRITER")
        reader = Aurora("Aurora READER")
        global_db = Aurora("Global DB DR")
        ecs >> Edge(label=L(did, "1")) >> writer
        writer >> Edge(label=L(did, "2")) >> reader
        writer >> Edge(label=L(did, "3")) >> global_db


def diagram_06_data_dynamodb() -> None:
    did = "data-dynamodb"
    with Diagram(
        "06 — DynamoDB Hybrid (numbered flow)",
        filename=str(OUT_GENERATED / "06-data-dynamodb-hybrid"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        ecs = ECS("ECS Checkout")
        ddb, aurora = Dynamodb("DynamoDB dedup"), Aurora("Aurora ledger")
        lam = Lambda("Streams audit")
        ecs >> Edge(label=L(did, "1")) >> ddb >> Edge(label=L(did, "3")) >> lam
        ecs >> Edge(label=L(did, "2")) >> aurora


def diagram_07_request_path() -> None:
    did = "request-path-sequence"
    with Diagram(
        "07 — Request Path (numbered flow)",
        filename=str(OUT_GENERATED / "07-request-path-alb-ecs"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        c, cf, waf = Users("Client"), CloudFront("CloudFront"), WAF("WAF")
        alb, ecs = ALB("ALB"), ECS("checkout-api")
        aurora, sm, stripe = Aurora("Aurora"), SecretsManager("Secrets"), _stripe_node()
        c >> Edge(label=L(did, "1")) >> cf >> Edge(label=L(did, "2")) >> waf
        waf >> Edge(label=L(did, "3")) >> alb >> Edge(label=L(did, "4")) >> ecs
        ecs >> Edge(label=L(did, "5")) >> sm
        ecs >> Edge(label=L(did, "6")) >> stripe
        ecs >> Edge(label=L(did, "7")) >> aurora


def diagram_08_webhooks() -> None:
    did = "webhook-sqs"
    with Diagram(
        "08 — Webhook Pipeline (numbered flow)",
        filename=str(OUT_GENERATED / "08-webhook-sqs-pipeline"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        stripe, alb = _stripe_node(), ALB("ALB")
        val, sqs = Lambda("Verify signature"), SQS("SQS")
        consumer, aurora = ECS("Consumer"), Aurora("Aurora dedup")
        dlq, alarm = SQS("DLQ"), Cloudwatch("Alarm")
        stripe >> Edge(label=L(did, "1")) >> alb >> Edge(label=L(did, "2")) >> val
        val >> Edge(label=L(did, "3")) >> sqs >> Edge(label=L(did, "4")) >> consumer
        consumer >> Edge(label=L(did, "5")) >> aurora
        sqs >> Edge(label=L(did, "6")) >> dlq >> alarm


def diagram_09_reconciliation() -> None:
    did = "reconciliation"
    with Diagram(
        "09 — Reconciliation (numbered flow)",
        filename=str(OUT_GENERATED / "09-reconciliation-eventbridge"),
        show=False,
        direction="TB",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        eb, lam = Eventbridge("EventBridge"), Lambda("reconciliation")
        aurora, stripe = Aurora("Aurora"), _stripe_node()
        s3, sns, cw = S3("S3 reports"), SNS("SNS"), Cloudwatch("gap metric")
        eb >> Edge(label=L(did, "1")) >> lam
        lam >> Edge(label=L(did, "2")) >> aurora
        lam >> Edge(label=L(did, "3")) >> stripe
        lam >> Edge(label=L(did, "4")) >> cw
        lam >> Edge(label=L(did, "5")) >> s3
        lam >> Edge(label=L(did, "6")) >> sns


def diagram_10_client() -> None:
    did = "client-spa"
    with Diagram(
        "10 — Client SPA (numbered flow)",
        filename=str(OUT_GENERATED / "10-client-cloudfront-spa"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        spa = Mobile("React SPA\nsessionStorage key")
        cf, alb, ecs, aurora = CloudFront("CloudFront"), ALB("ALB"), ECS("checkout-api"), Aurora("orders")
        cf >> Edge(label=L(did, "1")) >> spa
        spa >> Edge(label=L(did, "2")) >> alb >> Edge(label=L(did, "3")) >> ecs >> aurora
        ecs >> Edge(label=L(did, "4"), style="dashed") >> spa


def diagram_11_single_region() -> None:
    did = "single-region-multi-az"
    with Diagram(
        "11 — Single Region Multi-AZ (numbered flow)",
        filename=str(OUT_GENERATED / "11-single-region-multi-az"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        r53, alb = Route53("Route 53"), ALB("ALB")
        ecs, aurora_w, nat, stripe = ECS("ECS"), Aurora("WRITER"), NATGateway("NAT"), _stripe_node()
        r53 >> Edge(label=L(did, "1")) >> alb >> Edge(label=L(did, "2")) >> ecs
        ecs >> Edge(label=L(did, "3")) >> aurora_w
        ecs >> Edge(label=L(did, "4")) >> nat >> Edge(label=L(did, "5")) >> stripe


def diagram_12_multi_region_dr() -> None:
    did = "multi-region-dr"
    with Diagram(
        "12 — Multi-Region DR (numbered flow)",
        filename=str(OUT_GENERATED / "12-multi-region-dr"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        users, r53, stripe = Users("Clients"), Route53("Route 53"), _stripe_node()
        albe, ecse, aurorae = ALB("ALB east"), ECS("ECS east"), Aurora("Aurora PRIMARY")
        albw, ecsw, auroraw = ALB("ALB west"), ECS("ECS west"), Aurora("SECONDARY")
        users >> Edge(label=L(did, "1")) >> r53 >> albe >> ecse >> aurorae
        aurorae >> Edge(label=L(did, "2")) >> auroraw
        ecse >> stripe
        r53 >> Edge(label=L(did, "5"), style="dashed") >> albw >> Edge(label=L(did, "5")) >> ecsw
        ecsw >> Edge(label=L(did, "6")) >> stripe


def diagram_13_active_active() -> None:
    did = "active-passive-vs-aa"
    with Diagram(
        "13 — Active-Passive vs Active-Active (numbered flow)",
        filename=str(OUT_GENERATED / "13-active-passive-vs-active-active"),
        show=False,
        direction="TB",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        r53, alb, ecs, aurora = Route53("Route 53 writes"), ALB("ALB east"), ECS("ECS"), Aurora("PRIMARY")
        cf = CloudFront("CloudFront reads")
        r53 >> Edge(label=L(did, "1")) >> alb >> ecs >> aurora
        cf >> Edge(label=L(did, "2")) >> ecs
        e1, w1 = ECS("ECS east AA"), ECS("ECS west AA")
        dde, ddw = Dynamodb("DDB east"), Dynamodb("DDB west")
        stripe = _stripe_node()
        e1 >> Edge(label=L(did, "3")) >> dde >> Edge(label=L(did, "4")) >> ddw >> w1
        e1 >> stripe
        w1 >> Edge(label=L(did, "4")) >> stripe


def diagram_14_webhook_dr() -> None:
    did = "webhook-dr"
    with Diagram(
        "14 — Webhook DR (numbered flow)",
        filename=str(OUT_GENERATED / "14-webhook-dr-failover"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        stripe, r53 = _stripe_node(), Route53("Route 53")
        albe, sqse, lame = ALB("ALB east"), SQS("SQS east"), Lambda("consumer east")
        albw, sqsw, lamw = ALB("ALB west"), SQS("SQS west"), Lambda("consumer west")
        aurora, dlq = Aurora("event_id dedup"), SQS("DLQ")
        stripe >> Edge(label=L(did, "1")) >> r53 >> Edge(label=L(did, "2")) >> albe >> sqse >> lame >> aurora
        r53 >> Edge(label=L(did, "3"), style="dashed") >> albw >> sqsw >> lamw >> Edge(label=L(did, "4")) >> aurora
        sqse >> dlq


def diagram_15_security() -> None:
    did = "security-perimeter"
    with Diagram(
        "15 — Security (numbered flow)",
        filename=str(OUT_GENERATED / "15-security-perimeter"),
        show=False,
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        users = Users("Clients")
        shield, waf, cf = Shield("Shield"), WAF("WAF"), CloudFront("CloudFront")
        alb, ecs, aurora = ALB("ALB"), ECS("ECS private"), Aurora("Aurora KMS")
        iam, sm, kms = IAM("IAM roles"), SecretsManager("Secrets"), KMS("KMS")
        ct, logs, s3 = Cloudtrail("CloudTrail"), CloudwatchLogs("Logs"), S3("Audit S3")
        users >> Edge(label=L(did, "1")) >> shield >> Edge(label=L(did, "2")) >> waf
        waf >> Edge(label=L(did, "3")) >> cf >> alb >> Edge(label=L(did, "4")) >> ecs
        ecs >> Edge(label=L(did, "5")) >> iam >> sm
        aurora >> Edge(label=L(did, "6")) >> kms
        ecs >> aurora
        logs >> Edge(label=L(did, "7")) >> s3
        ct >> s3


def diagram_16_observability() -> None:
    did = "observability"
    with Diagram(
        "16 — Observability (numbered flow)",
        filename=str(OUT_GENERATED / "16-observability"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        ecs = ECS("checkout-api")
        logs, cw, s3, sns = CloudwatchLogs("Logs"), Cloudwatch("Metrics"), S3("Archive"), SNS("PagerDuty")
        ecs >> Edge(label=L(did, "1")) >> logs >> Edge(label=L(did, "3")) >> s3
        ecs >> Edge(label=L(did, "2")) >> cw >> Edge(label=L(did, "4")) >> sns


def diagram_17_sweeper() -> None:
    did = "sweeper"
    with Diagram(
        "17 — Sweeper (numbered flow)",
        filename=str(OUT_GENERATED / "17-sweeper-lambda"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        eb, lam = Eventbridge("EventBridge 30s"), Lambda("sweeper")
        lease, aurora, stripe, cw = Dynamodb("lease"), Aurora("processing rows"), _stripe_node(), Cloudwatch("metric")
        eb >> Edge(label=L(did, "1")) >> lam >> Edge(label=L(did, "2")) >> lease
        lam >> Edge(label=L(did, "3")) >> aurora >> Edge(label=L(did, "4")) >> stripe
        lam >> Edge(label=L(did, "5")) >> cw


def diagram_18_dr_game_day() -> None:
    did = "dr-game-day"
    with Diagram(
        "18 — DR Game Day (numbered flow)",
        filename=str(OUT_GENERATED / "18-dr-game-day"),
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
        edge_attr=EDGE_ATTR,
    ):
        fis, ssm = SystemsManagerParameterStore("AWS FIS"), SystemsManagerParameterStore("fail_closed")
        ops, aurora = Users("On-call"), Aurora("Promote west")
        r53, script, stripe, verify = Route53("DNS west"), ECS("100 checkouts"), _stripe_node(), Cloudwatch("Verify")
        fis >> Edge(label=L(did, "1")) >> ssm >> Edge(label=L(did, "2")) >> ops
        ops >> Edge(label=L(did, "3")) >> aurora >> Edge(label=L(did, "4")) >> r53
        r53 >> Edge(label=L(did, "5")) >> script >> Edge(label=L(did, "5")) >> stripe >> Edge(label=L(did, "6")) >> verify


GENERATORS = [
    diagram_01_end_to_end,
    diagram_02_vpc_production,
    diagram_03_pattern_a,
    diagram_04_pattern_b,
    diagram_05_data_aurora,
    diagram_06_data_dynamodb,
    diagram_07_request_path,
    diagram_08_webhooks,
    diagram_09_reconciliation,
    diagram_10_client,
    diagram_11_single_region,
    diagram_12_multi_region_dr,
    diagram_13_active_active,
    diagram_14_webhook_dr,
    diagram_15_security,
    diagram_16_observability,
    diagram_17_sweeper,
    diagram_18_dr_game_day,
]


def main() -> int:
    OUT_GENERATED.mkdir(parents=True, exist_ok=True)
    OUT_STATIC.mkdir(parents=True, exist_ok=True)
    print(f"Generating {len(GENERATORS)} numbered AWS architecture PNGs...")
    for gen in GENERATORS:
        print(f"  • {gen.__name__}")
        gen()
    pngs = sorted(OUT_GENERATED.glob("*.png"))
    for png in pngs:
        shutil.copy2(png, OUT_STATIC / png.name)
    print(f"Done: {len(pngs)} PNGs → {OUT_STATIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
