# Speaking Script — Module 08: AI Strategy and Intelligent Enterprise Architecture

**Total runtime target:** 120 minutes  
**Tone:** Executive, practical, risk-aware—no hype  
**Case study:** NorthStar Financial Services (fictional)

Instructors may paraphrase; timing cues are targets.

---

## [0:00–0:05] Welcome and framing

> Welcome back to the Enterprise Architecture Leadership Masterclass.  
> Today is Module 08: AI Strategy and Intelligent Enterprise Architecture.  
> You remain Lead Enterprise Architect at NorthStar Financial Services—fictional.  
> By the end of this session you will score AI use cases, design a governed incident decision assistant, prove validation and human-in-the-loop, and evaluate quality with a labeled dataset.

---

## [0:05–0:15] Business scenario

> The COO wants AI everywhere. Three business units propose chatbots. None can name an operating KPI. Meanwhile Incident Response is drowning in noisy tickets.  
> If your first move is to pick a model brand, you skipped strategy.

**Ask the room:**

> What evidence would make an incident decision assistant a conditional-go rather than a science fair?

---

## [0:15–0:35] Architecture concept

> Enterprise AI strategy is a portfolio of use cases scored on value, feasibility, data readiness, risk, operability, cost, and alignment.  
> For operational decisions we prefer structured JSON outputs, schema validation, and deterministic rules that separate *proposal* from *decision*. Human-in-the-loop is a designed control—not a vague promise someone will glance at the screen.  
> Evaluation is part of architecture: a labeled set and an explicit quality measure. Token cost is a non-functional requirement.

**Check for understanding:**

> Name one field that must never be free-text-only if we route payment-impacting incidents.

---

## [0:35–0:50] Instructor demonstration

> I will demonstrate the governed path. Mock mode is first-class—Bedrock is optional.

**Demo steps (narrate while doing):**

1. Show a filled scorecard: conditional-go with HITL for severity ≥ High.
2. Walk API → Step Functions → infer → validate/route → DynamoDB/S3.
3. Invoke a sample incident; show valid JSON.
4. Break a required field; show HITL routing.
5. Score a handful of eval-set rows; state the quality measure and a cost note.

> Notice we do not auto-execute remediations. Advise and route first.

---

## [0:50–1:30] Guided lab

> About forty minutes. Individual submissions.  
> Lab: Build NorthStar’s Governed AI Decision Assistant.  
> Deliverables: scorecard, architecture notes, invoke evidence (mock OK), HITL path, eval results, cost/token notes, cleanup if AWS used.  
> Midway progress check at about twenty minutes.

**[1:10] Mid-lab check**

> Are you blocked on Bedrock—or on defining HITL triggers and a quality measure?

---

## [1:30–1:45] Architecture review

> ARB-style review: alignment, residual risk, alternatives, feasibility, operability.

**Prompt:**

> Walk us from one KPI to one scorecard risk to one HITL trigger—and tell us what you still will not automate.

---

## [1:45–1:55] Assignment briefing

> Assignment Module 08: strategy package with scorecard, governed architecture, HITL policy, eval write-up, and executive risk/cost narrative. These feed the capstone AI governance artifacts. Rubric rewards trade-offs and honesty about residual risk.

---

## [1:55–2:00] Close

> Cleanup if you deployed. Formative quiz available. Next: Module 09—governance and the Architecture Review Board, including how AI decisions get approved.  
> Thank you—leave the hype on the whiteboard.
