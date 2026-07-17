# Speaking Script — Module 04: Target-State Architecture and Transformation Roadmaps

**Total runtime target:** 120 minutes  
**Tone:** Executive, practical, trade-off aware  
**Case study:** NorthStar Financial Services (fictional)

Instructors may paraphrase; timing cues are targets.

---

## [0:00–0:05] Welcome and framing

> Welcome back to the Enterprise Architecture Leadership Masterclass.  
> Today is Module 04: Target-State Architecture and Transformation Roadmaps.  
> Remember: you are the newly appointed Lead Enterprise Architect at NorthStar Financial Services—our fictional enterprise case study.  
> By the end of this session you will define a target state, choose modernization dispositions, design three transition architectures, and draft a 24-month roadmap executives can fund and challenge.

> Fiction reminder: NorthStar and all application names are invented for learning.

---

## [0:05–0:15] Business scenario

> Maya Chen, our CIO, opens ExCo with a beautiful slide: one cloud, one CRM, AI everywhere—Target 2028.  
> Elena Vos, Retail Banking president, asks: which of my acquired products still run next year, and who pays for dual-run?  
> Raj Patel, CISO, asks: where do identity and audit evidence live while we migrate?  
> Marcus wants to lift everything to cloud this year. Priya wants a customer master rewrite before any CRM move.  
> Your job is not a prettier vision. Your job is a defensible target state, honest transitions, and a roadmap with value per wave.

**Ask the room:**

> If you had to cut Maya’s slide to one sentence that a CFO would fund, what would it say?

---

## [0:15–0:35] Architecture concept — target + strategies

> Let’s define target state properly. It is the coherent future landscape we intend to operate—capabilities, application patterns, integration and data ownership, security and resilience posture, and operating-model rules.  
> It is not a vendor catalog, not a full inventory rewrite, and not a promise of greenfield.

**Whiteboard / slide:** Target-State Canvas

> Fill outcomes, principles, constraints, and especially non-goals. If you cannot name non-goals, you are doing marketing.

> Now strategies. We use seven: rehost, replatform, refactor, replace, retire, retain, consolidate.  
> TIME from Module 03 is the portfolio lens. These seven are execution choices. Do not treat them as identical.  
> At NorthStar, consolidate matters because acquisitions created duplicates. Retain matters because StarCore will not be rewritten in year one.

**Check for understanding:**

> Why is “migrate to cloud” not an acceptable disposition by itself?

---

## [0:35–0:50] Transitions + roadmaps (concept continued) + demo setup

> Transition architectures are interim landscapes with systems of record, temporary interfaces, and exit criteria.  
> Without exit criteria, temporary becomes permanent—FileBridge forever.  
> You will design three: Stabilize and standardize; strategic journeys coexist; shrink dual-run.

> Roadmaps are not project plans. They answer what landscapes and outcomes, in what order, why.  
> Sequence with foundation before fashion, explicit dependencies, and value every six to eight months.  
> Use value-versus-risk to prioritize—and kill low-value noise like a fourth CRM or unconstrained AI platform.

---

## [0:50–1:05] Instructor demonstration

> Watch how I would approach this as NorthStar’s Lead EA. I will make trade-offs explicit—including what I am not choosing.

**Demo steps (narrate while doing):**

1. Draft five principles and two non-goals (no StarCore rewrite Y1; no fourth CRM).  
2. Disposition pass: StarCore retain+replatform; CRMs consolidate; file bridges consolidate/retire; orphan reports retire.  
3. Transition A exit criteria live: landing-zone guardrails on; CRM survivor ADR approved; new partners on API path. Sketch Phase 0–1 roadmap rows with dependencies.

> Notice the artifact shape. Your lab should produce something an executive or ARB could consume—not a brainstorm dump.

---

## [1:05–1:40] Guided lab

> You now have about 35 minutes. Work in pairs if you want, but submissions are individual.  
> Lab: Create NorthStar’s Target-State Roadmap.  
> Deliverables: target-state architecture, three transition states, 24-month roadmap with value, risks, executive summary.  
> I will circulate. At the halfway mark I will call a 2-minute progress check.

**[1:22] Mid-lab check**

> What decision is hardest right now—and what evidence would make it easier?  
> Read one exit criterion aloud—is it observable?

---

## [1:40–1:50] Architecture review

> Let’s review 1–2 volunteer artifacts. We will practice ARB-style questions: alignment, risk, alternatives, and feasibility—not nitpicks on formatting.

**Prompt:**

> Which dependency, if late, breaks your Phase 2 value story—and what would you tell the CFO?

---

## [1:50–1:55] Assignment briefing

> Polish the lab into submission quality before Module 05. Use templates 23, 24, and 09.  
> Rubric emphasis this week: feasibility and roadmap, trade-off analysis, and business alignment. Security/resilience: call out identity and audit in coexistence—even though Module 07 goes deeper.  
> Capstone link: target-state, transition plan, and roadmap become core portfolio artifacts.

---

## [1:55–2:00] Close

> Key takeaways:  
> 1. Target state is patterns, principles, outcomes, and non-goals—not vision theater.  
> 2. Transitions without exit criteria are how temporary platforms become permanent cost.  
> 3. Roadmaps earn funding when they show value, risk reduction, and dependencies per wave.  
> Next module: Cloud and Platform Strategy—your Phase 0 landing zone becomes real. Office hours: bring your weakest exit criterion.

---

## Optional office-hour prompts

- Help me defend retain for StarCore against a rewrite vendor pitch.  
- Stress-test my dual-write reconciliation exit criteria.  
- Rebuild my roadmap after a 30% budget cut.
