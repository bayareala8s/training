

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

# 6. High-Level Architecture Overview

This section provides a **top-down view of the system architecture**, introducing the major components, their responsibilities, and how they interact. Detailed component behavior and flow-level walkthroughs are covered in later sections.

---

## 6.1 Architecture Overview

The Self-Serve File Transfer Backend Engine is a **distributed, event-driven system** designed to orchestrate and execute file transfers across SFTP and S3 endpoints in a secure and resilient manner.

The architecture is intentionally divided into two logical planes:

* **Control Plane** – responsible for orchestration, governance, validation, and state management
* **Data Plane** – responsible for the actual movement of file bytes

This separation ensures:

* Independent scaling characteristics
* Clear ownership of responsibilities
* Reduced blast radius during failures
* Improved security posture

---

## 6.2 Control Plane vs Data Plane Separation

### 6.2.1 Control Plane Responsibilities

The Control Plane manages **what should happen** and **when**, but never performs heavy data movement.

**Primary responsibilities:**

* Accept API requests (endpoint onboarding, transfer requests)
* Validate inputs and enforce policy
* Create and persist transfer jobs
* Orchestrate workflows and retries
* Enforce idempotency and lease ownership
* Track job lifecycle and status
* Emit logs, metrics, and audit records

**Key characteristics:**

* Stateless compute
* Durable state stored externally
* Highly available and multi-region
* Optimized for correctness and governance

---

### 6.2.2 Data Plane Responsibilities

The Data Plane performs **how data moves**, focusing on efficiency and reliability for file transfer workloads.

**Primary responsibilities:**

* Establish SFTP connections
* Stream files between endpoints
* Perform multipart uploads for large files
* Enforce atomic delivery patterns
* Handle retries at the transport layer
* Emit transfer-level logs and metrics

**Key characteristics:**

* Network-intensive workloads
* Streaming-based (no full file buffering)
* Horizontally scalable
* Short-lived, ephemeral compute

---

### 6.2.3 Control vs Data Plane Summary

| Aspect         | Control Plane                   | Data Plane        |
| -------------- | ------------------------------- | ----------------- |
| Purpose        | Orchestration & governance      | Byte movement     |
| State          | Durable (DynamoDB, S3 metadata) | Stateless         |
| Scaling        | Event-driven                    | Throughput-driven |
| Failure impact | Job delay                       | Transfer retry    |
| Security       | IAM-centric                     | Network + IAM     |

---

## 6.3 Logical Architecture (Component View)

At a logical level, the system consists of the following layers:

### 6.3.1 Ingress Layer

* API entry point for customers
* Accepts endpoint onboarding, transfer requests, and status queries
* Routes requests to the control plane

---

### 6.3.2 Orchestration Layer

* Creates and manages transfer jobs
* Drives workflow execution
* Applies retries, branching, and error handling
* Coordinates execution across regions

---

### 6.3.3 State and Metadata Layer

* Stores:

  * endpoint configurations
  * job records
  * execution leases
  * deduplication keys
* Serves as the system of record

---

### 6.3.4 Transfer Execution Layer

* Executes file transfers using streaming workers
* Interfaces with SFTP servers and S3
* Handles large files and retries
* Isolated from orchestration logic

---

### 6.3.5 Observability Layer

* Centralized logging
* Metrics and alarms
* Audit trail for compliance and investigations

---

## 6.4 Deployment Architecture (Multi-Region View)

### 6.4.1 Regional Deployment Model

The platform is deployed identically in:

* **us-gov-west-1**
* **us-gov-east-1**

Each region includes:

* Full control plane stack
* Full data plane capability
* Independent networking and egress paths
* Independent monitoring and alarms

---

### 6.4.2 Active-Active Behavior

* Both regions accept inbound requests
* Both regions can execute transfers
* Only one region executes a given partition at a time
* Ownership is enforced using a lease-based mechanism

