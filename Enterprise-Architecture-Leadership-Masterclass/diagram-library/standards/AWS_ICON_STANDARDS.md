# AWS Icon Standards

## Rule

**Never substitute generic database, server, or cloud icons when an official AWS Architecture Icon exists.**

Use the latest [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/) package. Draw.io / diagrams.net embeds the `mxgraph.aws4` shape library — prefer that for `.drawio` files.

## Required service icons (Masterclass)

| Domain | Icons |
| ------ | ----- |
| Org / identity | Organizations, IAM, Cognito, SSO (IAM Identity Center) |
| Edge / network | Route 53, CloudFront, VPC, IGW, NAT Gateway*, Transit Gateway*, ELB, WAF, Shield |
| Compute | Lambda, ECS, EKS†, Step Functions |
| Integration | API Gateway, EventBridge, SQS, SNS, AWS Transfer Family |
| Data | DynamoDB, Aurora, RDS, S3, Redshift, Glue, Lake Formation, Athena |
| Security | KMS, Secrets Manager, Systems Manager, CloudTrail, Config |
| Ops | CloudWatch, Budgets |
| AI | Bedrock, (Guardrails as label/control) |

\* NAT Gateway — only when teaching why labs avoid it or when showing production patterns  
† EKS — architecture/concept only in this course (not a lab default)

## Mermaid limitation

Mermaid cannot embed official AWS SVG icons. For Mermaid sources:

1. Use **precise AWS service names** as node labels (e.g., `Amazon API Gateway`, `AWS Lambda`)  
2. Prefer `flowchart` / `C4Context`-style clarity  
3. Pair every Mermaid diagram with a **Draw.io** version that uses official AWS stencils  

SVG/PNG exports from Draw.io (or icon-composited pipelines) are the presentation masters for AWS reference architectures.

## Draw.io AWS stencil usage

```text
Shape library: AWS / AWS19 / AWS23 (latest available in diagrams.net)
Style: official product icon + service name below or beside
Group: AWS Cloud / Region / VPC / Availability Zone / Security Group as frames
```

## Icon sizing

| Context | Icon size |
| ------- | --------- |
| Slide reference architecture | 48–64px |
| Dense lab diagram | 40–48px |
| Executive (few icons) | 64–80px |

## Versioning

Record icon pack version in `diagram-manifest.json` → `awsIconPack` field when regenerating exports.
