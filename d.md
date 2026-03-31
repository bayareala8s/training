Here is a **SADD-ready explanation** of the **Current State – System Context View (C4 Level 1)** in a clear, principal-architect tone:

---

# 📄 **Current State – System Context View Explanation**

The Current State System Context View provides a high-level representation of the NIS EFT Backend within the broader enterprise ecosystem, illustrating its interactions with external systems, users, and supporting platforms. This view focuses on system boundaries and key data exchange interfaces rather than internal implementation details.

At the core of the architecture is the **NIS EFT Backend**, which functions as the central orchestration and processing engine for file transfer operations. It facilitates secure and reliable data movement between source systems and target systems using multiple protocols and integration patterns.

---

## 🔹 **Core System**

* **NIS EFT Backend (Software System)**
  The NIS EFT Backend acts as the central platform responsible for:

  * Orchestrating file transfer workflows
  * Managing data movement between systems
  * Handling protocol translation (SFTP, S3, HTTPS)
  * Ensuring reliability, retry handling, and processing logic

It serves as the **core engine of the platform**, coordinating all inbound and outbound data flows.

---

## 🔹 **External Systems and Interactions**

### 1. **Source Systems**

Source systems represent upstream applications or partner systems that initiate file transfers.

**Supported interactions include:**

* **PUT (SFTP)** → Upload files via SFTP
* **S3 PUT (HTTPS)** → Upload files directly to S3 using HTTPS
* **GET (SFTP)** → Retrieve files from the backend

These systems act as **data producers and consumers**, depending on the workflow.

---

### 2. **Target Systems**

Target systems are downstream systems that receive processed or transferred files.

**Supported interactions include:**

* **PUT (SFTP)** → Deliver files via SFTP
* **S3 PUT (HTTPS)** → Deliver files into S3 buckets

The NIS EFT Backend ensures reliable delivery, including retry and failure handling mechanisms.

---

### 3. **ELMA (Observability System)**

ELMA provides centralized monitoring, logging, and observability capabilities.

**Role:**

* Collects metrics, logs, and events from the backend
* Enables operational visibility and troubleshooting
* Supports alerting and system health monitoring

This ensures the platform maintains **operational excellence and transparency**.

---

### 4. **GitLab (CI/CD Platform)**

GitLab is used for DevOps and deployment automation.

**Role:**

* Hosts source code repositories
* Executes CI/CD pipelines
* Manages build, test, and deployment workflows

This enables **consistent, automated, and controlled deployments** of the backend system.

---

## 🔹 **Data Flow Overview**

The system supports **bi-directional data movement**:

* **Inbound Flow:**
  Source Systems → NIS EFT Backend
  (via SFTP, S3, HTTPS)

* **Outbound Flow:**
  NIS EFT Backend → Target Systems
  (via SFTP, S3)

* **Observability Flow:**
  NIS EFT Backend → ELMA
  (logs, metrics, events)

* **Deployment Flow:**
  GitLab → NIS EFT Backend
  (CI/CD pipeline deployments)

---

## 🔹 **Key Characteristics of Current State**

| Characteristic         | Description                                         |
| ---------------------- | --------------------------------------------------- |
| Centralized Processing | NIS EFT Backend acts as single orchestration engine |
| Protocol Flexibility   | Supports SFTP, S3, and HTTPS                        |
| Decoupled Integrations | Source and target systems are loosely coupled       |
| Observability Enabled  | Integrated with ELMA for monitoring                 |
| CI/CD Automation       | GitLab enables automated deployments                |
| Enterprise Integration | Designed for multiple internal and external systems |

---

## 🔹 **Architectural Observations (Current State)**

* The architecture is **hub-and-spoke**, with the backend as the central hub
* Supports **multiple integration patterns**, increasing flexibility
* Relies on **external observability system (ELMA)** for monitoring
* CI/CD is **externally managed via GitLab pipelines**
* System boundaries are clearly defined between producers, consumers, and processing engine

