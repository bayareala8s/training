#!/usr/bin/env python3
"""Generate remaining lab workbooks (3–15 except 2 which is hand-written)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def lab(
    slug: str,
    title: str,
    overview: str,
    scenario: str,
    architecture: str,
    objectives: list[str],
    prereq: str,
    aws: str,
    time: str,
    cost: str,
    setup: str,
    infra: str,
    app: str,
    integ: str,
    test: str,
    fail: str,
    obs: str,
    sec: str,
    questions: list[str],
    cleanup: str,
):
    body = f"""# {title}

## Lab Overview

{overview}

## Business Scenario

{scenario}

## Architecture

{architecture}

## Learning Objectives

{chr(10).join('- ' + o for o in objectives)}

## Prerequisites

{prereq}

## AWS Services Used

{aws}

## Estimated Time

{time}

## Estimated AWS Cost

{cost}

## Step 1 — Setup

{setup}

## Step 2 — Infrastructure

{infra}

## Step 3 — Application

{app}

## Step 4 — Integration

{integ}

## Step 5 — Testing

{test}

## Step 6 — Failure Testing

{fail}

## Step 7 — Observability

{obs}

## Step 8 — Security Review

{sec}

## Step 9 — Architecture Questions

{chr(10).join(f'{i}. {q}' for i, q in enumerate(questions, 1))}

## Step 10 — Cleanup