**Result:**

* High availability without duplicate processing
* Predictable failover behavior
* No “cold standby” region

---

## 6.5 High-Level Textual Architecture Diagram

```
                +--------------------+
                |      Clients       |
                | (Customers / Apps) |
                +----------+---------+
                           |
                           v
                    +-------------+
                    | API Gateway |
                    +------+------+
                           |
                           v
              +----------------------------+
              |        Control Plane       |
              |----------------------------|
              | Lambda (Validation)        |
              | Step Functions (Workflow)  |
              | EventBridge / SQS          |
              | DynamoDB (Jobs, Endpoints) |
              +-------------+--------------+
                            |
                            | (Task Launch)
                            v
              +----------------------------+
              |         Data Plane         |
              |----------------------------|
              | ECS Fargate Transfer Tasks |
              | SFTP Clients               |
              | Multipart S3 Uploads       |
              +-------------+--------------+
                            |
          +-----------------+------------------+
          |                                    |
          v                                    v
   +-------------+                     +--------------+
   |   S3 Buckets |                     | SFTP Servers |
   | (Raw/Staging)|                     | (Internal /  |
   +-------------+                     |  External)   |
                                        +--------------+
```

---

## 6.6 High-Level Data Flow Summary

1. Customer submits endpoint or transfer request
2. Control plane validates and creates a transfer job
3. Workflow orchestration determines execution path
4. Data plane worker streams data between endpoints
5. Job status is updated and exposed via API
6. Logs and metrics are captured throughout execution

---

## 6.7 Key Design Outcomes

This high-level architecture:

* Cleanly separates concerns
* Scales independently for orchestration vs data movement
* Supports large file transfers reliably
* Enables Active-Active multi-region deployment
* Aligns with security, resiliency, and operational standards

---

## 6.8 Section Summary

This section provides a top-level view of the system architecture, highlighting the separation of control and data planes, the logical layering of components, and the multi-region deployment model. Detailed component behavior, job lifecycle management, and flow-specific logic are covered in subsequent sections.

---



# 7. Detailed Architecture Design

This section provides a **component-level deep dive** into the architecture, describing how each major service participates in the system and how responsibilities are clearly divided between the **Control Plane** and the **Data Plane**.

---

## 7.1 Control Plane Architecture

The Control Plane is responsible for **governance, orchestration, validation, correctness, and state management**.
It does **not** perform any heavy file movement.

---

### 7.1.1 API Gateway

**Purpose**
API Gateway serves as the **single ingress point** for all customer and system interactions.

**Responsibilities**

* Expose REST APIs for:

  * Endpoint onboarding (`POST /endpoints`)
  * Transfer initiation (`POST /transfers`)
  * Schedule creation (`POST /schedules`)
  * Status queries (`GET /jobs/{jobId}`)
* Enforce authentication and authorization
* Apply request validation and throttling
* Provide consistent error handling

**Design Decisions**

* API Gateway is used instead of direct Lambda invocation to:

  * centralize auth
  * enforce rate limits
  * provide auditability
* Payload size limits enforced to prevent misuse
* No file data is ever sent through APIs

**Failure Behavior**

* If API Gateway is unavailable in one region, Route53 routes traffic to the other region
* Requests are idempotent and safe to retry

---

### 7.1.2 AWS Lambda (Control Plane Functions)

**Purpose**
Lambda functions implement **control logic**, not data transfer.

**Key Lambda Roles**

* Endpoint validation and registration
* Transfer job creation
* Schedule processing
* Status and metadata retrieval
* Helper functions (policy evaluation, endpoint resolution)

**Responsibilities**

* Validate request schemas
* Enforce customer ownership and isolation
* Generate job IDs and idempotency keys
* Persist state in DynamoDB
* Publish events to EventBridge/SQS

**Design Decisions**

* Lambdas are stateless
* No secrets stored in environment variables
* No file content processed in Lambda

