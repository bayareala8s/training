

# 1. Document Control

## 1.1 Document Purpose

This Software Architecture Design Document (SAD) describes the target architecture for the **Self-Serve File Transfer Backend Engine** deployed in **AWS GovCloud**. The document is intended for review and approval by the **Architecture Review Board (ARB/ARC)** and serves as the authoritative reference for design decisions, security posture, resiliency strategy, operational model, and cost considerations.

The goal is to provide an enterprise-grade, scalable, and secure backend engine that enables file transfers between:

* **SFTP → SFTP**
* **SFTP → S3**
* **S3 → S3**
* **S3 → SFTP**

with support for both **push and pull** models, including **external partner SFTP endpoints**, and file sizes ranging from **1KB to 30GB**.

---

## 1.2 Intended Audience

This document is intended for:

* Architecture Review Board members
* Enterprise Architecture and Platform Architecture teams
* Information Security / Risk / Compliance teams
* Infrastructure / Operations / SRE teams
* Product Management stakeholders
* Development teams responsible for implementation and support

---

## 1.3 Scope of Document

This document covers:

* System context and architectural overview
* Detailed control plane and data plane design
* Transfer job model and endpoint configuration model
* Active-Active deployment strategy across **us-gov-west-1** and **us-gov-east-1**
* Security and compliance controls aligned with Zero Trust
* Performance, resiliency, operations, and cost pillars
* Known constraints, risks, and mitigations
* Evidence plans (testing, monitoring, operational readiness)

---

## 1.4 Definitions, Acronyms, and Abbreviations

| Term          | Definition                                                                             |
| ------------- | -------------------------------------------------------------------------------------- |
| ARC / ARB     | Architecture Review Committee / Board                                                  |
| Control Plane | Components that validate, orchestrate, and track transfers (API, orchestration, state) |
| Data Plane    | Components that move file bytes (S3, Transfer Family, Fargate workers)                 |
| HA            | High Availability                                                                      |
| DR            | Disaster Recovery                                                                      |
| RTO           | Recovery Time Objective                                                                |
| RPO           | Recovery Point Objective                                                               |
| MTD           | Maximum Tolerable Downtime                                                             |
| CRR           | Cross-Region Replication (S3)                                                          |
| Idempotency   | Safe retry without duplication                                                         |
| Lease         | Time-bound lock to prevent dual-region execution                                       |
| Endpoint      | Configuration describing a source or target (SFTP or S3)                               |
| Transfer Job  | A unit of work describing a file transfer attempt and lifecycle                        |

---

## 1.5 References

* AWS Well-Architected Framework (GovCloud deployment principles)
* Internal System IT security policies and standards
* FRISS policies (as applicable)
* Internal SDLC and change management standards
* Architecture Review Board submission guidelines

*(Links intentionally omitted for document portability; can be added as footnotes in final version.)*

---

## 1.6 Revision History

| Version | Date       | Author   | Summary                                          |
| ------- | ---------- | -------- | ------------------------------------------------ |
| 0.1     | YYYY-MM-DD | Himanshu | Initial draft for ARC review                     |
| 0.2     | YYYY-MM-DD | Himanshu | Added multi-region DR, security, and ops details |
| 1.0     | YYYY-MM-DD | Himanshu | Final ARC submission                             |

---

# 2. Executive Summary

## 2.1 Business Context

Multiple business and integration teams require secure and reliable file transfers across internal systems and external partners. Existing transfer mechanisms often involve manual onboarding, bespoke scripts, inconsistent operational monitoring, and limited resiliency guarantees. This increases operational risk and reduces transparency for customers and leadership.

---

## 2.2 Problem Statement

Current file transfer approaches have the following challenges:

* Manual onboarding and inconsistent standards for endpoints and credentials
* Limited self-service capability for customers
* Incomplete end-to-end observability and status tracking
* Weak multi-region resiliency and unclear DR behavior
* Difficulty handling large transfers reliably (up to 30GB), especially across external SFTP

---

## 2.3 Proposed Solution Overview

The proposed solution is a **Self-Serve File Transfer Backend Engine** built using AWS GovCloud managed services and event-driven orchestration. The platform separates:

* **Control Plane** for job creation, orchestration, policy enforcement, and status tracking
* **Data Plane** for streaming byte transfer across SFTP and S3, optimized for 1KB–30GB workloads

The system is deployed in **Active-Active mode** across **us-gov-west-1** and **us-gov-east-1**, using a **partitioned ownership model (Option B)** to prevent duplicate transfers while enabling failover.

---

## 2.4 Key Architectural Decisions