Here is a **SADD-ready explanation** of the **Current State – C4 Container View**, written in a **clear, principal-architect tone**:

---

# 📄 **Current State – Container View Explanation (C4 Level 2)**

The Current State Container View provides a detailed representation of the internal structure of the NIS EFT Backend, breaking down the system into key containers (logical building blocks) and illustrating how they interact to support end-to-end file transfer workflows.

This view highlights the runtime components, supporting services, and integration points that collectively enable secure, scalable, and observable file transfer operations.

---

## 🔹 **System Boundary**

The **NIS EFT Backend Services** define the system boundary and encapsulate all core processing components. Within this boundary, multiple containers collaborate to manage file ingestion, processing, orchestration, monitoring, and notification.

---

## 🔹 **Core Containers and Responsibilities**

### 1. **AWS Transfer Family (SFTP)**

* **Type:** Managed container (AWS service)
* **Role:**

  * Provides secure SFTP endpoints for file ingestion and delivery
  * Acts as the entry and exit point for file transfers
* **Capabilities:**

  * Supports inbound (PUT/GET via SFTP)
  * Integrates with S3 for storage-backed transfers

👉 This component serves as the **secure file gateway** for the platform.

---

### 2. **Execution Workers (Lambda)**

* **Type:** Serverless compute container
* **Role:**

  * Executes file transfer workflows
  * Handles validation, transformation, and retry logic
  * Orchestrates movement between source and target systems
* **Capabilities:**

  * Event-driven execution
  * Scales automatically based on workload

👉 This is the **core processing engine** of the system.

---

### 3. **Provisioning Pipeline (CI/CD + Terraform)**

* **Type:** DevOps container
* **Role:**

  * Automates infrastructure provisioning and updates
  * Deploys application components and configurations
* **Capabilities:**

  * Uses GitLab pipelines and Terraform
  * Ensures consistent and repeatable deployments

👉 This enables **infrastructure automation and governance**.

---

### 4. **Monitoring & Logging (CloudWatch)**

* **Type:** Observability container
* **Role:**

  * Collects logs, metrics, and traces
  * Provides operational visibility into system behavior
* **Capabilities:**

  * Enables performance monitoring
  * Supports troubleshooting and debugging

👉 This ensures **system observability and operational insight**.

---

### 5. **Alerting & Notifications (SNS / Webhooks)**

* **Type:** Notification container
* **Role:**

  * Sends alerts for job completion, failures, and critical events
  * Notifies operators and downstream systems
* **Capabilities:**

  * Integrates with external systems (e.g., ELMA)
  * Supports event-driven notifications

👉 This enables **real-time operational awareness**.

---

## 🔹 **External Systems and Interactions**

### **Source Systems**

* Upload/download files via:

  * **SFTP (PUT/GET)**
  * **S3 (HTTPS PUT)**

### **Target Systems**

* Receive files via:

  * **SFTP (PUT)**
  * **S3 (HTTPS PUT)**

### **GitLab**

* Drives CI/CD pipelines and provisioning

### **ELMA**

* Receives monitoring, logging, and alerting data for enterprise observability

---

## 🔹 **End-to-End Flow**

1. Source systems initiate file transfer via SFTP or S3
2. AWS Transfer Family handles secure ingestion
3. Execution Workers (Lambda) process the file:

   * Validate
   * Route
   * Retry if needed
4. File is delivered to target systems
5. Monitoring data is captured in CloudWatch
6. Alerts are sent via SNS / Webhooks to ELMA

---

## 🔹 **Key Architectural Characteristics**

| Characteristic           | Description                                             |
| ------------------------ | ------------------------------------------------------- |
| Serverless-first design  | Lambda-based execution for scalability                  |
| Managed services         | Transfer Family, CloudWatch reduce operational overhead |
| Event-driven processing  | Trigger-based execution model                           |
| Decoupled architecture   | Separation of ingestion, processing, and notification   |
| Observability integrated | Centralized monitoring and alerting                     |
| CI/CD enabled            | Infrastructure and application automation via GitLab    |

