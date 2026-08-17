# Instructor Guide

**Cloud-Native Data Engineering on AWS**  
10 Weeks · 72 Hours · Professional Certificate Course

---

## Course Overview

This guide supports instructors delivering the course: scheduling, lab timing, discussion prompts, grading tips, and office hours topics. Align delivery with [SYLLABUS.md](./SYLLABUS.md) and [ASSESSMENT.md](./ASSESSMENT.md).

### Course Arc

```text
Weeks 1–3   Foundations → Ingestion → ETL
Weeks 4–6   Quality → Modeling → Orchestration
Weeks 7–9   Security → Operations → AI/ML Data
Week 10     Enterprise Capstone
```

### Weekly Rhythm (Recommended)

| Session | Duration | Activity |
|---------|----------|----------|
| Lecture | 2 hours | Concepts, architecture, AWS service mapping |
| Lab Block 1 | 1.5–2 hours | Guided hands-on (Labs .1–.2) |
| Lab Block 2 | 1.5–2 hours | Independent lab completion + assignment intro |
| Office Hours | 1 hour | Optional; see weekly topics below |

**Async option:** Release lecture Monday; labs due Sunday; live session Thursday for demos and Q&A.

---

## Teaching Schedule

### Week 1 – Modern Data Engineering Foundations

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | [week-01-lecture.md](../modules/module-01-foundations/lectures/week-01-lecture.md) |
| Lab 1.1 | 90m | S3 data lake Terraform |
| Lab 1.2 | 90m | Zone structure + sample data |
| Assignment 1 | 3h async | Architecture design document |

**Module outcomes:** Students deploy S3 lake with zones; understand medallion architecture.

---

### Week 2 – Data Ingestion Patterns

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | [week-02-lecture.md](../modules/module-02-ingestion/lectures/week-02-lecture.md) |
| Lab 2.1 | 90m | Lambda ingestion |
| Lab 2.2 | 90m | EventBridge automation |
| Lab 2.3 | 60m | S3 event processing |
| Assignment 2 | 3h async | Ingestion design |

---

### Week 3 – AWS Glue ETL Engineering

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | [week-03-lecture.md](../modules/module-03-glue-etl/lectures/week-03-lecture.md) |
| Lab 3.1 | 120m | Raw → Cleaned ETL |
| Lab 3.2 | 90m | Glue crawlers |
| Lab 3.3 | 90m | ETL optimization |
| Assignment 3 | 3h async | ETL pipeline design |

**Checkpoint:** By end of Week 3, students should have data in cleaned zone.

---

### Week 4 – Data Quality & Reliability

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | [week-04-lecture.md](../modules/module-04-data-quality/lectures/week-04-lecture.md) |
| Lab 4.1 | 120m | Quality framework |
| Lab 4.2 | 90m | Validation automation |
| Lab 4.3 | 60m | Quarantine zone |
| Assignment 4 | 4h async | Data quality SLAs |

---

### Week 5 – Data Modeling & Analytics

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | Module 5 lecture (when available) |
| Labs | 4–5h | Star schema, Athena optimization |
| Assignment 5 | 3h async | Modeling exercise |

**Mid-course note:** Week 5–6 is a good time for **Architecture Review** (10% assessment)—peer review of platform designs.

---

### Week 6 – Orchestration & Workflow Automation

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | Step Functions, dependency management |
| Labs | 4–5h | Multi-stage workflows, retry logic |
| Assignment 6 | 3h async | Orchestration design |

**Data Platform Project milestone (10%):** Due end of Week 6 or 7—integrated platform with ingestion, ETL, catalog, basic monitoring.

---

### Week 7 – Security, Governance & Compliance

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | IAM, encryption, PII, audit |
| Labs | 4–5h | Access controls, governance validation |
| Assignment 7 | 3h async | Security review |

---

### Week 8 – Monitoring, Cost Optimization & Operations

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | [week-08-lecture.md](../modules/module-08-monitoring-ops/lectures/week-08-lecture.md) |
| Lab 8.1 | 90m | CloudWatch dashboards |
| Lab 8.2 | 90m | SNS alerts + anomaly detection |
| Lab 8.3 | 75m | Cost Explorer + tags |
| Assignment 8 | 4h async | Operations runbook |

**Infrastructure:** [`infrastructure/modules/monitoring/main.tf`](../infrastructure/modules/monitoring/main.tf)

---

