Below is a **SADD-ready, formalized version** of Sections **3.6.7 Operational Assurance** and **3.6.8 Operational Practices**, rewritten in enterprise architecture language appropriate for ARC / FRB documentation.

---

# **3.6.7 Operational Assurance**

Operational Assurance for the Self-Serve EFT Platform is achieved through layered monitoring, logging, metrics collection, and analytics designed to provide situational awareness without creating hard runtime dependencies on observability tooling. Monitoring systems enhance operational visibility but are not required for core transaction processing or platform availability.

The platform leverages the following technologies for operational awareness:

* **Amazon CloudWatch** for metrics, log aggregation, alarms, and dashboard visualization
* **AWS CloudTrail** for immutable API audit logging
* **Centralized Log Aggregation / SIEM Integration** for security event correlation
* **Custom Business Metrics** for file transfer counts, latency, error rates, and replay events
* **TransferTracker (DynamoDB)** for operational state tracking and reconciliation

Observability services are deployed in a decoupled manner. A failure in monitoring infrastructure does not impact file transfer processing, workflow execution, or transfer state management. However, such failures generate separate alerts for remediation.

Operational metrics include:

* Transfer success/failure rates
* Duplicate detection counts
* Workflow execution latency
* Regional health status
* S3 replication lag (RPO monitoring)
* DynamoDB replication latency
* Failover invocation timestamps

Dashboards provide near-real-time system health, SLA tracking, and region status visibility. All audit logs are retained in accordance with regulatory retention requirements.

---

# **3.6.8 Operational Practices (Administration, RBAC, Automation, Resiliency)**

Operational governance of the EFT Platform is aligned with enterprise resiliency standards and incorporates role-based access control (RBAC), automation-driven remediation, and predefined failover decision criteria.

## 3.6.8.1 Failover Strategy & Decision Framework

The platform is deployed in an Active-Active configuration across:

* us-gov-west-1
* us-gov-east-1

There is no standby region; both regions remain active and capable of executing transfers.

Failover behavior includes:

* DNS failover updates to redirect traffic
* Region-specific bucket targeting via DNS TXT lookup
* Independent control plane and data plane per region

Failover invocation criteria include:

* Sustained regional service degradation exceeding defined SLA thresholds
* Control plane unavailability
* Transfer execution backlog exceeding defined recovery time thresholds
* AWS regional service advisory indicating material impairment

RTO target: **≤ 15 minutes**
RPO target:

* S3 replication: up to 15 minutes
* DynamoDB replication: typically < 1 minute

Outage classification examples:

* Sub-second DNS propagation impact
* Multi-minute region impairment requiring traffic shift
* Cross-region data reconciliation delay

The decision to initiate failover is operationally defined and documented in runbooks. In high-impact scenarios, failover may be triggered instead of extended troubleshooting to minimize blast radius.

---

## 3.6.8.2 Blast Radius Handling

Each failure category has a predefined response model:

| Failure Type              | Blast Radius    | Handling Action                                     |
| ------------------------- | --------------- | --------------------------------------------------- |
| Single workflow failure   | File-level      | Automatic retry with idempotency check              |
| Destination system outage | Target-specific | Retry with exponential backoff; isolate destination |
| Partial file upload       | File-level      | Validation failure; no workflow trigger             |
| Region degradation        | Regional        | DNS failover & traffic shift                        |
| Replication lag           | Cross-region    | Operational notification; reconciliation monitoring |

Replay logic ensures only failed destinations are retried, preventing broadcast duplication.

---

## 3.6.8.3 Automation & Resiliency Tooling

Resiliency automation is implemented using:

* **Step Functions** for deterministic workflow orchestration
* **Lambda chaining** for scalable execution
* **TransferTracker idempotency enforcement**
* **EventBridge** for decoupled event routing
* **SOAR integrations (if applicable)** for security incident response
* **Policy-based IAM authorization enforcement**
* **ISFW / segmentation controls** for internal boundary enforcement

Dynamic authorization policies restrict cross-enclave access and enforce prefix-level S3 scoping.

Automation includes:

* Duplicate prevention checks
* Partial upload detection prior to workflow execution
* Replay targeting only failed endpoints
* Regional health detection triggering operational alerts
* Automated alarm escalation

---

## 3.6.8.4 Administration & RBAC

Administrative access is segmented by I-profile:

