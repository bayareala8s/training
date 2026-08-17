# Week 8 — Capstone Scenarios (Inspiration)

These scenarios illustrate how capstone tracks map to real enterprise initiatives. Students are **not** required to replicate them exactly—use them for scope and narrative inspiration.

## Scenario A — Option 1: Landing zone for acquisition

**Context:** A holding company acquires a startup on AWS single-account. IT must integrate them into OU structure with SCPs, shared VPC, and separate state per account within 90 days.

**Capstone alignment:** OU design doc, networking baseline, remote state per account, CI plan on PR.

**Presentation hook:** “Reduce audit findings from 12 to 0 on account separation.”

---

## Scenario B — Option 2: Shared services for 40 product teams

**Context:** Each team built its own VPC; IP overlap blocks acquisitions. Platform delivers hub VPC + centralized flow logs and subnet outputs.

**Capstone alignment:** Hub design, consumable outputs, monitoring.

**Presentation hook:** “Standard attachment pattern cuts VPC design time from 2 weeks to 2 days.”

---

## Scenario C — Option 3: DR after regional degradation

**Context:** SaaS must survive regional API degradation with RTO 4h. Secondary region stack maintained by Terraform; failover runbook includes Route 53 and RDS promotion steps.

**Capstone alignment:** Dual region, state strategy, runbook (tabletop demo acceptable).

**Presentation hook:** “Tabletop proved gap in lock table DR—fixed before production.”

---

## Scenario D — Option 4: Internal platform for 200 developers

**Context:** Teams copy-paste Terraform from Stack Overflow. Platform ships versioned VPC and ECS modules + GitHub Actions template.

**Capstone alignment:** ≥2 modules, golden path doc, reusable CI workflow.

**Presentation hook:** “Time-to-first-deploy dropped from 5 days to 4 hours.”

---

## Lab tie-in

See [04-hands-on-labs.md](04-hands-on-labs.md) and [`../../capstone/README.md`](../../capstone/README.md).