### Week 9 – Data Engineering for AI & ML

| Component | Time | Materials |
|-----------|------|-----------|
| Lecture | 2h | [week-09-lecture.md](../modules/module-09-ai-ml-data/lectures/week-09-lecture.md) |
| Lab 9.1 | 120m | ML dataset prep (`prepare_ml_dataset.py`) |
| Lab 9.2 | 120m | Feature store pipeline |
| Lab 9.3 | 90m | AI quality validation |
| Assignment 9 | 4h async | Recommendation pipeline design |

---

### Week 10 – Enterprise Capstone

| Component | Time | Materials |
|-----------|------|-----------|
| Kickoff lecture | 2h | [week-10-lecture.md](../modules/module-10-capstone/lectures/week-10-lecture.md) |
| Build time | 6–8h async | [capstone-checklist.md](../modules/module-10-capstone/assignments/capstone-checklist.md) |
| Presentations | 3–4h live | 15–20 min per student + Q&A |

**Capstone weight:** 30% of course grade. See [capstone/rubric.md](../capstone/rubric.md).

---

## Lab Timing Summary

| Module | Lab | Est. Time | Cumulative |
|--------|-----|-----------|------------|
| 1 | 1.1 S3 Terraform | 90m | 1.5h |
| 1 | 1.2 Zones | 90m | 3h |
| 2 | 2.1–2.3 Ingestion | 4h | 7h |
| 3 | 3.1–3.3 Glue ETL | 5h | 12h |
| 4 | 4.1–4.3 Quality | 4.5h | 16.5h |
| 8 | 8.1–8.3 Monitoring | 4.25h | ~20h |
| 9 | 9.1–9.3 AI/ML | 5.5h | ~25.5h |

**Tip:** Students who fall behind after Week 3 rarely catch up—intervene early.

---

## Discussion Prompts by Week

Use these in lecture breaks, forums, or breakout rooms. Each module lecture also includes discussion questions.

### Week 1
1. Why keep raw data if we always transform before analytics?
2. When would Redshift beat Athena for RetailCo?
3. How does medallion architecture support governance?

### Week 2
1. How do you make ingestion idempotent when sources resend files?
2. EventBridge vs direct Lambda triggers—trade-offs?
3. What belongs in the ingestion layer vs ETL layer?

### Week 3
1. Schema-on-read vs schema-on-write in Glue jobs?
2. When do crawlers cause problems at scale?
3. How do job bookmarks change failure recovery?

### Week 4
1. Error vs warning severity—who decides?
2. Should bad data ever reach curated with a flag?
3. How do SLAs change team behavior?

### Week 5
1. Star schema vs wide tables on the lake—when each?
2. Partition design mistakes you've seen?
3. How much denormalization is too much?

### Week 6
1. Step Functions vs Airflow for this course platform?
2. Where should retry logic live—orchestrator or job?
3. How do you test failure paths without breaking prod?

### Week 7
1. Who should access raw zone PII?
2. Encryption with SSE-S3 vs KMS CMK—when CMK?
3. How does shared responsibility apply to data lakes?

### Week 8
1. Should every Glue failure page on-call?
2. How do you justify data platform AWS spend to finance?
3. `TreatMissingData`—breaching vs notBreaching for batch jobs?

### Week 9
1. Point-in-time features—why harder on lakes?
2. When skip feature store and use Parquet?
3. What metadata must RAG chunks carry?

### Week 10
1. Minimum viable capstone that still scores well?
2. How explain architecture to a non-technical executive in 60 seconds?
3. What would you build with two more weeks?

---

## Grading Tips

### Weekly Labs (30%)

| Do | Don't |
|----|-------|
| Use rubric: correctness, documentation, best practices | Accept screenshots without verification steps |
| Spot-check one AWS resource via student output JSON | Penalize heavily for minor CLI typos |
| Accept equivalent implementations if documented | Require identical resource names across students |
| Give partial credit for blocked AWS accounts with local proof | Accept copied code without LAB-REPORT.md |

**Lab report minimum:** What was built, verification checklist, one screenshot or CLI output.

### Assignments (20%)

- Assignments 1, 4, 8, 9 are **document-heavy**—grade on completeness, realism, and alignment with lecture concepts
- Use assignment-specific rubrics in each `assignments/assignment-NN.md`
- Flag plagiarism: architecture diagrams should differ; identical SLA JSON is suspicious

