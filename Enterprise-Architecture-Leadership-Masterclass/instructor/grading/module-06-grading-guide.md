# Grading Guide — Module 06

**Applies to:** Lab 06 + Module 06 assignment  
**Rubric:** Standard architecture rubric + `assessments/rubrics/module-06-rubric.md`  
**Answer key:** `assessments/answer-keys/module-06-answer-key.md`  
**Reference:** `instructor/reference-solutions/module-06/reference-solution.md`

---

## Score bands

| Band | Lab | Assignment package |
| ---- | --- | ------------------ |
| Excellent (4) | Four paths evidenced (or one blocked with solid architecture narrative); SNS confirmed; cleanup logged; matrix scored with criteria | Ownership clear; two ADRs with alternatives/consequences; Transfer cost trade-off explicit; data-flow separates SoR from files |
| Proficient (3) | Most paths work; minor missing evidence; cleanup present | Matrix complete; ADRs present but thinner trade-offs |
| Developing (2) | Patterns asserted without evidence; Transfer Family over-scoped; no DLQ discussion | Matrix without scores; ownership vague; shared-DB proposed |
| Beginning (1) | No cleanup; unsafe cost choices; copy-paste diagrams with no NorthStar fit | No ADRs; ESB-for-everything without criteria |

## What to reward

- Multi-criteria scoring (not fashion)
- Domain vs platform ownership language
- Failure-mode thinking (DLQ, duplicates, late files)
- Cost-aware Transfer Family decision
- Explicit “lab ≠ prod” security notes

## What to penalize

- Shared database as integration strategy
- Deploying Transfer Family / NAT / EKS in lab
- Missing cleanup
- Platform owning business event semantics without challenge
- ADRs that only restate the chosen option

## Quiz

Formative by default. Use answer key. Scenario items graded on trade-off quality and NorthStar realism.

## Capstone feed

Flag strong matrices/ADRs for reuse in Module 10 integration section.
