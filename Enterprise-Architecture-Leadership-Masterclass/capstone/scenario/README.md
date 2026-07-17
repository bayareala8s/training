# Capstone Scenario — NorthStar Enterprise Transformation Program

> **Fiction notice:** NorthStar Financial Services is a fictional organization created for BayLearn instructional use. It is not affiliated with any real company.

---

## Situation refresh (Week 10)

NorthStar Financial Services is an 8,000-employee financial services and digital payments company with 4 million retail customers and 1,500 business partners across the United States, Europe, and Asia. After multiple acquisitions, the estate exceeds 300 applications. Hosting is hybrid. BU architects make local decisions; enterprise governance is inconsistent.

Leadership has restated strategic intent:

1. Reduce operating costs by **20%** over 24 months (directional target)
2. Improve customer/merchant onboarding cycle time
3. Launch digital products faster via shared platforms
4. Standardize cloud adoption and FinOps
5. Improve resilience and compliance evidence
6. Consolidate integration platforms
7. Establish governed AI capabilities
8. Improve executive visibility into technology risk and decisions

The Executive Committee has asked the Lead Enterprise Architect to present the **NorthStar Enterprise Transformation Program**: an integrated proposal that connects strategy to architecture choices, sequenced delivery, governance, and clear decision asks.

Constraints remain: acquired companies, coexistence for 24 months, limited platform capacity, and **no big-bang rewrite**.

---

## What “good” looks like for the committee

- Outcome-led narrative (not a module replay)
- Credible coexistence and phased value
- Explicit trade-offs (including rejected paths)
- Security, identity, and resilience designed in
- Governed AI—not shadow experiments
- Decision asks the committee can approve, defer, or reject

---

## Political realities (use in defense)

- BU presidents defend local autonomy and sunk vendor commitments
- CISO demands evidence paths and least privilege
- Platform/SRE leaders worry about supportability and cost
- Data leaders push golden records and portable SoRs
- CIO/CTO need speed without irreversible tax

---

## Scope boundaries

**In scope:** Enterprise operating model, capability-aligned investment, portfolio dispositions, target/transition/roadmap, platform and integration standards, security/resilience, AI governance, ARB model, ADRs, executive memo and presentation.

**Out of scope:** Detailed vendor negotiations, legal contract redlines, production change tickets, real cloud spend.

---

## Program ask framing (use in memo + final slide)

Typical numbered asks:

1. Adopt the architecture operating model, principles, and ARB charter
2. Fund Wave 1 platform foundations (landing zone, identity, observability, FinOps)
3. Approve integration backbone and master-data direction (with coexistence)
4. Adopt resilience classes (RTO/RPO) for mission-critical payment and onboarding paths
5. Adopt governed AI policy and authorize the incident decision-support pilot under HITL

Tune wording to your analysis; do not invent fake regulatory filings.

---

## Inputs you already have

Weekly labs 1–9 artifacts, plus [`../../student/datasets/northstar-application-inventory.csv`](../../student/datasets/northstar-application-inventory.csv).

Authoritative requirements: [`../student-brief/capstone-brief.md`](../student-brief/capstone-brief.md).

---

## Success definition (student)

You succeed when a panel unfamiliar with your weekly journey can understand the stakes, destination, journey, controls, and asks—and when your document pack proves the work behind the story.