1. **Partitioned Active-Active execution**

   * Both regions accept requests; only one executes per partition using a DynamoDB lease.
2. **Fargate-based transfer workers for SFTP**

   * Supports streaming, large files, retries, and controlled egress.
3. **S3 staging for SFTP→SFTP**

   * Improves reliability, DR, and operational re-drive.
4. **Event-driven architecture**

   * S3 events and scheduled triggers drive jobs through EventBridge/SQS into Step Functions.
5. **Endpoint configuration via APIs**

   * Customer registers endpoints (SFTP/S3) via POST API; secrets stored in Secrets Manager; configs in DynamoDB.

---

## 2.5 Summary of Benefits

* **Resiliency:** Multi-region HA/DR with controlled failover behavior
* **Security:** Zero Trust aligned identity + encryption + least privilege
* **Reliability:** Idempotency and leases prevent duplicate delivery
* **Scalability:** Supports small to very large files with predictable performance
* **Operational Excellence:** Centralized logs/metrics, runbooks, and rollback strategy
* **Self-Service:** Customers can onboard endpoints and track transfers with clear status APIs

---

## 2.6 ARC Decision Requested

Approval is requested for:

* Deploying the system across **us-gov-west-1 and us-gov-east-1** in partitioned Active-Active mode
* Using ECS Fargate streaming workers for SFTP transfers (including external partners)
* Using S3 staging patterns for SFTP→SFTP delivery reliability and DR

---

## 2.7 Non-Goals (clarity for reviewers)

The following are not goals for the initial release:

* Full UI portal (backend-first)
* Non-SFTP protocols such as FTPS/HTTPS transfers
* Real-time streaming ingestion beyond file transfers
* Complex transformations beyond optional checksum/scan

---

## 2.8 Stakeholder Summary (One-liner)

This architecture provides a secure, resilient, self-service backend engine for enterprise file transfers in GovCloud, with clear operational controls and predictable DR behavior.

---



# 3. Business and Functional Overview

## 3.1 Business Objectives

The Self-Serve File Transfer Backend Engine is designed to achieve the following business objectives:

* Provide a **standardized, enterprise-approved file transfer capability** for internal systems and external partners
* Enable **self-service onboarding** of file transfer endpoints without manual infrastructure changes
* Improve **operational reliability** and reduce incidents caused by bespoke scripts or unmanaged transfers
* Support **regulatory and audit requirements** through end-to-end traceability and logging
* Reduce **time-to-onboard** new integrations while maintaining strong security controls
* Ensure **high availability and disaster recovery** for mission-critical file exchanges

---

## 3.2 In-Scope Capabilities

The following capabilities are included in the scope of this architecture:

* Self-service registration of **SFTP and S3 endpoints**
* On-demand and scheduled file transfers
* Event-driven (push) and polling-based (pull) transfer models
* External partner SFTP integration
* Support for file sizes ranging from **1KB to 30GB**
* End-to-end job tracking and status visibility
* Idempotent execution and duplicate prevention
* Multi-region Active-Active deployment for HA/DR
* Secure secret handling and encryption
* Operational observability and audit logging

---

## 3.3 Out-of-Scope Capabilities

The following capabilities are explicitly out of scope for the initial implementation:

* Graphical user interface (UI) or customer portal
* Protocols other than SFTP and S3 (e.g., FTPS, HTTPS)
* Inline data transformation beyond optional checksum or validation
* Real-time streaming or message-based ingestion
* Content-level business validation of transferred files
* Manual file manipulation or operator-driven transfers

These capabilities may be considered for future iterations but are not required for ARC approval of this design.

---

## 3.4 Supported File Transfer Flows

The platform supports four primary file transfer flows, each designed to meet different business and integration needs.

### 3.4.1 SFTP → SFTP

**Business Use Case**

* Receive files from one external partner and forward them to another
* Act as an intermediary or clearing layer between two systems

**Key Characteristics**

* External or internal SFTP endpoints
* Two-leg transfer using S3 as a staging and checkpoint layer
* Supports large files and retries without re-pulling from source

**Example**

> Partner A uploads a daily claims file. The platform securely stages the file and delivers it to Partner B’s SFTP.

---

### 3.4.2 SFTP → S3

**Business Use Case**

* Ingest files from partners into cloud storage for downstream processing
* Centralize raw data storage for analytics or compliance

**Key Characteristics**

* Supports both AWS Transfer Family SFTP and external partner SFTP
* Streaming upload to S3 with multipart support
* Event-driven or scheduled polling

**Example**

