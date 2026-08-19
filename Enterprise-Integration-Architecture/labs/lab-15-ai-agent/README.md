# AI lab — Enterprise integration operations agent

## Lab Overview

Build tools: file status, failed transactions, explain errors, queue depth, processing status, recommend remediation, request reprocess. Reads execute when authorized. Writes require HITL.

## Business Scenario

Ops wants ChatGPT energy. You will give them a **governed tool channel** instead of a database user.

## Architecture

`diagrams/12-ai-agent-integration.md`. Forbidden: LLM → DynamoDB/S3 data plane.

## Learning Objectives

- Tool schemas.
- Catalog reads.
- Approval workflow for reprocess.
- Audit events.
- Optional Bedrock; default mock planner for cost.

## Prerequisites

Module 15. Lab 6 catalog concepts. Lab 3 queue depth.

## AWS Services Used

Lambda tools, DynamoDB catalog + approvals, SQS optional, Step Functions optional, Bedrock **optional**.

## Estimated Time

4 hours.

## Estimated AWS Cost

Mock agent: < $0.40. Bedrock tokens extra—keep off unless you opt in (`enable_bedrock=false`).

## Step 1 — Setup

Copy tfvars. Keep Bedrock false unless your account is enabled.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-15-ai-agent`

## Step 3 — Application

`lambda/lab15_tools` plus `scripts/ops_agent.py` (mock planner that can only call HTTP tools).

## Step 4 — Integration

Ask: file status, failed tx count, queue depth. Then request reprocess and approve via the approval API.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-15-ai-agent`

## Step 6 — Failure Testing

Try a write without approval — must fail. Try a tool not in the allow-list — must fail.

## Step 7 — Observability

Trace user → tool → API → catalog. Token/cost metric if Bedrock on.

## Step 8 — Security Review

Tool IAM is GetItem on catalog, not Scan *. No s3:GetObject on payload prefixes for the agent role.

## Step 9 — Architecture Questions

1. Draw the forbidden vs required architectures from memory.
2. Is MCP automatically safe?
3. Who cannot approve their own reprocess?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-15-ai-agent`
