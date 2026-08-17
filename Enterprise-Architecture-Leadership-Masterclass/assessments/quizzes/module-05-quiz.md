# Module 05 Quiz — Cloud and Platform Strategy

**Type:** Formative  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-05-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: M5-LO2] [Difficulty: Easy]

A landing zone is best described as:

- A. A single VPC shared by all applications
- B. A foundational multi-account environment with guardrails
- C. A migration factory spreadsheet
- D. An executive cloud slogan

### Q2 — [Application] [LO: M5-LO1] [Difficulty: Medium]

NorthStar wants faster digital products but still runs acquired cores on-prem. The most coherent near-term posture is:

- A. Active-active multi-cloud for all systems
- B. Cloud-first for new products with hybrid coexistence for cores
- C. Freeze cloud until cores are rewritten
- D. One shared production account for everything

### Q3 — [Trade-off analysis] [LO: M5-LO3] [Difficulty: Medium]

For enterprise CloudTrail-style API audit logging, the default platform stance should usually be:

- A. Build a custom audit pipeline before any trail
- B. Buy/use provider-native trail into a governed archive
- C. Rely on application logs only
- D. Disable logging to save cost

### Q4 — [Architecture judgment] [LO: M5-LO2] [Difficulty: Medium]

Which account type most urgently needs hard spend limits and expiration?

- A. Security/audit
- B. Shared services
- C. Sandbox
- D. Regulated payments production

### Q5 — [Leadership judgment] [LO: M5-LO5] [Difficulty: Medium]

A BU demands its own landing zone “for speed.” Your best first response as Lead EA is:

- A. Approve immediately to preserve relationships
- B. Reject permanently without discussion
- C. Explore needs, then offer golden paths + exception criteria
- D. Tell them to wait for a 3-year platform rewrite

### Q6 — [Recall] [LO: M5-LO4] [Difficulty: Easy]

FinOps tagging primarily enables:

- A. Encryption at rest
- B. Cost allocation and accountability
- C. Faster DNS resolution
- D. Automatic multi-region failover

### Q7 — [Application] [LO: M5-LO4] [Difficulty: Medium]

Lab 05 includes an AWS Budget near $5. The architectural teaching point is:

- A. Budgets replace security controls
- B. Cost guardrails are part of platform design
- C. Budgets are only for Finance after go-live
- D. Serverless needs no cost management

### Q8 — [Trade-off analysis] [LO: M5-LO4] [Difficulty: Hard]

Enabling AWS Config for all resource types in a short student lab is risky mainly because:

- A. It cannot tag resources
- B. It often introduces ongoing cost unsuitable for ephemeral labs
- C. It replaces CloudTrail completely
- D. It requires NAT Gateway

### Q9 — [Architecture judgment] [LO: M5-LO2] [Difficulty: Hard]

Which set is the best “minimum before migration acceleration” for NorthStar?

- A. Identity baseline, central audit logging, tagging/budgets
- B. EKS, OpenSearch, and NAT Gateways in every account
- C. Multi-cloud active-active and custom IDP portal
- D. Per-team audit formats with no shared archive

### Q10 — [Leadership judgment] [LO: M5-LO3] [Difficulty: Medium]

A strong platform ADR should include:

- A. Only the chosen vendor logo
- B. Decision, alternatives, consequences, and review/exit criteria
- C. Implementation code only
- D. A promise that no trade-offs exist

---

## Scenario questions (3)

### S1 — [Application] [LO: M5-LO1] [Difficulty: Medium]

**Scenario:** NorthStar’s CEO wants “multi-cloud” after a competitor outage news cycle. Skills are thin; one provider dominates today.

**Prompt:** Recommend a posture for 24 months. Include alternatives and primary risk.

**Response guidance:** 150–250 words; recommendation, alternatives, primary risk.

### S2 — [Trade-off analysis] [LO: M5-LO3] [Difficulty: Hard]

**Scenario:** Platform team proposes building an internal developer portal for 18 months instead of buying a commercial tool.

**Prompt:** Outline how you would run build-versus-buy and what evidence would decide it.

### S3 — [Architecture judgment] [LO: M5-LO4] [Difficulty: Hard]

**Scenario:** Finance cannot map 30% of cloud spend to products. Migrations are scheduled to accelerate next quarter.

**Prompt:** What FinOps controls do you mandate before acceleration, and what do you explicitly defer?

---

## Discussion questions (2)

### D1 — [Leadership judgment]

How should NorthStar balance product-team autonomy with platform guardrails without becoming a ticket bottleneck?

### D2 — [Trade-off analysis]

When is a central platform investment *not* the right next dollar versus fixing a product-specific risk?
