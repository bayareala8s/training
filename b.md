# Figure 6 – Target State – C4 Component View

The Target State Component View illustrates the core components of the NIS Enterprise File Transfer (EFT) Backend Engine and how they collectively enable a scalable, resilient, secure, and event-driven enterprise file transfer platform. The architecture leverages managed AWS services to support high-volume file transfers, operational resiliency, workflow orchestration, and automated recovery across multiple regions.

## Core Components

* **API Gateway + Lambda**
  Provides the control-plane APIs for onboarding, configuration, and operational management.

* **AWS Transfer Family (SFTP)**
  Serves as the secure managed ingress/egress layer for external file transfers.

* **Amazon S3**
  Acts as the durable storage layer for inbound and outbound files and triggers downstream processing events.

* **Amazon EventBridge**
  Enables centralized event routing and decoupled event-driven processing.

* **Amazon SQS**
  Provides asynchronous buffering, retry handling, workload decoupling, and resiliency.

* **AWS Step Functions**
  Orchestrates end-to-end file transfer workflows, retries, branching, and recovery logic.

* **AWS Lambda & ECS Fargate**
  Deliver hybrid compute processing optimized for both small and large file workloads.

* **Amazon DynamoDB**
  Maintains onboarding metadata, workflow state, transfer tracking, and idempotency records.

* **Recovery Orchestrator & DLQs**
  Support automated recovery, replay handling, operational resiliency, and failure management.

## Key Architectural Decisions

* API Gateway + Lambda used only for control-plane APIs; no data-plane file movement through APIs
* API layer stores onboarding metadata in DynamoDB before workflow initiation
* Amazon S3 acts as the primary ingestion and event trigger layer
* S3 ObjectCreated events routed through EventBridge for centralized event handling
* Amazon SQS introduced between EventBridge and Step Functions for buffering and resiliency
* Asynchronous event-driven processing model adopted to eliminate tight coupling
* AWS Step Functions selected as the central workflow orchestrator
* Conditional workflow branching implemented for small vs large file processing paths
* AWS Lambda used for lightweight/small file processing workloads
* Amazon ECS Fargate used for large file and long-running transfer operations
* Retry handling centralized within Step Functions instead of embedded worker retries
* DynamoDB used as the single source of truth for workflow state and idempotency
* Workflow checkpoints persisted after major processing stages to support recovery
* Recovery model supports resume-from-last-successful-step capability
* Centralized observability enabled using CloudWatch integrated with enterprise monitoring platforms
* Security enforced through least-privilege IAM roles per component
* Data-plane transfers restricted to S3/SFTP paths only; no file payloads traverse API layer