**Failure Behavior**

* Transient failures retried automatically
* Errors surfaced to caller with correlation IDs

---

### 7.1.3 AWS Step Functions (Workflow Orchestration)

**Purpose**
Step Functions orchestrate **end-to-end transfer workflows**.

**Responsibilities**

* Drive job lifecycle:

  * RECEIVED
  * QUEUED
  * RUNNING
  * VERIFYING
  * SUCCEEDED / FAILED
* Acquire and renew execution leases
* Determine execution paths by flow type
* Handle retries and compensating actions
* Launch ECS Fargate tasks for data plane execution

**Design Decisions**

* One primary state machine with flow-specific branches
* Explicit retry and backoff policies
* Timeouts defined per workflow stage
* Map states used only when concurrency is explicitly controlled

**Failure Behavior**

* Failed states transition jobs to FAILED with reason codes
* Execution can be re-driven safely using idempotency keys

---

### 7.1.4 Amazon SQS

**Purpose**
SQS provides **buffering and decoupling** between job creation and execution.

**Responsibilities**

* Absorb traffic spikes
* Prevent overload of downstream components
* Enable asynchronous execution

**Design Decisions**

* Separate queues by workflow category where necessary
* DLQs configured for poison messages
* Visibility timeout aligned to processing start latency

**Failure Behavior**

* Messages retried automatically
* DLQ alerts trigger operator investigation

---

### 7.1.5 Amazon EventBridge

**Purpose**
EventBridge routes **events and schedules** into the system.

**Responsibilities**

* Receive S3 ObjectCreated events
* Trigger scheduled polling jobs
* Fan-out events to SQS or Step Functions
* Provide loose coupling between producers and consumers

**Design Decisions**

* Event-driven model preferred over polling where possible
* Rules scoped by event source and detail type

**Failure Behavior**

* Events retried by AWS
* Missed events mitigated via idempotent job creation

---

### 7.1.6 Amazon DynamoDB (State and Metadata)

**Purpose**
DynamoDB serves as the **system of record**.

**Data Stored**

* Endpoint configurations
* Transfer jobs
* Lease/lock records
* Deduplication keys

**Design Decisions**

* Strongly consistent reads for lease acquisition
* Global Tables used for multi-region availability
* Partition keys designed to avoid hot partitions

**Failure Behavior**

* Built-in multi-AZ resilience
* Retry logic handles throttling
* PITR enabled for recovery

---

## 7.2 Data Plane Architecture

The Data Plane is responsible for **efficient, reliable movement of file bytes**.

---

### 7.2.1 Amazon S3

**Purpose**
S3 provides durable storage for:

* Raw inbound files
* Staging for SFTP→SFTP transfers
* Outbound delivery sources

**Responsibilities**

* Persist file data durably
* Trigger events on object creation
* Serve as a DR checkpoint

**Design Decisions**

* Server-side copy for S3→S3 flows
* Multipart uploads for large files
* Cross-Region Replication for DR
* Lifecycle policies for cost control

**Failure Behavior**

* High durability and availability
* Replication lag monitored

---

### 7.2.2 AWS Transfer Family (SFTP)

**Purpose**
Provides a **managed SFTP endpoint** for inbound partner uploads.

**Responsibilities**

* Authenticate partners using SSH keys
* Write uploaded files directly to S3
* Emit audit logs

**Design Decisions**

* No self-managed SFTP servers
* Centralized inbound SFTP reduces operational burden
* Used primarily for inbound (push) scenarios

**Failure Behavior**

* AWS-managed HA
* Partner retries if service unavailable

---

### 7.2.3 Amazon ECS Fargate (Transfer Workers)

**Purpose**
ECS Fargate executes **streaming transfer workers** for SFTP-based flows.

**Responsibilities**

* Establish SFTP connections
* Stream data between endpoints
* Perform multipart uploads/downloads
* Enforce atomic delivery (`.tmp → rename`)
* Emit detailed transfer logs and metrics