### Architecture Reviews (10%)

- 10-minute student presentation + 5-minute peer feedback
- Score: clarity, justification, response to questions
- Provide structured feedback form: ingestion, storage, ETL, security, monitoring

### Data Platform Project (10%)

Minimum bar:
- S3 zones deployed
- One ingestion path
- One Glue job
- Catalog entry
- Basic CloudWatch metric or dashboard screenshot

### Capstone (30%)

Use [capstone/rubric.md](../capstone/rubric.md). Calibration session recommended:

1. Review one Excellent, one Good, one Needs Improvement sample together
2. Align on pass/fail gate items (repo, tags, presentation, no secrets)
3. Bonus points sparingly (+0 to +3)

**Presentation grading:** Content 60%, delivery 40%. A working demo significantly boosts Implementation and Monitoring scores.

---

## Office Hours Topics by Week

| Week | Expected Student Questions | Prep |
|------|---------------------------|------|
| 1 | AWS account setup, Terraform errors, bucket naming | [SETUP.md](../setup/SETUP.md) |
| 2 | IAM permissions, Lambda deployment packages | Sample IAM policy |
| 3 | Glue DPU costs, job failures, crawler confusion | Glue console walkthrough |
| 4 | Python env, validator extension | quality_runner.py FAQ |
| 5 | Athena partition errors, SQL tuning | Example EXPLAIN |
| 6 | Step Functions JSON, state limits | Minimal SFN template |
| 7 | KMS key policies, PII examples | Masking code snippet |
| 8 | SNS email confirmation, empty dashboards | monitoring/main.tf |
| 9 | pandas install, PSI interpretation | prepare_ml_dataset.py |
| 10 | Scope anxiety, demo failures, terraform destroy | capstone-checklist.md |

### Common Blockers (All Weeks)

| Issue | Resolution |
|-------|------------|
| `AccessDenied` | Student IAM policy; use course lab policy template |
| S3 bucket name taken | Change `project` in tfvars |
| Glue job OOM | Reduce data volume; increase workers |
| Unexpected AWS charges | Budget alert; enforce destroy after labs |
| SNS no email | Confirm subscription link |

---

## Session Plans (Sample 3-Hour Live Block)

### Standard Technical Week (e.g., Module 8)

| Time | Activity |
|------|----------|
| 0:00–0:15 | Recap previous module; learning objectives |
| 0:15–1:15 | Lecture with 2 discussion breaks |
| 1:15–1:25 | Break |
| 1:25–2:25 | Live demo: deploy dashboard from Lab 8.1 JSON |
| 2:25–2:55 | Students start Lab 8.1; instructor circulates |
| 2:55–3:00 | Assign Lab 8.2–8.3; mention Assignment 8 |

### Capstone Presentation Day

| Time | Activity |
|------|----------|
| Per student | 15–20 min present + 5 min Q&A |
| Between | 5 min buffer for setup |
| End | Course wrap-up; cleanup reminder; career resources |

**12 students × 25 min ≈ 5 hours**—split across two sessions if needed.

---

## Instructor Checklist (Start of Course)

- [ ] AWS org or student account guidance documented
- [ ] Budget alerts recommended ($50/dev)
- [ ] LMS loaded with module README links
- [ ] Grading rubrics shared with students
- [ ] Capstone scenarios reviewed; students choose by Week 9
- [ ] Backup AWS account for live demos

## Instructor Checklist (End of Course)

- [ ] All capstones graded with rubric worksheet
- [ ] Students reminded to `terraform destroy`
- [ ] Course feedback survey sent
- [ ] Portfolio / career session optional ([CAREER-OUTCOMES.md](./CAREER-OUTCOMES.md))

---

## Additional Resources

| Resource | Path |
|----------|------|
| Student handbook | [STUDENT-HANDBOOK.md](./STUDENT-HANDBOOK.md) |
| Assessment weights | [ASSESSMENT.md](./ASSESSMENT.md) |
| Capstone rubric | [capstone/rubric.md](../capstone/rubric.md) |
| Presentation guide | [capstone/presentation-guide.md](../capstone/presentation-guide.md) |
| Infrastructure modules | [infrastructure/README.md](../infrastructure/README.md) |

---

## Contact & Iteration

Document recurring student friction each cohort and update lab troubleshooting tables. Module 8–10 content includes operational and capstone materials designed for direct classroom use without supplementary slides.
