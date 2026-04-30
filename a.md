

## **Key Architectural Decisions (Container Layer – Current State)**

| #  | Decision                                                             | Rationale                                                    | Impact / Trade-offs                                     |
| -- | -------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| 1  | Use AWS Transfer Family as managed SFTP ingress layer                | Avoid building custom SFTP servers                           | Limited protocol flexibility, dependency on AWS service |
| 2  | Use centralized Execution Workers (Lambda-based) for file processing | Simplifies compute model and reduces infrastructure overhead | Constrained by Lambda limits (timeout, memory)          |
| 3  | Backend service tightly orchestrates transfer workflows              | Centralized control and routing logic                        | Creates coupling and scaling bottleneck                 |
| 4  | Synchronous / semi-batch execution model                             | Easier to reason about flows                                 | Lower scalability vs event-driven                       |
| 5  | No dedicated orchestration engine (e.g., Step Functions not used)    | Simpler implementation                                       | Limited visibility, retry control, and state management |
| 6  | Logging handled via CloudWatch integrated with ELMA                  | Centralized observability                                    | Limited correlation across distributed flows            |
| 7  | Alerts via SNS / Webhooks                                            | Basic operational awareness                                  | Reactive instead of proactive alerting                  |
| 8  | CI/CD pipeline via GitLab                                            | Standardized deployments                                     | Limited environment-aware automation                    |
| 9  | No separation between ingestion, processing, and delivery layers     | Simpler architecture                                         | Reduced isolation, impacts fault containment            |
| 10 | Lack of explicit idempotency layer                                   | Simpler processing logic                                     | Risk of duplicate file processing                       |
| 11 | No anti-malware scanning container/service                           | Not implemented currently                                    | **Critical security gap (explicit ARC concern)**        |
| 12 | No dedicated metadata store for workflow state tracking              | Lightweight design                                           | Limits observability, recovery, and auditability        |

---



👉 **“Create target container decisions”**
