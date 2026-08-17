# Module 01 Quiz — The Enterprise Architect’s Role

**Type:** Formative (default)  
**Items:** 10 MCQ + 3 scenario + 2 discussion  
**Case study:** NorthStar Financial Services (fictional)

Answer key: `assessments/answer-keys/module-01-answer-key.md` (instructor)

---

## Multiple choice (10)

### Q1 — [Recall] [LO: M01-LO1] [Difficulty: Easy] [Category: Role definition]

At NorthStar, what best describes the primary job of enterprise architecture?

- A. Personally designing every solution so delivery teams stay consistent  
- B. Connecting business strategy to technology direction across domains through decision quality, reuse, and risk visibility  
- C. Approving every pull request that touches shared libraries  
- D. Replacing all BU architects with a centralized design team in week one  

### Q2 — [Application] [LO: M01-LO1] [Difficulty: Medium] [Category: Role boundaries]

Partner Channels wants a new file-transfer tool. Payments already runs two file platforms. Which move best reflects Lead EA accountability (vs. solution architecture alone)?

- A. Immediately build the partner API yourself in a three-week spike  
- B. Frame the capability and decision class, surface enterprise cost/risk, and force a platform-level trade-off  
- C. Tell Partner Channels they are free to choose any tool because federation means no standards  
- D. Ban all file transfer and mandate APIs enterprise-wide without coexistence planning  

### Q3 — [Trade-off analysis] [LO: M01-LO2] [Difficulty: Medium] [Category: Operating model]

Which statement best captures a real trade-off for NorthStar’s Year-1 operating model?

- A. Hybrid is always best practice for every enterprise worldwide  
- B. Centralization maximizes consistency but often faces high political cost where BU architects already exist  
- C. Pure federation guarantees shared platform funding  
- D. Broad ARBs always increase delivery speed  

### Q4 — [Architecture judgment] [LO: M01-LO3] [Difficulty: Medium] [Category: Principles]

Which draft is closest to a usable architecture principle for NorthStar?

- A. “We will be cloud-native and agile.”  
- B. “Prefer Kubernetes for all workloads.”  
- C. “We will prefer platform golden paths before creating new platforms; exceptions are time-boxed with owners and sunsets.”  
- D. “Buy the best vendor in each category.”  

### Q5 — [Leadership judgment] [LO: M01-LO4] [Difficulty: Medium] [Category: Influence]

You lack line authority over Retail’s architects. Which approach best builds influence in the first 30 days?

- A. Mandate compliance to a 40-principle wiki and escalate non-compliance immediately  
- B. Skip listening and launch a weekly ARB for all projects  
- C. Conduct a listening tour with BU architects and co-author a short principle set while landing one useful decision  
- D. Redesign Payments’ core systems personally to prove expertise  

### Q6 — [Recall] [LO: M01-LO2] [Difficulty: Easy] [Category: Governance vocabulary]

In this course, what is the key difference between a **guardrail** and a **gate**?

- A. Guardrails are human approvals; gates are automated  
- B. Guardrails are preventive/automated controls enabling safer autonomy; gates are review checkpoints requiring approval  
- C. They are synonyms for ARB  
- D. Gates apply only to AI systems; guardrails apply only to cloud accounts  

### Q7 — [Application] [LO: M01-LO3] [Difficulty: Medium] [Category: Exceptions]

A Payments team needs a 60-day exception to an integration principle for a regulatory deadline. What is the most architecture-healthy response?

- A. Deny all exceptions to “set an example”  
- B. Grant a silent verbal exception with no record  
- C. Approve a time-boxed exception with risk note, owner, sunset date, and recorded decision  
- D. Require twelve signatures including CEO for any exception  

### Q8 — [Trade-off analysis] [LO: M01-LO2] [Difficulty: Hard] [Category: ARB scope]

NorthStar proposes an ARB that reviews every project. What is the most likely failure mode?

- A. Too much executive visibility into risk  
- B. Review queues, ceremony without decision quality, and teams bypassing the process  
- C. Immediate elimination of all duplicate platforms  
- D. Automatic improvement in golden-path adoption  

### Q9 — [Architecture judgment] [LO: M01-LO2] [Difficulty: Hard] [Category: Decision rights]

Payments proposes a second API gateway “only for high-volume payment APIs.” Under a sound Year-1 hybrid model, how should this be classified?

- A. Purely local solution choice with Engineering Manager solely Accountable and EA uninvolved  
- B. Sprint backlog prioritization decision owned only by Product  
- C. Cross-domain / platform decision class with Platform (and EA/Security consulted); ARB if thresholds for exception/material risk are met  
- D. Immediate ExCo vote before any technical analysis  

### Q10 — [Leadership judgment] [LO: M01-LO4] [Difficulty: Medium] [Category: Influence]

Wealth announces a near-signed CRM platform decision in a town hall without consulting EA. What is the strongest first move?

- A. Publicly veto the deal in the town hall  
- B. Ignore it to avoid conflict  
- C. Private engagement with Wealth and CIO: map decision class, quantify integration/identity risk, document alternatives, and escalate only if material thresholds are met  
- D. Rewrite the operating model overnight to centralize all architects under you  

---

## Scenario questions (3)

### S1 — [Application] [LO: M01-LO2] [Difficulty: Medium] [Category: Operating model]

**Scenario:** NorthStar’s CIO offers two staffing options: (1) move all BU architects under the Lead EA within 60 days, or (2) keep them federated and fund a three-person enterprise architecture office plus a narrow ARB.

**Prompt:** Recommend an option for Year 1. Name the primary benefit, the primary risk you accept, and one mitigation.

**Response guidance (student-facing):** 150–250 words; state recommendation, alternatives, and primary risk.

### S2 — [Trade-off analysis] [LO: M01-LO3] [Difficulty: Hard] [Category: Principles]

**Scenario:** A working group drafts 28 principles including vendor names, “API-first,” and “zero trust everywhere,” with no exception process.

**Prompt:** Explain why this set will fail at NorthStar and outline how you would reshape it into 8–10 principles that executives and delivery teams can use.

### S3 — [Architecture judgment] [LO: M01-LO4] [Difficulty: Hard] [Category: Leadership]

**Scenario:** Your organizational readiness scores show weak golden paths (2/4) and only moderate sponsorship (2/4). A risk officer wants a heavy gate-based governance model immediately.

**Prompt:** What governance increment do you propose for the next 90 days, what do you refuse to launch yet, and how do you still take material risk seriously?

---

## Discussion questions (2)

### D1 — [Leadership judgment] [LO: M01-LO4] [Category: Influence]

When should a Lead EA escalate to the CIO versus continuing to influence peer-to-peer—and what signals tell you escalation will help rather than brand you as political?

### D2 — [Trade-off analysis] [LO: M01-LO2] [Category: Autonomy vs control]

How much local autonomy should NorthStar’s BU architects retain in Year 1, and which decision classes must remain enterprise-accountable even if it creates friction with BU presidents?