---

## 🔹 **Architectural Observations (Current State)**

* Strong use of **managed AWS services**, reducing operational burden
* **Lambda-centric execution**, which may introduce limits for very large file processing
* Observability and alerting are **well integrated**
* CI/CD is **externally orchestrated via GitLab**
* Architecture is **modular and extensible**, but tightly centered on Lambda execution

Here is a **SADD-ready explanation** of the **Current State – C4 Component View**, written in a **principal architect tone** and aligned for ARC review:

---

# 📄 **Current State – Component View Explanation (C4 Level 3)**

The Current State Component View provides a detailed breakdown of the internal components within the NIS EFT Backend system and illustrates how they collaborate to execute end-to-end file transfer workflows. This view focuses on the runtime building blocks, their responsibilities, and the interaction patterns between them.

The architecture follows an event-driven, serverless model where file ingestion triggers downstream processing components, enabling scalable and loosely coupled operations.

---

## 🔹 **System Boundary**

All core components operate within the **AWS Cloud boundary**, forming the NIS EFT Backend Services. External systems such as Source Systems, Target Systems, GitLab, and ELMA interact with this boundary through defined interfaces.

---

## 🔹 **Core Components and Responsibilities**

### 1. **AWS Transfer Family (SFTP Server)**

* **Role:**

  * Provides secure SFTP endpoints for file ingestion and retrieval
  * Acts as the external interface for partner systems
* **Functionality:**

  * Handles PUT/GET operations via SFTP
  * Stores incoming files in S3-backed storage

👉 Serves as the **secure ingress/egress gateway**.

---

### 2. **Amazon S3 (Customer Bucket)**

* **Role:**

  * Acts as the central storage layer for all file transfers
* **Functionality:**

  * Stores inbound files from source systems
  * Triggers downstream processing via object creation events
* **Key Behavior:**

  * **Object Create Event → Lambda Trigger**

👉 Serves as the **event-driven storage backbone**.

---

### 3. **Lambda Function (Execution Component)**

* **Role:**

  * Core processing engine for file transfer workflows
* **Functionality:**

  * Processes file events triggered from S3
  * Applies validation and routing logic
  * Initiates file delivery to target systems
  * Handles retry and error logic

👉 This is the **central orchestration and processing component**.

---

### 4. **CloudWatch (Monitoring & Logging)**

* **Role:**

  * Captures logs, metrics, and execution traces
* **Functionality:**

  * Provides visibility into Lambda execution and system behavior
  * Supports debugging, performance monitoring, and auditing

👉 Enables **observability and operational insight**.

---

### 5. **SNS (Alerting & Notifications)**

* **Role:**

  * Sends notifications for events and failures
* **Functionality:**

  * Publishes alerts for job completion, errors, and critical events
  * Integrates with external systems such as ELMA

👉 Provides **real-time alerting and communication**.

---

### 6. **Provisioning Pipeline (GitLab CI/CD)**

* **Role:**

  * Automates deployment and infrastructure provisioning
* **Functionality:**

  * Uses Terraform and GitLab pipelines
  * Builds and deploys backend services

👉 Ensures **consistent, automated deployment lifecycle**.

---

## 🔹 **External Systems and Interaction**

### **Source Systems**

* Interact via:

  * **SFTP (PUT/GET)**
  * **S3 PUT (HTTPS)**
* Upload files into the system

### **Target Systems**

* Receive processed files via:

  * **SFTP (PUT)**
  * **S3 PUT (HTTPS)**

### **ELMA**

* Receives logs, alerts, and operational insights

---

## 🔹 **End-to-End Component Flow**

