

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


# 15. Cost Optimization Pillar

This section documents how the Self-Serve File Transfer Backend Engine is designed to **optimize cost across its full lifecycle**, including acquisition, utilization, maintenance, and decommissioning. It also outlines the ongoing strategy for **monitoring, forecasting, and governing spend**, and compares alternative architectural patterns from a cost perspective.

---

## 15.1 Total Cost of Ownership (TCO) Overview

Total Cost of Ownership (TCO) is evaluated across the **entire lifecycle of the solution**, not only runtime infrastructure.

TCO includes:

* Resource acquisition and build
* Runtime utilization
* Operational support and maintenance
* Decommissioning and scale-down

The architecture is intentionally designed to:

* Minimize fixed and idle costs
* Shift spend toward usage-based services
* Reduce operational labor costs
* Avoid long-term infrastructure commitments

---

## 15.2 Resource Acquisition Costs

### 15.2.1 Hardware and Infrastructure

| Cost Category | Approach               | Cost Impact                 |
| ------------- | ---------------------- | --------------------------- |
| Servers       | Fully managed services | No hardware cost            |
| SFTP servers  | AWS Transfer Family    | No self-managed hosts       |
| Compute       | Serverless / Fargate   | No pre-provisioned capacity |
| Storage       | Amazon S3              | Pay per GB stored           |

There are **no upfront capital expenditures** for hardware.

---

### 15.2.2 Software and Build Costs

| Area              | Cost Consideration          |
| ----------------- | --------------------------- |
| Operating systems | Included (managed services) |
| Middleware        | Included                    |
| Licensing         | None                        |
| CI/CD             | Shared enterprise tooling   |

The platform relies entirely on **AWS-managed services**, eliminating third-party licensing costs.

---

## 15.3 Resource Utilization Costs

### 15.3.1 Primary Runtime Cost Drivers

| Component       | Cost Driver                 |
| --------------- | --------------------------- |
| API Gateway     | Requests                    |
| Lambda          | Invocations and duration    |
| Step Functions  | State transitions           |
| ECS Fargate     | vCPU/memory × runtime       |
| S3              | Storage and requests        |
| NAT Gateway     | Data processed              |
| Transfer Family | Endpoint-hours and sessions |
| DynamoDB        | Read/write capacity         |

---

### 15.3.2 Utilization-Based Design Decisions

* No always-on compute
* ECS tasks run **only during transfers**
* Large files consume more resources **only while active**
* Control plane remains low-cost due to lightweight operations

This ensures costs scale **linearly with usage**, not provisioned capacity.

---

### 15.3.3 Support, Licensing, and Training

| Area               | Cost Impact                |
| ------------------ | -------------------------- |
| Software licensing | None                       |
| OS patching        | None                       |
| SFTP maintenance   | None                       |
| On-call operations | Shared enterprise rotation |
| Training           | One-time enablement        |

Operational labor costs are significantly lower than self-managed alternatives.

---

## 15.4 Resource Maintenance Costs

### 15.4.1 Patching and Upgrades

| Component      | Maintenance Model |
| -------------- | ----------------- |
| API Gateway    | AWS managed       |
| Lambda         | AWS managed       |
| Step Functions | AWS managed       |
| ECS Fargate    | AWS managed       |
| S3 / DynamoDB  | AWS managed       |

There are:

* No patching windows
* No OS upgrades
* No middleware upgrades

---

### 15.4.2 Operational Maintenance

| Activity              | Cost Impact |
| --------------------- | ----------- |
| Configuration updates | Low         |
| Scaling adjustments   | Automatic   |
| Incident remediation  | Infrequent  |

---

## 15.5 Resource Removal and Decommissioning

### 15.5.1 Decommissioning Strategy

| Resource         | Removal Cost                         |
| ---------------- | ------------------------------------ |
| ECS tasks        | Zero                                 |
| Lambda functions | Zero                                 |
| Step Functions   | Zero                                 |
| DynamoDB tables  | Zero after deletion                  |
| S3 buckets       | Storage cost until retention expires |

---

### 15.5.2 Cost Implications

* No stranded infrastructure
* No sunk cost on unused capacity
* Storage costs controlled via lifecycle policies

