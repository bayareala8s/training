# Capstone Evaluation Rubric

**Total: 100 points** (maps to 30% of course grade)

| Criterion | Points | Excellent (full) | Needs improvement |
|-----------|--------|------------------|-------------------|
| Architecture | 20 | Clear boundaries, event flows, AWS diagram aligned with implementation | Monolith disguised as microservices; missing diagrams |
| Implementation | 25 | 3+ services on ECS, working APIs, EventBridge integration | Local-only or single service |
| Security | 15 | JWT/IAM, secrets not in code, least-privilege roles | Hardcoded credentials; open endpoints |
| Observability | 15 | Dashboards, traces, actionable alarms | Logs only, no tracing |
| CI/CD | 15 | Automated test, build, deploy; rollback documented | Manual deploy only |
| Demo & documentation | 10 | Clear demo, cost analysis, runbook | Incomplete or unreadable docs |

## Pass Threshold

- **≥ 70** — Pass  
- **≥ 85** — Distinction  
- **< 70** — Revise and resubmit (cohort policy applies)
