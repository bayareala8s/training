# Speaking Script — Module 01: The Enterprise Architect’s Role

**Total runtime target:** 120 minutes  
**Tone:** Executive, practical, trade-off aware  
**Case study:** NorthStar Financial Services (fictional)

Instructors may paraphrase; timing cues are targets.

---

## [0:00–0:05] Welcome and framing

> Welcome to the Enterprise Architecture Leadership Masterclass on BayLearn.  
> Today is Module 01: The Enterprise Architect’s Role.  
> Remember: you are the newly appointed Lead Enterprise Architect at NorthStar Financial Services—our **fictional** enterprise case study. It is not a real company and is not affiliated with any employer.  
> By the end of this session you will have a first-cut architecture operating model: mission, decision rights, principles, engagement, and a clear stance on how you will influence outcomes without relying only on your title.  
> [Slide 1] BayLearn branding—navy, white, gold accents. We keep slides sparse; the thinking happens on the whiteboard and in your artifacts.

**Housekeeping (30 seconds):** lab timebox, breaks, office hours pointer.

---

## [0:05–0:15] Business scenario

> [Slide 2] Here is NorthStar’s starting condition.  
> NorthStar has more than three hundred applications, hybrid hosting, and multiple acquired companies still partially integrated. Leadership wants cost down about twenty percent, faster onboarding, faster digital products, stronger resilience, governed AI, and better executive visibility into technology risk.  
> Critically for today: architects already exist inside business units—Retail, Payments, Partner Channels, Wealth—but there is **no consistent enterprise governance**. Decisions are made independently. Security is often late. Duplicate platforms keep appearing.  
> Last quarter, three overlapping customer-identity initiatives were funded. Partner onboarding still spans multiple file-transfer approaches. The CIO has asked you for an architecture operating model before the next Executive Committee technology review—not another framework slideshow.

**Ask the room:**

> If NorthStar’s architecture function disappeared tomorrow, which business outcome would get worse first—and through what mechanism?  
> Take twenty seconds. Then I’ll take two voices.

*[Listen. Affirm causal reasoning. Redirect title debates.]*

> Good. Hold that tension. Your job is not to personally redesign every system. Your job is to improve **decision quality** across the enterprise.

---

## [0:15–0:35] Architecture concept

### [0:15–0:22] What EA really is

> [Slide 3–4] Learning objectives, then definition.  
> Enterprise architecture is a leadership system that connects strategy to technology direction across domains. It clarifies where autonomy is safe, what should be shared, and which risks need explicit executive trade-offs.  
> It is not a drawing service. It is not owning every backlog. It is not approving every pull request.

> [Slide 5] Look at role boundaries. Solution architects optimize inside a solution boundary. Platform and cloud architects create golden paths and guardrails. Engineering managers own team delivery. Enterprise architects own cross-domain decision quality, principles, and portfolio risk visibility.  
> Overlapping titles are fine. Overlapping accountabilities without decision rights create the NorthStar failure mode—architecture theater.

> [Whiteboard / Slide 6] Decision stack—draw with me: strategy outcomes, capabilities, investment themes, principles and decision rights, platforms and guardrails, then solution choices.  
> When someone asks “Should we buy Product X?”, climb the stack. Do not start with vendor features.

**Check for understanding:**

> In one sentence: what is EA accountable for at NorthStar that a strong solution architect is not?

### [0:22–0:30] Operating model

> [Slides 8–9] An operating model is not just an org chart. It includes mission, structure option, decision rights, RACI, engagement model, cadence, and capacity.  
> Three structural options—and I will not crown a universal winner.  
> **Centralized:** consistency and clear accountability, but slow and politically expensive after acquisitions.  
> **Federated:** local speed and respect for BU power, but enterprise standards become optional and shared platforms starve.  
> **Hybrid:** federated domain and solution architects remain in BUs; a small enterprise office owns principles, cross-domain decision rights, platform partnership, and executive risk visibility; ARB handles material exceptions only.  
> For NorthStar Year 1, hybrid usually fits—because architects already sit in BUs and you need a coalition. That is **fit**, not dogma. If you choose central or pure federate, you must name the risk you accept.

> [Slide 10] Engagement modes: consult, collaborate, govern. Misuse any mode and you become either a bottleneck or irrelevant.  
> Bias toward automated guardrails. Reserve human gates for high-impact decisions.

> [Slide 11] Decision classes—local within guardrails; domain target; enterprise principles; golden-path changes; material exceptions including high-risk AI and multi-year lock-in.  
> Let’s place Payments’ “second API gateway for latency” on this board. That is not a local story choice. Treat it as platform / cross-domain.

