# Assessment structure

## Grade breakdown

| Component | Weight | Notes |
|-----------|--------|-------|
| Weekly labs (1–7) | 40% | 10 pts each → normalized to 40% |
| Quizzes (weeks 1–6) | 15% | 6 quizzes, equal weight |
| Participation | 10% | Reviews, forum, attendance |
| Capstone | 35% | See [capstone.md](capstone.md) |

**Pass:** Overall ≥ **80%** and capstone ≥ **70%**.

---

## Weekly lab rubrics

Each lab: **10 points** (see individual lab guides). Late policy: instructor-defined (default: −10% per day, max 3 days).

| Week | Lab | Submission folder |
|------|-----|-------------------|
| 1 | Lab 1 | `submissions/week-01/` |
| 2 | Lab 2 | `submissions/week-02/` |
| 3 | Lab 3 | `submissions/week-03/` |
| 4 | Lab 4 | `submissions/week-04/` |
| 5 | Lab 5 | `submissions/week-05/` |
| 6 | Lab 6 | `submissions/week-06/` |
| 7 | Lab 7 | `submissions/week-07/` |
| 8 | Capstone | `submissions/capstone/` |

---

## Quizzes (weeks 1–6)

Format: **12 questions** per quiz (10 multiple choice + 2 short answer), **open book**, 30-minute time limit in LMS.

### Week 1 — Sample questions

1. Primary benefit of Transfer Family over EC2 SFTP?  
2. Which S3 scope is appropriate for a single partner home directory?  
3. What service stores SFTP user keys in “Service managed” mode?  

### Week 2 — Sample questions

1. Which principal assumes the Transfer access role?  
2. When is SSE-KMS required vs. SSE-S3 for a compliance narrative?  
3. Name two audit evidence sources for “who uploaded file X.”  

### Week 3 — Sample questions

1. Why are S3 events at-least-once?  
2. Name one idempotency key strategy.  
3. What prefix would you use for quarantine?  

### Week 4 — Sample questions

1. Difference between Standard and Express workflows for MFT?  
2. What does a `Catch` block do?  
3. Where is correlation_id most useful?  

### Week 5 — Sample questions

1. Connector vs. server use case?  
2. Where should partner passwords live?  
3. Why do partners care about egress IP?  

### Week 6 — Sample questions

1. What claim must Cognito JWT contain for authZ?  
2. Why not return IAM access keys in self-serve API?  
3. Minimum entities in connection catalog model?  

**Full quiz banks (72 questions with answers):** [`docs/quizzes/`](quizzes/)

| Week | Quiz (learner) | Answer key |
|------|----------------|------------|
| 1 | [week-01-quiz.md](quizzes/week-01-quiz.md) | [week-01-answers.md](quizzes/week-01-answers.md) |
| 2 | [week-02-quiz.md](quizzes/week-02-quiz.md) | [week-02-answers.md](quizzes/week-02-answers.md) |
| 3 | [week-03-quiz.md](quizzes/week-03-quiz.md) | [week-03-answers.md](quizzes/week-03-answers.md) |
| 4 | [week-04-quiz.md](quizzes/week-04-quiz.md) | [week-04-answers.md](quizzes/week-04-answers.md) |
| 5 | [week-05-quiz.md](quizzes/week-05-quiz.md) | [week-05-answers.md](quizzes/week-05-answers.md) |
| 6 | [week-06-quiz.md](quizzes/week-06-quiz.md) | [week-06-answers.md](quizzes/week-06-answers.md) |

**Combined instructor edition:** [full-bank-with-answers.md](quizzes/full-bank-with-answers.md)

---

## Participation (10%)

| Activity | Points (internal) |
|----------|-----------------|
| Week 3 architecture review (peer) | 3 |
| Week 5 partner matrix critique | 3 |
| Forum: 2 substantive posts | 2 |
| Live session attendance (≥ 6/8) | 2 |

---

## Capstone grading

See [capstone.md](capstone.md) rubric (100 pts scaled to 35% course weight).

---

## LMS gradebook mapping

| LMS column | Weight % |
|------------|----------|
| `Lab01`–`Lab07` | 5.71 each (40% total) |
| `Quiz01`–`Quiz06` | 2.5 each (15% total) |
| `Participation` | 10 |
| `Capstone` | 35 |

Import structure: [`../lms/module-manifest.json`](../lms/module-manifest.json).

---

## Appeals and remediation

- One capstone resubmit allowed within 14 days if score 60–69.  
- Lab resubmits: one per week, best score counts (instructor discretion).
