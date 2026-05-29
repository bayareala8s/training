# Complete Course Index

## Architecture diagrams (17)

| Resource | Location |
|----------|----------|
| **Diagram index** | [diagrams/README.md](diagrams/README.md) |
| Weekly schedule | [diagrams/WEEKLY-DIAGRAM-SCHEDULE.md](diagrams/WEEKLY-DIAGRAM-SCHEDULE.md) |
| Export PNG/SVG | [diagrams/EXPORT-GUIDE.md](diagrams/EXPORT-GUIDE.md) |

## For Instructors

| Resource | Location |
|----------|----------|
| Start here | [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) |
| Setup | [TEACHING_GUIDE.md](TEACHING_GUIDE.md) |
| 10-week schedule | [schedule/10-week-schedule.md](schedule/10-week-schedule.md) |
| Lecture notes (detailed, 90 min each) | [../lectures/README.md](../lectures/README.md) |
| Lab facilitation | [../instructor/](../instructor/) |
| Assignments & rubrics | [../assignments/](../assignments/) |
| Quizzes | [../assessments/quizzes/](../assessments/quizzes/) |
| Capstone rubric | [../capstone/rubrics.md](../capstone/rubrics.md) |

## For Students

| Resource | Location |
|----------|----------|
| Handbook | [STUDENT_HANDBOOK.md](STUDENT_HANDBOOK.md) |
| Labs (week 1–9) | [../labs/](../labs/) |
| Starter code | [../starters/python/](../starters/python/) |
| API contracts | [../contracts/openapi/](../contracts/openapi/) |
| Capstone | [../capstone/README.md](../capstone/README.md) |

## Runnable Platform

```bash
docker compose up --build
./scripts/demo-platform.sh
```

| Service | Port | Health |
|---------|------|--------|
| User | 8001 | /health |
| Product | 8002 | /health |
| Order | 8003 | /health |
| Notification | 8004 | /health |

## AWS (Modules 4–9)

```bash
cd infrastructure/terraform && terraform apply
```

## File Count Overview

- **10** lecture modules
- **10** instructor note files
- **9** hands-on labs + capstone
- **9** assignments
- **4** Python microservices (reference implementation)
- **Terraform** VPC, ECS, ECR, EventBridge, DynamoDB
