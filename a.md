

---

## **Rollback Strategy**

| Area               | Approach                                                                             |
| ------------------ | ------------------------------------------------------------------------------------ |
| Deployment Model   | Versioned deployments with immutable artifacts (Lambda, ECS, Step Functions)         |
| Rollback Trigger   | Automated via CloudWatch alarms (error rate, latency, failures) or manual invocation |
| Rollback Mechanism | Revert to last stable version using CI/CD pipeline (GitLab + Terraform)              |
| Data Protection    | In-flight transfers allowed to complete; no forced termination                       |
| Consistency        | Idempotent processing ensures no duplicate or partial data                           |
| Recovery Time      | Target: < 15 minutes                                                                 |
| Scope              | Component-level rollback (Lambda / workflow / config)                                |

---

## **Key Decisions**

* Use versioned artifacts for safe rollback
* Avoid terminating in-flight transfers
* Enable automated rollback via monitoring signals

---



## **Migration Strategy**

| Phase   | Description                | Approach                                               | Risk Mitigation                       |
| ------- | -------------------------- | ------------------------------------------------------ | ------------------------------------- |
| Phase 0 | Inventory & Classification | Identify all workflows (SFTP, S3, volume, criticality) | No migration without classification   |
| Phase 1 | Pilot Migration            | Migrate low-risk / low-volume flows                    | Validate architecture + rollback      |
| Phase 2 | Parallel Run               | Run legacy and new system in parallel                  | Compare outputs, validate correctness |
| Phase 3 | Gradual Cutover            | Incrementally migrate remaining workflows              | Rollback per workflow if issues       |
| Phase 4 | Full Migration             | Decommission legacy flows                              | Ensure stability before shutdown      |

---

## **Migration Principles**

* No big-bang migration
* Workflow-level isolation
* Rollback available per workflow
* Data validation before cutover

---

## **Cutover Strategy**

| Scenario          | Approach                     |
| ----------------- | ---------------------------- |
| Low-risk flows    | Direct migration             |
| Critical flows    | Parallel run + validation    |
| External partners | Coordinated migration window |

---

## **Rollback During Migration**




# 📌 **Cost Optimization Strategy**

## **Cost Model**

| Area            | Approach                                              |
| --------------- | ----------------------------------------------------- |
| Pricing Model   | Pay-per-use (Lambda, Step Functions, S3, EventBridge) |
| Billing Drivers | Requests, compute duration, storage, data transfer    |
| Cost Visibility | AWS Cost Explorer + tagging strategy                  |
| Allocation      | Per workflow / per customer tagging                   |

---

## **Key Cost Drivers**

| Service        | Driver                 | Optimization Lever             |
| -------------- | ---------------------- | ------------------------------ |
| Lambda         | Invocations + duration | Memory tuning, batching        |
| S3             | Storage + requests     | Lifecycle policies             |
| Data Transfer  | GB transferred         | Reduce external SFTP transfers |
| Step Functions | State transitions      | Reduce unnecessary steps       |
| Fargate        | vCPU + memory time     | Right-sizing, selective usage  |

---

## **Optimization Decisions**

| # | Decision                                                   | Impact                                 |
| - | ---------------------------------------------------------- | -------------------------------------- |
| 1 | Use serverless compute (Lambda) for event-driven workloads | Eliminates idle compute cost           |
| 2 | Use S3 as staging layer                                    | Low-cost durable storage               |
| 3 | Apply S3 lifecycle policies (→ Glacier)                    | Reduces long-term storage cost         |
| 4 | Prefer S3-to-S3 transfers over SFTP where possible         | Reduces network cost                   |
| 5 | Use event-driven triggers (EventBridge/S3 events)          | Avoid polling cost                     |
| 6 | Use managed services (Transfer Family, Step Functions)     | Reduces operational overhead           |
| 7 | Tag all resources by workflow/customer                     | Enables cost tracking and optimization |

---

## **Cost Controls**

| Control           | Implementation                               |
| ----------------- | -------------------------------------------- |
| Budget Alerts     | AWS Budgets with threshold alerts            |
| Anomaly Detection | AWS Cost Anomaly Detection                   |
| Monitoring        | CloudWatch metrics for usage patterns        |
| Governance        | Periodic cost review and optimization cycles |

---

## **Assumptions**

* Costs based on current workload estimates
* Data transfer patterns may vary by customer
* External SFTP usage drives higher cost variability

---