* I-4 Privileged Admin: Config & IAM management
* I-5 Governance/Oversight: Read-only audit access
* I-6 Internal Automated: Scoped service roles

Controls include:

* Mandatory MFA for administrative users
* Separation of duties
* Approval-based CI/CD deployments
* Immutable audit logging
* Periodic access recertification

---

## 3.6.8.5 Resiliency Knowledge Base

Operational playbooks, failover procedures, and resiliency automation references are maintained in the enterprise knowledge repository. These include:

* Failover execution steps
* DNS update procedures
* Replication monitoring procedures
* Incident response automation workflows
* Escalation matrices

---

# Summary

The Operational Assurance and Operational Practices framework ensures:

* Monitoring does not introduce availability dependency
* Clear failover decision thresholds
* Defined RTO/RPO posture
* Controlled blast radius
* Automated remediation
* Role-based governance
* Regulatory audit alignment

---

Below is a **formal SADD-ready description** for Sections **3.6.3 Vendor Input**, **3.6.4 Dependencies**, and **3.6.5 Resiliency Calculations**, written in enterprise architecture language aligned to your EFT platform.

---

# **3.6.3 Vendor Input and Guidance for Product Line / Technology Stack**

The EFT Platform architecture leverages AWS GovCloud managed services as foundational components of its resiliency model. Architectural patterns including multi-region Active-Active deployment, service-level isolation, event-driven orchestration, and stateless compute execution are aligned with AWS Well-Architected Framework best practices and AWS resiliency design guidance.

AWS documentation and service-level agreements (SLAs) support the platform’s defined blast-radius segmentation strategy, including:

* Regional isolation between us-gov-west-1 and us-gov-east-1
* S3 cross-region replication for data durability
* DynamoDB global tables for state synchronization
* Independent control plane and data plane per region
* Managed compute isolation (Lambda / Fargate task-level containment)

Vendor guidance supports the principle that regional service failures are isolated events and that properly architected cross-region failover mechanisms can reduce operational impact. AWS SLA documentation confirms service availability targets for core services used in this design, including S3, DynamoDB, Lambda, and Route 53.

Documentation references include:

* AWS GovCloud Service Level Agreements
* AWS Well-Architected Framework – Reliability Pillar
* AWS Multi-Region Resiliency Patterns
* AWS Transfer Family High Availability Guidance

The defined blast radius assumptions — file-level, workflow-level, region-level, and cross-region — are consistent with AWS documented failure domain boundaries.

---

# **3.6.4 Dependencies**

The EFT Platform relies on the following managed services for availability and uptime:

### Core Service Dependencies

* Amazon S3 (object storage and landing zones)
* AWS Lambda (workflow execution)
* AWS Step Functions (orchestration)
* Amazon DynamoDB (TransferTracker and state management)
* Amazon EventBridge (event routing)
* AWS Transfer Family (SFTP endpoints)
* Amazon Route 53 (DNS routing and failover)
* AWS KMS (encryption key management)

### SLA Considerations

Service-level availability targets (per AWS public documentation):

* Amazon S3: ≥ 99.99% availability
* DynamoDB: ≥ 99.99% availability
* Lambda: ≥ 99.95% availability
* Route 53: ≥ 100% availability SLA (DNS query resolution)
* AWS Transfer Family: Regionally scoped availability

Where services provide less than 99.99% SLA (e.g., Lambda 99.95%), platform-level availability is improved through:

* Stateless retry mechanisms
* Idempotency enforcement
* Multi-region active deployment
* Decoupled event-driven architecture

### Impact of Dependency Downtime

If a critical dependency becomes unavailable:

* S3 outage (regional): New uploads in that region are blocked; traffic shifts to alternate region
* DynamoDB outage (regional): Transfer state updates delayed; failover to secondary region
* Lambda outage: Workflow execution retries; region-level failover if sustained
* Route 53 disruption: DNS-level impact; dependent on TTL and failover configuration
* Transfer Family outage: SFTP ingress impacted; alternate region endpoint used

The architecture ensures that no single service outage results in total platform failure. Blast radius is limited to regional or workflow-level scope, and cross-region redundancy mitigates prolonged service interruption.

---

# **3.6.5 Resiliency Calculations (SLA → MTD → RTO → RPO)**

## Starting Point: SLA = 99.9%

A 99.9% SLA equates mathematically to:

