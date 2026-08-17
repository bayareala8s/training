# Slide Outline — Module 06: Integration, Application, and Data Architecture

**Format:** 16:9  
**Target length:** 20 slides  
**Brand:** BayLearn — dark navy, white, restrained gold accents  
**Rule:** Minimal text on slides; detail lives in speaker notes

---

## Slide 1 — Module title

**On slide:**  
Enterprise Architecture Leadership Masterclass  
Module 06: Integration, Application, and Data Architecture  
BayLearn | BayAreaLa8s

**Notes:** Welcome; fiction notice for NorthStar; session outcome: pattern matrix + reference architecture + ADRs + lab evidence.

---

## Slide 2 — You are the Lead EA

**On slide:** NorthStar Financial Services (fictional) · Lead Enterprise Architect  
**Notes:** Artifacts feed capstone integration architecture; Module 05 platform baseline assumed.

---

## Slide 3 — Business scenario

**On slide:** Partner SFTP sprawl · Payment events needed · Sync account lookups · “ESB for everything” email  
**Notes:** Resist theology; demand criteria and failure modes.

---

## Slide 4 — Learning objectives

**On slide:**  
1. Pattern matrix with criteria  
2. Domain vs platform ownership  
3. Data product / master data ownership  
4. Deploy serverless reference paths  

**Notes:** Map each to lab/assignment deliverable.

---

## Slide 5 — Interaction styles collide

**On slide:** Sync · Events · Files · Batch — different SLAs, same enterprise  
**Notes:** One hub rarely optimizes all four.

---

## Slide 6 — Pattern families

**On slide:** Sync API · Async events · Queues · Streaming · File/SFTP · Batch ETL · Shared DB (discourage)  
**Notes:** Brief definitions; shared DB as anti-pattern.

---

## Slide 7 — Selection is multi-criteria

**On slide:** Latency · Coupling · Volume · Reliability · Security · Cost · Ops complexity  
**Notes:** Show template 16; score aloud one interface.

---

## Slide 8 — NorthStar interface table

**On slide:** Account → Sync · Payments → Events+queue · Partners → Files · Regulatory → Workflow  
**Notes:** Primary/secondary; invite challenge.

---

## Slide 9 — Failure modes

**On slide:** Timeout · Duplicate · Poison · Late/missing file  
**Notes:** Ask which pattern absorbs each; introduce DLQ.

---

## Slide 10 — Domains vs platform

**On slide:** Domains own meaning · Platform owns mechanisms  
**Notes:** Event names are business language; bus is plumbing.

---

## Slide 11 — Application boundaries

**On slide:** Accounts · Payments · Partners · Shared integration platform  
**Notes:** Avoid org-chart-as-architecture; capability link to Module 02.

---

## Slide 12 — Shared database trap

**On slide:** “Just for now” → permanent coupling  
**Notes:** Ban as integration strategy in student designs.

---

## Slide 13 — Data products and masters

**On slide:** Product · Owner · Contract · SLA · Not “a dump in the lake”  
**Notes:** Partner files ≠ customer golden record.

---

## Slide 14 — Events as contracts

**On slide:** Schema · Versioning · Consumers · Replay  
**Notes:** Year-one pragmatism vs registry stretch.

---

## Slide 15 — Instructor demo agenda

**On slide:** 1) Account API 2) Payment event 3) S3 partner landing 4) Step Functions + SNS  
**Notes:** Show Terraform lab06; tags; intentional authZ debt.

---

## Slide 16 — Cost warning

**On slide:** Transfer Family = conceptual · S3 landing in lab · Cleanup same day  
**Notes:** Point to cleanup script and cost estimate doc.

---

## Slide 17 — Lab launch

**On slide:** 40 minutes · Four paths · Matrix + 2 ADRs · Confirm SNS  
**Notes:** Mid-lab check; artifacts by minute 35.

---

## Slide 18 — Architecture review prompts

**On slide:** Alignment · Risk · Alternatives · Feasibility · Ownership  
**Notes:** ARB-style; pick one matrix + one ADR.

---

## Slide 19 — Assignment

**On slide:** Matrix · Data-flow · ADR-M06-01/02 · Evidence + cleanup  
**Notes:** Rubric emphasis; capstone feed.

---

## Slide 20 — Close / next module

**On slide:** Destroy today · Quiz · Module 07 Security & Resilience  
**Notes:** Thank cohort; DLQ/blast-radius teaser.
