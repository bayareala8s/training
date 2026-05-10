
# Resiliency & Reliability

The NIS Enterprise File Transfer (EFT) platform is designed as a resilient, multi-region file transfer platform deployed across AWS GovCloud regions using an active-passive recovery model between us-gov-west-1 (primary) and us-gov-east-1 (secondary). The architecture supports automated failover, replay-based recovery, replicated storage, and operational resiliency to minimize service disruption and data loss during infrastructure or application failures.

The platform provides the following resiliency capabilities:

* Multi-region deployment with Route53-based failover routing
* Cross-region metadata replication using DynamoDB Global Tables
* Cross-region file replication using Amazon S3 replication
* Queue-based asynchronous workflow processing for failure isolation
* Replay and recovery orchestration for incomplete or failed transfers
* Centralized monitoring, alerting, and operational visibility
* Idempotent processing controls to prevent duplicate delivery

The resiliency strategy is designed to support:

* 99.90% service availability
* 15-minute recovery time objective (RTO)
* Near-zero metadata recovery point objective (RPO)
* ≤15-minute file recovery point objective through replicated storage

The architecture isolates failures through decoupled workflow processing using queues, retry mechanisms, replay processing, and workflow orchestration. Recovery orchestration services continuously monitor for stale transfers, missed processing events, and incomplete workflows to automatically initiate recovery processing when required.

The platform is designed to handle multiple failure scenarios including:

* Regional outages
* SFTP endpoint failures
* Storage service disruptions
* Workflow execution failures
* Queue backlogs or throttling
* Event delivery failures
* Metadata replication lag
* Large file transfer interruptions
* Cross-account integration failures
* Dependency service outages

To support operational resiliency, the platform integrates with enterprise observability and monitoring systems to provide:

* Transfer visibility
* Regional health monitoring
* Workflow monitoring
* Failure detection and alerting
* Replication monitoring
* Queue and processing visibility

Key resiliency mechanisms implemented within the platform include:

* Automated retry handling
* Dead-letter queue processing
* Replay-safe workflow execution
* Transaction deduplication controls
* Recovery orchestration workflows
* Distributed regional deployment
* Fault-isolated processing pipelines

Residual risks remain for certain scenarios such as in-flight uploads during regional failover, replication timing dependencies, and external AWS service outages. These risks are mitigated through replay operations, operational monitoring, and regional recovery procedures where applicable.
