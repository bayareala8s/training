

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






# 📌 **Operational Excellence (Rewritten — ARC Ready)**

## **Key Decisions**

| # | Decision                           | Description                                                   |
| - | ---------------------------------- | ------------------------------------------------------------- |
| 1 | Centralized logging via CloudWatch | All system events, transfers, and errors are logged centrally |
| 2 | Metrics-based monitoring           | Track success rate, latency, error rate                       |
| 3 | Alerting via SNS                   | Trigger alerts on threshold breaches                          |
| 4 | CI/CD via GitLab                   | Automated build, test, and deployment pipelines               |
| 5 | Infrastructure as Code (Terraform) | Consistent and repeatable environment provisioning            |
| 6 | Versioned deployments              | All components deployed as immutable versions                 |
| 7 | Automated rollback                 | Rollback triggered on failure or threshold breach             |

---

## **Observability**

| Area    | Implementation            |
| ------- | ------------------------- |
| Logging | CloudWatch Logs           |
| Metrics | CloudWatch Metrics        |
| Alerts  | SNS notifications         |
| Audit   | Centralized log retention |

---

## **Deployment Model**

| Area              | Approach                |
| ----------------- | ----------------------- |
| Deployment        | CI/CD pipeline (GitLab) |
| Promotion         | Dev → QA → UAT → Prod   |
| Release Type      | Versioned deployments   |
| Downtime Strategy | Rolling / zero-downtime |

---

## **Testing Strategy**

| Type                | Scope                          |
| ------------------- | ------------------------------ |
| Unit Testing        | Component-level validation     |
| Integration Testing | Service interaction validation |
| End-to-End Testing  | Full workflow validation       |
| Resiliency Testing  | Failure and retry scenarios    |

---

## **Rollback Strategy**

| Area       | Approach                            |
| ---------- | ----------------------------------- |
| Mechanism  | Version rollback                    |
| Trigger    | Failure detection / alert threshold |
| Automation | Automatic + manual                  |
| Scope      | Lambda, Step Functions, ECS, APIs   |





# ✅ Replace With This (ARC-READY VERSION)

## **Performance & Scaling Model**

### **Workload Assumptions (Baseline)**

| Metric               | Current    | Target         | Source                                      |
| -------------------- | ---------- | -------------- | ------------------------------------------- |
| Transfers/day        | 100K       | 10M            | Existing system metrics + growth projection |
| TPS (avg)            | ~1.16/sec  | ~116/sec       | Derived                                     |
| Peak TPS (2x)        | ~2.3/sec   | ~230/sec       | Burst assumption                            |
| Avg file size        | ~0.45 MB   | ~0.45 MB       | Observed                                    |
| Throughput (avg)     | ~0.53 MB/s | ~52.5 MB/s     | Calculated                                  |
| Concurrent workflows | 16         | 16–100 (burst) | Design assumption                           |
| Large file threshold | >100 MB    | >100 MB        | Defined boundary                            |

---

## **Scaling Strategy**

| Area                   | Approach       | Control                      |
| ---------------------- | -------------- | ---------------------------- |
| Orchestration          | Step Functions | Execution concurrency limits |
| Lightweight processing | Lambda         | Reserved concurrency         |
| Heavy processing       | ECS Fargate    | Task scaling                 |
| Queue buffering        | SQS            | Queue depth control          |

---

## **Concurrency Management**

| Component      | Limit                | Strategy                          |
| -------------- | -------------------- | --------------------------------- |
| Lambda         | Regional concurrency | Reserved concurrency + throttling |
| Step Functions | Execution limits     | Controlled parallelism            |
| SQS            | Virtually unlimited  | Backpressure buffer               |
| Fargate        | Task limits          | Auto scaling                      |

---

## **Backpressure & Throttling**

| Scenario            | Handling                         |
| ------------------- | -------------------------------- |
| Spike in requests   | SQS absorbs load                 |
| Lambda saturation   | Throttling + retry               |
| Downstream slowdown | Queue buildup + controlled drain |
| Retry storms        | Exponential backoff              |

---

## **Queue Depth & Alerting**

| Metric             | Threshold    | Action               |
| ------------------ | ------------ | -------------------- |
| Queue depth        | > X messages | Scale consumers      |
| Processing latency | > Y sec      | Trigger alert        |
| Error rate         | > Z%         | Pause ingestion      |
| Lambda throttles   | > threshold  | Increase concurrency |

---

## **Large File Handling**

| Category | Definition | Handling                |
| -------- | ---------- | ----------------------- |
| Small    | < 10 MB    | Lambda                  |
| Medium   | 10–100 MB  | Lambda / Step Functions |
| Large    | > 100 MB   | ECS Fargate             |

---

## **Monitoring Metrics (Driving Scaling Decisions)**

| Metric             | Usage                  |
| ------------------ | ---------------------- |
| Queue depth        | Scaling trigger        |
| Lambda concurrency | Capacity control       |
| Execution latency  | Bottleneck detection   |
| Error rate         | Stability signal       |
| Throughput (MB/s)  | Performance validation |

---

## **Failover Scaling Consideration**

| Scenario            | Behavior                         |
| ------------------- | -------------------------------- |
| Regional failover   | 2x workload handled              |
| Retry burst         | Temporary spike absorbed via SQS |
| Reconciliation load | Processed via batch scaling      |

---




