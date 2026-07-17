# Reference Solution — Module 04

**Classification:** Instructor-only — do not distribute to students  
**Module:** Target-State Architecture and Transformation Roadmaps  
**Lab:** Create NorthStar’s Target-State Roadmap  
**Case study:** NorthStar Financial Services (fictional)

> This is a **sample** strong solution, not the only correct answer. Grade reasoning quality, not match-to-key.

---

## Executive summary (sample)

NorthStar will reduce run cost and improve onboarding/partner cycle time by consolidating duplicate engagement and integration platforms, while retaining and carefully replatforming StarCore and stabilizing PayForge on the critical path. Over 24 months we execute three transition states: (A) guardrails and freeze sprawl, (B) strategic journeys with controlled coexistence, (C) dual-run burn-down and retirees. We are **not** rewriting StarCore in year one, **not** launching unconstrained AI platforms, and **not** allowing a fourth CRM. Decisions needed: approve CRM survivor ADR, fund partner API platform, adopt temporary-interface end-date policy, and accept dual-run budget with a burn-down target.

---

## 1. Strategic capabilities (sample)

| Capability | Disposition | Target pattern |
| ---------- | ----------- | -------------- |
| Customer onboarding | Invest | Unified digital onboarding journey services on shared identity + golden record |
| Payment processing | Invest / Sustain | PayForge as payments SoR pattern; APIs hardened; selective refactor |
| Partner integration | Invest | Enterprise API/event platform; file only by exception |
| Customer engagement (CRM) | Invest | Single enterprise CRM pattern; BU configuration not separate cores |
| Core banking / ledger | Sustain | StarCore retained as SoR; replatform infrastructure; strangler at edges |
| Identity & access | Invest | Central workforce + customer identity patterns; landing-zone enforced |
| Customer data / golden record | Invest | Enterprise-owned golden record with clear stewardship |
| Integration platform | Invest | Shared API gateway + event bus; retire redundant file hubs |
| Observability / incident | Sustain / Invest | Shared telemetry golden path for critical journeys |
| Shadow analytics / orphan reporting | Exit | Retire; governed analytics platform absorbs |

---

## 2. Target principles (sample)

1. **Capabilities over applications** — fund outcomes; apps are disposable vessels.  
2. **Platforms before product-local stacks** — reuse enterprise identity, integration, data, observability.  
3. **API- and event-first** — new file/DB links require ARB exception with end date.  
4. **Data has an owner** — customer golden record is enterprise-stewarded.  
5. **Security and resilience by design** — coexistence includes identity, audit, reconciliation.  
6. **Cloud via landing zone** — no unmanaged accounts.  
7. **Coexistence is temporary** — dual-run and bridges have exit criteria and dates.

**Non-goals (24 months):** StarCore full rewrite; fourth CRM; speculative enterprise AI platform; big-bang cutover of payments.

---

## 3. Target application architecture (sample narrative)

**Engagement:** One CRM pattern (NovaCRM selected as survivor in this sample). Onboarding journey services strangler around OnboardX; BU portals retire behind the journey.

**Systems of record:** StarCore remains core ledger/banking SoR. PayForge remains payments SoR with hardened APIs.

**Shared platforms:** Identity; API/event integration; golden record/data services; observability; landing-zone shared services.

**Explicit deferrals:** Advanced AI assistants wait for Module 08-style governance; deep DR redesign detailed in Module 07 but RTO/RPO classes declared for onboarding and payments now.

---

## 4. Dispositions (sample)

| App / group | Strategy | Execution note | Dual-run? | Rationale |
| ----------- | -------- | -------------- | --------- | --------- |
| StarCore Banking Suite | Retain | Replatform waves (DB/runtime/ops) | Limited at edges | High coupling; regulatory SoR; rewrite unjustified Y1 |
| PayForge | Replatform | Then selective Refactor of APIs | Yes (canary) | Critical path; avoid full replace |
| NovaCRM | Consolidate survivor | Invest / light refactor | Yes (reads→writes) | Best fit for enterprise engagement pattern |
| LegacyCRM | Consolidate → Retire | Replace by migration to Nova | Yes | Duplicate capability; loser of consolidate |
| OnboardX | Refactor | Strangler + consolidate BU portals | Yes | Strategic CX theme |
| BU onboarding portals | Consolidate / Retire | Into onboarding journey | Yes | Duplicates |
| PartnerLink Classic | Consolidate | Drain via API platform | Yes | Legacy partner entry |
| FileBridge | Retire | After volume drain | Yes | Redundant file hub |
| SyncHub | Retire | After volume drain | Yes | Redundant file hub |
| Orphan reporting cubes (×3) | Retire | Move to governed analytics | No | Cost without strategic value |
| HR payroll batch feed | Rehost | Facility exit | No | Commodity; low change |

