# Appendix – Resiliency & Reliability

## Purpose

This appendix explains how the Enterprise File Transfer (EFT) platform continues operating during failures, outages, and processing interruptions. The design focuses on protecting customer data, avoiding duplicate file delivery, and restoring services in a controlled and predictable manner.

The platform uses multiple recovery layers including retries, queue-based buffering, regional failover, monitoring, and operational recovery procedures.

---

# Regional Failover Design

The EFT platform operates across two AWS GovCloud regions using a primary and secondary region model. The primary region handles normal traffic while the secondary region remains available for failover when needed.

Failover is intentionally controlled by operations teams instead of being fully automatic. This reduces the risk of unnecessary failovers caused by temporary network or infrastructure issues.

During failover:

* Traffic is redirected from the primary region to the secondary region
* DNS and internal routing records are updated
* Processing services are enabled in the secondary region
* Processing services in the primary region are disabled

Both DMZ SFTP endpoints and internal SFTP endpoints fail over together as a single operational activity. Independent failover of individual endpoint types is not supported because it could create inconsistent processing behavior.

---

# Failure Detection and Monitoring

The platform continuously monitors system health and transfer activity before raising operational alerts.

CloudWatch monitoring combines multiple signals including:

* Service health checks
* Transfer processing activity
* Queue depth monitoring
* Workflow execution status
* File ingestion activity

For external SFTP services, Route53 health checks monitor endpoint connectivity. Internal SFTP services use CloudWatch metrics because those endpoints are not internet-facing.

Additional monitoring exists for:

* Lambda execution failures
* ECS task failures
* SQS queue growth
* Step Functions workflow failures
* DynamoDB replication lag
* Poller execution activity
* RecoveryOrchestrator health status

SNS notifications alert operations teams when configured thresholds are exceeded.

---

# Failback Process

After the primary region becomes healthy again, operations teams perform a controlled failback process.

Failback occurs in two stages:

1. New inbound traffic is redirected back to the primary region
2. Remaining in-flight processing in the secondary region is allowed to complete safely

Once processing queues are drained and active workflows complete, processing services are re-enabled in the primary region.

This controlled approach reduces the risk of duplicate processing or incomplete transfers during recovery operations.

---

# Split-Brain Prevention

The platform is designed to prevent situations where both regions process the same workload simultaneously.

To reduce this risk:

* Only one region actively processes workloads at a time
* Failover updates all related services together
* Each region maintains independent processing queues and workflows
* Shared services are limited to metadata replication and object replication services

The design also uses multiple validation checks before outbound delivery occurs.

Each region maintains a local deduplication table to prevent duplicate processing within the region. A shared TransferTracker table provides an additional validation step before files are delivered externally.

Conditional database updates are used to ensure the same file cannot be delivered twice.

---

# SQS Retry and Recovery Behavior

Amazon SQS acts as the primary buffering and retry layer for the platform.

If processing temporarily fails, messages remain in the queue and are retried automatically after the visibility timeout expires.

If retries continue to fail after configured retry limits are reached, the message is moved to a Dead Letter Queue (DLQ) for investigation.

This design allows the platform to recover automatically from most temporary failures without manual intervention.

---

# RecoveryOrchestrator Service

The RecoveryOrchestrator service provides an additional recovery layer for failures not handled through standard retries.

The service periodically scans for:

* Files stuck in staging locations
* Transfers remaining in-progress for extended periods
* Missing processing notifications
* Incomplete failover states
* Stale or orphaned transfers

When issues are identified, transfers are safely re-queued for processing.

This mechanism helps recover transfers that could otherwise remain incomplete after outages or interrupted processing events.

---

# Handling Large File Transfers

Large file transfers are processed using ECS Fargate tasks.

If a processing task fails because of timeout, memory pressure, or connectivity issues, Step Functions automatically retries the operation.

Files remain stored in Amazon S3 throughout processing so that data is not lost even if compute services fail.

CloudWatch alarms monitor large file transfer workflows and ECS task execution failures to provide operational visibility.

---

# DynamoDB Replication and Deduplication

DynamoDB Global Tables replicate metadata between regions using near real-time replication.

Small replication delays can occur during failover events, so the design does not rely entirely on replicated metadata for duplicate prevention.

Each region maintains local transaction validation controls while the shared TransferTracker table provides final outbound validation before delivery occurs.

This layered approach reduces the risk of duplicate file delivery across regions.

---

# Poller Recovery

The SFTP poller service exists in both regions, but only one region actively polls external systems at a time.

During failover:

* The primary poller is disabled
* The secondary poller is enabled

This prevents duplicate polling and duplicate ingestion from external SFTP servers.

CloudWatch alarms monitor poller activity and queue behavior to detect stalled or failed polling operations.

---

# S3 and Regional Failure Handling

Amazon S3 provides durable storage for inbound and processing files.

S3 Replication Time Control (RTC) replicates completed files between regions.

If a regional outage occurs during an active upload, partially uploaded files may not replicate because replication only starts after upload completion. In those situations, customers may need to reconnect and upload the file again after failover completes.

Completed files already stored in S3 remain protected and available in the secondary region.

---

# Reliability Summary

The EFT platform uses a layered resiliency approach based on:

* Queue-based buffering
* Automatic retries
* Controlled regional failover
* Recovery workflows
* Monitoring and operational visibility
* Duplicate prevention controls

Most temporary failures recover automatically through retries and queue-based processing. Larger outages are handled through controlled operational failover procedures designed to minimize customer impact and maintain processing integrity.
