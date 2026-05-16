# Core Containers & Responsibilities

* **API Layer (API Gateway + Lambda)**
  Provides secure onboarding, operational APIs, and workflow initiation capabilities.

* **AWS Transfer Family (SFTP)**
  Delivers managed and secure external file transfer connectivity.

* **Eventing & Queueing (EventBridge + SQS)**
  Enables asynchronous processing, workload buffering, and traffic spike handling.

* **Workflow Orchestration (Step Functions)**
  Coordinates end-to-end workflows with built-in retries and resiliency controls.

* **Execution Workers (ECS Fargate + Lambda)**
  Executes transfer, validation, and processing workloads using a hybrid compute model.

* **State & Metadata Store (DynamoDB)**
  Maintains workflow state, metadata, checkpointing, and recovery capabilities.

* **Observability (CloudWatch + ELMA + Dynatrace)**
  Provides centralized monitoring, alerting, logging, and operational visibility.

* **Architecture Outcome**
  Delivers a scalable, resilient, and secure event-driven platform designed to support future growth targets up to 10M transfers per day.


# Key Architectural Decisions – Container Layer (C2)

## Eventing & Queueing (EventBridge + SQS)

* Adopted an event-driven architecture using EventBridge for service decoupling and scalable event routing.
* Implemented SQS buffering to absorb traffic spikes and improve workload resiliency.
* Enabled asynchronous processing to isolate ingestion from execution workloads.
* Improves scalability, fault isolation, and operational stability.

---

## Workflow Orchestration (AWS Step Functions)

* AWS Step Functions selected as the centralized orchestration engine.
* Supports retries, branching, exception handling, and workflow coordination.
* Orchestrates execution across Lambda and ECS Fargate workers.
* Simplifies complex workflow management while improving resiliency and recoverability.

---

## Execution Model (Lambda + ECS Fargate)

* Adopted a hybrid compute model aligned to workload characteristics.
* Lambda handles lightweight and short-duration operations.
* ECS Fargate processes large-file and compute-intensive workloads.
* Enables elastic scaling and optimized compute cost utilization.

---

## State & Metadata Management (DynamoDB)

* DynamoDB selected for workflow state, execution metadata, and status tracking.
* Supports idempotency, checkpointing, and resume/restart capabilities.
* Provides low-latency and highly scalable storage for high-throughput workloads.
* Enhances resiliency, auditability, and operational recovery.

---

## Observability & Monitoring

* CloudWatch used for native AWS logging, metrics, and alerting.
* Operational telemetry integrated with ELMA and Dynatrace for enterprise observability.
* Centralized monitoring enables proactive detection, troubleshooting, and operational visibility.

---

## Security & Scalability

* Implemented Zero Trust and defense-in-depth security principles across all layers.
* Services are independently scalable to support future growth targets up to 10M transfers per day.
* Queue-based buffering and orchestration improve resiliency during peak load conditions.