1. Source system uploads file via SFTP or S3
2. File is stored in **S3 (Customer Bucket)**
3. **S3 Object Creation Event** triggers Lambda
4. Lambda processes the file:

   * Validates
   * Determines target
   * Transfers file
5. File is delivered to **Target Systems**
6. Logs are captured in **CloudWatch**
7. Alerts are sent via **SNS → ELMA**

---

## 🔹 **Key Architectural Characteristics**

| Characteristic            | Description                                |
| ------------------------- | ------------------------------------------ |
| Event-driven architecture | S3 events trigger processing               |
| Serverless execution      | Lambda handles compute dynamically         |
| Decoupled design          | Storage and processing are loosely coupled |
| Managed services          | Reduced operational overhead               |
| Observability integrated  | CloudWatch and SNS                         |
| CI/CD automation          | GitLab pipeline driven                     |

---

## 🔹 **Architectural Observations (Current State)**

* Strong reliance on **Lambda for orchestration**, which may limit handling of very large files
* **S3 as central trigger point**, simplifying event-driven design
* **No explicit workflow orchestration layer** (e.g., Step Functions not present)
* Limited visibility into **complex retry/state management**
* Highly scalable for small-to-medium workloads, but may face constraints at scale

---



Here is a **SADD-ready explanation** of the **Target State – System Context View (C4 Level 1)** in a clear, ARC-ready tone:

---

# **Target State – System Context View Explanation**

The Target State System Context View illustrates the NIS EFT Backend within the broader target ecosystem and highlights the major external systems, integration channels, and supporting platforms that interact with it. This view shows the NIS EFT Backend as the central software system responsible for orchestrating secure, scalable, and observable file transfer operations across source systems, target systems, onboarding interfaces, deployment pipelines, and enterprise observability platforms.

In the target state, the **NIS EFT Backend** remains the core engine of the platform, but its ecosystem is expanded to support greater automation, self-service onboarding, improved operational visibility, and enterprise monitoring. The platform acts as the central integration hub for inbound and outbound file transfer workflows while also exposing APIs for onboarding and status-related operations.

---

## **Core System**

### **NIS EFT Backend**

The NIS EFT Backend is the core software system that manages end-to-end file transfer workflows. It is responsible for:

* orchestrating inbound and outbound file transfers,
* supporting multiple protocols such as **SFTP**, **S3 over HTTPS**, and **API over HTTPS**,
* managing workflow execution, validation, retry handling, and state tracking,
* integrating with observability and deployment platforms, and
* enabling scalable and resilient operations across enterprise use cases.

This backend serves as the **central processing and coordination layer** for the platform.

---

## **External Systems and Interactions**

### **1. Self-Serve Onboarding Portal**

The Self-Serve Onboarding Portal is a new addition in the target state and represents a major business capability enhancement.

**Role:**

* Allows customers and internal users to submit onboarding requests
* Enables registration of endpoints, transfer configurations, and workflow parameters
* Supports status inquiry and request tracking

**Interaction with NIS EFT Backend:**

* Communicates via **API / HTTPS**

**Architectural significance:**

* Introduces self-service capability
* Reduces manual onboarding effort
* Improves customer experience and operational efficiency

---

### **2. Source Systems**

Source systems continue to act as upstream producers and consumers of files.

**Supported interactions include:**

* **PUT (SFTP)** for secure file upload
* **S3 PUT (HTTPS)** for direct object delivery
* **GET (SFTP)** for retrieval use cases

These systems provide inbound files and may also retrieve output depending on the workflow pattern.

---

### **3. Target Systems**

Target systems remain downstream consumers of files processed or routed by the backend.

**Supported interactions include:**

* **PUT (SFTP)** for secure outbound delivery
* **S3 PUT (HTTPS)** for object-based delivery

The NIS EFT Backend ensures reliable and protocol-appropriate delivery to these systems.

---

### **4. GitLab**

GitLab continues to provide CI/CD and DevOps pipeline support.

