# Instructor Guide — Production-Grade Microservices on AWS

## Before You Teach

1. Clone this repository and read [TEACHING_GUIDE.md](TEACHING_GUIDE.md).
2. Run `docker compose up --build` locally to verify all services.
3. Create a dedicated AWS account or OU for the cohort (budget alerts recommended).
4. Decide student track: **Python (recommended for labs)**, Java, or Node.js.
5. Publish the cohort schedule using `docs/schedule/10-week-schedule.md`.

## Weekly Flow (Recommended)

| Segment | Duration | Activity |
|---------|----------|----------|
| Lecture | 90 min | `lectures/module-XX-*.md` |
| Break | 15 min | |
| Lab | 120 min | `labs/module-XX/README.md` |
| Review | 45 min | Architecture review / Q&A |

**Homework:** `assignments/module-XX.md` due before next session.

## Architecture diagrams

**17 professional Mermaid diagrams:** [diagrams/README.md](diagrams/README.md)  
**Weekly schedule:** [diagrams/WEEKLY-DIAGRAM-SCHEDULE.md](diagrams/WEEKLY-DIAGRAM-SCHEDULE.md)  
**Export to PNG:** [diagrams/EXPORT-GUIDE.md](diagrams/EXPORT-GUIDE.md)

## Materials Map

| Week | Instructor | Student Lab | Lecture |
|------|------------|-------------|---------|
| 1 | `instructor/module-01.md` | `labs/module-01/` | `lectures/module-01-foundations.md` |
| 2 | `instructor/module-02.md` | `labs/module-02/` | `lectures/module-02-api-design.md` |
| 3 | `instructor/module-03.md` | `labs/module-03/` | `lectures/module-03-docker.md` |
| 4 | `instructor/module-04.md` | `labs/module-04/` | `lectures/module-04-ecs.md` |
| 5 | `instructor/module-05.md` | `labs/module-05/` | `lectures/module-05-events.md` |
| 6 | `instructor/module-06.md` | `labs/module-06/` | `lectures/module-06-data.md` |
| 7 | `instructor/module-07.md` | `labs/module-07/` | `lectures/module-07-security.md` |
| 8 | `instructor/module-08.md` | `labs/module-08/` | `lectures/module-08-observability.md` |
| 9 | `instructor/module-09.md` | `labs/module-09/` | `lectures/module-09-cicd.md` |
| 10 | `instructor/module-10.md` | `capstone/` | `lectures/module-10-capstone.md` |

## Grading

Use rubrics in `docs/assessment.md` and `capstone/rubrics.md`. Instructor solution branches or `instructor/solutions/` (distribute separately if needed).

## Common Student Issues

- **Docker port conflicts:** Change ports in `.env`.
- **AWS credentials:** Use IAM Identity Center or scoped lab roles; never share root keys.
- **ECS deploy fails:** Usually missing ECR image or wrong subnet/security group — see Module 4 troubleshooting in instructor notes.

## Academy Positioning

This is the flagship microservices course in the BayAreaLa8s Cloud/DevOps/AI academy. Cross-sell Terraform and Data Engineering courses after Week 4.
