

## **Key Architectural Decisions (Current State)**

| #  | Decision                                              | Rationale                                  | Impact / Trade-off                                  |
| -- | ----------------------------------------------------- | ------------------------------------------ | --------------------------------------------------- |
| 1  | Deployment in CFS2 (Cloud-native environment)         | Align with enterprise cloud strategy       | Dependency on cloud services and networking         |
| 2  | Centralized EFT Backend Engine                        | Simplifies orchestration and routing       | Potential bottleneck and scaling limitation         |
| 3  | Support SFTP-based file transfers                     | Industry standard for secure file exchange | Limited scalability and performance vs event-driven |
| 4  | Support S3-based transfers (PUT/GET via HTTPS)        | Enables cloud-native storage integration   | Mixed protocol complexity                           |
| 5  | Backend-driven orchestration (synchronous/semi-batch) | Simpler control flow                       | Less resilient vs event-driven model                |
| 6  | Limited event-driven architecture                     | Legacy design pattern                      | Reduced scalability and responsiveness              |
| 7  | No standardized idempotency enforcement               | Simpler implementation                     | Risk of duplicate processing                        |
| 8  | Basic retry mechanisms                                | Handles transient failures                 | Not optimized (no exponential backoff control)      |
| 9  | Observability via ELMA                                | Central monitoring                         | Limited end-to-end traceability                     |
| 10 | CI/CD via GitLab pipelines                            | Standardized deployments                   | Limited automation for infra changes                |
| 11 | No explicit malware scanning for external transfers   | Not implemented today                      | Security gap (explicit ARC concern)                 |
| 12 | Tight coupling between ingestion and processing       | Simpler flow                               | Limits scalability and isolation                    |



# 📌 **External Systems / Dependencies Table**

👉 Copy-paste this next

---

## **External Systems & Dependencies**

| Dependency     | Type                   | Description                                            | Interaction                            | Criticality |
| -------------- | ---------------------- | ------------------------------------------------------ | -------------------------------------- | ----------- |
| ELMA           | Observability System   | Provides logging, monitoring, and operational insights | Receives logs and metrics from backend | High        |
| GitLab         | CI/CD Platform         | Manages build and deployment pipelines                 | Deploys backend services               | Medium      |
| Source Systems | External/Internal Apps | Systems that initiate file transfers                   | Push (SFTP/S3) or Pull workflows       | High        |
| Target Systems | External/Internal Apps | Systems that receive files                             | Receive via SFTP or S3                 | High        |
| SFTP Endpoints | External Systems       | Partner-managed secure file transfer endpoints         | File ingestion and delivery            | High        |
| S3 Storage     | Cloud Storage          | Intermediate or final storage layer                    | File staging and transfer              | High        |


