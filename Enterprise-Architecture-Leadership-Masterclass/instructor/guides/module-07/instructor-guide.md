# Instructor Guide — Module 07: Security, Risk, Compliance, and Resilience

**Audience:** BayLearn instructors  
**Student materials:** modules/, labs/, assessments/ (non-key)  
**Classification:** Instructor-only when combined with reference solutions  
**Case study:** NorthStar Financial Services (fictional)

---

## 1. Module purpose

Enable students to treat security, risk, compliance, and resilience as first-class architecture concerns—producing trust boundaries, STRIDE models, RTO/RPO with recovery evidence, and control-evidence matrices tied to a low-cost AWS lab.

## 2. Learning objectives

1. Apply Zero Trust principles and trust-boundary design (M07-LO1)
2. Perform lightweight STRIDE threat modeling (M07-LO2)
3. Define RTO/RPO and validate recovery (M07-LO3)
4. Produce a control-evidence matrix mapped to AWS controls (M07-LO4)

## 3. Prerequisites

Modules 05–06 recommended. AWS CLI + Terraform 1.5+. Budget alert verified. See `modules/module-07-security-resilience/prerequisites.md`.

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Business scenario and Zero Trust | 15 |
| STRIDE + resilience concepts | 20 |
| Instructor demonstration | 15 |
| Guided lab | 40 |
| Architecture review / debrief | 15 |
| Assignment briefing | 10 |
| Buffer / breaks | 5 |

## 5. Opening business scenario

Priya Raman (fictional CISO) cannot answer who can read Restricted settlement files within an hour. Recovery objectives are assumed, not tested. Students must make boundaries, controls, and evidence explicit.

## 6. Lesson flow

1. Zero Trust ≠ product; draw trust boundaries for the landing zone
2. STRIDE pass with owners and residual risk
3. RTO/RPO tiers; prefer versioning + drill over expensive always-on DR
4. Control-evidence matrix as executive/audit artifact
5. Lab deploy → encrypt → delete/restore drill → matrix → cleanup

## 7. Questions to ask

1. Where does trust change when a partner object lands in S3?
2. Which STRIDE category is least controlled by “encryption on”?
3. Who owns RTO/RPO for settlement files—business or platform?
4. What evidence would you bring to internal audit tomorrow?

## 8. Whiteboard sequence

See `whiteboard-plan.md`. Summary:

1. Actors → boundaries → data classes
2. STRIDE sticky notes on boundaries
3. RTO/RPO box with pattern choices and cost callouts

## 9. Demonstration steps

1. Show `terraform.tfvars.example` with `enable_replication = false` and explain cost
2. Walk IAM role policy prefixes vs wildcards
3. Show head-object SSE-KMS and list-object-versions restore narrative
4. Show one control-evidence row mapping to `terraform output` ARNs

## 10. Break points

- After concept block (~35 min)
- Mid-lab check (~75 min): “What is your hardest residual risk?”

## 11. Lab facilitation

See `lab-facilitation-guide.md`.

**Lab goal:** Deploy the security/resilience slice, prove recovery, produce evidence matrix, clean up.

**Timebox rule:** Protect the last 25 minutes for review + assignment briefing even if labs are incomplete. Cleanup is mandatory before leaving.

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| AccessDenied on KMS | Point to key policy principals + role kms actions |
| Wants to enable CRR immediately | Ask for cost envelope; default to simulated DR |
| STRIDE as vocabulary only | Require abuse case + owner + priority |
| Skips cleanup | Hold lab credit; run script together |

## 13. Debrief questions

1. Which control gave the most risk reduction per dollar?
2. What residual risk remains after the lab?
3. How does this artifact feed the capstone?

## 14. Assignment briefing

Executive resilience brief + refined control-evidence matrix + one ADR on CRR vs simulated DR. Rubric emphasizes security/resilience and trade-off analysis.

## 15. Suggested homework

- Finish lab deliverables and cleanup confirmation
- Module 07 quiz (formative)
- Polish assignment for next session

---

## Materials checklist

- [ ] Slides loaded
- [ ] Speaking script reviewed
- [ ] Lab Terraform path verified
- [ ] Reference solution reviewed privately
- [ ] Grading guide open for office hours
- [ ] Budget/cleanup reminders on slide
