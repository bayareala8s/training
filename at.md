

# 12. Resiliency and Reliability Pillar

This section documents how the Self-Serve File Transfer Backend Engine achieves **high availability, fault tolerance, and disaster recovery**, including quantified **RTO/RPO metrics**, **Maximum Tolerable Downtime (MTD)**, **resiliency patterns**, and **failure impact analysis**.

---

## 12.1 Resiliency Objectives

The platform is designed to:

* Remain available during component, AZ, or regional failures
* Recover automatically without manual intervention
* Prevent duplicate file delivery during failover
* Preserve data integrity and auditability
* Provide predictable and measurable recovery behavior

---

## 12.2 Recovery Time Objective (RTO) and Recovery Point Objective (RPO)

### 12.2.1 Definitions

* **RTO**: Maximum acceptable time to restore service after a failure
* **RPO**: Maximum acceptable amount of data loss measured in time

---

### 12.2.2 RTO / RPO Targets

| Component / Functionality | RTO          | RPO       |
| ------------------------- | ------------ | --------- |
| Control Plane APIs        | < 5 minutes  | 0         |
| Job orchestration         | < 10 minutes | 0         |
| Data Plane execution      | < 15 minutes | Near-zero |
| S3-staged files           | N/A          | 0         |
| Endpoint metadata         | < 5 minutes  | 0         |

---

### 12.2.3 Rationale for RTO/RPO Values

* **RTO is primarily driven by lease expiration**, not infrastructure recovery
* **RPO is near-zero** due to:

  * DynamoDB Global Tables
  * S3 Cross-Region Replication
* No in-memory state is required for recovery

---

## 12.3 Maximum Tolerable Downtime (MTD)

### 12.3.1 Business Line MTD

| Business Function      | MTD        |
| ---------------------- | ---------- |
| Inbound file ingestion | 30 minutes |
| Outbound file delivery | 30 minutes |
| Status visibility      | 15 minutes |
| Customer onboarding    | 4 hours    |

---

### 12.3.2 Alignment to Architecture

* Architecture recovers well within MTD for all critical functions
* Onboarding delays during DR events are acceptable and documented

---

## 12.4 Same-Site Fault Tolerance

### 12.4.1 Availability Zone Resilience

* All AWS services used are **multi-AZ by default**
* No single-AZ dependency exists
* ECS tasks can be restarted in alternate AZs automatically

---

### 12.4.2 Component-Level Fault Tolerance

| Component      | Fault Tolerance |
| -------------- | --------------- |
| API Gateway    | Multi-AZ        |
| Lambda         | Multi-AZ        |
| Step Functions | Multi-AZ        |
| DynamoDB       | Multi-AZ        |
| ECS Fargate    | Multi-AZ        |
| S3             | Regional        |

---

## 12.5 Disaster Recovery Strategy

### 12.5.1 DR Model Summary

The system uses a **Partitioned Active-Active Multi-Region** DR strategy.

| Attribute           | Behavior     |
| ------------------- | ------------ |
| Standby region      | None         |
| Failover            | Automatic    |
| Data replication    | Continuous   |
| Manual intervention | Not required |

---

### 12.5.2 DR Workflow

1. Primary region failure detected
2. Lease expiration occurs
3. Secondary region acquires leases
4. Execution resumes automatically
5. Observability and alerts notify operators

---

## 12.6 Resiliency Patterns (Industry Standard Definitions)

### 12.6.1 Backup and Restore

* Used for:

  * Configuration recovery
  * Audit retention
* DynamoDB PITR enabled
* S3 versioning enabled

---

### 12.6.2 Pilot Light

* Not used
* Rejected due to manual promotion requirements

---

### 12.6.3 Warm Standby

* Not used
* Rejected due to idle cost and complexity

---

### 12.6.4 Multi-Region Active/Active (Selected)

| Characteristic    | Implementation |
| ----------------- | -------------- |
| Active regions    | 2              |
| Execution control | Lease-based    |
| Data consistency  | Strong         |
| Duplication risk  | Eliminated     |