**Role:**

* Hosts source code and configuration repositories
* Executes build and deployment pipelines
* Automates infrastructure and application changes

**Interaction with NIS EFT Backend:**

* Supports deployment and provisioning workflows

This ensures the target platform remains **automated, version-controlled, and operationally manageable**.

---

### **5. ELMA**

ELMA remains part of the enterprise observability ecosystem.

**Role:**

* Receives logging, monitoring, and operational insights
* Supports enterprise observability and operational analysis

**Interaction with NIS EFT Backend:**

* Backend forwards operational data and events for centralized visibility

---

### **6. Dynatrace**

Dynatrace is added in the target state as an additional enterprise observability and metrics platform.

**Role:**

* Provides enhanced operational monitoring and metrics analysis
* Collects application and platform-level telemetry from the file transfer backend services
* Supports performance tracking, anomaly detection, and operational diagnostics

**Architectural significance:**

* Expands observability maturity
* Enables deeper insight into performance and resource behavior
* Supports proactive operations and reliability management

---

## **Data Flow Overview**

The target state supports multiple integration paths:

### **Inbound Flow**

* Source Systems → NIS EFT Backend
  via **SFTP**, **S3/HTTPS**

### **Outbound Flow**

* NIS EFT Backend → Target Systems
  via **SFTP**, **S3/HTTPS**

### **Onboarding / Control Flow**

* Self-Serve Onboarding Portal → NIS EFT Backend
  via **API/HTTPS**

### **Deployment Flow**

* GitLab → NIS EFT Backend
  via CI/CD pipelines

### **Observability Flow**

* NIS EFT Backend → ELMA
* NIS EFT Backend → Dynatrace

These flows show that the target platform is not only a transfer engine, but also a more complete service platform with onboarding, monitoring, and deployment integration.

---

## **Key Architectural Characteristics of Target State**

| Characteristic             | Description                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| Centralized backend engine | NIS EFT Backend remains the platform core                          |
| Self-service enablement    | New onboarding portal improves automation and customer experience  |
| Multi-protocol support     | Supports SFTP, S3/HTTPS, and API/HTTPS                             |
| Enhanced observability     | Integrates with both ELMA and Dynatrace                            |
| CI/CD automation           | GitLab supports continuous deployment and provisioning             |
| Enterprise integration hub | Connects source systems, target systems, and operational platforms |

---

## **Target State Architectural Observations**

* The target state expands the backend from a transfer-focused system into a broader **service platform**
* The addition of the **Self-Serve Onboarding Portal** addresses a major business pain point in manual onboarding
* The addition of **Dynatrace** strengthens enterprise observability and operational insight
* The backend remains the central integration point, but the surrounding ecosystem becomes more automated and operationally mature
* The target context better supports scalability, governance, and user autonomy compared with the current state

---

# **Strong Closing Statement**

The target state system context positions the NIS EFT Backend as a centralized, enterprise-grade file transfer platform that not only enables secure movement of data between source and target systems, but also supports self-service onboarding, automated deployment, and enhanced observability through tighter integration with enterprise tooling.

Here is a **SADD-ready explanation** of the **Target State – C4 Container View**, written in a **principal architect tone** and aligned for ARC review:

---

# 📄 **Target State – Container View Explanation (C4 Level 2)**

The Target State Container View provides a detailed representation of the internal architecture of the NIS EFT Backend Services, illustrating how the system is decomposed into scalable, decoupled containers that collectively enable secure, resilient, and high-throughput file transfer operations.

In the target state, the architecture evolves from a simple event-driven Lambda model to a **fully orchestrated, distributed workflow system**. It introduces explicit layers for API access, orchestration, event handling, execution, and state management, improving scalability, reliability, and operational control.

---

## 🔹 **System Boundary**

