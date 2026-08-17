# Module 09 Quiz — Architecture Governance and Executive Communication

**Type:** Formative (default)  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-09-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: M9-LO1] [Difficulty: Easy]

Which set best describes a complete architecture governance stack?

- A. Principles, standards, guardrails, exceptions, and review forums  
- B. Principles, project charters, and annual audits only  
- C. Cloud provider Well-Architected reviews alone  
- D. Executive steering committees without standards

### Q2 — [Application] [LO: M9-LO1] [Difficulty: Medium]

A team deploys a new service using the approved landing zone and standard services with no new data stores. What is the most appropriate control intensity?

- A. Full Architecture Review Board before every release  
- B. Guardrail-first / pipeline policy checks  
- C. Skip all controls because it is agile  
- D. Require CIO personal approval

### Q3 — [Trade-off analysis] [LO: M9-LO2] [Difficulty: Medium]

Retail Payments wants a second cloud for contractor familiarity. What is the strongest enterprise trade-off against approval?

- A. Marketing credits are lower than the primary cloud  
- B. Dual operating models for identity, logging, DR, and FinOps  
- C. Contractors prefer different IDEs  
- D. The logo colors differ by provider

### Q4 — [Architecture judgment] [LO: M9-LO2] [Difficulty: Medium]

Which disposition is most appropriate when critical security evidence is missing but the business date is near?

- A. Approve unconditionally to protect the date  
- B. Reject permanently with no alternative  
- C. Defer with a specific evidence list and deadline—or approve only a narrower safe scope  
- D. Approve and ask Security to “catch up later”

### Q5 — [Leadership judgment] [LO: M9-LO4] [Difficulty: Medium]

A BU president says licenses are already signed. The Lead EA should:

- A. Automatically approve to avoid conflict  
- B. Separate sunk commercial cost from architecture disposition and still evaluate enterprise risk  
- C. Cancel the vendor contract in the ARB meeting  
- D. Escalate only after production outage

### Q6 — [Recall] [LO: M9-LO3] [Difficulty: Easy]

A high-quality ADR must include:

- A. Only the final decision statement  
- B. Context, options considered, decision, and consequences  
- C. A full project plan and budget workbook  
- D. Vendor marketing literature

### Q7 — [Application] [LO: M9-LO3] [Difficulty: Medium]

Why should CloudNova hosting and VectorForge SoR be separate ADRs?

- A. Because ADRs must be exactly one page  
- B. Because they are independent irreversible decisions with different drivers and consequences  
- C. Because Security refuses to read long documents  
- D. Because BayLearn requires five ADRs every week

### Q8 — [Trade-off analysis] [LO: M9-LO2] [Difficulty: Hard]

“Approve with conditions” is worse than “Reject” when:

- A. Conditions are testable and owned  
- B. Conditions are vague, unowned, or unlikely to be enforced—creating a silent approve  
- C. The CIO prefers short memos  
- D. The team uses Markdown

### Q9 — [Architecture judgment] [LO: M9-LO2] [Difficulty: Hard]

Standing contractor cluster-admin for nine months most directly violates which design intent?

- A. Least privilege and time-bounded elevation  
- B. Horizontal scaling  
- C. Twelve-factor configuration  
- D. Trunk-based development

### Q10 — [Leadership judgment] [LO: M9-LO4] [Difficulty: Medium]

The best opening line of an executive decision memo is:

- A. A history of the enterprise architecture practice  
- B. A clear decision requested in one sentence  
- C. A list of all microservices  
- D. An apology for governance process

---

## Scenario questions (3)

### S1 — [Application] [LO: M9-LO2] [Difficulty: Medium]

**Scenario:** Platform can onboard Retail Payments to the landing zone in 15 business days. The BU claims any delay over one week loses a merchant cohort.

**Prompt:** Recommend a disposition path that protects standards while addressing merchant outcomes. Include one scope-phasing idea.

**Response guidance (student-facing):** 150–250 words; state recommendation, alternatives, and primary risk.

### S2 — [Trade-off analysis] [LO: M9-LO3] [Difficulty: Hard]

**Scenario:** VectorForge benchmarks show 3× throughput on synthetic tests. Encryption uses vendor-managed keys; PITR is not purchased.

**Prompt:** Argue for or against approving VectorForge as SoR using at least two decision drivers beyond raw throughput.

### S3 — [Architecture judgment] [LO: M9-LO4] [Difficulty: Hard]

**Scenario:** Your ARB rejects PayWireFX as a framework but the contractors have already written 20% of mappings in its DSL.

**Prompt:** Write the memo paragraph that explains the decision and the salvage path for work already done.

---

## Discussion questions (2)

### D1 — [Leadership judgment]

How should Lead EAs build trust with BU presidents while still rejecting divergent platform choices?

### D2 — [Trade-off analysis]

When, if ever, should NorthStar intentionally adopt a second cloud provider? What governance controls would you require?
