

## **Key Architectural Decisions (Component Layer – Current State)**

| #  | Decision                                                 | Rationale                                    | Impact / Trade-offs                                    |
| -- | -------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------ |
| 1  | Use AWS Transfer Family (SFTP) as ingestion component    | Managed service reduces operational overhead | Limited extensibility and protocol flexibility         |
| 2  | Use S3 as intermediate landing/staging layer             | Decouples ingestion from processing          | Adds latency and storage dependency                    |
| 3  | Trigger processing via S3 event notifications → Lambda   | Enables event-driven processing model        | Tight coupling to S3 events                            |
| 4  | Use Lambda as primary execution component                | Serverless compute simplifies scaling        | Constrained by timeout, memory, and execution limits   |
| 5  | Single Lambda handles validation + routing + transfer    | Simplifies implementation                    | Violates separation of concerns, harder to scale/debug |
| 6  | No orchestration layer (Step Functions not used)         | Reduces system complexity                    | Limited retry control, visibility, and state tracking  |
| 7  | Direct push from Lambda to target systems                | Minimizes intermediate hops                  | Reduces resiliency and retry flexibility               |
| 8  | Monitoring via CloudWatch integrated with ELMA           | Centralized logging approach                 | Limited end-to-end traceability                        |
| 9  | Alerts via SNS                                           | Simple notification mechanism                | Reactive alerting, lacks intelligent correlation       |
| 10 | CI/CD provisioning via GitLab + Terraform                | Infrastructure automation                    | Limited runtime adaptability                           |
| 11 | No dedicated validation/malware scanning component       | Not implemented                              | **Security gap (critical ARC finding)**                |
| 12 | No metadata/state persistence layer                      | Simplifies processing                        | Limits auditability and recovery capability            |
| 13 | No explicit retry queue (e.g., SQS)                      | Simpler architecture                         | Risk of data loss on failure                           |
| 14 | Tight coupling between ingestion → processing → delivery | Straightforward flow                         | Limits scalability and fault isolation                 |



That’s what will separate you from everyone else in the room.