* 8.76 hours of allowable downtime per year
* 43.8 minutes per month
* 10.1 minutes per week

The platform’s resiliency posture targets effective availability exceeding 99.9% through multi-region redundancy.

---

## Maximum Tolerable Downtime (MTD)

MTD is defined as the maximum acceptable period the platform can be unavailable before causing material business impact.

For EFT services:

* MTD Target: ≤ 60 minutes

---

## Recovery Time Objective (RTO)

RTO defines the maximum time to restore service following a regional failure.

For regional failover:

* RTO Target: ≤ 15 minutes

This includes:

* DNS failover propagation
* Traffic redirection
* Workflow stabilization

---

## Recovery Point Objective (RPO)

RPO defines acceptable data loss window.

* S3 Cross-Region Replication: ≤ 15 minutes (asynchronous replication window)
* DynamoDB Global Tables: Typically < 1 minute replication lag

Therefore:

* RPO Target: ≤ 15 minutes worst-case (S3 dependent)

---

## Combined Resiliency Model

The relationship across resiliency metrics is:

SLA → Defines allowable annual downtime
MTD → Defines maximum business tolerance
RTO → Defines recovery execution time
RPO → Defines data loss tolerance

The platform’s Active-Active architecture ensures that RTO and RPO remain within defined MTD boundaries.

---

# Summary

The EFT Platform resiliency model:

* Aligns with AWS documented availability guarantees
* Defines explicit blast-radius containment
* Implements multi-region redundancy
* Quantifies SLA, MTD, RTO, and RPO
* Minimizes dependency-driven systemic failure
* Ensures compliance with regulatory availability expectations

---

Below is a **formal ARC-ready description** for the **Support**, **SLA Alignment**, and **Scalability Overview** sections, written at the level expected for an Architecture Review Committee submission.

---

# **Support Model Overview (ARC Description)**

The Self-Serve File Transfer (EFT) Platform introduces a cloud-native, event-driven architecture that integrates into the existing NIS operational support model without materially altering core support structures. The platform leverages managed AWS GovCloud services, reducing infrastructure-level operational overhead while increasing automation, observability, and fault isolation.

The solution will be incorporated into the existing enterprise SLA framework and NIS support model. No reduction in service level objectives is required. The platform’s design improves failure isolation and operational transparency compared to legacy transfer mechanisms.

Support responsibilities are distributed as follows:

* **Level 1 (Service Desk):** Incident intake, initial triage, customer communication.
* **Level 2 (Platform Operations):** Workflow diagnostics, transfer state validation, failover verification.
* **Level 3 (Engineering):** Root cause analysis, code-level remediation, architecture tuning.
* **Cloud Vendor (AWS):** Managed service availability per documented SLA.

The system leverages structured logging, centralized metrics, and automated alerting to ensure rapid detection and triage of operational events. All support workflows are documented in the RTM and associated runbooks.

---

# **SLA Alignment and Maintenance Considerations**

The platform aligns with the existing enterprise SLA target of **99.9% availability or greater**, with architectural capability to exceed this target via multi-region deployment.

### Maintenance Windows

Because the platform relies on fully managed AWS services and stateless compute (Lambda, Fargate), routine maintenance activities do not require coordinated downtime. Deployment activities are performed using:

* Blue/Green release strategies
* Infrastructure-as-Code (Terraform)
* Rolling updates with no shared runtime dependency

Maintenance windows are expected to be non-disruptive. If region-level failover testing is executed, traffic redirection occurs via DNS failover with an RTO target of ≤ 15 minutes.

### Availability and Security Rating Alignment

The platform operates within GovCloud boundaries and adheres to enterprise security classification standards. There are no misalignments between:

* Required availability levels
* Supported security rating
* Encryption requirements
* Segmentation policies

If temporary exceptions (POA&M items) arise, they will be documented within the Security section of the SADD.

---

# **Operational Relationship and Runbook Development**

Fine-grained operational procedures—including incident playbooks, failover decision matrices, and blast-radius containment workflows—are developed and maintained as living operational artifacts outside the Infrastructure Design document. These are tracked within:

* Detail Configuration Design (DCD)
* Runbook repository
* Confluence resiliency automation knowledge base
* Incident response SOP documentation

The architecture is intentionally designed to minimize manual intervention and promote automation-first recovery.

---

# **Current Service Level Agreement (SLA) Reference**

