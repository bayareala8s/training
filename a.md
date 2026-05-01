

# **Key Architectural Decisions – Target State System Context**

## **1. System Role & Responsibility**

| Decision ID | Area              | Decision                                                                                | Rationale                                                                               | Impact                                                          |
| ----------- | ----------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| AD-01       | Core Architecture | NIS EFT Backend is the **central orchestration engine** for all file transfer workflows | Ensures single control point for workflow execution, retry handling, and state tracking | Simplifies coordination, improves consistency and observability |
| AD-02       | System Boundaries | Source and Target systems remain **external systems**                                   | Maintains loose coupling and avoids tight integration dependencies                      | Improves scalability and onboarding flexibility                 |
| AD-03       | Observability     | ELMA and Dynatrace act as **external observability platforms**                          | Leverages enterprise-standard monitoring tools instead of custom solutions              | Enables centralized monitoring and operational visibility       |
| AD-04       | DevOps            | GitLab is used for **CI/CD and deployment automation**                                  | Aligns with enterprise DevOps standards                                                 | Ensures consistent, automated deployments                       |

---

## **2. Integration & Interaction Model**

| Decision ID | Interaction             | Protocol                | Direction     | Decision                                            | Rationale                                                  |
| ----------- | ----------------------- | ----------------------- | ------------- | --------------------------------------------------- | ---------------------------------------------------------- |
| AD-05       | Source → Backend        | SFTP / HTTPS (S3 PUT)   | Inbound       | Support both file-based and object-based ingestion  | Enables compatibility with legacy and cloud-native systems |
| AD-06       | Backend → Target        | SFTP / HTTPS (S3 PUT)   | Outbound      | Preserve protocol based on target system capability | Avoids forcing protocol changes on downstream systems      |
| AD-07       | Portal → Backend        | API / HTTPS             | Control Plane | Use API-based interaction only                      | Decouples onboarding/control from file transfer execution  |
| AD-08       | Backend → Observability | Logs / Metrics / Events | Outbound      | Centralized telemetry forwarding                    | Enables unified monitoring and alerting                    |

---

## **3. Control Plane vs Data Plane Separation**

| Decision ID | Area                 | Decision                                                          | Rationale                                                            | Impact                                       |
| ----------- | -------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------- |
| AD-09       | Architecture Pattern | Separate **Control Plane** and **Data Plane**                     | Prevents orchestration logic from impacting data transfer throughput | Improves scalability and fault isolation     |
| AD-10       | Control Plane        | API + Step Functions used for orchestration and state transitions | Enables event-driven workflow execution                              | Supports high concurrency and resiliency     |
| AD-11       | Data Plane           | SFTP and S3 used for actual file movement                         | Optimized for large data transfer workloads                          | Ensures efficient and scalable data movement |

---

## **4. Protocol Strategy**

| Decision ID | Protocol    | Decision                                        | Rationale                                    | Impact                         |
| ----------- | ----------- | ----------------------------------------------- | -------------------------------------------- | ------------------------------ |
| AD-12       | SFTP        | Retained as a supported protocol                | Required for legacy and partner integrations | Ensures backward compatibility |
| AD-13       | S3 (HTTPS)  | Preferred for cloud-native transfers            | Provides higher scalability and performance  | Reduces operational overhead   |
| AD-14       | API (HTTPS) | Used for control and onboarding operations only | Separates control from data movement         | Improves system modularity     |

---

## **5. Observability & Monitoring**

| Decision ID | Area     | Decision                             | Metrics / Signals                            | Rationale                                  |
| ----------- | -------- | ------------------------------------ | -------------------------------------------- | ------------------------------------------ |
| AD-15       | Metrics  | Centralized monitoring via Dynatrace | Throughput, latency, error rate, concurrency | Enables performance visibility             |
| AD-16       | Logging  | Logs forwarded to ELMA               | Execution logs, failures, audit events       | Supports troubleshooting and auditability  |
| AD-17       | Alerting | Threshold-based alerting configured  | Queue depth, failures, latency spikes        | Enables proactive issue detection          |
| AD-18       | Tracing  | End-to-end workflow visibility       | Step execution states, retries               | Improves debugging and root cause analysis |

---

## **6. Deployment & Change Management**

