"""Step-by-step flow definitions for Stripe payment idempotency diagrams.

Used by generate_stripe_aws_architecture_pngs.py (edge labels) and
inject_stripe_diagram_steps.py (markdown step tables).
"""

from __future__ import annotations

# Each entry: list of (step_number, short_label, explanation)
DIAGRAM_STEPS: dict[str, list[tuple[str, str, str]]] = {
    "aws-deployment-context": [
        ("1", "Client request", "Web/mobile user initiates checkout with `Idempotency-Key` header."),
        ("2", "Edge routing", "CloudFront serves static UI; API traffic passes WAF and Route 53 to ALB."),
        ("3", "Load balance", "ALB routes to healthy ECS Fargate checkout-api task."),
        ("4", "Claim idempotency key", "ECS inserts `processing` row in Aurora (`idempotency_keys`)."),
        ("5", "Load Stripe secret", "ECS fetches `sk_live_*` from Secrets Manager."),
        ("6", "Call Stripe", "POST `payment_intents` with same `Idempotency-Key` (25s timeout)."),
        ("7", "Webhook ingest", "Stripe sends event → webhook worker enqueues to SQS."),
        ("8", "Async process", "Consumer dedupes `event_id`, updates orders/charges in Aurora."),
        ("9", "Sweeper heal", "Lambda queries stuck `processing` rows; reconciles with Stripe."),
        ("10", "Reconciliation", "Hourly Lambda compares Aurora ledger vs Stripe settlements."),
        ("11", "Observability", "Structured logs and metrics emitted to CloudWatch."),
    ],
    "interview-aws-reference": [
        ("1", "Client → CloudFront", "TLS-terminated entry; static assets cached."),
        ("2", "CloudFront → ALB", "API path forwarded to Application Load Balancer."),
        ("3", "ALB → ECS", "Route to checkout service; validate idempotency key format."),
        ("4", "ECS → Aurora", "Atomic claim or cache hit on `idempotency_keys`."),
        ("5", "ECS → Stripe", "PaymentIntent create with merchant idempotency key."),
        ("6", "Stripe → SQS", "Webhook buffered for at-least-once delivery."),
        ("7", "SQS → Webhook Lambda", "Dedupe `event_id`; idempotent order update."),
        ("8", "EventBridge → Reconciliation", "Scheduled hourly ledger vs Stripe diff."),
    ],
    "interview-timeout-sequence": [
        ("1", "First POST", "Client sends charge with `Idempotency-Key: abc`."),
        ("2", "DB lookup", "API begins transaction; inserts `processing`."),
        ("3", "Gateway charge", "Stripe authorizes; success at gateway."),
        ("4", "504 timeout", "Response lost — client in **ambiguous** state."),
        ("5", "Retry same key", "Client retries with **identical** key (not new UUID)."),
        ("6", "Dedup hit", "DB returns `completed`; cached 200 — no second charge."),
    ],
    "aws-whiteboard": [
        ("1", "Sync path", "Client → CloudFront → ALB → ECS API."),
        ("2", "Persist state", "Write `idempotency_keys` + ledger rows in Aurora."),
        ("3", "Stripe call", "External authorization — **UNKNOWN zone** if response lost."),
        ("4", "Webhook async", "Stripe event → SQS → worker updates ledger."),
        ("5", "Reconciliation", "EventBridge cron compares ledger ↔ Stripe (backstop)."),
    ],
    "aws-sizing-5k": [
        ("1", "ALB ingress", "5K req/s TLS termination and path routing."),
        ("2", "ECS scale-out", "10–30 Fargate tasks; auto-scale on p99 latency."),
        ("3", "Aurora writes", "Idempotency + ledger strong consistency (writer)."),
        ("4", "DynamoDB optional", "High-QPS idempotency shard if Aurora contends."),
        ("5", "NAT egress", "Outbound HTTPS to `api.stripe.com`."),
    ],
    "sticky-routing": [
        ("1", "Read path", "Route 53 latency routing → CloudFront catalog (geo)."),
        ("2", "Write path", "Route 53 failover → **single** ALB us-east-1 only."),
        ("3", "Checkout", "ECS processes payment; Aurora primary is sole writer."),
    ],
    "c4-logical": [
        ("1", "Ingress", "Clients hit API Gateway / load balancer."),
        ("2", "Orchestrate", "Payment Service claims idempotency key."),
        ("3", "Persist", "Write idempotency store + ledger atomically."),
        ("4", "Events", "Outbox publishes domain events (deduped)."),
        ("5", "Stripe", "External charge with same idempotency key."),
        ("6", "Webhook", "Async confirmation updates ledger."),
        ("7", "Reconcile", "Worker diffs ledger vs Stripe settlements."),
    ],
    "vpc-production-full": [
        ("1", "User → edge", "CloudFront + WAF + Route 53 health-checked routing."),
        ("2", "ALB → ECS", "Cross-AZ load balance to checkout-api tasks."),
        ("3", "Claim key", "INSERT `idempotency_keys` on Aurora writer."),
        ("4", "Secrets", "Fetch Stripe API key from Secrets Manager."),
        ("5", "NAT → Stripe", "Egress via NAT Gateway; POST with Idempotency-Key."),
        ("6", "Webhook queue", "Stripe webhook → ALB → SQS → ECS consumer."),
        ("7", "Sweeper", "Lambda heals `processing` rows every 30s."),
        ("8", "Reconcile", "EventBridge triggers hourly Stripe vs ledger job."),
        ("9", "Replica sync", "Aurora reader + cross-AZ sync for HA."),
    ],
    "pattern-a": [
        ("1", "Load UI", "CloudFront + S3 serves checkout SPA."),
        ("2", "Checkout API", "ECS receives POST with idempotency key."),
        ("3", "Persist order", "Aurora stores order + key **before** Stripe call."),
        ("4", "Stripe charge", "Same key passed to Stripe global dedup cache."),
        ("5", "Webhook", "Stripe confirms → ECS updates order status."),
    ],
    "pattern-b": [
        ("1", "Internal call", "Billing/marketplace services call Payment API."),
        ("2", "API gateway", "ALB authenticates internal service."),
        ("3", "Dedup claim", "Payment API writes idempotency store."),
        ("4", "Ledger", "Immutable charge row created."),
        ("5", "Stripe", "External gateway with platform-owned keys."),
    ],
    "state-machine": [
        ("1", "Received", "POST arrives with `Idempotency-Key`."),
        ("2", "Validated", "Schema, auth, request hash computed."),
        ("3", "Claimed", "INSERT `processing` (unique constraint)."),
        ("4", "Gateway pending", "Call Stripe outside long DB transaction."),
        ("5a", "Completed", "Cache response; terminal success."),
        ("5b", "Failed", "Cache error (e.g. 402); terminal failure."),
        ("R1", "Dedup hit", "Retry returns cached response — skip gateway."),
        ("R2", "Conflict", "Same key, different body → 422."),
        ("R3", "In-flight", "Concurrent duplicate → 409 or short poll."),
    ],
    "data-aurora": [
        ("1", "ECS write", "All checkout tasks write to single Aurora writer."),
        ("2", "Sync replica", "In-region readers serve consistent reads if needed."),
        ("3", "DR replicate", "Async replication to us-west-2 Global DB / replica."),
    ],
    "data-dynamodb": [
        ("1", "Conditional put", "DynamoDB `PutItem` claims idempotency key atomically."),
        ("2", "Ledger write", "Aurora stores orders/charges (relational integrity)."),
        ("3", "Audit stream", "DynamoDB Streams → Lambda metrics/audit."),
    ],
    "request-path-sequence": [
        ("1", "HTTPS ingress", "Client POST `/api/checkout` via CloudFront."),
        ("2", "WAF filter", "Rate limit and OWASP rule check."),
        ("3", "ALB route", "Forward to healthy ECS task."),
        ("4", "Claim key", "INSERT `idempotency_keys` status=`processing`."),
        ("5", "Get secret", "Secrets Manager returns Stripe API key."),
        ("6", "Stripe API", "POST `payment_intents` with Idempotency-Key."),
        ("7", "Persist result", "UPDATE idempotency + INSERT charge."),
        ("8", "Respond", "200 success or 504 ambiguous to client."),
    ],
    "ambiguous-timeout-sequence": [
        ("1", "First attempt", "INSERT `processing`; call Stripe."),
        ("2", "Timeout", "504 to client; row stays `processing`."),
        ("3", "Retry", "Client retries **same key**."),
        ("4", "Poll Stripe", "Query PI or retry POST — Stripe dedupes."),
        ("5", "Complete", "UPDATE `completed`; return cached 200."),
    ],
    "webhook-sqs": [
        ("1", "Stripe POST", "Webhook hits ALB `/api/webhooks/stripe`."),
        ("2", "Verify sig", "Validate `Stripe-Signature` HMAC."),
        ("3", "Enqueue", "Push raw event to SQS (fast ACK)."),
        ("4", "Consume", "Worker pulls message; INSERT `event_id` dedup."),
        ("5", "Update order", "Idempotent `UPDATE orders SET paid`."),
        ("6", "DLQ", "Poison messages → DLQ → CloudWatch alarm."),
    ],
    "reconciliation": [
        ("1", "Schedule", "EventBridge cron `rate(1 hour)`."),
        ("2", "Fetch ledger", "Lambda reads Aurora charges for window."),
        ("3", "Fetch Stripe", "List Balance Transactions from Stripe API."),
        ("4", "Diff", "Join on `stripe_pi_id`; flag gaps."),
        ("5", "Report", "Write CSV to S3; emit `reconciliation_gap_count`."),
        ("6", "Alert", "SNS → PagerDuty on any mismatch."),
    ],
    "client-spa": [
        ("1", "Generate key", "Browser stores UUID in `sessionStorage` (once per checkout)."),
        ("2", "POST checkout", "SPA calls ALB with `Idempotency-Key`."),
        ("3", "Process", "ECS claims key; calls Stripe."),
        ("4", "504 poll", "On timeout, return 202; SPA polls `GET /orders/{id}`."),
    ],
    "single-region-multi-az": [
        ("1", "DNS", "Route 53 resolves to regional ALB."),
        ("2", "Multi-AZ LB", "ALB distributes across AZ-a/b/c."),
        ("3", "ECS tasks", "Stateless workers in each AZ."),
        ("4", "Aurora writer", "Single writer; sync replicas in other AZs."),
        ("5", "NAT egress", "Stripe API calls via NAT Gateway."),
    ],
    "multi-region-dr": [
        ("1", "Normal", "Route 53 → us-east-1 ALB → ECS → Aurora primary."),
        ("2", "Replicate", "Aurora Global DB streams to us-west-2."),
        ("3", "Detect failure", "Health checks fail; enable `payments_fail_closed`."),
        ("4", "Promote", "West Aurora promoted to writer."),
        ("5", "Failover DNS", "Route 53 → us-west-2 ALB."),
        ("6", "Retry same key", "Clients retry; Stripe returns cached PI."),
    ],
    "active-passive-vs-aa": [
        ("1", "Recommended writes", "All payment writes → single region ALB."),
        ("2", "CDN reads", "CloudFront serves catalog globally."),
        ("3", "Anti-pattern", "Dual-region writes without global dedup."),
        ("4", "Risk", "DynamoDB Global Tables lag → duplicate charges."),
    ],
    "webhook-dr": [
        ("1", "Stripe webhook", "Global delivery to Route 53 endpoint."),
        ("2", "Primary region", "East ALB → SQS → Lambda → Aurora dedup."),
        ("3", "Failover", "Route 53 flips to west ALB + SQS."),
        ("4", "Dedup", "Same `event_id` processed once across regions."),
    ],
    "security-perimeter": [
        ("1", "DDoS", "Shield Standard at edge."),
        ("2", "WAF", "Rate limit, geo block, OWASP rules."),
        ("3", "TLS", "CloudFront TLS 1.3 termination."),
        ("4", "VPC isolate", "ECS in private subnets; SG allows ALB only."),
        ("5", "IAM + secrets", "Task role least privilege; Secrets Manager for Stripe key."),
        ("6", "Encrypt", "Aurora encrypted with KMS."),
        ("7", "Audit", "CloudTrail + CloudWatch Logs → S3 archive."),
    ],
    "observability": [
        ("1", "Emit logs", "ECS structured JSON per charge."),
        ("2", "CloudWatch", "Logs + custom metrics dashboards."),
        ("3", "Archive", "S3 long-term storage."),
        ("4", "Alert", "Alarms → SNS → PagerDuty."),
        ("5", "Query", "Athena ad-hoc audit on S3 logs."),
    ],
    "sweeper": [
        ("1", "Trigger", "EventBridge every 30 seconds."),
        ("2", "Acquire lease", "DynamoDB lease / advisory lock (singleton)."),
        ("3", "Scan stuck", "SELECT `processing` older than 30s."),
        ("4", "Query Stripe", "GET PaymentIntent by metadata/key."),
        ("5", "Heal row", "Mark `completed` or `failed`; emit metric."),
    ],
    "dr-game-day": [
        ("1", "Inject failure", "AWS FIS stops east ECS/RDS."),
        ("2", "Fail closed", "SSM `payments_fail_closed=true`."),
        ("3", "Promote DB", "On-call promotes Aurora west."),
        ("4", "DNS flip", "Route 53 → west ALB."),
        ("5", "Synthetic traffic", "100 checkouts with pre-set keys."),
        ("6", "Verify", "Exactly one `pi_xxx` per key in Stripe."),
    ],
    "single-region-az-failover": [
        ("1", "AZ-a fails", "Primary AZ becomes unreachable."),
        ("2", "ALB drain", "Unhealthy targets removed from rotation."),
        ("3", "ECS reschedule", "Tasks spin up in AZ-b and AZ-c."),
        ("4", "Aurora failover", "Writer promoted to sync replica (~30–120s)."),
        ("5", "Client retry", "Same idempotency key → dedup hit or Stripe cache."),
    ],
    "dr-failover-sequence": [
        ("1", "Detect", "Region impairment; PagerDuty alert."),
        ("2", "Fail closed", "SSM `payments_fail_closed=true`."),
        ("3", "Promote", "Detach/promote Aurora Global DB secondary."),
        ("4", "Scale west", "ECS tasks 0 → production count."),
        ("5", "DNS failover", "Route 53 → us-west-2 ALB."),
        ("6", "Resume", "Disable fail closed; clients retry same keys."),
        ("7", "Stripe dedup", "Same Idempotency-Key returns cached PaymentIntent."),
    ],
    "dynamodb-global-antipattern": [
        ("1", "East write", "ECS writes idempotency key to local region."),
        ("2", "West write", "Concurrent write before replication completes."),
        ("3", "Replication lag", "1–30s Global Tables delay."),
        ("4", "Duplicate risk", "Both regions may call Stripe with different keys."),
    ],
    "authority-failover": [
        ("1", "Local DB", "Merchant idempotency store — may lag on async DR."),
        ("2", "Stripe cache", "Global 24h idempotency — retry same key."),
        ("3", "Reconciliation", "Hourly backstop heals crash-window gaps."),
    ],
    "component-failover": [
        ("1", "ALB", "Removes unhealthy AZ targets automatically."),
        ("2", "ECS", "Replaces crashed tasks (stateless)."),
        ("3", "Aurora", "Auto-failover writer to sync replica."),
        ("4", "Fail closed", "SSM flag during promotion uncertainty."),
        ("5", "Stripe retry", "Same Idempotency-Key on all retries."),
        ("6", "Sweeper", "Heals orphaned `processing` rows."),
    ],
    "active-active-sequence": [
        ("1", "East charge", "POST with key `ord_991`."),
        ("2", "Stripe caches", "PI created; key stored globally."),
        ("3", "Partition/lag", "West has no dedup row yet."),
        ("4", "Safe retry", "Same key to Stripe → cached PI."),
        ("5", "Bug retry", "New key → **duplicate charge**."),
    ],
    "test-environment": [
        ("1", "CI tests", "Unit/integration in pipeline."),
        ("2", "Staging deploy", "ECS + Aurora in isolated VPC."),
        ("3", "Stripe test mode", "Test keys in Secrets Manager."),
        ("4", "Load test", "k6 from EC2 → ALB at 5K QPS."),
        ("5", "Chaos", "FIS kills tasks / Aurora failover."),
        ("6", "DR drill", "Route 53 failover + same-key verification."),
    ],
    "production-readiness": [
        ("1", "Network", "VPC 3-AZ private subnets validated."),
        ("2", "Data", "Aurora Multi-AZ sync replication."),
        ("3", "Scale", "5K QPS load test passed."),
        ("4", "Secrets", "No keys in environment variables."),
        ("5", "Async", "SQS + DLQ webhooks operational."),
        ("6", "Reconcile", "EventBridge hourly job running."),
        ("7", "Alerts", "CloudWatch alarms → PagerDuty."),
        ("8", "DR", "Game day completed; RPO/RTO documented."),
        ("9", "E2E", "Same-key retry → single PaymentIntent verified."),
        ("10", "Fail closed", "SSM flag tested during promotion."),
    ],
    "gantt-rollout": [
        ("1", "Week 1", "VPC, ALB, Aurora, ECS cluster."),
        ("2", "Week 2–3", "Idempotency schema + Stripe adapter."),
        ("3", "Week 4", "SQS webhooks + consumer."),
        ("4", "Week 6", "EventBridge reconciliation."),
        ("5", "Week 7", "FIS chaos + DR game day."),
        ("6", "Week 8", "Route 53 weighted canary → 100%."),
    ],
}


def step_table_markdown(diagram_id: str) -> str:
    steps = DIAGRAM_STEPS.get(diagram_id)
    if not steps:
        return ""
    lines = [
        "",
        "**Step-by-step flow:**",
        "",
        "| Step | Action | Explanation |",
        "|------|--------|-------------|",
    ]
    for num, action, explanation in steps:
        lines.append(f"| **{num}** | {action} | {explanation} |")
    lines.append("")
    return "\n".join(lines)


def edge_label(step: str, action: str) -> str:
    return f"{step}. {action}"