The platform inherits the current CRM-managed SLA for customer file transfer services. No SLA reduction is introduced. Where applicable, the new platform will be added as an eligible service under the existing enterprise service catalog.

---

# **Scalability Overview (ARC Narrative)**

The Self-Serve File Transfer Platform is designed using a cloud-native, horizontally scalable architecture. The system eliminates shared runtime bottlenecks by leveraging:

* Stateless Lambda functions for orchestration
* Event-driven processing via EventBridge
* Isolated Fargate tasks for execution workers
* Auto-scaling compute per file or workflow
* Multi-region active deployment

### Scaling Characteristics

* Scaling unit: File transfer workflow
* Compute scaling: Per invocation / per task
* Queue-based load absorption prevents upstream throttling
* No fixed server capacity constraints
* No shared monolithic runtime

Vertical scaling is selectively applied only for large-file Fargate workers where CPU/memory tuning improves throughput performance. Horizontal scaling remains the dominant elasticity model.

### Resiliency and Scaling Interaction

Scaling mechanisms are regionally independent. A regional surge does not impact alternate region capacity. This supports blast-radius isolation and reduces systemic risk during high-volume or failure conditions.

---

# ARC Positioning Summary

From an ARC perspective:

* No negative impact to existing SLA posture
* Improved operational isolation compared to legacy file transfer systems
* Automated failover and recovery posture
* Clear blast-radius segmentation
* Managed service reliance with documented vendor SLA backing
* Horizontal scalability with no infrastructure management burden

---

Below is a **formal ARC-ready description** for the **Environments**, **Network Placement**, and **Site Placement / Execution Site** sections, written at enterprise architecture review depth and aligned to your EFT / Self-Serve File Transfer platform.

---

# **Environments (ARC Description)**

The Self-Serve File Transfer (EFT) Platform is deployed using a structured, lifecycle-aligned environment model that maps directly to the Software Development Lifecycle (SDLC). Each environment is logically and operationally isolated to ensure separation of duties, controlled promotion, and blast-radius containment.

## 1. Development (DEV)

**Purpose:**
Supports feature development, integration testing, and infrastructure validation.

**Characteristics:**

* Non-production data (synthetic or masked datasets)
* Lower SLA and resiliency posture
* Reduced scale configuration
* Engineering-owned

**Network Placement:**
Deployed within a designated GovCloud VPC aligned to lower-tier segmentation policy. No external customer ingress permitted.

**Geographic Location:**
Primary GovCloud region (us-gov-west-1).

---

## 2. Quality Assurance (QA / TEST)

**Purpose:**
Supports functional testing, integration validation, resiliency testing, and failover validation prior to production promotion.

**Characteristics:**

* Controlled test data
* Simulated failover validation
* Production-equivalent architecture topology
* Used by QA and operational readiness teams

**Network Placement:**
Segregated VPC with stricter inbound/outbound controls compared to DEV.

**Geographic Location:**
Deployed in both primary and secondary GovCloud regions to validate cross-region replication behavior.

---

## 3. Production (PROD)

**Purpose:**
Customer-facing operational environment for enterprise file transfer services.

**Characteristics:**

* 99.9%+ SLA target
* Multi-region Active-Active deployment
* Cross-region data replication (S3 + DynamoDB)
* Full observability, alerting, and automated failover
* Strict RBAC enforcement

**Network Placement:**
Deployed in National IT CST tier aligned with production-grade segmentation and zero-trust principles.

**Geographic Location:**

* Primary: us-gov-west-1
* Secondary: us-gov-east-1

Regional independence ensures containment of geographic or regional failure events.

---

## 4. Contingency / Disaster Recovery (DR)

**Purpose:**
Supports regional failover scenarios and business continuity planning.

**Characteristics:**

* Standby regional capacity
* Automated DNS-based failover
* RTO ≤ 15 minutes
* RPO ≤ 15 minutes (S3 replication window)

DR is not a separate architecture but an operational mode of the Production environment via cross-region deployment.

---

# **Network Placement – Reasoning (ARC Description)**

The EFT platform is deployed within GovCloud-based VPC constructs aligned to FRS Tier segmentation policy. The network design enforces strict isolation across:

* Environment boundaries (DEV, QA, PROD)
* Regional boundaries
* Customer tenant boundaries
* Execution workload boundaries

## Key Design Principles

1. **Zero Trust Enforcement**

   * IAM-based authentication
   * Policy-based authorization
   * No implicit network trust

