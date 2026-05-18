# Appendix – Resiliency & Reliability

## Purpose

This appendix describes how the Enterprise File Transfer (EFT) platform handles failures, regional outages, retries, recovery, and failover operations. The design focuses on protecting customer data, preventing duplicate processing, and keeping file transfers operational during infrastructure or application failures.

The platform runs across two AWS GovCloud regions using an active/warm-standby design. The primary region handles normal traffic while the secondary region remains ready for failover when required.

---

# Regional Failover Design

The platform supports manual regional failover for both DMZ and internal SFTP services. Failover is intentionally operator-controlled to avoid unnecessary failovers caused by temporary network or service issues.

When failover occurs, traffic is moved from the primary region to the secondary region using the operational failover script. The script updates public DNS records, internal PHZ records, scheduler states, and recovery services together. Both DMZ and internal SFTP endpoints always fail over together. Independent failover of only one endpoint type is not supported because that could create split-brain processing conditions.

The failover process also enables processing services in the secondary region and disables services that should no longer run in the primary region.

---

# Failure Detection

The platform uses multiple monitoring signals before raising an operational alert. CloudWatch composite alarms combine health checks, transfer activity, and processing metrics to confirm a real outage before escalation occurs.

For external SFTP services, Route53 TCP health checks monitor connectivity while Transfer Family metrics monitor file activity. Internal SFTP services use CloudWatch metrics such as error counts and missing upload events because the internal endpoints are not internet-facing.

Additional monitoring exists for:

* Lambda failures
* SQS queue depth
* Step Functions execution failures
* DynamoDB replication lag
* Poller activity
* ECS task failures
* RecoveryOrchestrator execution health

SNS notifications alert the operations team when thresholds are exceeded.

---

# Failback Process

After the primary region becomes healthy again, operators perform failback using the failback action of the same operational script.

Failback occurs in two stages. First, new traffic is redirected back to the primary region. During this time, the secondary region continues processing any remaining in-flight work. Once queues are drained and active Step Functions executions complete, processing services are fully re-enabled in the primary region.

This approach prevents files from being processed twice during failback.

---

# Split-Brain Prevention

The architecture is designed to prevent split-brain conditions where two regions process the same workload independently.

The failover script always updates both DMZ and internal endpoints together in a single operation. There are no separate failover scripts for individual endpoints.

Each region has its own processing pipeline with separate SQS queues, Lambda functions, and Step Functions workflows. Shared services are limited to DynamoDB Global Tables and S3 cross-region replication.

Duplicate delivery protection is handled in multiple layers. Regional TransactionDedup tables prevent duplicate processing inside a region, while the TransferTracker global table prevents duplicate outbound deliveries across regions.

---

# SQS Retry and Recovery Behavior

Amazon SQS acts as the primary resiliency buffer for the platform. Messages remain in the queue until processing succeeds. If a Lambda function fails or times out, the message becomes visible again after the visibility timeout expires and is retried automatically.

If processing continues to fail after the configured retry limit, the message is moved to a Dead Letter Queue (DLQ) for investigation.

This design prevents data loss during temporary failures and allows processing to recover automatically without operator involvement in most cases.

---

# RecoveryOrchestrator

The RecoveryOrchestrator service provides an additional recovery layer for failures not handled by standard retries.

The RecoveryOrchestrator periodically scans for:

* Files stuck in staging buckets
* Transfers marked as “in-progress” for too long
* Missing EventBridge notifications
* Incomplete failover states

When stale or orphaned transfers are found, the files are safely re-queued for processing.

This mechanism helps recover transfers that could otherwise remain incomplete after failover events or unexpected processing interruptions.

---

# Handling Large File Transfers

Large files are processed using ECS Fargate tasks. If a task fails because of timeout, memory issues, or destination connectivity problems, Step Functions retries the operation automatically.

If retries continue to fail, the workflow can fail over to a secondary destination when configured. Files remain stored in Amazon S3 during the entire process, so data is not lost even if compute processing fails.

CloudWatch alarms monitor ECS task failures and workflow execution failures to provide operational visibility.

---

# DynamoDB Replication and Deduplication

DynamoDB Global Tables replicate metadata between both regions with near real-time replication. Small replication delays can occur during failover events, so the design avoids relying only on replicated state for deduplication.

Each region maintains its own TransactionDedup table to prevent duplicate processing locally. The TransferTracker global table provides the final validation step before delivery to external destinations.

Conditional DynamoDB updates are used to ensure the same file cannot be delivered twice.

---

# Poller Recovery

The SFTP poller service runs in both regions but only one region is active at a time. During failover, the primary poller is disabled and the secondary poller is enabled.

This prevents duplicate polling and duplicate ingestion from external SFTP servers.

CloudWatch alarms monitor poller execution activity and queue depth to detect failures or stalled processing.

---

# S3 and Regional Failure Handling

Amazon S3 provides durable storage for all inbound and processing files. S3 Replication Time Control (RTC) replicates completed objects between regions.

If a regional outage occurs during an active upload, partially uploaded files may not replicate because S3 replication only occurs after upload completion. In those cases, customers must reconnect and re-upload the file after failover completes.

Completed files already stored in S3 remain protected and available in the secondary region.

---

# VPC Endpoint and Infrastructure Failures

Lambda and ECS services access AWS services through VPC endpoints. Interface endpoints are deployed across multiple Availability Zones to reduce the risk of endpoint outages.

Gateway endpoints for S3 and DynamoDB are highly available by design. If a VPC endpoint issue occurs, processing for affected workflows may pause until AWS infrastructure connectivity is restored.

CloudWatch metrics and VPC Flow Logs provide operational visibility into connectivity failures.

---

# Reliability Summary

The EFT platform uses a layered resiliency design based on queues, retries, regional isolation, monitoring, and controlled failover procedures.

The design focuses on:

* Protecting completed transfers
* Preventing duplicate delivery
* Recovering in-flight processing safely
* Limiting operational risk during failover
* Providing clear operational visibility

Most transient failures recover automatically through retries and queue-based processing. Larger failures such as regional outages are handled through controlled operational failover procedures designed to maintain processing integrity and minimize customer impact.