---

## 15.6 Ongoing Cost Monitoring, Forecasting, and Analysis

### 15.6.1 Monitoring Tools

| Tool                 | Purpose             |
| -------------------- | ------------------- |
| AWS Cost Explorer    | Historical analysis |
| AWS Budgets          | Threshold alerts    |
| CloudWatch           | Usage correlation   |
| Cost allocation tags | Chargeback/showback |

---

### 15.6.2 Cost Allocation Strategy

Mandatory tags include:

* `Application = SelfServeFileTransfer`
* `CustomerId`
* `FlowType`
* `Environment`
* `Region`

This enables:

* Per-customer cost visibility
* Per-flow cost analysis
* Trend-based forecasting

---

### 15.6.3 Governance and Review

| Activity                   | Frequency |
| -------------------------- | --------- |
| Cost review                | Monthly   |
| Budget validation          | Quarterly |
| Optimization review        | Quarterly |
| Architecture re-evaluation | Annually  |

---

## 15.7 Cost Comparison Across Architecture Patterns

### 15.7.1 Patterns Evaluated

| Pattern              | Description                     |
| -------------------- | ------------------------------- |
| Pattern A            | Self-managed EC2 SFTP + scripts |
| Pattern B            | Lambda-heavy transfer approach  |
| Pattern C (Selected) | Managed services + Fargate      |

---

### 15.7.2 Relative Cost Comparison

| Dimension             | Pattern A | Pattern B | Pattern C     |
| --------------------- | --------- | --------- | ------------- |
| Idle capacity         | High      | Medium    | **Low**       |
| Maintenance labor     | High      | Medium    | **Low**       |
| Large file efficiency | Poor      | Limited   | **High**      |
| DR cost               | High      | Medium    | **Optimized** |
| Cost predictability   | Low       | Medium    | **High**      |
| TCO                   | High      | Medium    | **Lowest**    |

---

### 15.7.3 Current vs Target State Cost View

| Aspect               | Current State | Target State |
| -------------------- | ------------- | ------------ |
| Fixed infrastructure | Yes           | No           |
| Idle cost            | High          | Minimal      |
| DR duplication       | Manual        | Built-in     |
| Cost visibility      | Low           | High         |

---

## 15.8 Cost Risks and Mitigations

| Risk               | Impact            | Mitigation          |
| ------------------ | ----------------- | ------------------- |
| Unexpected spikes  | Cost surge        | Budgets + throttles |
| Large-file retries | Increased runtime | Checkpointing       |
| NAT saturation     | Increased cost    | Concurrency limits  |
| Log growth         | Storage cost      | Retention policies  |

---

## 15.9 Cost Disclaimer (ARC-Required)

> **Cost Disclaimer**
>
> All cost values, estimates, and comparisons in this document represent a **single point-in-time view** and are based on **current pricing, workload assumptions, and inputs provided by Product Teams**.
>
> Actual costs may vary due to:
>
> * Changes in usage patterns
> * AWS pricing updates
> * Regional pricing differences
> * External partner behavior
>
> Cost projections should be revisited periodically as the system scales and evolves.

---

## 15.10 Section Summary

This section demonstrates that the architecture is **cost-efficient by design**, minimizes idle spend, leverages managed services to reduce operational labor, and provides strong mechanisms for cost visibility, governance, and optimization over time.

---



# 16. Risks, Assumptions, and Mitigations

This section documents the **key risks**, **underlying assumptions**, and **mitigation strategies** associated with the Self-Serve File Transfer Backend Engine. It provides transparency into areas of uncertainty and demonstrates proactive risk management.

---

## 16.1 Key Risks

### 16.1.1 External Partner Availability Risk

**Description**
External SFTP endpoints are outside the control of the platform and may experience downtime, latency, or throttling.

**Impact**

* Delayed inbound or outbound file transfers
* Increased retries and execution duration

**Mitigation**

* Configurable retry and backoff policies
* Partner-specific concurrency limits
* Alerting on repeated failures
* Clear ownership boundaries documented

**Residual Risk**

* Medium (accepted)

---

### 16.1.2 Duplicate Transfer Risk