**Design Decisions**

* Task-per-job execution model
* CPU/memory sized dynamically based on file size
* No persistent storage required
* No inbound network access

**Failure Behavior**

* Task failures retried by orchestration
* Partial transfers safely retried due to idempotency

---

### 7.2.4 Network Architecture (VPC, NAT, Egress)

**Purpose**
Provide secure and controlled network access for data plane tasks.

**Design Decisions**

* Private subnets only
* No public IPs for compute
* NAT Gateways provide controlled egress
* Static egress IPs allow partner allowlisting
* Security Groups deny-by-default

**Failure Behavior**

* NAT failures mitigated via AZ redundancy
* Concurrency limits prevent saturation

---

## 7.3 Control Plane vs Data Plane Interaction

### Execution Flow Summary

1. Control Plane validates and creates job
2. Step Functions acquire lease
3. Control Plane launches Data Plane task
4. Data Plane streams data
5. Data Plane reports result
6. Control Plane updates job state

---

## 7.4 Detailed Design Outcomes

This architecture:

* Prevents duplicate transfers
* Supports large files reliably
* Is resilient to partial and full failures
* Separates concerns cleanly
* Scales independently for orchestration and throughput

---

## 7.5 Section Summary

This section detailed the internal architecture of both the control plane and data plane components, explaining how each AWS service contributes to reliability, scalability, and operational clarity. Subsequent sections build on this foundation to describe job lifecycle, flows, resiliency, security, and operations.

---




# 8. Transfer Job and Endpoint Model

This section describes how **transfer jobs** and **endpoint configurations** are modeled, stored, and managed within the platform. These models form the **core system of record** and enable idempotent execution, auditability, and safe multi-region operation.

---

## 8.1 Transfer Job Definition

A **Transfer Job** represents a single, logical unit of work to move one or more files from a **source endpoint** to a **target endpoint** under a defined policy.

Each transfer job is:

* Immutable once created (state transitions only)
* Identifiable by a unique job ID
* Traceable across logs, metrics, and audit records
* Executed exactly once (per idempotency key)

---

## 8.2 Transfer Job Lifecycle

### 8.2.1 Job States

The following lifecycle states are supported:

| State     | Description                        |
| --------- | ---------------------------------- |
| RECEIVED  | Job has been created and persisted |
| QUEUED    | Job is awaiting execution          |
| RUNNING   | Job execution in progress          |
| VERIFYING | Post-transfer verification         |
| SUCCEEDED | Transfer completed successfully    |
| FAILED    | Transfer failed permanently        |
| CANCELLED | Job cancelled prior to execution   |

State transitions are **explicit, auditable, and monotonic** (no backward transitions).

---

### 8.2.2 Job Lifecycle Guarantees

* A job is persisted **before execution**
* State transitions are recorded in DynamoDB
* Partial failures result in retry or FAILED state
* Jobs are never deleted automatically
* Re-drives create a **new job** referencing the original job

---

## 8.3 Job Creation and Ownership

### 8.3.1 Job Creation Triggers

Transfer jobs can be created by:

* Customer API calls (on-demand)
* Scheduled triggers (polling)
* Event-driven triggers (S3 ObjectCreated)

In all cases, job creation is handled by a **dedicated control-plane function**.

---

### 8.3.2 Job Ownership and Partitioning

To support Active-Active execution without duplication, each job is assigned a **partition identifier**:

```
partition_id = customer_id + source_endpoint_id + target_endpoint_id
```

Only one region may execute jobs for a given partition at a time, enforced through a **lease mechanism**.

---

## 8.4 Idempotency and De-duplication

### 8.4.1 Idempotency Key

Each job is associated with an **idempotency key** computed from deterministic inputs such as:

* Source endpoint
* Target endpoint
* File path or object key
* File metadata (size, timestamp, version)

This ensures:

