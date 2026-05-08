# Target State: System Context Diagram

The target state positions the NIS EFT Backend as the centralized orchestration platform for enterprise file transfer operations across internal systems, external partners, and downstream consumers.

The platform standardizes onboarding, transfer execution, monitoring, and operational visibility using enterprise integration patterns and cloud-native services.

## Core Platform Responsibilities

* Manage inbound and outbound file transfer workflows
* Support SFTP, Amazon S3, and API-based integrations
* Provide centralized workflow tracking and operational visibility
* Enable scalable, resilient, and automated transfer processing
* Integrate with enterprise monitoring and DevOps platforms

## External Systems & Interactions

| System                       | Purpose                                                                  |
| ---------------------------- | ------------------------------------------------------------------------ |
| Self-Serve Onboarding Portal | Supports onboarding requests, endpoint registration, and status tracking |
| Source Systems               | Send files through standardized SFTP or S3 integration patterns          |
| Target Systems               | Receive outbound file deliveries from the platform                       |
| GitLab                       | Provides CI/CD and deployment automation support                         |
| ELMA / Dynatrace             | Provide enterprise monitoring, logging, and operational visibility       |

# Key Architectural Decisions – Target State System Context

| Area              | Decision                                                   | Business Outcome                                             |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| Core Architecture | NIS EFT Backend acts as the central orchestration platform | Improves consistency, governance, and operational visibility |
| Integration Model | Source and target systems remain loosely coupled           | Simplifies onboarding and scalability                        |
| Protocol Strategy | Supports SFTP, S3 (HTTPS), and API integrations            | Enables both legacy and cloud-native integration patterns    |
| Observability     | Uses enterprise monitoring platforms (ELMA and Dynatrace)  | Provides centralized monitoring and operational insights     |
| DevOps            | GitLab used for CI/CD and deployment automation            | Supports standardized and automated deployments              |
| Scalability       | Horizontal scaling and parallel workflow execution         | Supports high-volume enterprise workloads and burst handling |