All containers operate within the **NIS EFT Backend Services boundary**, deployed on AWS. The system integrates with external systems such as Source Systems, Target Systems, Self-Serve Onboarding Portal, GitLab, ELMA, and Dynatrace.

---

## 🔹 **Core Containers and Responsibilities**

### **1. API Layer (Amazon API Gateway + Lambda)**

* **Role:**

  * Entry point for onboarding and operational APIs
* **Responsibilities:**

  * Accepts onboarding requests from the Self-Serve Portal
  * Validates and authorizes requests
  * Initiates workflow execution
  * Provides status query APIs

👉 Enables **self-service onboarding and control plane capabilities**

---

### **2. AWS Transfer Family (SFTP)**

* **Role:**

  * Secure ingress/egress gateway for file transfers
* **Responsibilities:**

  * Handles SFTP-based PUT/GET operations
  * Integrates with S3-backed storage

👉 Provides **secure external connectivity**

---

### **3. Eventing & Queuing (EventBridge / SQS)**

* **Role:**

  * Decouples ingestion from processing
* **Responsibilities:**

  * Captures events (file arrival, API triggers)
  * Buffers workloads
  * Enables asynchronous processing
  * Smooths traffic spikes

👉 Provides **resilience and scalability through decoupling**

---

### **4. Workflow Orchestrator (AWS Step Functions)**

* **Role:**

  * Central orchestration engine
* **Responsibilities:**

  * Manages end-to-end workflows
  * Handles retries, branching, and error handling
  * Coordinates execution steps across services

👉 Introduces **stateful orchestration and reliability**

---

### **5. Execution Workers (ECS Fargate + Lambda)**

* **Role:**

  * Execute file transfer operations
* **Responsibilities:**

  * Process large and small file transfers
  * Perform validation, transformation, and delivery
  * Handle retry logic

👉 Enables **hybrid compute model**:

* Lambda → lightweight tasks
* Fargate → large file processing

---

### **6. Status & Metadata Store (DynamoDB)**

* **Role:**

  * Persistent state store
* **Responsibilities:**

  * Tracks job status, execution state, and metadata
  * Supports idempotency and checkpointing
  * Enables resume and recovery

👉 Provides **state management and consistency**

---

### **7. Monitoring & Logging (CloudWatch)**

* **Role:**

  * Observability layer
* **Responsibilities:**

  * Captures logs, metrics, and traces
  * Enables operational dashboards and alerting

---

### **8. Alerting & Notifications (SNS / Webhooks)**

* **Role:**

  * Event-driven notification system
* **Responsibilities:**

  * Sends alerts for failures, completions, and critical events
  * Integrates with ELMA and other systems

---

### **9. Provisioning Pipeline (GitLab + Terraform)**

* **Role:**

  * Deployment and infrastructure automation
* **Responsibilities:**

  * Manages CI/CD pipelines
  * Provisions infrastructure
  * Deploys application components

👉 Enables **consistent and governed deployments**

---

## 🔹 **External Integrations**

| System            | Role                                    |
| ----------------- | --------------------------------------- |
| Self-Serve Portal | API-based onboarding and status queries |
| Source Systems    | File producers via SFTP / S3            |
| Target Systems    | File consumers via SFTP / S3            |
| ELMA              | Enterprise observability                |
| Dynatrace         | Advanced monitoring and telemetry       |
| GitLab            | CI/CD and provisioning                  |

---

## 🔹 **End-to-End Flow (Target State)**

1. **Onboarding / API Flow**

   * Portal → API Gateway → Workflow initiation → DynamoDB

2. **File Ingestion Flow**

   * Source → Transfer Family / S3 → EventBridge/SQS

3. **Processing Flow**

   * Event → Step Functions → Execution Workers

4. **Delivery Flow**

   * Workers → Target Systems (SFTP / S3)

5. **State & Observability**

   * Status stored in DynamoDB
   * Logs → CloudWatch → ELMA / Dynatrace
   * Alerts → SNS

---