**Description**
Multi-region execution introduces risk of duplicate file delivery if ownership is not strictly controlled.

**Impact**

* Data integrity issues
* Partner reconciliation challenges

**Mitigation**

* Partitioned Active-Active model
* Lease-based execution control
* Idempotency keys
* Atomic delivery (`.tmp → rename`)

**Residual Risk**

* Low

---

### 16.1.3 Large File Transfer Failures

**Description**
Transfers of files up to 30GB may fail due to network interruptions or partner limitations.

**Impact**

* Extended execution times
* Partial or failed transfers

**Mitigation**

* Streaming-based transfers
* Multipart uploads
* Retry with resume capability
* S3 staging for checkpointing

**Residual Risk**

* Low to Medium

---

### 16.1.4 Cost Spikes During Burst Traffic

**Description**
Unexpected spikes in transfer volume or file size can increase runtime costs.

**Impact**

* Budget overruns
* Increased NAT and compute spend

**Mitigation**

* Concurrency throttling
* AWS Budgets and alerts
* Per-customer quotas
* Periodic cost reviews

**Residual Risk**

* Low

---

### 16.1.5 Configuration Errors During Onboarding

**Description**
Incorrect endpoint or schedule configuration by customers may cause job failures.

**Impact**

* Failed transfers
* Support tickets

**Mitigation**

* Strong schema validation
* Connectivity tests before activation
* Soft-disable and rollback options
* Clear error messages

**Residual Risk**

* Low

---

### 16.1.6 Regional Outage Risk

**Description**
A full AWS GovCloud region outage could disrupt in-flight transfers.

**Impact**

* Temporary service degradation
* Job delays

**Mitigation**

* Partitioned Active-Active deployment
* Lease expiration and takeover
* Cross-region data replication
* Automated failover

**Residual Risk**

* Low

---

## 16.2 Assumptions

The architecture is built on the following assumptions:

| ID   | Assumption                                                 |
| ---- | ---------------------------------------------------------- |
| AS-1 | AWS GovCloud services remain available per published SLAs  |
| AS-2 | External partners support SFTP with SSH key authentication |
| AS-3 | External partners may not support push-based transfers     |
| AS-4 | File sizes may reach up to 30GB                            |
| AS-5 | Customers accept eventual consistency during failover      |
| AS-6 | System IT policies allow managed AWS services              |
| AS-7 | Retry-based delivery is acceptable for transient failures  |

These assumptions are reviewed periodically as usage evolves.

---

## 16.3 Mitigation Strategy Summary

| Risk Category  | Mitigation Strategy           |
| -------------- | ----------------------------- |
| Availability   | Multi-region Active-Active    |
| Data integrity | Idempotency + atomic delivery |
| Performance    | Streaming + tiered sizing     |
| Security       | Defense-in-depth + Zero Trust |
| Operations     | Automation + observability    |
| Cost           | Quotas + budgets              |

---

## 16.4 Open Issues and Follow-Ups

The following items are tracked for future evaluation:

| ID   | Item                        | Owner        | Status       |
| ---- | --------------------------- | ------------ | ------------ |
| OI-1 | UI portal for onboarding    | Product      | Backlog      |
| OI-2 | Additional protocols (FTPS) | Architecture | Future       |
| OI-3 | Partner SLA automation      | Product      | Under review |
| OI-4 | Advanced content validation | Architecture | Future       |

These items do not block ARC approval.

---

## 16.5 Section Summary

This section demonstrates that key architectural and operational risks have been identified, analyzed, and mitigated through design and process controls. Residual risks are explicitly documented and accepted where appropriate, providing transparency and confidence for ARC approval.

---




# 17. Alternatives Considered

This section documents the **architectural alternatives evaluated**, the **trade-offs analyzed**, and the **rationale for selecting the final architecture**. The goal is to demonstrate that multiple viable options were reviewed and that the chosen solution best satisfies business, technical, security, resiliency, and cost requirements.

---

## 17.1 Evaluation Criteria

All alternatives were evaluated against the following criteria:

* Support for **SFTP and S3** transfer flows
* Ability to handle **large files (up to 30GB)**
* Multi-region **high availability and disaster recovery**
* **Duplicate prevention** and correctness guarantees
* Alignment with **Zero Trust** and System IT security standards
* Operational complexity and supportability
* Cost efficiency and predictability
* Suitability for **GovCloud** deployment

---

## 17.2 Alternative 1: Self-Managed EC2-Based SFTP and Transfer Scripts

### Description

This option uses:

* EC2-hosted SFTP servers
* Custom scripts or cron jobs for file transfers
* Manual scaling and DR configuration

---

### Pros

* Full control over environment
* Familiar operational model

---

### Cons

* High operational overhead (patching, upgrades, monitoring)
* Always-on infrastructure with idle cost
* Complex DR setup and testing
* Higher security risk due to persistent servers
* Poor scalability for burst and large-file workloads

---

### Decision

**Rejected**

**Rationale**

* Does not meet operational excellence or cost optimization goals
* Introduces unnecessary security and maintenance risk

---

## 17.3 Alternative 2: Lambda-Only Serverless Transfer Model

### Description

This option relies exclusively on AWS Lambda for file transfers, including SFTP interactions.

---

### Pros

* Fully serverless
* No infrastructure management
* Cost-effective for very small files

---

### Cons

* Lambda execution time limit (15 minutes)
* Memory and disk limitations
* Unsuitable for files approaching 30GB
* Complex workaround logic required
* Increased risk of partial failures

---

### Decision

**Rejected**

**Rationale**

* Cannot reliably support large files or external SFTP transfers
* Violates performance and reliability requirements

---

## 17.4 Alternative 3: Active-Passive Multi-Region Architecture

### Description

One region actively processes transfers while the other remains on standby.

---

### Pros

* Simpler failover logic
* Clear primary/secondary roles

---

### Cons

* Idle infrastructure cost
* Slower recovery during failover
* Manual promotion often required
* Underutilization of secondary region

---

### Decision

**Rejected**

**Rationale**

* Does not meet availability and efficiency goals
* Higher RTO compared to Active-Active

---

## 17.5 Alternative 4: True Active-Active Without Partitioning

### Description

Both regions process all jobs concurrently with minimal coordination.

---

### Pros

* Maximum throughput
* Simplified routing logic

---

### Cons

* High risk of duplicate transfers
* Complex reconciliation logic
* Not acceptable for file-based integrations
* Violates data integrity expectations

---

### Decision

**Rejected**

**Rationale**

* Duplicate delivery risk is unacceptable for enterprise file transfers

---

## 17.6 Selected Architecture: Partitioned Active-Active with Managed Services

### Description

The selected architecture:

* Uses AWS managed services in GovCloud
* Separates control plane and data plane
* Employs partitioned Active-Active execution
* Uses lease-based ownership and idempotency
* Leverages ECS Fargate for large-file transfers

---

### Why This Option Was Selected

| Criterion            | Outcome         |
| -------------------- | --------------- |
| Large file support   | Fully supported |
| Duplicate prevention | Guaranteed      |
| Multi-region HA/DR   | Automated       |
| Security alignment   | Strong          |
| Operational overhead | Low             |
| Cost predictability  | High            |
| GovCloud readiness   | Fully compliant |

---

## 17.7 Summary Comparison Table

| Option             | Availability | Scalability | Security | Cost          | Operational Risk |
| ------------------ | ------------ | ----------- | -------- | ------------- | ---------------- |
| EC2-based          | Medium       | Low         | Medium   | High          | High             |
| Lambda-only        | Medium       | Medium      | High     | Low           | Medium           |
| Active-Passive     | Medium       | Medium      | High     | Medium        | Medium           |
| True Active-Active | High         | High        | Medium   | Medium        | High             |
| **Selected**       | **High**     | **High**    | **High** | **Optimized** | **Low**          |

---

## 17.8 Section Summary

Multiple architectural approaches were evaluated to meet the system’s functional and non-functional requirements. The selected **partitioned Active-Active architecture using AWS managed services** provides the best balance of **availability, correctness, security, operational simplicity, and cost efficiency**, making it the most suitable choice for enterprise-grade file transfers in AWS GovCloud.

---


