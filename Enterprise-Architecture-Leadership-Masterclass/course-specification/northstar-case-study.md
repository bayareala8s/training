# NorthStar Financial Services — Case Study Baseline

> **Fiction notice:** NorthStar Financial Services is a fictional organization created for BayLearn instructional use. It is not affiliated with any real company. All application names, costs, risks, and people are invented for learning.

---

## Organization profile

| Attribute | Value |
| --------- | ----- |
| Name | NorthStar Financial Services |
| Industry | Financial services and digital payments |
| Employees | 8,000 |
| Retail customers | 4 million |
| Business partners | 1,500 |
| Geography | United States, Europe, and Asia |
| Application estate | 300+ applications |
| Hosting | Hybrid on-premises and cloud |
| Structure | Multiple acquired companies still partially integrated |

---

## Student role

Students act as the newly appointed:

> **Lead Enterprise Architect for NorthStar Financial Services**

Every weekly lab contributes artifacts toward the final target-state architecture and the capstone: **NorthStar Enterprise Transformation Program**.

---

## Current problems

- More than 300 applications with unclear ownership
- Duplicate business capabilities across acquired lines of business
- Fragmented customer data and inconsistent golden records
- Manual partner onboarding
- Inconsistent API standards
- Multiple file-transfer platforms
- Weak cloud governance and uncontrolled account sprawl
- High operational cost
- Limited disaster recovery maturity
- Inconsistent identity controls
- Slow release cycles
- No unified AI strategy
- Architecture decisions made independently by teams
- Limited executive visibility into technical risk

---

## Business strategy (leadership intent)

NorthStar leadership wants to:

1. Reduce operating costs by **20%**
2. Improve customer onboarding experience and cycle time
3. Launch digital products faster
4. Standardize cloud adoption
5. Improve resilience and compliance posture
6. Consolidate integration platforms
7. Establish governed AI capabilities
8. Create shared enterprise platforms
9. Improve executive technology visibility and risk reporting

---

## Strategic themes (for capability and roadmap work)

| Theme | Example outcomes |
| ----- | ---------------- |
| Cost & consolidation | Fewer duplicate platforms; lower run cost |
| Customer experience | Faster onboarding; fewer data defects |
| Speed to market | Shorter release cycles; reusable platforms |
| Risk & resilience | Measurable RTO/RPO; stronger identity |
| Trustworthy AI | Governed use cases with audit and HITL |
| Executive visibility | Portfolio heatmaps; decision memos; ADR trail |

---

## Architecture starting conditions

- Architects exist inside business units, but **no consistent enterprise governance**
- Multiple cloud accounts and on-prem estates without a shared landing-zone standard
- Integration is a mix of APIs, files, point-to-point DB links, and batch jobs
- Security and compliance teams are engaged late
- Product teams optimize locally; enterprise risk is under-managed

---

## Named value streams (used across modules)

1. Customer onboarding  
2. Payment processing  
3. Partner integration  
4. Incident response  
5. Product delivery  

---

## Stakeholder archetypes

| Stakeholder | Primary concerns |
| ----------- | ---------------- |
| CEO / Executive Committee | Cost, growth, risk visibility |
| CIO / CTO | Platform strategy, delivery speed, tech debt |
| CISO / Risk & Compliance | Controls, evidence, third-party risk |
| Business unit presidents | Local autonomy, product speed |
| Platform / SRE leaders | Golden paths, reliability, cost |
| Data leaders | Master data, quality, analytics readiness |
| Engineering managers | Clarity of standards vs. delivery pressure |

Fictional named personas may be introduced in module materials; keep them consistent once introduced.

---

## Constraints students must respect

- Regulatory obligations typical of financial services (treat as class of controls; do not invent fake regulator names that imply real filings)
- Budget pressure: transformation must show phased value, not big-bang rewrite
- Coexistence: acquired systems cannot all be replaced in year one
- Skills: platform and cloud capabilities must be buildable incrementally
- Cost in AWS labs: keep ephemeral and serverless; clean up promptly

---

## How modules use NorthStar

| Module | NorthStar focus |
| ------ | --------------- |
| 1 | Establish the architecture function |
| 2 | Capability map and investment heatmap |
| 3 | Current-state portfolio and top risks |
| 4 | Target state, transitions, 24-month roadmap |
| 5 | Cloud/platform foundation and FinOps |
| 6 | Integration reference architecture |
| 7 | Security, threat model, DR |
| 8 | Governed AI incident decision assistant |
| 9 | ARB on a divergent business-unit proposal |
| 10 | Full transformation narrative and defense |

---

## Dataset notes

- Module 3 includes a fictional application inventory CSV (40+ apps)
- Capstone may extend the same inventory
- All datasets carry the fiction notice in file headers or README