## 🔹 **Key Architectural Improvements Over Current State**

| Area                | Improvement                                           |
| ------------------- | ----------------------------------------------------- |
| Orchestration       | Introduced Step Functions (explicit workflow control) |
| Scalability         | Event-driven + queue-based buffering                  |
| Large file handling | ECS Fargate support                                   |
| State management    | DynamoDB-based tracking                               |
| Self-service        | API + onboarding portal                               |
| Observability       | Enhanced with Dynatrace                               |
| Decoupling          | EventBridge/SQS layer                                 |

---

## 🔹 **Architectural Characteristics**

| Characteristic            | Description                              |
| ------------------------- | ---------------------------------------- |
| Event-driven architecture | Decoupled ingestion and processing       |
| Orchestrated workflows    | Step Functions manages lifecycle         |
| Hybrid compute model      | Lambda + Fargate                         |
| State-aware system        | DynamoDB for tracking and idempotency    |
| Highly scalable           | Queue-based buffering and autoscaling    |
| Resilient                 | Retry, failover, and recovery mechanisms |
| Observable                | Integrated monitoring and alerting       |

---

# 💡 **Strong Closing Line**

> “The target state container architecture transforms the platform into a fully orchestrated, event-driven, and state-aware system, enabling scalable, resilient, and enterprise-grade file transfer operations with enhanced automation, observability, and control.”

---

Here is a **SADD-ready explanation** of the **Target State – C4 Component View**, written in a **principal architect tone** and aligned strongly for ARC:

---

# 📄 **Target State – Component View Explanation (C4 Level 3)**

The Target State Component View provides a detailed breakdown of the internal components within the NIS EFT Backend Services and illustrates how they collaborate to enable a scalable, resilient, and event-driven file transfer platform. This view expands upon the container architecture by showing the fine-grained processing flow, including ingestion, event handling, orchestration, execution, state management, and observability.

The architecture adopts a **fully decoupled, event-driven, and workflow-orchestrated design**, ensuring high scalability, fault tolerance, and operational visibility.

---

## 🔹 **System Boundary**

All components operate within the **AWS Cloud boundary**, forming the NIS EFT Backend Services. External systems such as the Self-Serve Portal, Source Systems, Target Systems, GitLab, ELMA, and Dynatrace interact with the system through well-defined interfaces.

---

## 🔹 **Core Components and Responsibilities**

### **1. API Gateway + Lambda (Backend APIs)**

* **Role:**

  * Entry point for onboarding and control-plane operations
* **Responsibilities:**

  * Receives onboarding requests from the Self-Serve Portal (API/HTTPS)
  * Validates and processes requests
  * Writes onboarding and status records to DynamoDB

👉 Enables **self-service onboarding and API-driven control plane**

---

### **2. AWS Transfer Family (SFTP Server)**

* **Role:**

  * Secure file ingress and egress gateway
* **Responsibilities:**

  * Handles SFTP-based PUT/GET operations
  * Stores files into S3 (Customer Bucket)

---

### **3. Amazon S3 (Customer Bucket)**

* **Role:**

  * Central storage layer
* **Responsibilities:**

  * Stores inbound files
  * Triggers downstream processing using object creation events

👉 Acts as the **event trigger source**

---

### **4. EventBridge (Event Routing Layer)**

* **Role:**

  * Event ingestion and routing
* **Responsibilities:**

  * Captures S3 object events
  * Routes events to downstream processing systems

👉 Provides **event-driven decoupling**

---

### **5. SQS (Queue Buffering Layer)**

* **Role:**

  * Asynchronous buffering and workload smoothing
* **Responsibilities:**

  * Queues file processing requests
  * Prevents overload during traffic spikes
  * Enables retry and backpressure handling

👉 Provides **resilience and load leveling**

---

### **6. Step Functions (Workflow Orchestrator)**

* **Role:**

  * Central orchestration engine
