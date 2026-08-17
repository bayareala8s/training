# Lab 012: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Terraform modules for dual-region VPC | Must |
| FR-2 | ALB + health check `/health` | Must |
| FR-3 | RDS with cross-region replica stub | Must |
| FR-4 | Route 53 failover routing stub | Must |
| FR-5 | S3 CRR configuration stub | Should |
| FR-6 | Failover runbook document | Must |
| FR-7 | Config validator CLI | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | All resources tagged `lab=lab-012` | 100% |
| NFR-2 | Budget alarm defined | $25 threshold |
| NFR-3 | Default workflow plan-only | No accidental apply |

## Acceptance Criteria

### AC-1: Terraform validate

`terraform validate` succeeds on stubs.

### AC-2: Cost documentation

README cost warning and architecture cost table present.

### AC-3: Runbook

Failover steps with RTO/RPO and promote replica command template.

### AC-4: Cleanup

`terraform destroy` documented and tested dry-run.

## Out of Scope

- Full active-active global write path
- Kubernetes multi-cluster federation
- Production SOC2 controls

## Related Documentation

- [Disaster Recovery and Multi-Region](/docs/reliability-and-resilience/disaster-recovery-and-multi-region)