---

## 12.7 Resiliency Diagram (Textual)

```
          Region A (us-gov-west-1)
          -----------------------
          Control Plane
          Data Plane
          DynamoDB Global Tables
          S3 (CRR Enabled)
                 |
                 | Replication
                 v
          -----------------------
          Region B (us-gov-east-1)
          Control Plane
          Data Plane
          DynamoDB Global Tables
          S3 (CRR Enabled)
```

---

## 12.8 Failure Scenarios and Impact Analysis

### 12.8.1 Failure Matrix

| Failure Scenario      | Impact      | Mitigation     | Residual Risk |
| --------------------- | ----------- | -------------- | ------------- |
| Single Lambda failure | None        | Retry          | Low           |
| ECS task crash        | Delayed job | Retry          | Low           |
| AZ outage             | Minimal     | Multi-AZ       | Low           |
| Regional outage       | Short delay | Lease takeover | Medium        |
| External SFTP outage  | Job delay   | Retry/backoff  | Medium        |
| S3 replication lag    | DR delay    | Monitoring     | Low           |

---

## 12.9 Where Architecture Cannot Meet Resiliency Strategy

| Area                 | Limitation      | Mitigation          |
| -------------------- | --------------- | ------------------- |
| External partners    | Outside control | Retry & alert       |
| Partner SLAs         | Not enforceable | Business acceptance |
| Real-time guarantees | Not provided    | Eventual delivery   |

These limitations are **explicitly documented and accepted**.

---

## 12.10 Maintenance Windows

* No mandatory downtime for maintenance
* Maintenance performed via rolling deployments
* Non-critical operations paused during FOMC freeze

---

## 12.11 SLA Summary

| Metric                            | SLA   |
| --------------------------------- | ----- |
| Platform availability             | 99.9% |
| Transfer completion (non-partner) | 99.9% |
| Status API availability           | 99.9% |

SLA excludes:

* External partner availability
* Network failures outside AWS

---

## 12.12 Section Summary

This section demonstrates that the architecture meets enterprise resiliency expectations through quantified RTO/RPO targets, automated failover, and a partitioned Active-Active design. Known limitations are explicitly documented, mitigated where possible, and surfaced for ARC visibility and approval.

---


# 13. Security and Compliance Pillar

This section describes the **security architecture**, **defense-in-depth controls**, and **compliance posture** of the Self-Serve File Transfer Backend Engine deployed in **AWS GovCloud**. The design aligns with **Zero Trust Security Architecture**, System IT standards, and applicable FRISS policies, while transparently documenting known limitations and approved exceptions.

---

## 13.1 Security Architecture Overview

The platform is designed to protect **data confidentiality, integrity, and availability** across all file transfer flows involving internal systems and external partners.

Security is enforced through:

* Identity-centric access controls
* Network isolation and controlled egress
* Application-level authorization and validation
* Encryption in transit and at rest
* Comprehensive logging and auditability

The system follows a **defense-in-depth** strategy, ensuring that no single control failure results in a security breach.

---

## 13.2 Defense-in-Depth Strategy

Security controls are applied across multiple independent layers:

### 13.2.1 Identity Layer

* IAM-based authentication and authorization
* No shared or long-lived credentials
* Service-to-service access via IAM roles only

---

### 13.2.2 Network Layer

* Private VPC subnets for all compute
* No inbound access to data plane resources
* Controlled outbound access via NAT gateways
* Security groups deny all traffic by default

---

### 13.2.3 Application Layer

* API-level authorization
* Schema and payload validation
* Idempotency enforcement
* Explicit error handling without data leakage

---

### 13.2.4 Data Layer

* Encryption at rest for all data stores
* Tenant isolation via logical partitioning
* No plaintext storage of secrets or credentials

---

### 13.2.5 Monitoring and Audit Layer

* Centralized, immutable logs
* End-to-end correlation using job IDs
* Alerts for anomalous or suspicious activity

---

## 13.3 Access Control, Authentication, and Authorization