{cleanup}
"""
    path = ROOT / "labs" / slug / "README.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    print("wrote", path)


def main():
    lab(
        "lab-03-messaging",
        "Lab 3 — Enterprise messaging (SQS, DLQ, replay)",
        "Build Producer → SQS → Lambda → DynamoDB with a DLQ. Break it, inspect, fix, replay.",
        "Northbridge must process payment commands even when the poster is down. Commands are not broadcasts.",
        "Style: **Message**. See `diagrams/03-queue-architecture.md`.",
        ["Configure visibility vs function timeout.", "Send poison to DLQ.", "Replay after fix.", "Idempotent consumer."],
        "Module 3. Lab 2 optional.",
        "SQS, SQS DLQ, Lambda, DynamoDB, IAM, CloudWatch.",
        "3 hours.",
        "< $0.20 if destroyed. No Transfer Family.",
        "Copy `terraform/labs/lab-03-messaging/terraform.tfvars.example` to `terraform.tfvars`.",
        "`./scripts/lab_up.sh lab-03-messaging`",
        "`lambda/lab03_producer` and `lambda/lab03_consumer`. Consumer fails when `fail` is true or amount is the string `POISON`.",
        "Send a good message, then a poison message using the producer script in the lab folder.",
        "`python3 scripts/validate_lab.py lab-03-messaging`",
        "1. Poison message → DLQ.\n2. Shrink visibility in console (or tf) and send a slow message → duplicates.\n3. Replay from DLQ after removing POISON.",
        "Find correlation IDs on main queue vs DLQ. Alarm mentally: DLQ > 0.",
        "Queue policies: only producer send, only consumer receive. No `sqs:*` on `*`.",
        [
            "Is this an event or a command? Why?",
            "Why is FIFO not required for independent payment IDs?",
            "Write the inspect → fix → replay runbook in five lines.",
        ],
        "`./scripts/lab_down.sh lab-03-messaging`",
    )
    lab(
        "lab-04-pubsub",
        "Lab 4 — Pub/sub fan-out",
        "OrderCreated → SNS → inventory, notification, and analytics queues. Prove independence.",
        "Harbor checkout must not import email or analytics SDKs.",
        "Style: **Event/notification + queues**. `diagrams/04-pubsub-architecture.md`.",
        ["Fan-out with a queue per subscriber.", "Kill one consumer; others proceed.", "Optional filter for TEST orders."],
        "Module 4.",
        "SNS, SQS, Lambda, IAM.",
        "2.5 hours.",
        "< $0.20 destroyed.",
        "Copy tfvars example.",
        "`./scripts/lab_up.sh lab-04-pubsub`",
        "Three consumers in `lambda/lab04_*`.",
        "Publish one OrderCreated. Confirm three DynamoDB projections (or log lines).",
        "`python3 scripts/validate_lab.py lab-04-pubsub`",
        "Set notification Lambda reserved concurrency to 0. Publish again. Inventory still writes. Restore concurrency.",
        "Three log groups, one correlation ID.",
        "Notification role cannot write inventory items.",
        [
            "What experiment proves independence?",
            "When would EventBridge be a better bus than SNS?",
            "If analytics needs PII, how do you minimize the topic payload?",
        ],
        "`./scripts/lab_down.sh lab-04-pubsub`",
    )
    lab(
        "lab-05-events",
        "Lab 5 — EventBridge choreography",
        "OrderCreated → PaymentAuthorized → InventoryReserved → OrderCompleted.",
        "Harbor wants facts, not a hidden ESB process. Keep the saga visible in later capstones; this lab is choreography of facts.",
        "Style: **Event**. `diagrams/05-event-driven-architecture.md`.",
        ["PutEvents with schemas.", "Route by detail-type.", "Idempotent consumers.", "Discuss archive/replay without firing inventory twice."],
        "Module 5.",
        "EventBridge custom bus, rules, SQS or Lambda targets, DynamoDB.",
        "3.5 hours.",
        "< $0.30 destroyed. Custom event cost is tiny at lab volume.",
        "Copy tfvars.",
        "`./scripts/lab_up.sh lab-05-events`",
        "`lambda/lab05_*` plus `sample-data/events/*.json`.",
        "Put OrderCreated; observe the chain. Duplicate the same event id.",
        "`python3 scripts/validate_lab.py lab-05-events`",
        "Invalid schema event. Duplicate PaymentAuthorized. Optional: disable inventory rule and show payments still complete their fact.",
        "Trace one correlation ID across four functions.",
        "Only the order producer IAM can PutEvents of OrderCreated (lab may approximate with bus policy notes).",
        [
            "Which names are commands in disguise?",
            "When do you stop adding rules and start Step Functions?",
            "How would you replay *only* analytics?",
        ],
        "`./scripts/lab_down.sh lab-05-events`",
    )
    lab(
        "lab-06-file-transfer",
        "Lab 6 — Enterprise file transfer pipeline",
        "Partner → SFTP (optional) → Transfer Family → S3 → EventBridge → SQS → Lambda → destination, with validation, duplicates, metadata, audit, failures, notifications.",
        "A partner can only land a CSV at night. You still owe posting, ACK, and audit.",
        "Style: **File**. `diagrams/06-file-transfer-architecture.md`.",
        ["Landing prefixes as contracts.", "Checksum + duplicate detection.", "Quarantine vs accept.", "Catalog as the ops API.", "Cost-control the Transfer server."],
        "Module 6. SSH client optional.",
        "S3, EventBridge, SQS, Lambda, DynamoDB, SNS (email optional), Transfer Family **optional flag**.",
        "4–5 hours.",
        "S3/Lambda path: < $0.30. **Transfer Family is billed per hour while ONLINE.** Default Terraform flag `enable_transfer_family=false`. Enable only during the SFTP hour, then `terraform apply` to disable or destroy.",
        "Copy tfvars. Decide whether to enable Transfer Family. Prefer S3 put for the first pass.",
        "`./scripts/lab_up.sh lab-06-file-transfer`",
        "`lambda/lab06_validate`. Sample files in `sample-data/files/`.",
        "Upload a good CSV, a duplicate, a bad schema, a wrong checksum sidecar.",
        "`python3 scripts/validate_lab.py lab-06-file-transfer`",
        "Duplicate post attempt. Poison CSV. Optional: leave Transfer ONLINE and calculate weekend cost (then disable).",
        "Catalog items for each file; FileReceived vs FileQuarantined.",
        "Prefix isolation. KMS on the bucket. No public ACL.",
        [
            "At which state do you ACK POSTED?",
            "Why is ETag not enough integrity?",
            "How does Module 15 query this catalog?",
        ],
        "`./scripts/lab_down.sh lab-06-file-transfer` — confirm Transfer server is gone.",
    )
    lab(
        "lab-07-large-files",
        "Lab 7 — Large-file claim-check + status API",
        "API init → client uploads to S3 → event → pipeline → GET status. Do not send GB through the gateway.",
        "A partner uploads a multi-hundred-MB object. Mobile must not spin for the hash.",
        "Style: **File + API control plane**. `diagrams/09-large-file-architecture.md`.",
        ["Presigned upload to server-chosen key.", "202 + status resource.", "Claim-check events.", "Worker threshold discussion (Lambda vs Fargate)."],
        "Module 7. Use a small file in the lab; design for 10 GB in the ADR.",
        "API Gateway, Lambda, S3, EventBridge, DynamoDB.",
        "3 hours.",
        "< $0.30. Abort incomplete multipart via lifecycle.",
        "Copy tfvars.",
        "`./scripts/lab_up.sh lab-07-large-files`",
        "`lambda/lab07_init_upload`, `lab07_process`, `lab07_status`.",
        "POST /uploads, PUT to presigned URL with `sample-data/files/small.bin`, GET status until COMPLETED.",
        "`python3 scripts/validate_lab.py lab-07-large-files`",
        "Expire a presign (wait or shorten). Upload a checksum mismatch. Confirm FAILED status, not 200 on init.",
        "Status transitions in DynamoDB and logs.",
        "Presign cannot PUT to arbitrary keys. Job IDs unguessable. Authz on GET status.",
        [
            "Why not API Gateway for 25 GB?",
            "What is the claim check on the event?",
            "When do you choose Fargate over Lambda?",
        ],
        "`./scripts/lab_down.sh lab-07-large-files`",
    )
    lab(
        "lab-08-esb-modernization",
        "Lab 8 — Legacy ESB redesign + ADR",
        "You receive a legacy ESB architecture. You do **not** receive the answer. Produce keep/change/retire, strangler, risks, and a full ADR.",
        "Northbridge’s bus team has a six-week lead time. Digital wants events. Settlement is ISO on MQ. Marketing email is on the bus for historical reasons.",
        "As-is: `labs/lab-08-esb-modernization/as-is.md`. Target must use styles, not a new hub.",
        ["Inventory flows.", "Keep/change/retire table.", "Strangler waves.", "Dual-run for money.", "Complete ADR."],
        "Modules 8–9. Terraform optional.",
        "None required. Optional: reuse Lab 5 bus for a single strangler slice.",
        "3–4 hours (architecture). +2 hours optional build.",
        "$0 unless you deploy a slice.",
        "Read `as-is.md` and `templates/adr.md`.",
        "None required.",
        "None required.",
        "Write `submissions/lab-08/adr.md` and a target diagram.",
        "`python3 scripts/validate_lab.py lab-08-esb-modernization`",
        "Describe the incident if you strangler settlement first with no dual-run.",
        "How will you see drift during dual-run?",
        "What identity replaces the bus service account?",
        [
            "What stays on an adapter for 18 months and why?",
            "What is the policy for *new* maps?",
            "Defend EventBridge vs SNS vs SQS for each remaining flow.",
        ],
        "None, or destroy optional slice.",
    )
    lab(
        "lab-11-chaos",
        "Chaos lab — break integrations on purpose",
        "Deliberately induce Lambda failure, API timeout, consumer unavailable, invalid message, duplicate event, duplicate file, dependency outage. Diagnose with telemetry, then recover.",
        "You are on-call for Harbor + Northbridge lab platforms.",
        "Reuse stacks from labs 2–7. See Module 11.6 playbook.",
        ["Break with a hypothesis.", "Observe logs/metrics/DLQ.", "Fix.", "Prove an alarm exists or add one."],
        "Labs 2–7 deployed (you may do a subset). Module 11.",
        "Whatever you already deployed. Do not create NAT for chaos.",
        "3–4 hours.",
        "Same as underlying labs. Destroy when done.",
        "Pick at least four scenarios from `labs/lab-11-chaos/scenarios.md`.",
        "Use existing Terraform. Optional: reserved concurrency = 0.",
        "Inject poison via sample-data.",
        "Record notes in `submissions/lab-11/notes.md`.",
        "`python3 scripts/validate_lab.py lab-11-chaos` (checks notes file length).",
        "All seven scenarios if time allows. Minimum four.",
        "If nothing paged, add the alarm—that is the deliverable.",
        "Do not use AdministratorAccess to “make chaos easier.”",
        [
            "Which failure was silent, and which metric would catch it?",
            "How many retry layers fired?",
            "What is the user-visible degradation?",
        ],
        "Bring concurrency back. Destroy stacks.",
    )
    lab(
        "lab-12-security",
        "Security lab — insecure architecture",
        "Start from an intentionally weak stack. Find and fix identity, encryption, secrets, public access, and audit gaps.",
        "A contractor “got it working” with `*` policies and a public bucket.",
        "`diagrams/10-integration-security.md`. Findings table required.",
        ["Least privilege.", "KMS.", "No public write.", "Secrets not in git.", "CloudTrail awareness."],
        "Module 12. Lab 2 knowledge.",
        "IAM, S3, KMS, Lambda, optional Secrets Manager.",
        "3 hours.",
        "< $0.30 destroyed.",
        "Apply lab-12, which **starts insecure** (`insecure=true` default in example tfvars). Then tighten.",
        "`./scripts/lab_up.sh lab-12-security` then edit Terraform until validate passes.",
        "Do not add security theater. Fix data paths.",
        "Attempt to list other prefixes as the partner role—should fail after the fix.",
        "`python3 scripts/validate_lab.py lab-12-security` — FAIL until public access blocked and policies tightened.",
        "Try the pre-fix exploit paths documented in the lab notes (in your account only).",
        "CloudTrail / access logs conceptually; app audit of who invoked.",
        "Entire lab is a security review.",
        [
            "Why is encryption-on plus * IAM still a fail?",
            "Would an agent with this role be acceptable?",
            "Cross-account: what is ExternalId for?",
        ],
        "`./scripts/lab_down.sh lab-12-security`",
    )
    lab(
        "lab-13-observability",
        "Lab — Integration operations dashboard",
        "Trace User → API → Event → Queue → Lambda → DB. Dashboard: transactions, success, failure, latency, queue depth, DLQ, file counts, processing duration.",
        "Support cannot find a checkout. You will make the path visible.",
        "`diagrams/11-integration-observability.md`.",
        ["Correlation ID everywhere.", "JSON logs.", "Business vs technical metrics.", "Dashboard as code.", "DLQ widget."],
        "Module 13. Prefer Lab 2+3 running, or use the bundled mini-stack in lab-13 Terraform.",
        "CloudWatch dashboard, log groups, metric filters, alarms.",
        "3 hours.",
        "Log ingestion is the main cost—keep volume tiny; set short retention (3–7 days).",
        "Copy tfvars.",
        "`./scripts/lab_up.sh lab-13-observability`",
        "Emit EMF or metric filters from a small generator Lambda included in the stack.",
        "Run the generator; open the dashboard URL from Terraform output.",
        "`python3 scripts/validate_lab.py lab-13-observability`",
        "Stop emitting success metrics and emit failures; confirm widgets and optional alarm.",
        "The dashboard *is* this step.",
        "Redact payloads. No customerId as a metric dimension.",
        [
            "Which widget would you show a VP vs an SRE?",
            "Why is 202 rate a poor settlement SLO?",
            "How does the Module 15 agent use these names?",
        ],
        "`./scripts/lab_down.sh lab-13-observability`",
    )
    lab(
        "lab-15-ai-agent",
        "AI lab — Enterprise integration operations agent",
        "Build tools: file status, failed transactions, explain errors, queue depth, processing status, recommend remediation, request reprocess. Reads execute when authorized. Writes require HITL.",
        "Ops wants ChatGPT energy. You will give them a **governed tool channel** instead of a database user.",
        "`diagrams/12-ai-agent-integration.md`. Forbidden: LLM → DynamoDB/S3 data plane.",
        ["Tool schemas.", "Catalog reads.", "Approval workflow for reprocess.", "Audit events.", "Optional Bedrock; default mock planner for cost."],
        "Module 15. Lab 6 catalog concepts. Lab 3 queue depth.",
        "Lambda tools, DynamoDB catalog + approvals, SQS optional, Step Functions optional, Bedrock **optional**.",
        "4 hours.",
        "Mock agent: < $0.40. Bedrock tokens extra—keep off unless you opt in (`enable_bedrock=false`).",
        "Copy tfvars. Keep Bedrock false unless your account is enabled.",
        "`./scripts/lab_up.sh lab-15-ai-agent`",
        "`lambda/lab15_tools` plus `scripts/ops_agent.py` (mock planner that can only call HTTP tools).",
        "Ask: file status, failed tx count, queue depth. Then request reprocess and approve via the approval API.",
        "`python3 scripts/validate_lab.py lab-15-ai-agent`",
        "Try a write without approval — must fail. Try a tool not in the allow-list — must fail.",
        "Trace user → tool → API → catalog. Token/cost metric if Bedrock on.",
        "Tool IAM is GetItem on catalog, not Scan *. No s3:GetObject on payload prefixes for the agent role.",
        [
            "Draw the forbidden vs required architectures from memory.",
            "Is MCP automatically safe?",
            "Who cannot approve their own reprocess?",
        ],
        "`./scripts/lab_down.sh lab-15-ai-agent`",
    )


if __name__ == "__main__":
    main()
