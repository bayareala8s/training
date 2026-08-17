# Speaking Script — Module 07: Security, Risk, Compliance, and Resilience

**Total runtime target:** 120 minutes  
**Tone:** Executive, practical, trade-off aware  
**Case study:** NorthStar Financial Services (fictional)

Instructors may paraphrase; timing cues are targets.

---

## [0:00–0:05] Welcome and framing

> Welcome back to the Enterprise Architecture Leadership Masterclass.  
> Today is Module 07: Security, Risk, Compliance, and Resilience.  
> You remain the Lead Enterprise Architect at NorthStar Financial Services—our fictional case study.  
> By the end of this session you will turn trust boundaries, threat models, and RTO/RPO into evidence—not slogans.

---

## [0:05–0:15] Business scenario

> Priya Raman, our fictional CISO, got a simple audit question: who can read Restricted settlement files?  
> It took too long to answer. Encryption was “on,” but IAM was broad, and recovery objectives were assumed.  
> Your job is to make the platform slice explainable: boundaries, controls, tests, and evidence.

**Ask the room:**

> If audit called you in one hour, what three artifacts would you want already prepared?

---

## [0:15–0:35] Architecture concept

> Zero Trust is not a shopping list. It is continuous verification, least privilege, and assume-breach—expressed as trust boundaries.

**Whiteboard / slide:** Trust boundary swim lanes

> STRIDE gives us a shared language for abuse cases. Encryption does not cover Spoofing or Elevation by itself.  
> RTO and RPO are business targets. Patterns have costs. Versioning plus a drill is often the honest starting point; cross-region replication is optional and costs more.

**Check for understanding:**

> Which is more dangerous for Restricted data this week: no CRR, or untested restore with broad IAM?

---

## [0:35–0:50] Instructor demonstration

> Watch how I would approach this as NorthStar’s Lead EA. I will keep CRR off by default and narrate why.

**Demo steps (narrate while doing):**

1. Show terraform.tfvars with enable_replication false and BayLearn tags
2. Contrast wildcard IAM vs prefix-scoped writer/reader roles
3. Upload synthetic object with SSE-KMS; show versions; narrate restore
4. Sketch one control-evidence row tied to terraform outputs

> Notice the artifact shape. Your lab should produce something audit and executives can consume.

---

## [0:50–1:30] Guided lab

> You have about 40 minutes. Lab: Secure and Resilient NorthStar’s Digital Platform.  
> Deliverables: classification + boundaries, STRIDE, RTO/RPO + drill, control-evidence matrix, cleanup.  
> I will circulate. Mid-lab check at the halfway mark.

**[1:10] Mid-lab check**

> What decision is hardest right now—and what evidence would make it easier?

---

## [1:30–1:45] Architecture review

> Let’s review 1–2 volunteer matrices. We will ask ARB-style questions: alignment, residual risk, alternatives, feasibility.

**Prompt:**

> Show me one risk row where the evidence path is a real ARN—and tell me what residual risk remains.

---

## [1:45–1:55] Assignment briefing

> Produce an executive resilience brief, refined matrix, and an ADR choosing CRR versus simulated DR for settlement files.  
> Rubric emphasis: security/resilience and trade-off analysis.  
> Capstone link: threat model, RTO/RPO, risk-control artifacts.

---

## [1:55–2:00] Close

> Key takeaways:  
> 1. Boundaries and least privilege beat tool slogans.  
> 2. RTO/RPO without drills are fiction.  
> 3. Evidence matrices make risk discussable.  
> Next module: AI Strategy and the governed decision assistant. Cleanup before you leave. Office hours as scheduled.

---

## Optional office-hour prompts

- How would you separate KMS ownership into a security account?
- How do you negotiate a time-bound IAM exception with Payments?