2. **Segmentation by Blast Radius**

   * Each region isolated
   * Each workflow isolated
   * Execution tasks containerized

3. **Minimal Inbound Surface**

   * AWS Transfer Family (SFTP endpoint)
   * API Gateway endpoints
   * No direct compute access exposed

4. **Outbound Controls**

   * Controlled egress via VPC endpoints
   * Private service endpoints for AWS managed services

The network placement decision aligns with FRS Tier Strategy and supports compliance, regulatory controls, and security rating requirements.

No CST/GST misalignment is introduced. The deployment model remains within approved GovCloud hosting tiers.

---

# **Site Placement / Execution Site – Reasoning (ARC Description)**

## Geographic Strategy

The platform is deployed in two geographically separated AWS GovCloud regions:

* **Primary Execution Site:** us-gov-west-1
* **Secondary Execution Site:** us-gov-east-1

This geographic separation provides:

* Regional fault isolation
* Natural disaster resilience
* Reduced systemic cloud-region dependency risk

---

## Execution Site Design

All compute components (Lambda, Fargate tasks, Step Functions) execute regionally and independently.

Key characteristics:

* Stateless orchestration
* Isolated execution containers
* No cross-region runtime dependencies
* Replicated metadata store (DynamoDB Global Tables)
* Asynchronous data replication (S3 CRR)

In the event of a regional disruption:

* Route 53 DNS failover shifts traffic
* Execution resumes in alternate region
* No manual data restoration required

---

# Risk and Design Considerations

Potential design risks evaluated:

* Asynchronous replication lag (S3 RPO window)
* DNS propagation delay during failover
* Managed service SLA dependency

Mitigations include:

* Idempotent workflow execution
* Retry mechanisms
* Automated health checks
* Observability-based failover triggers

No site placement decision introduces unacceptable design risk under defined SLA and RTO/RPO targets.

---

# ARC Summary Position

From an ARC standpoint:

* Environments are clearly lifecycle-aligned
* Network placement adheres to Tier strategy
* Multi-region architecture reduces geographic risk
* Execution isolation minimizes blast radius
* DR is embedded within the production architecture
* No unsupported hosting model or security tier deviation is introduced

---

Below is a **formal ARC-ready description** for:

* Security Boundaries
* Security Management Programs
* Resiliency Requirements
* Capacity Requirements
* Key Design Risks
* Project Risk Register
* Key Project & Design Decisions

Written in enterprise architecture review language suitable for SADD / ARC submission.

---

# **Security Boundaries (ARC Description)**

## 1. Security Boundaries Between This Application and Other Applications

The Self-Serve File Transfer (EFT) Platform is deployed as a logically isolated, cloud-native application within AWS GovCloud. Security boundaries are enforced through:

* Dedicated VPC segmentation
* IAM role-based authorization
* Service-to-service authentication
* KMS-based encryption domains
* Tenant-level storage isolation (bucket and prefix-level controls)

There is no shared runtime between EFT and other enterprise applications. All inter-application communication occurs through authenticated APIs or SFTP endpoints secured via:

* TLS 1.2+ encryption in transit
* IAM least-privilege policies
* Network ACL and Security Group enforcement

Application-level blast radius is limited to individual tenants, workflows, or regions.

---

## 2. Security Boundary Between This Application and National IT

The EFT Platform resides within approved GovCloud hosting boundaries and adheres to FRS/National IT segmentation and zero-trust policies.

Boundary enforcement includes:

* No direct network trust with National IT systems
* Authentication via enterprise identity provider (SSO / RBAC)
* Controlled ingress through Transfer Family endpoints and API Gateway
* Private service endpoints for AWS service interaction

All integration with National IT systems occurs through defined, authenticated interfaces. No implicit network trust is assumed.

---

## 3. Security Management Programs Used

The platform operates under established enterprise security programs, including:

* Enterprise RBAC enforcement
* IAM policy governance
* Encryption-at-rest using AWS KMS
* Centralized logging and SIEM ingestion
* SOAR integration for automated incident response
* Vulnerability scanning and container image hardening
* Infrastructure-as-Code review and change control
* Audit logging for all transfer and administrative events

The system supports regulatory audit requirements through immutable logging and traceability of transfer events.

---

# **Resiliency Requirements (ARC Description)**

