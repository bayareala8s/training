# Slide Outline — Module 07: Security, Risk, Compliance, and Resilience

**Format:** 16:9  
**Target length:** 20 slides  
**Brand:** BayLearn — dark navy, white, restrained gold accents  
**Rule:** Minimal text on slides; detail lives in speaker notes

---

## Slide 1 — Module title

**On slide:**  
Enterprise Architecture Leadership Masterclass  
Module 07: Security, Risk, Compliance, and Resilience  
BayLearn | BayAreaLa8s

**Notes:** Welcome; outcome: evidence-backed security/resilience architecture for NorthStar (fictional).

---

## Slide 2 — Fiction notice

**On slide:** NorthStar Financial Services is a fictional instructional case study.

**Notes:** Repeat whenever new stakeholders join mid-cohort.

---

## Slide 3 — Business scenario

**On slide:** “Who can read Restricted settlement files?” — Audit question NorthStar could not answer quickly

**Notes:** Priya Raman (fictional CISO). Encryption on ≠ explainable access.

---

## Slide 4 — Learning objectives

**On slide:**  
1. Zero Trust boundaries  
2. STRIDE threat modeling  
3. RTO/RPO + recovery proof  
4. Control-evidence matrix

**Notes:** Map each to lab deliverable.

---

## Slide 5 — Zero Trust defined

**On slide:** Continuous verification · Least privilege · Assume breach

**Notes:** Not a vendor checklist; architecture posture.

---

## Slide 6 — Trust boundaries

**On slide:** Identity → Control → Data → Detect

**Notes:** Walk swim lanes; mark crossings.

---

## Slide 7 — Least privilege IAM

**On slide:** Prefix-scoped roles beat wildcards

**Notes:** Writer / reader / auditor split preview for lab.

---

## Slide 8 — STRIDE overview

**On slide:** S T R I D E with one settlement example each

**Notes:** Keep examples concrete; avoid abstract definitions only.

---

## Slide 9 — Threat model lightweight process

**On slide:** Scope → Boundaries → STRIDE → Prioritize → Controls → Evidence

**Notes:** Timebox discipline.

---

## Slide 10 — RTO vs RPO

**On slide:** Downtime tolerance vs data-loss tolerance

**Notes:** Business owns targets; architecture proposes patterns + cost.

---

## Slide 11 — Resilience patterns trade-off

**On slide:** Versioning · CRR · Active-active · Drills

**Notes:** Cost rises left to right for geographic resilience; drills are mandatory regardless.

---

## Slide 12 — Lab architecture

**On slide:** KMS + S3 versioning + IAM + CW/SNS + optional CRR

**Notes:** Cost warning: CRR off by default.

---

## Slide 13 — Cost and safety

**On slide:** No NAT / EC2 / EKS / OpenSearch · Budget alert · Cleanup script

**Notes:** Point to cleanup-lab07.sh.

---

## Slide 14 — Instructor demo agenda

**On slide:** tfvars · IAM contrast · SSE-KMS object · restore narrative · evidence row

**Notes:** Narrate decisions out loud.

---

## Slide 15 — Lab overview

**On slide:** Deliverables + 40-minute timebox + cleanup mandatory

**Notes:** Success = evidence, not perfect CRR.

---

## Slide 16 — Control-evidence matrix

**On slide:** Risk | Control | Implementation | Evidence | Owner

**Notes:** Show sanitized example only.

---

## Slide 17 — Common mistakes

**On slide:** Encryption ≠ access control · Untested DR · Wildcard IAM · Skip cleanup

**Notes:** Use humor lightly; stay professional.

---

## Slide 18 — Assignment

**On slide:** Executive brief · Matrix · ADR (CRR vs simulated DR)

**Notes:** Capstone contribution callout.

---

## Slide 19 — Key takeaways

**On slide:** Boundaries · Tested recovery · Evidence over slogans

**Notes:** Leadership behavior emphasis.

---

## Slide 20 — Next module

**On slide:** Module 08 — AI Strategy and Intelligent EA · Governed incident assistant

**Notes:** Tease HITL and Bedrock lab; office hours CTA.