### [0:30–0:35] Principles preview

> [Slides 13–14] Principles fail when they are fashion statements—“be cloud-native,” “prefer Kubernetes.”  
> A usable principle has statement, rationale tied to NorthStar strategy, implications, exception path, and signals. Aim for eight to ten.  
> Without exceptions, principles become lies. With uncontrolled exceptions, they become wallpaper. Time-box exceptions with owners and sunsets.

---

## [0:35–0:50] Instructor demonstration + leadership

> [Slide 15] Leadership assessment. You have a title. You do **not** have line authority over BU architects or engineering managers. If your model depends on obedience to title, it fails.  
> Influence sources: expertise, network, process usefulness, executive sponsorship, delivery credibility, and evidence.  
> Sequence: listen, shared problem framing, lightweight principles, one useful decision, visible risk reporting—then expand decision rights. Credibility before control.

> [Slide 16] Watch how I would approach a fragment of the lab as NorthStar’s Lead EA. I will make trade-offs explicit—including what I am *not* choosing.

**Demo steps (narrate while doing):**

1. Mission in plain language: “Architecture improves enterprise decision quality, reuse, and risk visibility—without owning delivery backlogs.”  
2. Reject broad ARB-for-everything; choose hybrid with narrow material gates.  
3. Place second API gateway in platform decision class; single Accountable = Platform Architect with EA and Security consulted; ARB if exception exceeds threshold.  
4. Draft principle “Prefer platform golden paths” with exception and signal; reject “be API-first” as a slogan.  
5. Risk register entry: “BU presidents bypass EA”—mitigation: faster engagement than chaos + CIO digest.

> Notice the artifact shape. Your lab should produce something a CIO could skim in ten minutes.

*[Optional 3-minute bio break here if not taken earlier.]*

---

## [0:50–1:30] Guided lab

> [Slides 17–18] Common mistakes in one glance: senior-designer trap, org chart without rights, shopping-list principles, ignoring BU architects.  
> You now have about forty minutes. Work in pairs if you want; submissions are individual.  
> Lab: Establish NorthStar’s Architecture Function.  
> Deliverables: mission, operating model diagram, RACI, eight to ten principles, decision rights, engagement model, risk register.  
> Use templates for principles and RACI. I will circulate. At the halfway mark I will call a two-minute progress check.

**[1:10] Mid-lab check**

> What decision is hardest right now—and what evidence would make it easier?

*[Take 2–3 answers. Unstick dual-A RACIs and technology principles.]*

> Ten-minute warning at approximately 1:20. At 1:30 we debrief even if polish remains—finish as homework.

---

## [1:30–1:45] Architecture review

> Let’s review one or two volunteer artifacts. We will practice ARB-style questions: alignment, risk, alternatives, and feasibility—not nitpicks on fonts.

**Prompt:**

> Walk Payments’ second API gateway through your decision classes. Who is Accountable? What did you reject? Where do Security and exceptions show up?

*[Use debrief-questions.md. Affirm trade-off language. Correct misconceptions gently.]*

> Complete this sentence together: “Architecture leadership at NorthStar succeeds when ___ without needing ___.”

---

## [1:45–1:55] Assignment briefing

> [Slide 19] Before Module 02, refine your lab into a CIO-ready pack and add a one-page influence narrative: how you will lead without line authority for ninety days.  
> Rubric emphasis this week: business alignment, trade-off analysis, and communication quality. Security and resilience should appear proportionately—do not omit Security from RACI.  
> Capstone link: mission, principles, decision rights, engagement, and architecture-function risks carry forward.  
> Formative quiz is available; use it as self-check, not trivia night.

---

## [1:55–2:00] Close

> [Slides 20–21] Key takeaways:  
> 1. EA is a decision and influence system—not universal design ownership.  
> 2. Operating models are trade-offs; hybrid fits NorthStar Year 1 because federated architects already exist—defend your fit factors.  
> 3. Principles need exceptions and signals; leadership needs credibility before control.  
> Next module: Business Architecture and Capability Mapping—we translate strategy into capability heatmaps so investment arguments stop being tool debates.  
> Office hours: bring blockers on decision classes or principle wording.  
> Thank you—see you at Module 02.

---

## Optional office-hour prompts

- “Help me collapse twelve principles to eight without losing security.”  
- “Is my ARB trigger list too broad for Year 1?”  
- “How do I phrase non-ownership of delivery without sounding useless to the CIO?”