The EFT Platform is designed to meet the following resiliency objectives:

* SLA Target: ≥ 99.9%
* RTO Target: ≤ 15 minutes (regional failover)
* RPO Target: ≤ 15 minutes (S3 replication window)
* Maximum Tolerable Downtime (MTD): ≤ 60 minutes

Resiliency architecture includes:

* Multi-region Active-Active deployment
* S3 Cross-Region Replication
* DynamoDB Global Tables
* Stateless compute execution
* Idempotent workflow processing
* DNS-based failover (Route 53)

Failure containment is structured across blast-radius layers:

* File-level
* Workflow-level
* Tenant-level
* Region-level

No single regional failure results in systemic platform outage.

---

# **Capacity Requirements (ARC Description)**

The platform is designed for elastic scaling without fixed infrastructure constraints.

## Scaling Model

* Primary scaling unit: File transfer workflow
* Lambda: Per invocation scaling
* Fargate: Task-based scaling for large transfers
* S3: Virtually unlimited storage scaling
* DynamoDB: On-demand throughput scaling

## Expected Load Characteristics

* Burst traffic supported via event-driven architecture
* No static server capacity planning required
* Queue-based load absorption prevents upstream throttling
* Large file workloads isolated to dedicated container execution

Capacity planning is focused on:

* Regional quota limits
* Concurrency controls
* Large file performance tuning

No vertical monolithic scaling is required for orchestration layers.

---

# **2.1 Key Design Risks (ARC Description)**

Below are the primary design risks expressed in “If X → Then Y → Mitigated by Z” format.

---

### Risk 1: Regional AWS Outage

If a GovCloud region becomes unavailable,
Then file ingress and workflow execution in that region are disrupted,
Mitigated by multi-region active deployment and DNS failover.

---

### Risk 2: Replication Lag (S3)

If cross-region replication experiences delay,
Then RPO window may approach defined 15-minute tolerance,
Mitigated by asynchronous design assumptions and retry/idempotency controls.

---

### Risk 3: Transfer Duplication During Failover

If clients retry transfers after failover,
Then duplicate sends may occur,
Mitigated by TransferTracker idempotency checks and deduplication logic.

---

### Risk 4: Misconfigured IAM Policy

If least-privilege boundaries are incorrectly configured,
Then unauthorized access or denial of service may occur,
Mitigated by policy validation, code review, and change control governance.

---

### Risk 5: DNS Failover Propagation Delay

If DNS TTL propagation is slower than expected,
Then failover RTO may increase,
Mitigated by short TTL configuration and health check monitoring.

---

### Risk 6: Large File Processing Bottleneck

If large file transfers saturate execution capacity,
Then processing latency increases,
Mitigated by dedicated Fargate scaling and workload isolation.

---

# **2.2 Project Risk Register**

A formal risk register is maintained within the project governance repository and includes:

* Risk ID
* Risk Description
* Likelihood
* Impact
* Mitigation Strategy
* Residual Risk
* Owner
* Review Date

The architecture design section provides technical mitigation context for each identified risk.

---

# **2.3 Key Project & Design Decisions (ARC Narrative)**

The architecture incorporates several foundational design decisions intended to balance resiliency, scalability, and operational control.

### 1. Multi-Region Active-Active Model

Both regions are capable of accepting ingress traffic. Workload execution is partitioned and controlled through distributed state management. This reduces regional blast radius while enabling continuity during failover events.

---

### 2. Stateless Execution Model

All orchestration components are stateless. Transfer state is externalized to DynamoDB. This eliminates single-node dependency and simplifies failover.

---

### 3. Event-Driven Architecture

The system uses event routing and decoupled processing to prevent synchronous dependency chains and cascading failures.

---

### 4. Idempotent Processing

Transfer workflows are designed to safely retry without duplication, protecting integrity during failover or client retries.

---

### 5. Managed Service Reliance

The platform intentionally leverages AWS managed services to reduce operational burden and infrastructure risk.

---

### 6. Tenant Isolation Model

Each customer’s transfer configuration and storage are logically isolated, ensuring misconfiguration or failure does not propagate across tenants.

---

# ARC Positioning Summary

From an Architecture Review Committee perspective:

* Clear security boundary enforcement
* Quantified resiliency objectives
* Explicit risk articulation with mitigation
* Managed service SLA alignment
* Horizontal scaling model
* Controlled blast-radius containment
* No unsupported hosting pattern introduced

