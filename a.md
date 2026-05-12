# Performance & Efficiency

## Workload Expectations

The target architecture is designed to support enterprise-scale file transfer growth across EFEDS and Cloud File platforms while maintaining resiliency, scalability, and operational stability.

### Expected Workload Profile

* Supports up to **10M file transfers per day**
* Handles a mix of **small, medium, and large file workloads**
* Designed for peak business-hour concurrency and burst traffic patterns
* Supports retry, replay, and failover processing scenarios

### Current vs Target Scale

* Current workload processes approximately **115K file transfers per day** across **5 Cash machines**
* Enterprise rollout across approximately **180 Cash machines** is projected to increase workload to approximately **4M transfers per day**
* The target architecture is sized for up to **10M file transfers per day** to support future growth and operational headroom

### Target Capacity Metrics

* ~31.8 TB weekly transfer volume
* ~4.5 TB daily transfer volume
* ~230 peak transactions per second
* ~105 MB/sec peak throughput
* 500 parallel large-file processing tasks (soft limit)

---

# Resource Sizing Strategy

The platform is sized to support expected growth, peak concurrency, and resiliency objectives.

### Key Principles

* Elastic cloud-native scaling
* Independent scaling for orchestration and compute layers
* Capacity headroom for failover and retry events
* Queue-based buffering for workload stabilization

The architecture prioritizes efficient baseline utilization while scaling dynamically during peak demand periods.

---

# Scaling Strategy

The platform primarily uses horizontal scaling to improve resiliency, throughput, and workload isolation.

### Scaling Approach

* Step Functions manage workflow parallelism
* Lambda scales lightweight processing automatically
* ECS Fargate handles compute-intensive and large-file workloads
* SQS absorbs spikes and smooths downstream load

Selective vertical scaling is applied for workloads requiring higher compute or memory allocation.

---

# Concurrency & Backpressure Management

Concurrency controls are implemented across orchestration, compute, and queueing layers to maintain platform stability during peak demand.

### Key Controls

* Reserved concurrency and throttling for Lambda
* Controlled workflow parallelism in Step Functions
* Auto scaling for ECS Fargate tasks
* SQS-based buffering and workload decoupling

### Backpressure Handling

* Traffic spikes absorbed through queue buffering
* Retry storms managed using exponential backoff
* Downstream slowdowns handled through controlled draining

This model prevents cascading failures and protects downstream dependencies.

---

# Large File Processing Strategy

The architecture uses a hybrid execution model optimized by file size and workload profile.

### Processing Model

* Small files processed using Lambda
* Medium workloads orchestrated through Step Functions
* Large and long-running transfers processed using ECS Fargate

This approach improves scalability, workload isolation, and cost efficiency.

---

# Failover & Resiliency Scaling

The platform is designed to sustain degraded operating conditions during regional failover and recovery events.

### Resiliency Considerations

* Surviving regions absorb increased workload during failover
* SQS buffers temporary retry and reconciliation spikes
* Batch scaling supports recovery and replay operations

The architecture maintains stable throughput while minimizing operational disruption during failure scenarios.

---

# Monitoring & Resource Utilization

Centralized observability provides end-to-end visibility across orchestration, compute, queueing, and storage services.

### Key Monitoring Areas

* Queue depth and backlog growth
* Workflow latency and execution health
* Lambda concurrency and throttling
* ECS utilization and throughput
* Error rates and retry activity

### Operational Objectives

* Early bottleneck detection
* Automated scaling decisions
* Capacity optimization
* Proactive resiliency management

Enterprise monitoring and alerting integrations support both real-time operations and long-term capacity planning.
