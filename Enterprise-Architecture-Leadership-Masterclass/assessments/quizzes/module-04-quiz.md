# Module 04 Quiz — Target-State Architecture and Transformation Roadmaps

**Type:** Formative (default)  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-04-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: LO-4.1] [Difficulty: Easy] [Category: Target state]

A target-state architecture is best described as:

- A. A complete inventory of every future application instance  
- B. A coherent future landscape of capabilities, patterns, controls, and operating rules  
- C. A vendor product roadmap adopted as enterprise strategy  
- D. A project Gantt chart spanning 24 months  

### Q2 — [Application] [LO: LO-4.1] [Difficulty: Medium] [Category: Target state]

NorthStar’s Lead EA drafts a target state with “AI everywhere” but no constraints or non-goals. The primary problem is:

- A. AI is out of scope until Module 08, so it must be deleted  
- B. The target cannot be challenged or funded as architecture leadership  
- C. Mermaid diagrams are missing  
- D. TIME dispositions are invalidated  

### Q3 — [Trade-off analysis] [LO: LO-4.2] [Difficulty: Medium] [Category: Modernization]

StarCore is highly coupled, regulatory-critical, and expensive to rewrite. The most defensible near-term strategy is usually:

- A. Replace in a single cutover within 6 months  
- B. Retire immediately and rebuild greenfield  
- C. Retain with replatform waves at the infrastructure/edge  
- D. Rehost only the UI tier and declare target achieved  

### Q4 — [Architecture judgment] [LO: LO-4.2] [Difficulty: Medium] [Category: Modernization]

NovaCRM and LegacyCRM both support customer engagement after acquisitions. The strategy that best addresses duplicate capability is:

- A. Retain both indefinitely to avoid conflict  
- B. Consolidate to a survivor and retire the loser  
- C. Rehost both to cloud without changing ownership  
- D. Refactor both in parallel to identical microservices  

### Q5 — [Leadership judgment] [LO: LO-4.2] [Difficulty: Medium] [Category: Modernization]

A product team says “our strategy is migrate to cloud.” As Lead EA you should:

- A. Approve because cloud is the target platform  
- B. Require a disposition (rehost/replatform/refactor/replace/retire/retain/consolidate)  
- C. Reject all cloud moves until Module 05  
- D. Convert the statement into a TIME=Eliminate decision  

### Q6 — [Recall] [LO: LO-4.3] [Difficulty: Easy] [Category: Transitions]

A transition architecture must include:

- A. Sprint tasks for every team  
- B. Interim landscape elements and observable exit criteria  
- C. Only a target diagram with no interim state  
- D. A vendor statement of work  

### Q7 — [Application] [LO: LO-4.3] [Difficulty: Medium] [Category: Transitions]

During CRM consolidation, NorthStar dual-writes customer updates. The best exit criterion is:

- A. “Dual-write project marked complete in the PMO tool”  
- B. “Teams feel confident about cutover”  
- C. “Reconciliation error rate below threshold for N weeks; write path freeze dated for loser CRM”  
- D. “Both CRMs remain writable forever for safety”  

### Q8 — [Trade-off analysis] [LO: LO-4.3] [Difficulty: Hard] [Category: Transitions]

Extending FileBridge as a “temporary” hub for 18 more months primarily risks:

- A. Faster partner onboarding with no downside  
- B. Encoding a temporary bridge as permanent cost and complexity  
- C. Automatic compliance approval  
- D. Eliminating the need for API platforms  

### Q9 — [Architecture judgment] [LO: LO-4.4] [Difficulty: Hard] [Category: Roadmaps]

Which roadmap design is weakest for executive funding?

- A. Phases with value, risk reduced, and dependencies  
- B. A backlog of 40 initiatives all starting Month 1  
- C. Value-versus-risk prioritization with explicit non-goals  
- D. Foundation guardrails before speculative platforms  

### Q10 — [Leadership judgment] [LO: LO-4.4] [Difficulty: Medium] [Category: Roadmaps]

CFO cuts 30% of transformation funding. The Lead EA should first:

- A. Keep the same target outcomes and hide scope cuts in technical jargon  
- B. Renegotiate outcomes and re-sequence waves based on value and risk  
- C. Cancel Transition A guardrails to save money  
- D. Replace the roadmap with a vendor proposal  

---

## Scenario questions (3)

### S1 — [Application] [LO: LO-4.2] [Difficulty: Medium] [Category: Modernization]

**Scenario:** PartnerLink Classic, FileBridge, and SyncHub all move partner files. New partner onboarding is slow; run cost is high. Marcus proposes rehosting all three to cloud “as Phase 1 wins.”

**Prompt:** Recommend a disposition approach for the three platforms. Explain what you would do with new partner volume vs legacy volume, and name the primary risk of Marcus’s proposal.

**Response guidance (student-facing):** 150–250 words; state recommendation, alternatives, and primary risk.

### S2 — [Trade-off analysis] [LO: LO-4.3] [Difficulty: Hard] [Category: Transitions]

**Scenario:** Elena agrees to consolidate CRMs but refuses any campaign freeze. Raj requires audit evidence during dual-write. Priya wants golden record rewrite before any CRM migration.

**Prompt:** Propose Transition B design choices that balance coexistence, evidence, and sequencing. What do you accept delaying, and what exit criteria unlock Transition C?

### S3 — [Architecture judgment] [LO: LO-4.4] [Difficulty: Hard] [Category: Roadmaps]

**Scenario:** Maya wants a visible CX win by Month 9. Raj wants identity/landing-zone guardrails first. A BU proposes funding a speculative AI platform in Phase 1.

**Prompt:** Build a high-level 24-month sequencing rationale (Phase 0–3). Where does the AI platform go, and how do you explain that to Maya in business language?

---

## Discussion questions (2)

### D1 — [Leadership judgment] [Category: Leadership]

How should a Lead EA communicate a consolidate decision to the business unit that “loses” its CRM—without pretending there is no loser, and without escalating into permanent dual retention?

### D2 — [Trade-off analysis] [Category: Roadmaps]

When should NorthStar prioritize risk-reduction initiatives ahead of customer-experience initiatives on the roadmap—and what signals tell you the balance is wrong?