| Decision ID | Area           | Decision                                 | Rationale                             | Impact                |
| ----------- | -------------- | ---------------------------------------- | ------------------------------------- | --------------------- |
| AD-19       | CI/CD          | GitLab pipelines used for deployment     | Standardized deployment process       | Reduces manual errors |
| AD-20       | Infrastructure | Infrastructure as Code (IaC) approach    | Ensures repeatability and consistency | Improves reliability  |
| AD-21       | Versioning     | Source-controlled configuration and code | Enables rollback and traceability     | Enhances governance   |

---

## **7. Scalability & Throughput Strategy (Optional but Strong for ARC)**

| Decision ID | Area              | Decision                                      | Rationale                           | Impact                               |
| ----------- | ----------------- | --------------------------------------------- | ----------------------------------- | ------------------------------------ |
| AD-22       | Scaling Model     | Horizontal scaling is primary approach        | Supports high concurrency workloads | Enables scaling to 10M transfers/day |
| AD-23       | Workload Handling | Parallel execution of workflows               | Improves throughput                 | Reduces processing latency           |
| AD-24       | Burst Handling    | System designed to absorb peak loads (2x TPS) | Ensures resilience during spikes    | Prevents service degradation         |

---

# ✅ Why This Will Pass Review

This version:

✔ Directly answers **“What are the key decisions?”**
✔ Removes all unnecessary narrative
✔ Uses **tables (explicit reviewer ask)**
✔ Separates concerns clearly (control, data, scaling, monitoring)
✔ Aligns with **IDD expectations**



# **Key Architectural Decisions – Container Layer (C2)**

## **1. API Layer (API Gateway + Lambda)**

| Decision ID | Container | Decision                                                                                 | Rationale                                                             | Impact                                                                 |
| ----------- | --------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| AD-C2-01    | API Layer | Use **Amazon API Gateway + Lambda** for all control-plane APIs                           | Serverless model enables scalability and reduces operational overhead | Supports burst onboarding and status queries without capacity planning |
| AD-C2-02    | API Layer | API layer handles **authentication, validation, and request orchestration trigger only** | Keeps API lightweight and stateless                                   | Improves performance and separation of concerns                        |
| AD-C2-03    | API Layer | API triggers **asynchronous workflows via EventBridge / Step Functions**                 | Avoids synchronous blocking operations                                | Improves system responsiveness and resiliency                          |

---

## **2. File Transfer Gateway (AWS Transfer Family)**

| Decision ID | Container      | Decision                                                     | Rationale                                     | Impact                                           |
| ----------- | -------------- | ------------------------------------------------------------ | --------------------------------------------- | ------------------------------------------------ |
| AD-C2-04    | Transfer Layer | Use **AWS Transfer Family (SFTP)** as managed ingress/egress | Eliminates need to manage SFTP infrastructure | Improves security and reduces operational burden |
| AD-C2-05    | Transfer Layer | Integrate Transfer Family with **S3 as backend storage**     | Decouples file ingestion from processing      | Enables event-driven architecture                |
| AD-C2-06    | Transfer Layer | Support both **SFTP and S3 PUT (HTTPS)** ingestion paths     | Supports legacy and modern clients            | Increases adoption flexibility                   |

---

## **3. Eventing & Queueing (EventBridge + SQS)**

| Decision ID | Container        | Decision                                 | Rationale                                             | Impact                                   |
| ----------- | ---------------- | ---------------------------------------- | ----------------------------------------------------- | ---------------------------------------- |
| AD-C2-07    | Eventing Layer   | Use **EventBridge for event routing**    | Enables event-driven integration across services      | Improves extensibility                   |
| AD-C2-08    | Queue Layer      | Use **SQS for buffering and decoupling** | Handles traffic spikes and prevents overload          | Improves reliability and fault isolation |
| AD-C2-09    | Processing Model | Adopt **asynchronous processing model**  | Avoids tight coupling between ingestion and execution | Enhances scalability                     |

---

## **4. Workflow Orchestration (Step Functions)**

| Decision ID | Container      | Decision                                                         | Rationale                                          | Impact                               |
| ----------- | -------------- | ---------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------ |
| AD-C2-10    | Orchestrator   | Use **AWS Step Functions as central workflow engine**            | Provides native state management and orchestration | Simplifies complex workflow handling |
| AD-C2-11    | Workflow Model | Implement **stateful orchestration with retries and branching**  | Handles failures gracefully                        | Improves resiliency                  |
| AD-C2-12    | Coordination   | Step Functions coordinates across **Lambda and Fargate workers** | Enables hybrid execution model                     | Optimizes cost and performance       |

---

## **5. Execution Layer (Lambda + ECS Fargate)**