> A partner uploads transaction files via SFTP, which are automatically stored in an S3 raw bucket.

---

### 3.4.3 S3 → S3

**Business Use Case**

* Internal data movement between buckets or storage tiers
* Lifecycle-driven or event-driven internal transfers

**Key Characteristics**

* Uses native S3 server-side copy
* No data plane compute required
* High throughput and low cost

**Example**

> Files arriving in a landing bucket are moved to a raw or curated bucket automatically.

---

### 3.4.4 S3 → SFTP

**Business Use Case**

* Deliver outbound files to external partners
* Publish generated reports, statements, or batch outputs

**Key Characteristics**

* Event-driven or on-demand execution
* Streaming download from S3 and upload to SFTP
* Atomic publish pattern (`.tmp` → rename)

**Example**

> A nightly report is generated in S3 and delivered to a partner’s SFTP endpoint.

---

## 3.5 Push vs Pull Transfer Models

The platform supports both **push-based** and **pull-based** transfer models to accommodate different partner and system behaviors.

### 3.5.1 Push Model (Event-Driven)

**Description**

* A transfer is triggered automatically when a file arrives
* Typical triggers include:

  * S3 ObjectCreated events
  * AWS Transfer Family uploads

**Advantages**

* Near real-time processing
* No polling overhead
* Lower latency

**Example**

> When a file lands in an S3 outbox, it is immediately delivered to a partner SFTP.

---

### 3.5.2 Pull Model (Scheduled or On-Demand)

**Description**

* The system initiates the transfer by polling or requesting files
* Typically used for external partner SFTP sources

**Advantages**

* Compatible with partners that cannot push
* Controlled execution and throttling
* Predictable schedules

**Example**

> Every 5 minutes, the system checks a partner SFTP directory for new files and downloads them.

---

## 3.6 Supported Deployment Regions

The platform is deployed in the following AWS GovCloud regions:

* **us-gov-west-1**
* **us-gov-east-1**

Both regions are:

* Fully provisioned
* Actively serving traffic
* Capable of executing transfers

Execution ownership is controlled through a **partitioned Active-Active model**, ensuring high availability without duplicate processing.

---

## 3.7 Functional Summary Table

| Capability                     | Supported |
| ------------------------------ | --------- |
| External SFTP integration      | Yes       |
| Managed SFTP (Transfer Family) | Yes       |
| S3 storage integration         | Yes       |
| Push transfers                 | Yes       |
| Pull transfers                 | Yes       |
| Large file support (30GB)      | Yes       |
| Multi-region HA/DR             | Yes       |
| Self-service onboarding        | Yes       |
| End-to-end status tracking     | Yes       |

---

## 3.8 Section Summary

This section outlines the business drivers and functional capabilities supported by the Self-Serve File Transfer Backend Engine. The platform provides a consistent, secure, and scalable foundation for file transfers across internal systems and external partners, while supporting multiple transfer models and deployment regions.

---



# 4. Requirements

This section defines the **functional and non-functional requirements** that drive the architecture and design decisions for the Self-Serve File Transfer Backend Engine. These requirements represent the minimum capabilities needed to support business use cases, regulatory expectations, and operational standards.

---

## 4.1 Functional Requirements

The system shall provide the following functional capabilities.

### 4.1.1 Endpoint Management

| ID   | Requirement                                                                        |
| ---- | ---------------------------------------------------------------------------------- |
| FR-1 | The system shall allow customers to register SFTP and S3 endpoints via secure APIs |
| FR-2 | The system shall store endpoint configuration metadata in a durable data store     |
| FR-3 | The system shall store credentials securely using AWS Secrets Manager              |
| FR-4 | The system shall support activation, deactivation, and update of endpoints         |
| FR-5 | The system shall validate endpoint connectivity prior to activation                |

---

### 4.1.2 Transfer Job Management

| ID    | Requirement                                                                      |
| ----- | -------------------------------------------------------------------------------- |
| FR-6  | The system shall allow customers to initiate transfers on demand                 |
| FR-7  | The system shall support scheduled transfers (polling model)                     |
| FR-8  | The system shall support event-driven transfers (push model)                     |
| FR-9  | The system shall create a durable transfer job record for every transfer attempt |
| FR-10 | The system shall track transfer job lifecycle states                             |
| FR-11 | The system shall prevent duplicate job execution                                 |

---

### 4.1.3 Supported Transfer Flows

| ID    | Requirement                                    |
| ----- | ---------------------------------------------- |
| FR-12 | The system shall support SFTP → SFTP transfers |
| FR-13 | The system shall support SFTP → S3 transfers   |
| FR-14 | The system shall support S3 → S3 transfers     |
| FR-15 | The system shall support S3 → SFTP transfers   |