### 13.3.1 Authentication

| Actor                | Authentication Mechanism     |
| -------------------- | ---------------------------- |
| Customer API clients | IAM / federated identity     |
| Internal services    | IAM roles                    |
| AWS services         | Service-linked IAM roles     |
| External SFTP users  | SSH key-based authentication |

**Key Decisions**

* Password-based authentication is not supported for SFTP
* No credentials are embedded in code or configuration
* Authentication context is validated on every request

---

### 13.3.2 Authorization

Authorization is enforced at **multiple levels**:

#### API Layer

* Per-customer authorization
* Endpoint and job ownership validation

#### Application Layer

* Flow-specific policy enforcement
* Prevention of cross-tenant access

#### IAM Layer

* Least-privilege IAM roles
* Fine-grained permissions for:

  * DynamoDB access
  * Secrets retrieval
  * ECS task execution

---

## 13.4 Encryption and Data Protection

### 13.4.1 Encryption in Transit

All data paths are encrypted:

| Path                   | Encryption |
| ---------------------- | ---------- |
| Client → API Gateway   | TLS 1.2+   |
| Control Plane services | TLS        |
| ECS → S3               | TLS        |
| ECS → External SFTP    | SSH        |
| Transfer Family → S3   | TLS        |

There are **no plaintext data paths** in the system.

---

### 13.4.2 Encryption at Rest

| Data Store      | Encryption |
| --------------- | ---------- |
| Amazon S3       | SSE-KMS    |
| DynamoDB        | KMS-backed |
| Secrets Manager | KMS-backed |
| CloudWatch Logs | KMS-backed |

Key management:

* Customer- or system-managed KMS keys
* IAM-scoped key usage
* Key rotation enabled where supported

---

### 13.4.3 Sensitive Data Handling

* Secrets stored only in AWS Secrets Manager
* Endpoint metadata stores references, not secrets
* Logs are scrubbed of sensitive fields
* Temporary files minimized and lifecycle-controlled

---

## 13.5 Zero Trust Security Architecture Alignment

The platform aligns with Zero Trust principles across all major framework components.

---

### 13.5.1 Identity and Access Management (IAM)

**Zero Trust Alignment**

* Every request authenticated
* Every action explicitly authorized
* No implicit trust based on network location

**Implementation**

* IAM roles per service
* No wildcard permissions
* Conditional access using resource and context attributes

---

### 13.5.2 Endpoint Security

| Endpoint Type   | Controls                     |
| --------------- | ---------------------------- |
| Lambda          | Managed runtime              |
| ECS Fargate     | Ephemeral tasks, no SSH      |
| Transfer Family | Managed SFTP, key-based auth |

There is **no persistent host access** in the architecture.

---

### 13.5.3 Network Security

* Private subnets only
* No public IPs on compute
* Static egress IPs for partner allowlisting
* East-west traffic encrypted by AWS

Network location alone does not grant access.

---

### 13.5.4 Application Security

* Strict schema validation
* Rate limiting and throttling
* Idempotency prevents replay attacks
* Explicit error messages without internal details

---

### 13.5.5 Data Security

* Tenant isolation via partition keys
* Access scoped by IAM and job ownership
* S3 prefixes segregated per customer
* Cross-region replication encrypted

---

## 13.6 Compliance with System IT Policies and Standards

### 13.6.1 System IT Policy Alignment

| Policy Area             | Status    |
| ----------------------- | --------- |
| Encryption standards    | Compliant |
| IAM and access control  | Compliant |
| Logging and audit       | Compliant |
| Multi-region resiliency | Compliant |
| Change management       | Compliant |

---

### 13.6.2 FRISS Policy Alignment

| FRISS Domain         | Alignment  |
| -------------------- | ---------- |
| Data confidentiality | Enforced   |
| Data integrity       | Enforced   |
| Access control       | Enforced   |
| Auditability         | Enforced   |
| Third-party risk     | Documented |

---

## 13.7 Known Security Limitations and Exceptions

### 13.7.1 External Partner SFTP Systems