* Event replay does not create duplicate jobs
* API retries are safe
* Failover does not cause duplicate execution

---

### 8.4.2 Deduplication Behavior

* Job creation uses **conditional writes** in DynamoDB
* Duplicate idempotency keys are rejected or mapped to existing jobs
* Execution retries reference the same job record

---

## 8.5 Lease and Lock Management

### 8.5.1 Lease Purpose

Leases prevent:

* Concurrent execution of the same job
* Dual-region execution during failover
* Race conditions under retry scenarios

---

### 8.5.2 Lease Behavior

* Lease records stored in DynamoDB
* Leases include:

  * owning region
  * expiration timestamp
  * heartbeat timestamp
* Long-running jobs renew leases periodically
* Lease expiration allows safe takeover

---

## 8.6 Transfer Job Data Model (Logical)

A transfer job record contains the following logical attributes:

* job_id
* customer_id
* flow_type
* source_endpoint_id
* target_endpoint_id
* policy_id
* partition_id
* idempotency_key
* status
* retry_count
* error_code / error_message
* timestamps (created, started, completed)
* execution_region

The job record does **not** contain:

* Credentials
* Secrets
* File content

---

## 8.7 Endpoint Configuration Model

### 8.7.1 Endpoint Definition

An **Endpoint** describes a reusable connection configuration to a source or target system.

Endpoints are:

* Created and managed by customers
* Long-lived and reusable
* Referenced by ID in transfer jobs

---

### 8.7.2 Supported Endpoint Types

| Endpoint Type        | Description               |
| -------------------- | ------------------------- |
| S3                   | Amazon S3 bucket + prefix |
| Transfer Family SFTP | Managed inbound SFTP      |
| External SFTP        | Partner-hosted SFTP       |

---

### 8.7.3 Endpoint Attributes (Logical)

| Attribute        | Description               |
| ---------------- | ------------------------- |
| endpoint_id      | Unique identifier         |
| endpoint_type    | SFTP or S3                |
| direction        | INBOUND / OUTBOUND / BOTH |
| host / bucket    | Remote host or S3 bucket  |
| path / prefix    | Base directory or prefix  |
| auth_type        | SSH key (SFTP)            |
| secret_ref       | Secrets Manager ARN       |
| preferred_region | Optional execution hint   |
| max_concurrency  | Partner protection        |
| status           | ACTIVE / DISABLED         |

---

## 8.8 Secrets Management Strategy

### 8.8.1 Secrets Handling

* Secrets are stored **only** in AWS Secrets Manager
* Endpoint records store only a reference (ARN)
* Secrets include:

  * private SSH keys
  * passwords (if required)
* Secrets are never logged or returned via APIs

---

### 8.8.2 Access Control

* ECS tasks and Lambdas have scoped IAM permissions
* Only authorized components can retrieve secrets
* Secrets rotation supported without job recreation

---

## 8.9 Endpoint Lifecycle Management

### 8.9.1 Endpoint Creation

* Customer submits endpoint via POST API
* Validation and connectivity checks performed
* Endpoint stored as ACTIVE

### 8.9.2 Endpoint Update

* Endpoint can be updated without affecting existing jobs
* Future jobs reference updated configuration

### 8.9.3 Endpoint Deactivation

* Endpoint can be DISABLED
* New jobs are rejected
* Existing jobs complete or fail gracefully

---

## 8.10 Auditability and Traceability

Every job and endpoint change is:

* Logged with timestamp and actor
* Traceable via job_id and endpoint_id
* Retained per audit policy

This enables:

* Compliance reviews
* Incident investigation
* Historical reporting

---

## 8.11 Section Summary

This section defines the core **job and endpoint models** that underpin the system’s reliability and correctness. By separating configuration from execution, enforcing idempotency, and using lease-based ownership, the platform ensures safe, auditable, and deterministic file transfers across regions and failure scenarios.

---




