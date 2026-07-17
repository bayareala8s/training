# Speaking Script — Module 05: Cloud and Platform Strategy

**Total runtime target:** 120 minutes  
**Tone:** Executive, practical, trade-off aware  
**Case study:** NorthStar Financial Services (fictional)

---

## [0:00–0:05] Welcome and framing

> Welcome back. Today is Module 05: Cloud and Platform Strategy.  
> You remain Lead Enterprise Architect at NorthStar—our fictional case.  
> By the end of this session you will be able to defend a cloud posture, sketch a landing zone, decide build-versus-buy for a platform capability, and show FinOps controls in AWS.

---

## [0:05–0:15] Business scenario

> The CIO said “cloud-first.” Teams opened accounts. Finance cannot allocate spend. Security cannot find a single audit trail. Cost is up; speed is not.  
> Ask the room: What must be true before we accelerate migrations?

---

## [0:15–0:35] Architecture concept

> Cloud strategy is posture, principles, and placement—not a migration spreadsheet.  
> Whiteboard the landing zone: audit, shared, workloads, sandboxes.  
> Capability map: what is platform-provided versus team-owned.  
> Check for understanding: Name one capability that is commodity and one that is differentiating for NorthStar.

---

## [0:35–0:50] Instructor demonstration

> Watch how I approach this. I will use native CloudTrail into a central audit bucket rather than building a custom pipeline—commodity control, buy/reuse.  
> Then I’ll show the Terraform lab outputs and curl the health endpoint. Tags and budget are not optional decoration—they are architecture.

---

## [0:50–1:30] Guided lab

> Forty minutes. Lab 05: platform foundation. Deliverables include strategy artifacts plus working validate and cleanup.  
> Mid-lab check: What decision is hardest—and what evidence would help?

---

## [1:30–1:45] Architecture review

> Volunteer: show capability map or ADR. ARB-style questions: alignment, risk, alternatives, feasibility.

---

## [1:45–1:55] Assignment briefing

> Package the cloud strategy, FinOps policy, and ADR. Rubric emphasis: trade-offs and feasibility. Capstone link: platform baseline.

---

## [1:55–2:00] Close

> Takeaways: (1) Platform before unmanaged migration. (2) Buy commodity controls. (3) FinOps is a control plane.  
> Next: Module 06 Integration, Application, and Data Architecture. Destroy lab resources tonight.
