# Lab 012: Architecture

## Overview

**Active-passive multi-region** reference — primary `us-east-1`, DR `us-west-2` — suitable for interview deep-dives and controlled AWS hands-on.

```mermaid
flowchart TB
    subgraph Global
        R53[Route 53 Failover Policy]
        CF[CloudFront optional]
    end
    subgraph Primary us-east-1
        VPC1[VPC]
        ALB1[ALB]
        ECS1[ECS Tasks]
        RDS1[RDS Multi-AZ]
        S3P[S3 Bucket]
    end
    subgraph DR us-west-2
        VPC2[VPC]
        ALB2[ALB]
        ECS2[ECS Tasks scaled down]
        RDS2[Cross-Region Replica]
        S3D[S3 Replica Bucket]
    end
    R53 --> ALB1
    R53 --> ALB2
    ALB1 --> ECS1 --> RDS1
    ALB2 --> ECS2 --> RDS2
    RDS1 -->|async replication| RDS2
    S3P -->|CRR| S3D
```

## Failover Sequence

```mermaid
sequenceDiagram
    participant Ops
    participant R53 as Route 53
    participant DR as DR Region
    participant RDS as RDS Replica

    Note over R53: Primary health check fails
    R53->>R53: Failover to secondary record
    Ops->>RDS: Promote replica (if manual DR)
    Ops->>DR: Scale ECS service
    Ops->>Ops: Validate RPO from lag metrics
```

## RTO / RPO Targets (Lab)

| Metric | Target | Mechanism |
|--------|--------|-----------|
| RPO | 5 min | RDS async CRR lag (typical lab) |
| RTO | 15 min | DNS TTL + ECS scale + promote |

Document that production targets require testing and may differ.

## Cost Hotspots

| Resource | Cost driver | Lab mitigation |
|----------|-------------|----------------|
| NAT Gateway | Hourly + GB | Single NAT; destroy promptly |
| RDS | Instance + storage | `db.t4g.micro`, skip Multi-AZ if plan-only |
| Cross-region transfer | Replication | Minimal test data |
| ALB | Hourly + LCU | One ALB per region only |

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `terraform/` | VPC, ALB, RDS, Route53 stubs |
| `src/main.py` | Config validation, dry-run failover |
| `runbooks/failover.md` | Operational steps (create in implementation) |
| `config/lab.tfvars.example` | Sized-down variables |

## Docker Topology (Local)

`localstack` partial AWS API simulation — **not** full multi-region fidelity.

## Related Documentation

- [AWS Fundamentals](/docs/cloud-architecture/aws-fundamentals)
- [Cloud Cost Optimization](/docs/cost-and-finops/cloud-cost-optimization)