* **Responsibilities:**

  * Coordinates end-to-end workflow execution
  * Handles branching (large vs small file)
  * Manages retries, failure handling, and state transitions

👉 Enables **stateful workflow control and reliability**

---

### **7. Execution Layer (Hybrid Compute)**

#### **a. ECS Fargate (Large File Processing)**

* Handles **large file transfers**
* Provides scalable compute with higher resource capacity
* Executes long-running tasks

#### **b. Lambda (Small File Processing)**

* Handles **lightweight / small file transfers**
* Provides low-latency, serverless execution

👉 Enables **right-sized compute for different workloads**

---

### **8. DynamoDB (Status & Metadata Store)**

* **Role:**

  * Persistent state management
* **Responsibilities:**

  * Stores onboarding data
  * Tracks transfer status and execution history
  * Supports idempotency and checkpointing

👉 Enables **stateful, recoverable workflows**

---

### **9. CloudWatch (Monitoring & Logging)**

* **Role:**

  * Observability and monitoring
* **Responsibilities:**

  * Captures logs, metrics, and traces
  * Provides operational visibility

---

### **10. SNS (Alerting & Notifications)**

* **Role:**

  * Notification and alerting system
* **Responsibilities:**

  * Sends alerts for failures, completion, and critical events
  * Integrates with ELMA and external systems

---

### **11. GitLab CI/CD (Provisioning Pipeline)**

* **Role:**

  * Deployment and infrastructure automation
* **Responsibilities:**

  * Builds and deploys application components
  * Provisions infrastructure using Terraform

---

## 🔹 **End-to-End Processing Flow**

### **1. Onboarding Flow**

* Self-Serve Portal → API Gateway → Lambda → DynamoDB
* Stores onboarding configuration and metadata

---

### **2. File Ingestion Flow**

* Source Systems → SFTP / S3 → S3 Bucket
* S3 Object Create Event → EventBridge → SQS

---

### **3. Workflow Orchestration**

* SQS → Step Functions
* Determines execution path (small vs large file)

---

### **4. Execution Flow**

* Small file → Lambda
* Large file → ECS Fargate

---

### **5. Delivery Flow**

* Execution layer → Target Systems (SFTP / S3)

---

### **6. State & Observability**

* Status updates → DynamoDB
* Logs → CloudWatch
* Alerts → SNS → ELMA / Dynatrace

---

## 🔹 **Key Architectural Capabilities**

| Capability              | Description                           |
| ----------------------- | ------------------------------------- |
| Event-driven processing | S3 → EventBridge → SQS                |
| Workflow orchestration  | Step Functions manages lifecycle      |
| Hybrid compute          | Lambda + Fargate                      |
| State management        | DynamoDB-based tracking               |
| Decoupling              | Queue-based buffering                 |
| Scalability             | Horizontal scaling across all layers  |
| Resiliency              | Retry, backpressure, failover support |
| Observability           | CloudWatch + ELMA + Dynatrace         |

---

## 🔹 **Key Improvements Over Current State**

| Area             | Current State           | Target State                  |
| ---------------- | ----------------------- | ----------------------------- |
| Orchestration    | Implicit (Lambda logic) | Explicit (Step Functions)     |
| Scaling          | Limited Lambda-based    | Hybrid (Lambda + Fargate)     |
| Decoupling       | Minimal                 | EventBridge + SQS             |
| State management | Limited                 | DynamoDB                      |
| Onboarding       | Manual                  | API-driven self-service       |
| Resiliency       | Basic retries           | Full workflow-level retries   |
| Observability    | CloudWatch              | CloudWatch + ELMA + Dynatrace |

---

# 💡 **Strong Closing Line**

> “The target state component architecture establishes a fully decoupled, event-driven, and state-aware processing model that enables scalable, resilient, and enterprise-grade file transfer operations, with clear separation of concerns across ingestion, orchestration, execution, and observability layers.”

---



