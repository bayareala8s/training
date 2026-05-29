#!/usr/bin/env python3
"""
Generate detailed architecture diagrams using official AWS Architecture Icons.

Outputs PNG + SVG under docs/diagrams/aws-stencils/{png,svg}/.
Requires: Graphviz (`dot`) and the `diagrams` package (see scripts/requirements-diagrams.txt).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PNG = REPO_ROOT / "docs" / "diagrams" / "aws-stencils" / "png"
OUT_SVG = REPO_ROOT / "docs" / "diagrams" / "aws-stencils" / "svg"

# diagrams imports after path check — needs graphviz on PATH
from diagrams import Cluster, Diagram, Edge  # noqa: E402
from diagrams.aws.compute import (  # noqa: E402
    EC2ContainerRegistry,
    ElasticContainerServiceContainer,
    ElasticContainerService,
    Fargate,
)
from diagrams.aws.database import Dynamodb  # noqa: E402
from diagrams.aws.devtools import Codedeploy  # noqa: E402
from diagrams.aws.general import General, InternetAlt1, Users  # noqa: E402
from diagrams.aws.integration import Eventbridge  # noqa: E402
from diagrams.aws.management import CloudwatchLogs, Cloudwatch  # noqa: E402
from diagrams.aws.network import (  # noqa: E402
    CloudMap,
    ElbApplicationLoadBalancer,
    InternetGateway,
    NATGateway,
    PrivateSubnet,
    PublicSubnet,
    VPC,
)
from diagrams.aws.security import (  # noqa: E402
    IdentityAndAccessManagementIamRole,
    SecretsManager,
)
from diagrams.onprem.ci import GithubActions  # noqa: E402
from diagrams.onprem.iac import Terraform  # noqa: E402

GRAPH_ATTR = {
    "fontsize": "13",
    "bgcolor": "white",
    "pad": "0.4",
    "splines": "ortho",
    "nodesep": "0.6",
    "ranksep": "0.8",
}


def _emit(name: str, builder) -> None:
    base = OUT_PNG.parent / name
    OUT_PNG.mkdir(parents=True, exist_ok=True)
    OUT_SVG.mkdir(parents=True, exist_ok=True)
    for fmt, folder in (("png", OUT_PNG), ("svg", OUT_SVG)):
        with Diagram(
            name.replace("-", " ").title(),
            filename=str(folder / name),
            show=False,
            outformat=fmt,
            direction="TB",
            graph_attr=GRAPH_ATTR,
        ):
            builder()
    print(f"  {name} (.png + .svg)")


def diagram_01_platform_overview() -> None:
    students = Users("Students / API clients")
    with Cluster("AWS Region (us-east-1)"):
        alb = ElbApplicationLoadBalancer("ALB\npath routing")
        with Cluster("ECS Fargate — ms-course-dev-cluster"):
            usr = ElasticContainerServiceContainer("user-service\n:8001")
            prd = ElasticContainerServiceContainer("product-service\n:8002")
            ord_svc = ElasticContainerServiceContainer("order-service\n:8003")
            ntf = ElasticContainerServiceContainer("notification-service\n:8004")
        ecr = EC2ContainerRegistry("Amazon ECR\n4 repos")
        eb = Eventbridge("EventBridge\nms-course-dev-bus")
        ddb = Dynamodb("DynamoDB\norders table")
        logs = CloudwatchLogs("CloudWatch Logs\n/ecs/ms-course-dev")
        sm = SecretsManager("Secrets Manager\nJWT")

    students >> Edge(label="HTTP :80") >> alb
    alb >> usr
    alb >> prd
    alb >> ord_svc
    alb >> ntf
    ord_svc >> Edge(label="GET /products") >> prd
    ord_svc >> Edge(label="POST /events") >> ntf
    ord_svc >> Edge(label="PutEvents") >> eb
    ord_svc >> Edge(style="dashed", label="optional") >> ddb
    ecr >> Edge(style="dashed", label="pull images") >> ord_svc
    [usr, prd, ord_svc, ntf] >> logs
    sm >> Edge(style="dashed") >> usr


def diagram_10_vpc_ecs_deployment() -> None:
    users = Users("Internet users")
    internet = InternetAlt1("Internet")
    with Cluster("AWS Region us-east-1"):
        with Cluster("VPC 10.0.0.0/16  (ms-course-dev-vpc)"):
            igw = InternetGateway("Internet Gateway")
            with Cluster("Public subnets (2 AZs)"):
                pub = PublicSubnet("10.0.0.0/24 · 10.0.1.0/24")
                alb = ElbApplicationLoadBalancer("ALB\nms-course-dev-alb")
                nat = NATGateway("NAT Gateway\n(platform_active)")
            with Cluster("Private subnets (2 AZs)"):
                priv = PrivateSubnet("10.0.10.0/24 · 10.0.11.0/24")
                with Cluster("ECS Fargate — ms-course-dev-cluster"):
                    ecs = ElasticContainerService("ECS Cluster")
                    usr = Fargate("user-service")
                    prd = Fargate("product-service")
                    ord_svc = Fargate("order-service")
                    ntf = Fargate("notification-service")
                sd = CloudMap("Cloud Map\nms-course-dev.local")
        ecr = EC2ContainerRegistry("ECR")
        eb = Eventbridge("EventBridge")
        ddb = Dynamodb("DynamoDB orders")
        cw = Cloudwatch("CloudWatch")
        sm = SecretsManager("Secrets Manager")

    users >> internet >> igw >> alb
    alb >> usr
    alb >> prd
    alb >> ord_svc
    alb >> ntf
    [usr, prd, ord_svc, ntf] >> nat >> internet
    ord_svc >> eb
    ord_svc >> ddb
    ecs >> cw
    ecr >> Edge(style="dashed") >> [usr, prd, ord_svc, ntf]
    [usr, prd, ord_svc, ntf] - Edge(style="dotted", label="DNS") - sd
    pub - Edge(style="invis") - priv


def diagram_10_alb_routing() -> None:
    users = Users("Client")
    alb = ElbApplicationLoadBalancer("ALB :80\nListener + rules")
    usr = ElasticContainerServiceContainer("user-service TG\n/users* /auth*")
    prd = ElasticContainerServiceContainer("product-service TG\n/products*")
    ord_svc = ElasticContainerServiceContainer("order-service TG\n/orders*")
    ntf = ElasticContainerServiceContainer("notification-service TG\n/events*")
    welcome = General("Default action\nCourse welcome 200")

    users >> alb
    alb >> Edge(label="priority 10") >> usr
    alb >> Edge(label="priority 11") >> prd
    alb >> Edge(label="priority 12") >> ord_svc
    alb >> Edge(label="priority 13") >> ntf
    alb >> Edge(label="default") >> welcome


def diagram_09_eventbridge_flow() -> None:
    with Cluster("Publishers"):
        order = ElasticContainerServiceContainer("order-service\nTask role: events:PutEvents")
    bus = Eventbridge("Custom Event Bus\nms-course-dev-bus")
    with Cluster("Targets (course)"):
        notify = ElasticContainerServiceContainer("notification-service\nvia ALB /events")
        logs = CloudwatchLogs("CloudWatch Logs\naudit rule")
    schema = Edge(label="detail-type: OrderPlaced\ncontracts/events/order-placed.json")

    order >> schema >> bus
    bus >> Edge(label="rule → HTTP") >> notify
    bus >> Edge(label="rule → logs") >> logs


def diagram_13_security_iam() -> None:
    user = Users("Student / client")
    with Cluster("Edge"):
        alb = ElbApplicationLoadBalancer("ALB SG\n:80 from 0.0.0.0/0")
    with Cluster("ECS tasks SG"):
        tasks = ElasticContainerServiceContainer("4 services\nself-ingress + from ALB")
    with Cluster("IAM per task"):
        exec_role = IdentityAndAccessManagementIamRole("Execution role\nECR pull · logs")
        task_role = IdentityAndAccessManagementIamRole("Task role\nPutEvents · DynamoDB")
    sm = SecretsManager("JWT_SECRET\nenv / Secrets Manager")
    user >> Edge(label="HTTPS/HTTP") >> alb >> tasks
    exec_role >> Edge(style="dashed") >> tasks
    task_role >> Edge(style="dashed") >> tasks
    sm >> Edge(style="dashed", label="bcrypt + JWT") >> tasks


def diagram_14_observability() -> None:
    with Cluster("ECS Fargate tasks"):
        s1 = ElasticContainerServiceContainer("user-service")
        s2 = ElasticContainerServiceContainer("product-service")
        s3 = ElasticContainerServiceContainer("order-service")
        s4 = ElasticContainerServiceContainer("notification-service")
    logs = CloudwatchLogs("/ecs/ms-course-dev\nper-container streams")
    metrics = Cloudwatch("Metrics\nCPU · memory · ALB 5xx")
    alarms = Cloudwatch("Alarms → SNS\n(extension)")

    [s1, s2, s3, s4] >> Edge(label="stdout") >> logs
    [s1, s2, s3, s4] >> Edge(label="Container Insights") >> metrics
    metrics >> alarms


def diagram_15_cicd_ecr_ecs() -> None:
    dev = Users("Developer")
    gh = GithubActions("GitHub Actions\nbuild · test · push")
    tf = Terraform("Terraform\ninfrastructure/terraform")
    ecr = EC2ContainerRegistry("Amazon ECR\nlinux/amd64 images")
    deploy = Codedeploy("ECS rolling deploy\naws-deploy.sh")
    ecs = ElasticContainerService("ECS Services\nforce new deployment")

    dev >> gh >> Edge(label="docker push") >> ecr
    dev >> tf >> Edge(label="apply") >> ecs
    gh >> ecr
    ecr >> deploy >> ecs


def diagram_17_cost_lifecycle() -> None:
    with Cluster("Running (platform_active=true)"):
        alb = ElbApplicationLoadBalancer("ALB")
        nat = NATGateway("NAT")
        tasks = Fargate("ECS tasks ×4")
    with Cluster("Stopped (aws-stop.sh)"):
        zero = ElasticContainerService("ECS desired = 0")
    with Cluster("Idle monthly cost"):
        cheap = Dynamodb("DynamoDB · ECR · VPC\n~$0–2/mo")

    stop = Edge(label="aws-stop.sh", color="darkorange")
    start = Edge(label="aws-start.sh", color="darkgreen")

    tasks >> stop >> zero
    zero >> start >> tasks
    alb >> Edge(style="dashed", label="destroyed when stopped") >> zero
    zero >> cheap


DIAGRAMS = [
    ("01-aws-platform-overview", diagram_01_platform_overview),
    ("09-eventbridge-order-flow", diagram_09_eventbridge_flow),
    ("10-vpc-ecs-deployment-detail", diagram_10_vpc_ecs_deployment),
    ("10-alb-path-routing-detail", diagram_10_alb_routing),
    ("13-security-iam-network-detail", diagram_13_security_iam),
    ("14-observability-cloudwatch-detail", diagram_14_observability),
    ("15-cicd-github-ecr-ecs-detail", diagram_15_cicd_ecr_ecs),
    ("17-aws-cost-lifecycle-detail", diagram_17_cost_lifecycle),
]


def main() -> int:
    import shutil

    if not shutil.which("dot"):
        print("Graphviz (dot) is required. Install: brew install graphviz", file=sys.stderr)
        return 1

    print("Generating AWS stencil diagrams (official AWS icons via diagrams package)...")
    for name, builder in DIAGRAMS:
        try:
            _emit(name, builder)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAILED {name}: {exc}", file=sys.stderr)
            return 1

    print(f"\nDone. {len(DIAGRAMS)} diagrams → {OUT_PNG.relative_to(REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