---

## 5. Three transition states (sample)

### Transition A — Stabilize & standardize (Months 0–8)

- Landing zone + identity guardrails for new accounts/workloads  
- Sprawl freeze policy; orphan retire wave  
- CRM survivor ADR (NovaCRM); begin read consolidation  
- New partners on API path only; freeze new FileBridge partners  

**Exit criteria:**

- 100% new cloud accounts via landing-zone pipeline  
- CRM survivor ADR approved by ARB/ExCo  
- ≥30% new partner onboardings on API path  
- ≥10 orphan apps decommissioned with evidence  

### Transition B — Strategic journeys coexist (Months 8–16)

- Onboarding strangler live for priority segments  
- Golden record dual-write + reconciliation dashboards  
- LegacyCRM write freeze; migration waves  
- PayForge replatform complete for critical path; canary refactors  

**Exit criteria:**

- Measurable onboarding cycle-time improvement on strangler cohort  
- Reconciliation error rate below agreed threshold for N consecutive weeks  
- LegacyCRM write-off date published; ≥50% eligible customers on Nova write path  
- PayForge critical-path SLOs met on replatformed stack  

### Transition C — Shrink dual-run (Months 16–24)

- Retire FileBridge, SyncHub, LegacyCRM  
- Remove unjustified temporary bridges  
- Golden paths default; ARB exceptions only  
- Dual-run cost below threshold  

**Exit criteria:**

- FileBridge/SyncHub/LegacyCRM decommissioned  
- Dual-run cost index ≤ agreed % of Peak Transition B  
- No new permanent file hubs; exception register clean  
- Target principles enforced via guardrails + ARB metrics  

---

## 6. 24-month roadmap (sample)

| Phase | Months | Theme | Business value | Risk reduced | Dependencies | Funding note |
| ----- | ------ | ----- | -------------- | ------------ | ------------ | ------------ |
| 0 | 0–3 | Foundation | Stop sprawl cost growth | Identity/cloud drift | Exec policy approval | Platform OPEX + small CAPEX |
| 1 | 3–8 | Transition A value | Early run-cost takeout; partner path | Orphans; file growth | Phase 0 guardrails | Consolidation program tranche 1 |
| 2 | 8–16 | Transition B value | Onboarding CX; payments stability | Integration fragility; data defects | API platform; CRM ADR; golden record stewardship | Tranche 2 + BU change budget |
| 3 | 16–24 | Transition C value | Dual-run cost down; target default | Concentration; evidence gaps | Volume drain; write freeze complete | Decommission + warranty funding |

### Initiative backlog (sample)

| ID | Initiative | Phase | Value | Risk↓ | Effort | Priority |
| -- | ---------- | ----- | ----: | ----: | -----: | -------- |
| I1 | Landing zone + identity guardrails | 0 | 3 | 5 | 3 | Do first |
| I2 | Orphan retire wave | 1 | 3 | 4 | 2 | Do first |
| I3 | Partner API platform | 1 | 5 | 4 | 4 | Do first |
| I4 | CRM survivor + read consolidate | 1 | 4 | 3 | 3 | Do first |
| I5 | Onboarding strangler | 2 | 5 | 3 | 4 | Do next |
| I6 | Golden record dual-write | 2 | 5 | 4 | 4 | Do next |
| I7 | PayForge replatform | 2 | 4 | 5 | 4 | Do next |
| I8 | Retire file bridges + LegacyCRM | 3 | 4 | 4 | 3 | Finish |
| I9 | Speculative AI platform | — | 2 | 1 | 5 | Non-goal |
| I10 | Fourth CRM | — | 1 | 1 | 4 | Non-goal |

---

## 7. Risks (sample)

| Risk | Mitigation |
| ---- | ---------- |
| Dual-run cost overrun | Burn-down KPI; Transition C gates funding |
| Data divergence in dual-write | Reconciliation SLO; pause cutover if breached |
| BU resistance to CRM loser path | Exec decision record; migration support funding |
| PayForge change induces outage | Canary; rollback; change freeze calendar |
| Temporary bridges extended politically | ARB end-date policy; exception sunset reports |
| Skills shortage on platform team | Phase 0 hiring/partner surge; scope non-goals |

---

## 8. Grading note

Students may pick LegacyCRM as survivor, different phase boundaries, or stronger risk-first sequencing. **Accept** if trade-offs, exit criteria, dependencies, and NorthStar constraints are explicit and coherent. **Penalize** replace-everything, missing exits, wish-list roadmaps, and ignored coexistence.