---

### 4.1.4 Large File Handling

| ID    | Requirement                                                                           |
| ----- | ------------------------------------------------------------------------------------- |
| FR-16 | The system shall support file sizes from 1KB up to 30GB                               |
| FR-17 | The system shall support streaming transfers without loading entire files into memory |
| FR-18 | The system shall support multipart uploads for large files                            |
| FR-19 | The system shall retry failed transfers in a controlled manner                        |

---

### 4.1.5 Status and Observability

| ID    | Requirement                                                         |
| ----- | ------------------------------------------------------------------- |
| FR-20 | The system shall expose transfer job status via API                 |
| FR-21 | The system shall provide detailed error information for failed jobs |
| FR-22 | The system shall provide audit logs for transfer activity           |
| FR-23 | The system shall correlate logs and metrics using a job identifier  |

---

## 4.2 Non-Functional Requirements

### 4.2.1 Availability

| ID     | Requirement                                                                   |
| ------ | ----------------------------------------------------------------------------- |
| NFR-A1 | The system shall be highly available across multiple Availability Zones       |
| NFR-A2 | The system shall be deployed across multiple AWS GovCloud regions             |
| NFR-A3 | The system shall continue processing transfers during a single-region failure |
| NFR-A4 | The system shall prevent duplicate transfers during failover                  |

---

### 4.2.2 Scalability

| ID     | Requirement                                                                     |
| ------ | ------------------------------------------------------------------------------- |
| NFR-S1 | The system shall scale horizontally to support concurrent transfers             |
| NFR-S2 | The system shall support burst traffic without manual intervention              |
| NFR-S3 | The system shall apply backpressure to protect partner systems                  |
| NFR-S4 | The system shall scale independently for control plane and data plane workloads |

---

### 4.2.3 Performance

| ID     | Requirement                                                     |
| ------ | --------------------------------------------------------------- |
| NFR-P1 | The system shall efficiently transfer files up to 30GB          |
| NFR-P2 | The system shall minimize transfer latency for push-based flows |
| NFR-P3 | The system shall optimize throughput for large file transfers   |
| NFR-P4 | The system shall avoid unnecessary data movement or duplication |

---

### 4.2.4 Security

| ID      | Requirement                                                      |
| ------- | ---------------------------------------------------------------- |
| NFR-SC1 | The system shall enforce strong authentication and authorization |
| NFR-SC2 | The system shall encrypt data in transit and at rest             |
| NFR-SC3 | The system shall enforce least-privilege access controls         |
| NFR-SC4 | The system shall isolate customers and endpoints                 |
| NFR-SC5 | The system shall securely integrate with external partners       |

---

### 4.2.5 Compliance

| ID     | Requirement                                                 |
| ------ | ----------------------------------------------------------- |
| NFR-C1 | The system shall operate in AWS GovCloud regions            |
| NFR-C2 | The system shall comply with System IT security standards   |
| NFR-C3 | The system shall align with FRISS policies where applicable |
| NFR-C4 | The system shall retain audit logs per policy requirements  |

---

### 4.2.6 Observability

| ID     | Requirement                                                |
| ------ | ---------------------------------------------------------- |
| NFR-O1 | The system shall provide centralized logging               |
| NFR-O2 | The system shall expose operational metrics                |
| NFR-O3 | The system shall generate alerts on failures and anomalies |
| NFR-O4 | The system shall support root-cause analysis               |

---

## 4.3 Requirements Traceability (High-Level)

This architecture is designed so that:

* **Functional requirements** map directly to control plane components (API Gateway, Lambda, Step Functions)
* **Performance and scalability requirements** are primarily addressed by the data plane (ECS Fargate, S3)
* **Availability and resiliency requirements** are addressed through multi-region deployment and lease-based ownership
* **Security and compliance requirements** are enforced through IAM, encryption, and audit logging

Detailed traceability is documented in subsequent sections.

---

## 4.4 Section Summary

This section establishes the functional and non-functional requirements that guide the architecture. These requirements form the basis for design decisions related to scalability, resiliency, security, and operational excellence described in later sections of this document.

---



# 5. Architectural Principles and Constraints

This section describes the **core architectural principles**, **assumptions**, **constraints**, and **trade-offs** that shape the design of the Self-Serve File Transfer Backend Engine. These principles ensure the solution aligns with enterprise architecture standards while meeting business, security, and operational requirements.

---

## 5.1 Architectural Principles

