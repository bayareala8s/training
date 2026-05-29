# AWS Architecture Icon Diagrams (Stencils)

Detailed, production-style diagrams using **official AWS Architecture Icons** — for Module 4+ and instructor slides.

## Ready-to-use exports (PNG + SVG)

Generated with the [diagrams](https://diagrams.mingrammer.com/) Python package (same icon set as AWS stencils):

| Diagram | PNG | SVG | Matches |
|---------|-----|-----|---------|
| Platform overview (AWS) | [png](png/01-aws-platform-overview.png) | [svg](svg/01-aws-platform-overview.svg) | Diagram 01 |
| VPC + ECS deployment (detail) | [png](png/10-vpc-ecs-deployment-detail.png) | [svg](svg/10-vpc-ecs-deployment-detail.svg) | `infrastructure/terraform/`, Diagram 10 |
| ALB path routing (detail) | [png](png/10-alb-path-routing-detail.png) | [svg](svg/10-alb-path-routing-detail.svg) | `alb.tf` listener rules |
| EventBridge order flow | [png](png/09-eventbridge-order-flow.png) | [svg](svg/09-eventbridge-order-flow.svg) | Diagram 09 |
| Security IAM + network | [png](png/13-security-iam-network-detail.png) | [svg](svg/13-security-iam-network-detail.svg) | Diagram 13 |
| Observability CloudWatch | [png](png/14-observability-cloudwatch-detail.png) | [svg](svg/14-observability-cloudwatch-detail.svg) | Diagram 14 |
| CI/CD GitHub → ECR → ECS | [png](png/15-cicd-github-ecr-ecs-detail.png) | [svg](svg/15-cicd-github-ecr-ecs-detail.svg) | Diagram 15 |
| Cost lifecycle | [png](png/17-aws-cost-lifecycle-detail.png) | [svg](svg/17-aws-cost-lifecycle-detail.svg) | Diagram 17 |

## Editable draw.io sources (diagrams.net stencils)

For pixel-perfect edits in **diagrams.net** with the **AWS 2024** shape library:

| Source | Description |
|--------|-------------|
| [drawio/10-vpc-ecs-deployment-detail.drawio](drawio/10-vpc-ecs-deployment-detail.drawio) | VPC, public/private subnets, ALB, NAT, 4 Fargate services, ECR, EventBridge, DynamoDB, IAM |
| [drawio/10-alb-path-routing-detail.drawio](drawio/10-alb-path-routing-detail.drawio) | Listener rules → target groups |
| [drawio/09-eventbridge-order-flow.drawio](drawio/09-eventbridge-order-flow.drawio) | OrderPlaced event flow |

1. Open [diagrams.net](https://app.diagrams.net) → **Open Existing Diagram**
2. Choose a `.drawio` file above (icons use built-in `mxgraph.aws4` stencils)
3. Adjust layout, add AZ labels, or swap to newer AWS icon sets
4. **File → Export as** PNG/SVG for slides

Optional batch export (Draw.io Desktop CLI or Docker):

```bash
./scripts/export-aws-drawio.sh
# writes drawio-png/ and drawio-svg/ when drawio or jgraph/drawio image is available
```

## Regenerate everything

```bash
# Mermaid → png/svg (conceptual diagrams)
make diagrams

# Or step by step:
./scripts/export-diagrams.sh
python3 -m venv .venv-diagrams && .venv-diagrams/bin/pip install -r scripts/requirements-diagrams.txt
.venv-diagrams/bin/python scripts/generate-aws-stencil-diagrams.py
.venv-diagrams/bin/python scripts/generate-aws-drawio-sources.py
./scripts/export-aws-drawio.sh
```

**Requirements:** [Graphviz](https://graphviz.org/) (`brew install graphviz`) for AWS stencil PNG/SVG generation.

## Mermaid vs AWS stencils

| Use | Folder |
|-----|--------|
| Teaching concepts (DDD, sequences, sagas) | [../png/](../png/) from Mermaid |
| AWS console walkthroughs, labs 04–08, Well-Architected reviews | **this folder** (`aws-stencils/`) |

## Icon license

AWS Architecture Icons are provided by Amazon Web Services for use in architecture diagrams. See [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/).
