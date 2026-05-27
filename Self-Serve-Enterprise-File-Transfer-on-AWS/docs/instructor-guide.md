# Instructor guide (summary)

## Week 0 — Cohort setup

- [ ] Confirm sandboxes and billing alarms  
- [ ] Share `docs/technologies.md` prerequisites  
- [ ] LMS course import from `lms/module-manifest.json`  
- [ ] Optional: read-only demo of BayServe / BayRelay architecture (if client licensed)  

## Primary teaching materials

- **Full lecture content:** `docs/modules/week-NN.md` (use as slide/script source)
- **Syllabus index:** `docs/syllabus/week-NN.md` (objectives, deliverables, quiz reminder)
- **Labs:** `docs/labs/lab-NN-*.md`
- **Quizzes:** `docs/quizzes/week-NN-quiz.md` (learners) · `week-NN-answers.md` (instructors)
- **Lab 9 (Fargate):** `docs/modules/week-09-ecs-fargate.md` · demo: `./scripts/demo_ecs_large_file.sh` (use `LAB_LARGE_FILE_MB=10` in class)

## Weekly rhythm

| Day | Activity |
|-----|----------|
| Mon | Release module + lab (async) |
| Wed | Live session: concepts + demo (2–3 hr) |
| Fri | Office hours / lab Q&A (1 hr) |
| Sun | Lab due (configurable) |

## Live session outline (template)

1. Recap quiz highlights (10 min)  
2. Architecture whiteboard (30 min)  
3. Instructor demo (40 min)  
4. Break  
5. Lab preview + common failures (30 min)  
6. Q&A (20 min)  

## Common lab failures

| Lab | Issue | Fix |
|-----|-------|-----|
| 1 | Transfer `Unable to AssumeRole` | Trust `transfer.amazonaws.com` + `aws:SourceAccount` |
| 1 | Home directory path wrong | Match `/${BUCKET}/...` format |
| 3 | Duplicate processing | Verify idempotency table writes |
| 5 | Connector timeout | Security group / egress / host key |
| 6 | 403 on API | Cognito authorizer audience/issuer mismatch |

## Capstone coaching (weeks 6–8)

- Week 6: force track selection  
- Week 7: dry-run demo (5 min) with peer feedback  
- Week 8: final presentations, rubric scoring within 7 days  

## Enterprise private cohort

- Replace fictional partners in Lab 5 with client anonymized matrix  
- Capstone Track C preferred for migration engagements  
- NDA capstone brief stored outside git  

## Materials version

Align to `COURSE.md` version **1.0.0**. Report content issues to curriculum owner at BayAreaLa8s.
