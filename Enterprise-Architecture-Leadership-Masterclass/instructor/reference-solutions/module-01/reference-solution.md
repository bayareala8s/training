# Reference Solution — Module 01: Architecture Operating Model Pack

**Classification:** Instructor-only — do **not** distribute to students  
**Case study:** NorthStar Financial Services (**fictional**)  
**Role:** Lead Enterprise Architect  
**Quality bar:** Strong “4”-level exemplar on most rubric criteria for Week 1; not the only correct answer

---

## 1. Architecture mission (sample)

NorthStar Enterprise Architecture exists to improve **enterprise decision quality**, **reuse of shared platforms**, and **visibility of material technology risk**—so NorthStar can reduce operating cost, accelerate onboarding and product delivery, and strengthen resilience without requiring a big-bang rewrite of acquired estates.

We are accountable for principles, cross-domain decision rights, architecture engagement design, and executive-ready risk/decision artifacts.  
We are **not** accountable for owning product backlogs, sprint priorities, or designing every solution in detail.

---

## 2. Operating model choice

**Year-1 posture: Hybrid (federated domain/solution architects + enterprise EA office + narrow ARB).**

| Rejected option | Why rejected for Year 1 | Risk accepted by choosing hybrid |
| --------------- | ----------------------- | -------------------------------- |
| Full centralization | High political cost; existing BU architects; slows delivery during transformation | Slower consistency; relies on coalition |
| Pure federation | Recreates today’s failure—optional enterprise standards | Requires discipline on decision classes |

---

## 3. Operating model diagram (narrative equivalent)

Lead EA reports to CIO/CTO. ARB convened for material exceptions. Platform, Security Architecture, and Data Architecture are standing consulted partners. Retail, Payments, Partner Channels, and Wealth retain domain/solution architects who support delivery teams and escalate cross-domain issues per decision classes.

*(See also `modules/module-01-enterprise-architect-role/diagrams/operating-model.mmd`.)*

---

## 4. Decision rights summary

| Decision class | Accountable | Escalate when |
| -------------- | ----------- | ------------- |
| Local solution choices within guardrails | Solution Architect + Engineering Manager | Breaks principle; creates new platform; material security impact |
| Domain target-state / pattern selection | Domain Architect | Conflicts with another domain or shared platform |
| Enterprise principles & cross-domain standards | Lead Enterprise Architect (CIO approval) | ExCo strategy change |
| Platform golden-path changes | Platform Architect | Breaking change; cost or risk above threshold |
| Material exceptions, multi-year lock-in, high-risk AI production | ARB (CIO chair or delegate) | Residual risk above appetite → ExCo tech committee |

---

## 5. RACI (sample)

**R** Responsible · **A** Accountable · **C** Consulted · **I** Informed

| Activity / decision | EA | DA | SA | PA | ARB | CIO | SEC | DATA | BM | EM |
| ------------------- | -- | -- | -- | -- | --- | --- | --- | ---- | -- | -- |
| Set architecture principles | A | C | I | C | C | C | C | C | C | I |
| Approve principle exceptions | C | C | R | C | A | I | C | C | C | I |
| Domain target-state | C | A | R | C | I | I | C | C | C | I |
| Solution design within standards | I | C | A | C | — | — | C | C | C | R |
| Platform golden-path changes | C | I | I | A | C | I | C | C | I | I |
| Cloud account / landing-zone standards | C | I | I | A | C | I | C | I | I | I |
| Integration pattern exceptions | C | C | R | C | A | I | C | C | C | I |
| Data product ownership disputes | C | C | I | I | C | I | C | A | C | I |
| High-risk AI production release | C | C | R | C | A | I | C | C | C | I |
| Executive tech-risk reporting | A | C | I | C | I | C | C | C | I | I |

---

## 6. Engagement model (sample)

| Mode | Entry | Response target | Exit artifact |
| ---- | ----- | --------------- | ------------- |
| Consult | Slack/intake form; low cross-domain impact | 2 business days | Advice notes / optional ADR |
| Collaborate | Shared platform or multi-BU capability | Scheduled design session within 5 days | Joint ADR |
| Govern | Hits ARB trigger list | Next ARB (weekly) or emergency slot | Decision record + expiry |

**ARB triggers (Year 1 — narrow):** new platform capability; principle exception >90 days; multi-year vendor commitment above cost threshold; customer/identity data model change across BUs; high-risk AI in production; material resilience target change (RTO/RPO class).

**Non-triggers:** routine service features within golden paths; library upgrades; team coding standards.

---

## 7. Architecture principles (9 sample)

### P1 — Business outcomes over technology novelty

| Field | Content |
| ----- | ------- |
| Statement | We will choose architectures that advance named NorthStar outcomes (cost, onboarding speed, product speed, resilience, governed AI, visibility). |
| Rationale | Tool-led decisions created duplicate platforms and weak executive traceability. |
| Implications | Business sponsor and outcome KPIs required on material initiatives; novelty alone is insufficient justification. |
| Exceptions | Innovation spikes time-boxed ≤90 days with sunset. |
| Signals | % of ARB items with explicit outcome linkage. |

