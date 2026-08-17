# Instructor Guide — Module 05: Cloud and Platform Strategy

**Audience:** BayLearn instructors  
**Classification:** Instructor package (pair with reference solutions privately)

---

## 1. Module purpose

Enable students to define NorthStar’s cloud/platform strategy and prove foundational FinOps and audit controls on AWS at low cost.

## 2. Learning objectives

1. Define cloud strategy, posture, and placement principles
2. Design landing-zone concepts and platform capability maps
3. Complete build-versus-buy ADRs for platform capabilities
4. Apply FinOps tagging, budgets, and lifecycle in a live lab

## 3. Prerequisites

Modules 01–04 context; AWS CLI + Terraform; sandbox AWS account.

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Business scenario and lesson | 15 |
| Architecture concept (LZ + capabilities) | 20 |
| Instructor demonstration (Terraform outputs + ADR sketch) | 15 |
| Guided lab | 40 |
| Architecture review | 15 |
| Assignment briefing | 10 |
| Buffer / breaks | 5 |

## 5. Opening business scenario

CIO declares cloud-first; account sprawl begins; Finance cannot allocate spend; Security lacks a shared audit trail. Ask: “What must be true before we accelerate migrations?”

## 6. Lesson flow

1. Posture and principles (5.1)
2. Landing zone + capability map (5.2)
3. Build vs buy ADR (5.3)
4. FinOps + lab bridge (5.4)

## 7. Questions to ask

1. Is multi-cloud a strategy or a slogan here?
2. Who owns the audit account?
3. Which capability is commodity vs differentiator?
4. What happens at 80% budget?

## 8. Whiteboard sequence

See `whiteboard-plan.md`.

## 9. Demonstration steps

1. Show `environments/lab05` structure and tags
2. Apply (or show pre-applied outputs) and curl `/health`
3. Sketch ADR decision for “use native CloudTrail vs custom audit pipeline”

## 10. Break points

- After concept block (~35 min)
- Mid-lab check (~75 min)

## 11. Lab facilitation

See `lab-facilitation-guide.md`.  
**Lab goal:** Working foundation + strategy artifacts + cleanup.  
**Timebox rule:** Protect last 25 minutes for review + assignment even if labs incomplete.

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| IAM denied | Provide least-priv checklist; don’t broaden to Administrator casually |
| Stuck on Terraform errors | Pair debug; validate region and tfvars |
| Over-scoping landing zone | Push conceptual diagram—not Control Tower build |
| Want to enable Config | Cost warning; stretch only |

## 13. Debrief questions

Use `modules/module-05-cloud-platform/debrief-questions.md`.

## 14. Assignment briefing

Cloud strategy package + ADR; emphasize trade-offs and FinOps. Capstone: platform baseline.

## 15. Suggested homework

- Finish lab artifacts
- Quiz formative
- Read ahead Module 06 integration patterns template

---

## Materials checklist

- [ ] Slides loaded
- [ ] Speaking script reviewed
- [ ] Lab Terraform validated in instructor account recently
- [ ] Reference solution reviewed privately
- [ ] Grading guide open