**Limitation**

* External partner SFTP servers are outside System IT control.

**Impact**

* Cannot enforce partner-side patching, cipher standards, or uptime.

**Mitigation**

* SSH key authentication only
* Limited concurrency and throttling
* Strict retry and timeout controls
* Explicit shared responsibility documentation

---

### 13.7.2 End-to-End Mutual TLS

**Limitation**

* SFTP uses SSH, not mTLS.

**Decision**

* SSH encryption with key-based authentication is accepted as an equivalent secure control.

---

## 13.8 ARC Security Decisions and Trade-Offs

| Decision                  | Rationale                     |
| ------------------------- | ----------------------------- |
| Use managed AWS services  | Reduce attack surface         |
| Partitioned Active-Active | Prevent duplicate delivery    |
| S3 staging for SFTP→SFTP  | Improve reliability and audit |
| No persistent servers     | Minimize compromise risk      |

---

## 13.9 Security Monitoring and Incident Response

### 13.9.1 Security Monitoring

Monitored signals include:

* Authentication failures
* Unusual transfer patterns
* IAM permission anomalies
* Unexpected partner behavior

---

### 13.9.2 Incident Response

* All security events logged and correlated
* Alerts routed to on-call teams
* Runbooks define response procedures
* Post-incident reviews required

---

## 13.10 Section Summary

This section demonstrates that the architecture applies **defense-in-depth security controls**, aligns with **Zero Trust principles**, and meets System IT and FRISS policy expectations where technically feasible. Known limitations related to external partners are explicitly documented, mitigated, and presented for ARC awareness and approval.

---


# 14. Operational Excellence Pillar

This section describes how the Self-Serve File Transfer Backend Engine is **operated, deployed, monitored, and supported** to ensure reliability, safety, and compliance with enterprise operational standards. It also documents how the platform behaves during **FOMC freeze windows** and how changes are safely introduced and rolled back.

---

## 14.1 Operational Model Overview

The platform follows an **automation-first operational model** with minimal manual intervention.

Key characteristics:

* No always-on servers
* Immutable infrastructure
* Configuration-driven behavior
* Event-driven execution
* Clear separation between build, deploy, and runtime operations

Operations teams focus on **monitoring, incident response, and governance**, not manual execution.

---

## 14.2 FOMC Freeze Impact

### 14.2.1 FOMC Freeze Definition

During **FOMC (Federal Open Market Committee) freeze windows**, production changes are restricted to:

* Emergency break-glass fixes only
* Security patches if mandated
* No feature or infrastructure changes

---

### 14.2.2 Impact Assessment

| Area                    | Impact During FOMC Freeze |
| ----------------------- | ------------------------- |
| File transfer execution | No impact                 |
| In-flight jobs          | No impact                 |
| Job retries             | No impact                 |
| Status visibility       | No impact                 |
| Endpoint onboarding     | Restricted / queued       |
| Code deployments        | Blocked                   |
| Infrastructure changes  | Blocked                   |

---

### 14.2.3 Design Considerations for FOMC

* Runtime execution does **not depend on deployments**
* Endpoints and jobs are configuration-driven
* Transfers continue uninterrupted during freeze
* Onboarding requests can be queued for post-freeze activation

This design ensures **business continuity** during restricted change windows.

---

## 14.3 Software Development Lifecycle (SDLC)

### 14.3.1 Code and Change Review

All changes follow standard enterprise SDLC controls:

* Pull request required for all changes
* Minimum two peer reviewers
* Static code analysis
* Security scan
* Infrastructure changes reviewed by architecture

| Change Type          | Review Requirement         |
| -------------------- | -------------------------- |
| Application code     | Peer + senior engineer     |
| Infrastructure (IaC) | Architect review           |
| Security-sensitive   | Security review            |
| Emergency            | Post-implementation review |

---

### 14.3.2 Testing Strategy

The testing strategy covers multiple layers:

| Test Type         | Scope                            |
| ----------------- | -------------------------------- |
| Unit tests        | Lambda and helper logic          |
| Integration tests | API → DynamoDB → Step Functions  |
| Workflow tests    | Step Functions paths             |
| Transfer tests    | SFTP ↔ S3, small and large files |
| Failure injection | Task kill, network interruption  |
| DR tests          | Regional failover                |

Test evidence is retained for audit and ARC review.

---

### 14.3.3 Deployment Process

Deployments are:

* Fully automated via CI/CD
* Performed region-by-region
* Zero-downtime

**Deployment sequence**

1. Control Plane updates
2. Data Plane task definitions
3. Monitoring and alarms
4. Feature flags enabled

Production deployments require **manual approval**.

---

## 14.4 Rollback Plan Implementation

### 14.4.1 Rollback Principles

* Rollback must be fast and safe
* Rollback must not corrupt data
* Rollback must not require reprocessing files

---

### 14.4.2 Rollback Mechanisms

| Component         | Rollback Method          |
| ----------------- | ------------------------ |
| Lambda            | Version rollback         |
| Step Functions    | Previous state machine   |
| ECS Fargate       | Previous task definition |
| API Gateway       | Stage rollback           |
| Config (DynamoDB) | Versioned config revert  |

Job state and data remain intact during rollback.

---

## 14.5 Logging Strategy

### 14.5.1 Logging Scope

Logs are generated for:

* API requests and responses
* Job lifecycle events
* Workflow state transitions
* Transfer execution details
* Errors and retries
* Security-relevant events

---

### 14.5.2 Log Correlation

Every log entry includes:

* `job_id`
* `customer_id`
* `flow_type`
* `region`
* `execution_id`

This enables end-to-end traceability.

---

### 14.5.3 Log Retention

| Log Type         | Retention |
| ---------------- | --------- |
| Application logs | 90 days   |
| Audit logs       | 1 year    |
| Security logs    | 1 year    |
| DLQ messages     | 14 days   |

---

## 14.6 Monitoring and Alerting

### 14.6.1 Metrics Collected

| Component      | Key Metrics             |
| -------------- | ----------------------- |
| API Gateway    | Latency, 4xx/5xx        |
| Lambda         | Errors, duration        |
| Step Functions | Execution failures      |
| ECS Fargate    | CPU, memory, task exits |
| SQS            | Queue depth, age        |
| DynamoDB       | Throttles               |
| NAT Gateway    | Throughput              |

---

### 14.6.2 Alerting Strategy

* Alerts routed to on-call rotation
* Severity-based escalation
* Runbook links embedded in alerts

Alerts focus on **actionable signals**, not noise.

---

## 14.7 Deployment Diagram (Operational View)

```
Developer Commit
   ↓
CI Pipeline
   - Build
   - Test
   - Scan
   ↓
CD Pipeline
   ↓
Deploy to Dev
   ↓
Integration Tests
   ↓
Deploy to Test
   ↓
Approval Gate
   ↓
Deploy to Prod (West)
   ↓
Health Validation
   ↓
Deploy to Prod (East)
```

---

## 14.8 Customer Onboarding Flow (Operational View)

### 14.8.1 Onboarding Steps

1. Customer registers endpoint via POST API
2. Configuration validated and stored
3. Secrets stored in Secrets Manager
4. Connectivity test executed
5. Endpoint activated
6. Customer creates transfer job or schedule
7. Transfers execute automatically

---

### 14.8.2 Operational Guardrails

* Schema validation
* Rate limits
* Per-customer quotas
* Soft delete and disable support
* No operator involvement required

---

## 14.9 Runbooks and Operational Readiness

Runbooks are maintained for:

* Transfer failures
* Partner connectivity issues
* Regional failover
* Security incidents
* DLQ processing

Runbooks are versioned and reviewed regularly.

---

## 14.10 Section Summary

This section demonstrates that the platform is **operationally mature**, capable of running continuously through restricted change windows, and supported by strong SDLC, observability, rollback, and onboarding practices. The design minimizes operational risk while enabling safe and predictable change.