### P2 — Reuse before rebuild

| Field | Content |
| ----- | ------- |
| Statement | We will reuse existing capabilities and platforms before funding new ones. |
| Rationale | Supports ~20% run-cost reduction and reduces operational fragmentation. |
| Implications | New platform proposals must include reuse analysis and total cost comparison. |
| Exceptions | ARB-approved when reuse blocks regulated control or proven latency needs. |
| Signals | Count of duplicate active platforms; exception aging. |

### P3 — Secure and resilient by design

| Field | Content |
| ----- | ------- |
| Statement | We will design identity, data protection, and resilience into architectures—not bolt them on after vendor selection. |
| Rationale | Late security engagement is a stated NorthStar failure mode. |
| Implications | Security Architecture consulted on material classes; resilience targets declared for critical value streams. |
| Exceptions | Temporary risk acceptance with expiry and compensating controls. |
| Signals | % of material decisions with security consult recorded before contract. |

### P4 — Data as a product with clear ownership

| Field | Content |
| ----- | ------- |
| Statement | We will treat critical data domains as products with named owners and quality standards. |
| Rationale | Fragmented customer data blocks onboarding and analytics. |
| Implications | No silent second golden records; disputes escalate to Data Architecture accountability. |
| Exceptions | Acquired-system coexistence with mapped transition owners. |
| Signals | Named owners for priority domains; defect trends on onboarding data. |

### P5 — Prefer platform golden paths

| Field | Content |
| ----- | ------- |
| Statement | We will deliver common workload classes through supported golden paths before creating new platforms. |
| Rationale | Speeds delivery and concentrates security evidence. |
| Implications | Teams justify off-path work; Platform publishes path roadmaps. |
| Exceptions | Time-boxed ARB exceptions with migration owner. |
| Signals | % new services on-path; active off-path platforms. |

### P6 — Automate guardrails; minimize manual gates

| Field | Content |
| ----- | ------- |
| Statement | We will prefer automated preventive controls over manual review queues. |
| Rationale | Manual gates are bypassed under delivery pressure. |
| Implications | Invest in landing-zone policies and CI checks; ARB stays narrow. |
| Exceptions | Manual gate only for material classes lacking automation. |
| Signals | ARB volume trend; policy-as-code coverage. |

### P7 — Design for operability and cost transparency

| Field | Content |
| ----- | ------- |
| Statement | We will make operability and cost allocation visible in architecture choices. |
| Rationale | Uncontrolled cloud sprawl and high run cost are NorthStar problems. |
| Implications | Tagging, ownership, and support model required for new shared services. |
| Exceptions | Short experiments with cost caps. |
| Signals | Untagged spend; incident ownership clarity. |

### P8 — Make material architecture decisions explicit

| Field | Content |
| ----- | ------- |
| Statement | We will record material decisions as ADRs or executive decision memos. |
| Rationale | Invisible decisions recreate identity-project collision. |
| Implications | Decision class determines artifact depth; “tribal knowledge” insufficient. |
| Exceptions | Trivial local choices need no ADR. |
| Signals | ADR coverage on ARB and platform changes. |

### P9 — Human accountability for high-risk AI decisions

| Field | Content |
| ----- | ------- |
| Statement | We will keep named humans accountable for high-risk AI outcomes, with auditability and HITL where required. |
| Rationale | Leadership intends governed AI—not shadow models in production. |
| Implications | High-risk AI releases use govern mode; logging and override paths required. |
| Exceptions | Low-risk assistive AI on golden paths with standard controls. |
| Signals | Inventory of production AI use cases with risk tier and owner. |

---

## 8. Architecture-function risk register (sample)

| ID | Risk | L | I | Mitigation | Owner |
| -- | ---- | - | - | ---------- | ----- |
| AF-01 | BU presidents bypass EA for speed | H | H | Narrow gates + useful consult SLA; CIO monthly digest | Lead EA |
| AF-02 | Principles ignored / no exception visibility | M | H | Exception register with expiry; ARB trigger | Lead EA |
| AF-03 | EA capacity overload (hero designer trap) | H | M | Decision classes; refuse backlog ownership | Lead EA / CIO |
| AF-04 | Security remains late despite RACI | M | H | Block material contracts without SEC consult evidence | Lead EA / CISO delegate |
| AF-05 | Dual Accountables create thrash | M | M | RACI review in 60 days; single A rule | Lead EA |
| AF-06 | Golden paths lag behind delivery needs | M | H | Quarterly path roadmap with Platform; measured exceptions | Platform Architect |
| AF-07 | Acquired-BU cultural rejection of hybrid model | M | M | Co-author principles with BU architects in first 30 days | Lead EA |

---

## 9. Grading notes for this exemplar

- Strong on business alignment and trade-offs (explicit rejects)  
- Security present proportionately (P3, RACI, AF-04)  
- Feasibility: hybrid + 90-day sequencing implied in engagement  
- Students may differ on principle wording—score decision quality, not cloning
