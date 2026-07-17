# Module 06 Quiz — Integration, Application, and Data Architecture

**Type:** Formative (default)  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-06-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: M6-LO1] [Difficulty: Easy]

Which criterion set best supports integration pattern selection?

- A. Vendor preference and slide aesthetics only
- B. Latency, coupling, volume, reliability, security, cost, and ops complexity
- C. Number of microservices already deployed
- D. Whether the team likes Kafka

### Q2 — [Application] [LO: M6-LO1] [Difficulty: Medium]

For NorthStar customer-service account lookup with a two-second user SLA, the best primary pattern is usually:

- A. Nightly batch ETL
- B. Synchronous API
- C. Unordered file drop only
- D. Shared database read across LOBs with no API

### Q3 — [Trade-off analysis] [LO: M6-LO1] [Difficulty: Medium]

PaymentSubmitted needs buffering, retries, and poison isolation. Which combination fits best?

- A. Sync fan-out to every consumer with no queue
- B. Event to competing consumers via queue with a DLQ
- C. Partner SFTP as the only channel
- D. Direct DB insert from every channel app

### Q4 — [Architecture judgment] [LO: M6-LO2] [Difficulty: Medium]

In a healthy NorthStar model, who should own the *meaning* of the PaymentSubmitted event?

- A. The shared integration platform team alone
- B. The Payments business domain / LOB
- C. The partner’s SFTP vendor
- D. Whoever created the EventBridge bus first

### Q5 — [Leadership judgment] [LO: M6-LO2] [Difficulty: Medium]

A LOB proposes a shared database “just for now” so two products can integrate faster. The Lead EA should:

- A. Approve permanently because speed matters
- B. Treat it as hidden coupling debt, require an exit path, and prefer explicit APIs/events
- C. Delete both products from the capability map
- D. Mandate Transfer Family for all database access

### Q6 — [Recall] [LO: M6-LO5] [Difficulty: Easy]

Why does Lab 06 simulate partner files with S3 landing instead of deploying AWS Transfer Family?

- A. S3 cannot store files
- B. Managed Transfer endpoints can incur ongoing cost unsuitable for ephemeral labs
- C. Partners never use files
- D. Terraform cannot create S3 buckets

### Q7 — [Application] [LO: M6-LO3] [Difficulty: Medium]

Partner onboarding files arriving in a landing zone are best treated as:

- A. The customer golden record system of record
- B. An exchange format that must map into owned domain data products / masters
- C. Proof that analytics owns account corrections
- D. A replacement for payment event contracts

### Q8 — [Trade-off analysis] [LO: M6-LO4] [Difficulty: Hard]

A poison payment message repeatedly crashes a worker. Without a DLQ, the most likely operational outcome is:

- A. Automatic perfect healing with no human action
- B. Consumer stall or retry storms that block healthy messages
- C. Instant schema registry creation
- D. Free Transfer Family credits

### Q9 — [Architecture judgment] [LO: M6-LO1] [Difficulty: Hard]

An “ESB for everything” proposal is weakest when:

- A. NorthStar has multiple interaction styles with different SLAs and failure modes
- B. All traffic is identical batch files with one consumer
- C. There is only one system in the estate
- D. Latency and coupling requirements are identical everywhere

### Q10 — [Leadership judgment] [LO: M6-LO5] [Difficulty: Medium]

A strong integration ADR should include:

- A. Only the chosen pattern logo
- B. Decision, alternatives, consequences, and review/exit criteria (including cost)
- C. Implementation code only
- D. A promise that no trade-offs exist

---

## Scenario questions (3)

### S1 — [Application] [LO: M6-LO1] [Difficulty: Medium]

**Scenario:** NorthStar fraud wants near-real-time signals on payments; branch tellers still need immediate account balance reads.

**Prompt:** Recommend primary/secondary patterns for each need. Name one shared anti-pattern to reject.

**Response guidance:** 150–250 words; criteria explicit.

### S2 — [Trade-off analysis] [LO: M6-LO5] [Difficulty: Hard]

**Scenario:** A major partner insists on SFTP. Platform proposes always-on Transfer Family in every account “for consistency,” including student labs.

**Prompt:** How do you separate lab reference architecture from production MFT decision? What evidence decides buy/deploy Transfer or MFT?

### S3 — [Architecture judgment] [LO: M6-LO3] [Difficulty: Hard]

**Scenario:** Analytics publishes AccountCorrected events that conflict with Accounts domain updates; customer service sees oscillating values.

**Prompt:** Who should own authoritative corrections, and what platform guardrails would you propose?

---

## Discussion questions (2)

### D1 — [Leadership judgment]

How should NorthStar balance product-team autonomy to publish events with platform guardrails for schema, DLQ, and blast radius?

### D2 — [Trade-off analysis]

When is investing in a central integration platform *not* the right next dollar versus fixing a single product’s point-to-point risk?
