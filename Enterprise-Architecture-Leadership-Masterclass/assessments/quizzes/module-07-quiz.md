# Module 07 Quiz — Security, Risk, Compliance, and Resilience

**Type:** Formative (default)  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-07-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: M07-LO1] [Difficulty: Easy]

Zero Trust, in this course’s architecture sense, primarily means:

- A. Removing all VPNs and firewalls immediately
- B. Continuous verification, least privilege, and assume-breach across trust boundaries
- C. Encrypting all data with a single shared account key
- D. Outsourcing security entirely to a cloud provider

### Q2 — [Application] [LO: M07-LO1] [Difficulty: Medium]

A NorthStar partner uploads settlement files to S3. Which change most clearly enforces a trust boundary at the data plane?

- A. Placing the bucket in a private VPC endpoint discussion only
- B. Prefix-scoped IAM plus SSE-KMS with a restrictive key policy
- C. Adding more CloudWatch dashboards without access changes
- D. Sharing long-lived access keys in a team password manager

### Q3 — [Trade-off analysis] [LO: M07-LO3] [Difficulty: Medium]

Compared with enabling cross-region replication for a Tier-1 file store, a versioning + quarterly restore drill approach usually:

- A. Provides stronger region-impairment protection at lower cost
- B. Lowers ongoing cost but provides weaker protection against regional impairment
- C. Eliminates the need for RTO targets
- D. Removes the need for IAM least privilege

### Q4 — [Architecture judgment] [LO: M07-LO2] [Difficulty: Medium]

Which STRIDE category is most directly addressed by immutable access logging and evidence retention?

- A. Spoofing
- B. Tampering
- C. Repudiation
- D. Elevation of privilege

### Q5 — [Leadership judgment] [LO: M07-LO4] [Difficulty: Medium]

An executive asks, “Are we compliant?” The strongest EA response is:

- A. “Yes—encryption is enabled.”
- B. “We have residual risks X/Y; here are controls, evidence freshness, and open exceptions with expiry.”
- C. “Security owns that; architecture does not comment.”
- D. “The vendor certified us last year, so we are done.”

### Q6 — [Recall] [LO: M07-LO3] [Difficulty: Easy]

RPO measures:

- A. How long systems may be down
- B. How much data loss (in time) is acceptable
- C. How many regions are active
- D. How often audits occur

### Q7 — [Application] [LO: M07-LO2] [Difficulty: Medium]

A role can `s3:GetObject` on `s3://bucket/*` for Restricted settlements. Which threat is most aggravated?

- A. Information disclosure
- B. Denial of service via DNS
- C. Physical theft of an HSM
- D. Certificate pinning failures on mobile clients

### Q8 — [Trade-off analysis] [LO: M07-LO3] [Difficulty: Hard]

NorthStar wants RTO of 15 minutes for settlement landing and also wants minimal lab/platform cost. Which is the most coherent architecture response?

- A. Promise 15 minutes with versioning alone and no staffing model
- B. Challenge the RTO with business impact data or fund an operating model that can meet it
- C. Disable alarms to avoid noise
- D. Store plaintext copies in a public bucket for faster recovery

### Q9 — [Architecture judgment] [LO: M07-LO1] [Difficulty: Hard]

Which design most weakly supports Zero Trust for Restricted objects?

- A. Short-lived role assumption with prefix IAM
- B. KMS key policies listing explicit principal roles
- C. A single shared admin role used by all humans and jobs “for simplicity”
- D. TLS-only bucket policies denying insecure transport

### Q10 — [Leadership judgment] [LO: M07-LO4] [Difficulty: Medium]

A business unit demands a permanent wildcard IAM exception. The EA should:

- A. Approve permanently to protect delivery dates
- B. Refuse any exception under all circumstances
- C. Negotiate a time-bound exception with compensating controls, owner, and residual risk record
- D. Ignore the request until audit finds it

---

## Scenario questions (3)

### S1 — [Application] [LO: M07-LO2] [Difficulty: Medium]

**Scenario:** NorthStar’s settlement landing zone uses SSE-KMS, but contractors share a power-user role that can list all prefixes.

**Prompt:** Identify the primary STRIDE issues, propose control changes, and state residual risk if only encryption remains unchanged.

**Response guidance (student-facing):** 150–250 words; state recommendation, alternatives, and primary risk.

### S2 — [Trade-off analysis] [LO: M07-LO3] [Difficulty: Hard]

**Scenario:** Payments leadership wants RPO zero and RTO under 30 minutes for settlement files. Platform budget will not fund active-active multi-region this year.

**Prompt:** Recommend a phased resilience posture with explicit trade-offs and what you will not promise.

### S3 — [Architecture judgment] [LO: M07-LO4] [Difficulty: Hard]

**Scenario:** Internal audit asks for evidence that recovery objectives are tested.

**Prompt:** Design a minimal evidence pack (artifacts + owners + cadence) an EA can stand behind.

---

## Discussion questions (2)

### D1 — [Leadership judgment]

How should NorthStar’s architecture function partner with the CISO without becoming a second security team?

### D2 — [Trade-off analysis]

When is “simulated DR” an honest control versus a false sense of safety for Restricted financial data?