---

Below is a **formal ARC-ready description** for:

**Section 2 – Design Overview**
**2.0 Key Requirements**

Written at enterprise Architecture Review Committee depth and aligned to SADD expectations.

---

# **Section 2 – Design Overview**

## **2.0 Key Requirements (ARC Description)**

The Self-Serve File Transfer (EFT) Platform is designed to meet documented business, security, resiliency, scalability, and compliance requirements as captured in the project Requirements Traceability Matrix (RTM). The RTM serves as the authoritative artifact mapping business requirements to architectural controls and implementation components. Security boundaries, SAFR roles, resiliency targets, availability objectives, categorization, classification, and scalability requirements are formally documented within the RTM Business Requirements tab and associated security artifacts.

The architecture described herein reflects the technical realization of those requirements.

---

# **Security Authorization & Documentation Approach**

The EFT Platform will be documented under SAFR governance using a formal **System Security Plan (SSP)**, as the system introduces a distinct cloud-native architecture, cross-region resiliency posture, and tenant-isolated execution model. Where appropriate, supporting documentation from an Abridged Risk Assessment Plan (ARAP) may be referenced for inherited controls from GovCloud infrastructure.

Security documentation will include:

* System boundary definition
* Control inheritance mapping (AWS GovCloud FedRAMP controls)
* IAM and RBAC control structure
* Encryption posture (in transit and at rest)
* Audit and logging framework
* POA&M tracking (if applicable)

---

# **Security Boundaries Between This Application and Others**

The EFT Platform establishes a distinct logical information security boundary within AWS GovCloud. The boundary is defined by:

* Dedicated VPC constructs
* IAM-scoped service roles
* Customer tenant isolation controls
* Independent storage domains
* Regionally segmented execution environments

The platform does not share runtime, storage, or control plane resources with other enterprise applications. Interactions with external systems occur strictly via authenticated and encrypted interfaces, including:

* AWS Transfer Family (SFTP ingress)
* API Gateway (REST-based interactions)
* Event-based integrations

Each integration point is treated as a controlled interface crossing a defined security boundary.

---

# **Security Boundary Between This Application and National IT**

The EFT Platform operates within the GovCloud boundary approved under National IT governance. The security boundary between EFT and National IT systems is enforced through:

* No implicit network trust
* Explicit authentication via enterprise identity provider
* Policy-based authorization controls
* Segmented VPC architecture
* Controlled ingress/egress rules

National IT may define a separate information security boundary for core infrastructure services, while the EFT application maintains its own application-level boundary within that hosting context.

This layered boundary approach ensures that compromise of one application does not propagate laterally across enterprise systems.

---

# **Security Management Programs Used**

The platform operates under established enterprise security programs and governance structures, including:

* SAFR governance framework
* Enterprise IAM and RBAC policy enforcement
* Encryption using AWS KMS
* Centralized logging and SIEM ingestion
* SOAR-based incident response automation
* Vulnerability scanning and image hardening
* Infrastructure-as-Code governance and peer review
* Change management and deployment approval workflow

All security-relevant events, including file transfers, administrative changes, and failover events, are auditable.

---

# **SAFR Roles and Governance**

For each defined information security boundary, the following SAFR roles are identified:

* **Authorizing Official (AO)** – Enterprise-level risk acceptance authority
* **System Owner** – Accountable for system functionality and risk posture
* **Information System Security Officer (ISSO)** – Responsible for operational security oversight
* **Primary SAFR Contact** – Security coordination and documentation liaison

Where National IT defines a broader hosting boundary, shared responsibility is documented within the SSP.

---

# **Information Classification**

The EFT Platform supports enterprise file movement and may process data up to the highest classification defined for participating business units. The highest classification supported by this architecture is determined based on business sponsor requirements and documented in the RTM.

The architecture enforces:

* Encryption at rest
* Encryption in transit
* Access controls aligned to classification level
* Tenant-level isolation

Data classification handling is enforced through IAM policy controls and storage segmentation.

---

# **Summary for ARC**

From an Architecture Review Committee perspective:

* Requirements are formally traceable through the RTM
* A formal SSP will document the system boundary and control posture
* Security boundaries are explicitly defined and enforced
* National IT hosting alignment is preserved
* Governance roles are clearly established
* Classification handling is embedded in architecture design
* No implicit trust relationships exist

---