| Decision ID | Container       | Decision                                             | Rationale                                        | Impact                         |
| ----------- | --------------- | ---------------------------------------------------- | ------------------------------------------------ | ------------------------------ |
| AD-C2-13    | Execution       | Use **Lambda for lightweight tasks**                 | Fast startup and cost-efficient for small jobs   | Reduces compute cost           |
| AD-C2-14    | Execution       | Use **ECS Fargate for large file processing**        | Supports long-running and high-memory workloads  | Enables large file handling    |
| AD-C2-15    | Execution Model | Adopt **hybrid compute strategy (Lambda + Fargate)** | Matches workload characteristics to compute type | Optimizes scalability and cost |
| AD-C2-16    | Retry Handling  | Execution layer handles **idempotent retries**       | Prevents duplicate processing                    | Ensures data consistency       |

---

## **6. State & Metadata Store (DynamoDB)**

| Decision ID | Container   | Decision                                                | Rationale                                 | Impact                             |
| ----------- | ----------- | ------------------------------------------------------- | ----------------------------------------- | ---------------------------------- |
| AD-C2-17    | State Store | Use **DynamoDB for workflow state and metadata**        | Provides low-latency and scalable storage | Supports high throughput workloads |
| AD-C2-18    | Data Model  | Store **job status, execution state, and metadata**     | Enables tracking and observability        | Supports audit and reporting       |
| AD-C2-19    | Reliability | Implement **idempotency and checkpointing**             | Ensures safe retries and recovery         | Improves resiliency                |
| AD-C2-20    | Recovery    | Enable **resume/restart capability** using stored state | Prevents full reprocessing on failure     | Reduces operational impact         |

---

## **7. Observability (CloudWatch + ELMA + Dynatrace)**

| Decision ID | Container                | Decision                                                    | Rationale                                      | Impact                       |
| ----------- | ------------------------ | ----------------------------------------------------------- | ---------------------------------------------- | ---------------------------- |
| AD-C2-21    | Logging                  | Use **CloudWatch for native logging and metrics**           | AWS-native integration                         | Enables real-time monitoring |
| AD-C2-22    | Enterprise Observability | Forward telemetry to **ELMA and Dynatrace**                 | Aligns with enterprise observability standards | Centralized monitoring       |
| AD-C2-23    | Monitoring Model         | Capture **logs, metrics, and events across all containers** | Enables full visibility                        | Improves troubleshooting     |

---

## **8. Architectural Pattern Decisions (CRITICAL for ARC)**

| Decision ID | Area                 | Decision                                                    | Rationale                                     | Impact                           |
| ----------- | -------------------- | ----------------------------------------------------------- | --------------------------------------------- | -------------------------------- |
| AD-C2-24    | Architecture Pattern | Adopt **event-driven architecture**                         | Decouples components and improves scalability | Enables independent scaling      |
| AD-C2-25    | System Design        | Use **loosely coupled containerized services**              | Reduces interdependencies                     | Improves maintainability         |
| AD-C2-26    | Processing Model     | Separate **ingestion, orchestration, and execution layers** | Enforces clear boundaries                     | Improves reliability and scaling |
| AD-C2-27    | Failure Handling     | Design for **graceful failure and retry at each layer**     | Prevents cascading failures                   | Improves system stability        |


Good — now I can see exactly why Alfonso pushed back.

You’re still describing **what components do**
…but ARC wants **what decisions you made and why at THIS layer (C3)**.

Let me fix this properly so you can drop it directly into your IDD.

---

# ✅ **Key Architectural Decisions – Component Level (C3)**

*(Aligned to your Component Diagram — API, S3, EventBridge, SQS, Step Functions, Fargate, Lambda, DynamoDB)*

👉 Add this section **right after your Component Diagram**

---

## **Key Architectural Decisions (Component Layer)**

