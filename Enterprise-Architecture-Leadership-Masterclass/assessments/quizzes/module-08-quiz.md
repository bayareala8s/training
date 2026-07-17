# Module 08 Quiz — AI Strategy and Intelligent Enterprise Architecture

**Type:** Formative (default)  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-08-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: M08-LO1] [Difficulty: Easy]

An enterprise AI strategy is best described as:

- A. Deploying as many chatbots as possible
- B. A governed portfolio of use cases tied to outcomes, data readiness, risk, and operating model
- C. Choosing the largest foundation model available
- D. Replacing the Architecture Review Board with a prompt library

### Q2 — [Application] [LO: M08-LO1] [Difficulty: Medium]

NorthStar’s incident decision assistant scores high on value but elevated on routing harm. The best near-term decision is usually:

- A. No-go forever with no revisit criteria
- B. Conditional-go with HITL for high-severity and low-confidence cases
- C. Full autonomy for Critical severity
- D. Skip scoring and launch a LOB pilot chatbot

### Q3 — [Trade-off analysis] [LO: M08-LO2] [Difficulty: Medium]

For operational triage outputs, structured JSON with schema validation is preferred over free text primarily because:

- A. It uses more tokens always
- B. It enables deterministic validation, routing, and auditability
- C. Executives prefer reading raw JSON in meetings
- D. It eliminates the need for HITL forever

### Q4 — [Architecture judgment] [LO: M08-LO2] [Difficulty: Medium]

In a governed assistant pipeline, which statement is most accurate?

- A. The model output is automatically the business decision
- B. The model proposes; deterministic rules and HITL policy govern autonomy
- C. Logging full prompts with customer PII is required for quality
- D. Validation is optional if confidence is displayed

### Q5 — [Leadership judgment] [LO: M08-LO3] [Difficulty: Medium]

HITL for an incident assistant should be:

- A. Undefined—“a human will look somehow”
- B. Triggered by explicit rules (e.g., severity, confidence, schema failure, regulated actions)
- C. Applied only to Low severity to save time
- D. Removed once the first demo succeeds

### Q6 — [Recall] [LO: M08-LO3] [Difficulty: Easy]

Safe logging for NorthStar’s lab primarily means:

- A. Storing production customer records for realism
- B. Using synthetic incidents and redacting sensitive fields
- C. Disabling CloudWatch entirely
- D. Emailing raw prompts to ExCo

### Q7 — [Application] [LO: M08-LO4] [Difficulty: Medium]

A labeled evaluation set is used to:

- A. Replace architecture diagrams
- B. Measure assistant quality against an explicit metric before scaling autonomy
- C. Prove Bedrock is the only acceptable runtime
- D. Avoid documenting residual risk

### Q8 — [Trade-off analysis] [LO: M08-LO4] [Difficulty: Hard]

Mock Bedrock mode in Lab 08 is best justified when:

- A. Students want to skip validation and HITL
- B. Model access is unavailable, but architecture, validation, HITL, and eval can still be demonstrated
- C. Cost and risk controls are no longer required
- D. NorthStar decides AI strategy is finished

### Q9 — [Architecture judgment] [LO: M08-LO3] [Difficulty: Hard]

Token and cost tracking belong in the architecture because:

- A. They are purely aesthetic
- B. They are non-functional requirements affecting budgets, limits, and operability
- C. They replace the need for HITL
- D. They only matter after ExCo branding approval

### Q10 — [Leadership judgment] [LO: M08-LO1] [Difficulty: Medium]

A BU demands a public-facing advice chatbot with no KPI, weak data controls, and no HITL plan. The Lead EA should:

- A. Approve immediately to show innovation
- B. Score the use case, surface risk/data gaps, and recommend no-go or conditional-go with controls
- C. Quietly deploy without ARB
- D. Rename it “assistant” and skip scoring

---

## Scenario questions (3)

### S1 — [Application] [LO: M08-LO1] [Difficulty: Medium]

**Scenario:** Payments IR wants the assistant to auto-restart services on Critical severity predictions.

**Prompt:** Recommend go/conditional/no-go for *auto-restart*. Include HITL and residual risk.

### S2 — [Trade-off analysis] [LO: M08-LO2] [Difficulty: Hard]

**Scenario:** Platform proposes one shared free-text chatbot for IR, HR, and customer complaints to “standardize AI.”

**Prompt:** Argue for or against. What shared platform capabilities vs use-case-specific controls would you require?

### S3 — [Architecture judgment] [LO: M08-LO4] [Difficulty: Hard]

**Scenario:** Eval shows 90% category agreement but only 55% severity agreement; Critical labels sometimes emit hitl_required=false.

**Prompt:** What ship criteria would you set, and what architecture changes would you demand before broader rollout?

---

## Discussion questions (2)

### D1 — [Leadership judgment]

How should NorthStar communicate residual AI risk to ExCo without either hype or paralysis?

### D2 — [Trade-off analysis]

When is investing in AI platform controls *not* the right next dollar versus fixing basic incident data quality?