The architecture is guided by the following principles:

### 5.1.1 Separation of Control Plane and Data Plane

* The system explicitly separates **orchestration and governance (control plane)** from **file movement (data plane)**.
* Control plane components manage:

  * validation
  * job creation
  * orchestration
  * status tracking
* Data plane components handle:

  * streaming transfers
  * large file handling
  * network-intensive operations

**Benefit:** Improves scalability, reliability, and operational clarity.

---

### 5.1.2 Event-Driven and Asynchronous Processing

* Transfers are initiated through events (S3, schedules, API calls).
* Components communicate via EventBridge and SQS.
* Processing is decoupled and resilient to spikes.

**Benefit:** Enables elastic scaling and fault isolation.

---

### 5.1.3 Idempotent and Deterministic Execution

* Every transfer job is uniquely identified.
* Idempotency keys ensure retries do not result in duplicate transfers.
* Deterministic execution paths ensure predictable outcomes.

**Benefit:** Safe retries and consistent behavior under failure.

---

### 5.1.4 Stateless Compute with Durable State

* Compute components (Lambda, ECS Fargate) are stateless.
* All state is persisted in durable storage (DynamoDB, S3).
* Failures do not result in state loss.

**Benefit:** Simplifies recovery and scaling.

---

### 5.1.5 Secure by Design

* Security controls are applied at every layer.
* Least privilege is enforced by default.
* No secrets are embedded in code or configuration.

**Benefit:** Aligns with Zero Trust and compliance standards.

---

### 5.1.6 Managed Services First

* Preference for AWS managed services over self-managed infrastructure.
* Reduces operational overhead and patching requirements.

**Benefit:** Improves reliability and reduces total cost of ownership.

---

## 5.2 Assumptions

The architecture is based on the following assumptions:

| ID  | Assumption                                                 |
| --- | ---------------------------------------------------------- |
| A-1 | All deployments occur in AWS GovCloud                      |
| A-2 | External partners support SFTP with SSH key authentication |
| A-3 | Partners may not support push-based delivery               |
| A-4 | File sizes can be as large as 30GB                         |
| A-5 | External endpoints may be intermittently unavailable       |
| A-6 | Network latency and bandwidth vary across partners         |
| A-7 | System IT policies allow managed AWS services              |
| A-8 | Customers accept eventual retry for transient failures     |

---

## 5.3 Constraints

The architecture must operate within the following constraints:

### 5.3.1 Regulatory and Compliance Constraints

* Data must remain within AWS GovCloud regions.
* Encryption must be enforced in transit and at rest.
* Audit logs must be retained per policy.

---

### 5.3.2 Technical Constraints

| Constraint          | Description                                    |
| ------------------- | ---------------------------------------------- |
| Protocol support    | Only SFTP and S3 are supported                 |
| External systems    | External partner behavior cannot be controlled |
| Lambda limits       | Lambda cannot handle large file transfers      |
| Network egress      | External transfers require NAT gateways        |
| Partner concurrency | Partners may impose session limits             |

---

### 5.3.3 Operational Constraints

* Changes during FOMC freeze are restricted.
* No direct SSH or admin access to compute resources.
* Operations must rely on logs, metrics, and runbooks.

---

## 5.4 Key Trade-Offs

### 5.4.1 Reliability vs Simplicity

* Chosen approach uses S3 staging for SFTP→SFTP instead of direct streaming.
* This increases steps but improves retry and DR reliability.

---

### 5.4.2 Cost vs Performance

* Fargate is more expensive than serverless options for small files.
* Fargate is chosen to reliably support large file transfers and external network dependencies.

---

### 5.4.3 Availability vs Duplicate Risk

* True active-active execution was rejected.
* Partitioned Active-Active model chosen to eliminate duplicate transfers.

---

### 5.4.4 Flexibility vs Standardization

* Endpoint configurations are customer-managed.
* Standardized schemas and validations restrict unsupported configurations.

---

## 5.5 Architecture Constraints Summary

| Area              | Constraint             | Impact                       |
| ----------------- | ---------------------- | ---------------------------- |
| External partners | Limited control        | Retry/backoff required       |
| File size         | Up to 30GB             | Streaming required           |
| GovCloud          | Region restrictions    | Limited service availability |
| Security          | No static secrets      | Secrets Manager required     |
| Operations        | No manual intervention | Automation required          |

---

## 5.6 Section Summary

This section outlines the principles, assumptions, constraints, and trade-offs that inform the architectural design. These elements establish clear boundaries and rationale for design decisions presented in subsequent sections.

---