| Decision ID | Component            | Decision                                                                                          | Rationale                                   | Trade-off / Impact                               |
| ----------- | -------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------ |
| AD-C3-01    | API Gateway + Lambda | Use **API Gateway + Lambda for control-plane APIs only (no data-plane transfer)**                 | Separates control-plane from data-plane     | Prevents API bottleneck for large file transfers |
| AD-C3-02    | API Layer            | API writes **initial request + metadata to DynamoDB before triggering workflow**                  | Ensures traceability and idempotency        | Slight write latency but enables recovery        |
| AD-C3-03    | S3 (Customer Bucket) | Use **S3 as primary ingestion trigger (event source)** instead of direct API-triggered processing | Enables event-driven architecture           | Requires event consistency handling              |
| AD-C3-04    | S3 Events            | Use **S3 ObjectCreated events → EventBridge**                                                     | Decouples ingestion from processing         | Adds slight event propagation latency            |
| AD-C3-05    | EventBridge          | Use **EventBridge for routing events across workflows**                                           | Centralized event routing and extensibility | Additional service hop                           |
| AD-C3-06    | SQS                  | Introduce **SQS between EventBridge and Step Functions**                                          | Provides buffering and backpressure control | Adds queue management complexity                 |
| AD-C3-07    | Processing Model     | Use **asynchronous processing (no direct sync coupling)**                                         | Improves scalability and fault isolation    | Requires state tracking                          |
| AD-C3-08    | Step Functions       | Use **Step Functions as central orchestrator (not Lambda chaining)**                              | Native retry, state, branching              | Slightly higher cost vs pure Lambda              |
| AD-C3-09    | Workflow Logic       | Implement **conditional branching (large vs small file path)**                                    | Optimizes compute selection                 | Adds workflow complexity                         |
| AD-C3-10    | Execution Strategy   | Use **Lambda for small files and Fargate for large files**                                        | Right-sized compute for workload            | Requires routing logic                           |
| AD-C3-11    | Fargate              | Use **Fargate for long-running / large file transfers**                                           | Avoids Lambda timeout limitations           | Higher cost per execution                        |
| AD-C3-12    | Lambda Workers       | Use **Lambda for lightweight processing tasks**                                                   | Fast, cost-efficient execution              | Limited runtime and memory                       |
| AD-C3-13    | Retry Strategy       | Implement **retry at Step Functions level, not inside workers**                                   | Centralized failure handling                | Requires idempotent workers                      |
| AD-C3-14    | Idempotency          | Store **idempotency keys in DynamoDB**                                                            | Prevents duplicate processing               | Additional storage + logic                       |
| AD-C3-15    | State Store          | Use **DynamoDB as single source of truth for workflow state**                                     | Low latency and scalable                    | Eventual consistency considerations              |
| AD-C3-16    | Checkpointing        | Persist **workflow checkpoints after each major step**                                            | Enables resume/restart                      | Additional writes                                |
| AD-C3-17    | Failure Recovery     | Enable **resume from last successful step (not full restart)**                                    | Reduces reprocessing cost                   | Requires state orchestration                     |
| AD-C3-18    | Observability        | Emit **logs/metrics from all components to CloudWatch + forward to ELMA/Dynatrace**               | Centralized observability                   | Integration overhead                             |
| AD-C3-19    | Security             | Use **IAM roles per component (least privilege)**                                                 | Limits blast radius                         | More IAM management                              |
| AD-C3-20    | Data Flow            | Enforce **data never flows through API layer (only via S3/SFTP)**                                 | Improves performance and security           | Requires client integration alignment            |

---

# 🔥 This fixes ALL reviewer comments

### 1. Alfonso’s comment:

> “What are the Key Architectural Decisions for this level?”

✅ Now you are answering at:

* API behavior decisions
* Event routing decisions
* Workflow orchestration decisions
* Compute selection decisions
* State management decisions

👉 This is exactly **C3-level thinking**

---

### 2. Tooraj’s comment:

> “Remove unnecessary writing”

✅ This table:

* Removes fluff
* Is crisp
* Directly maps to diagram

---

### 3. Indentation issue:

> “Mixed levels of indentation is confusing”

👉 Replace ALL this:

* Nested bullets
* “Responsibilities under responsibilities”

👉 With:

* Clean table (above)
* OR single-level bullets only

---

# ⚠️ One IMPORTANT gap (Alfonso will ask next)

He already hinted:

> “Management? What kind of management operations will be performed?”

👉 You should ALSO add:

---

## **Operational / Management Decisions (SHORT TABLE)**

| Area         | Decision                                                             |
| ------------ | -------------------------------------------------------------------- |
| Monitoring   | CloudWatch + ELMA + Dynatrace for metrics, logs, alerts              |
| Retry Ops    | Step Functions manages retries centrally                             |
| Reprocessing | Failed jobs can be replayed using stored state in DynamoDB           |
| Deployment   | GitLab CI/CD pipelines automate infra + app deployment               |
| Scaling      | Serverless auto-scaling (Lambda, SQS, EventBridge) + Fargate scaling |
| Alerting     | SNS-based alerts for failures and SLA breaches                       |

