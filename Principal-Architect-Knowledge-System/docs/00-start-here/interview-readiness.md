---
id: interview-readiness
title: Interview Readiness
sidebar_position: 6
slug: /start-here/interview-readiness
---

# Interview Readiness

Interview readiness is tracked across weighted domains. Scores update as you complete chapters, labs, and mock interviews.

## Weighted Domains

| Domain | Weight |
|--------|--------|
| Distributed Systems Fundamentals | 15% |
| Consensus, Replication, Consistency | 15% |
| Databases and Storage | 10% |
| Networking and Operating Systems | 10% |
| System Design | 14% |
| Cloud and Platform Architecture | 10% |
| Reliability and Security | 10% |
| AI and Agentic Systems | 5% |
| Architecture Leadership | 5% |
| Communication and Behavioral | 5% |
| Coding Interview (if applicable) | 5% |

## Scoring Dimensions

Each domain tracks:

- **Knowledge score** — factual and conceptual understanding
- **Explanation score** — ability to teach from first principles
- **Design score** — system-design performance
- **Failure-analysis score** — identifying hidden failure modes
- **Interview-performance score** — timed mock interview results
- **Confidence** — self-assessed readiness
- **Evidence** — links to completed exercises and mock interviews

## Current Status

Readiness data lives in `progress/interview-readiness.yaml`. Run:

```bash
python3 scripts/generate_progress_report.py
```

## Readiness Checklist

Before scheduling interviews, confirm:

- [ ] Can explain partial failure and why it changes system design
- [ ] Can compare consistency models with explicit tradeoffs
- [ ] Can whiteboard Raft or Paxos safety argument
- [ ] Can complete a system design in 60 minutes with depth on failure handling
- [ ] Have confirmed with recruiter whether **coding rounds** apply — if yes, completed [Coding Preparation](/docs/coding-preparation/overview)
- [ ] Can implement rate limiter or idempotent handler pseudo-code in 25 minutes (if coding confirmed)
- [ ] Have 5+ behavioral stories with metrics and lessons learned
- [ ] Have reviewed target company preparation modules
- [ ] Have completed at least 2 full mock interviews with feedback

## Mock Interview Resources

- Prompt: `.cursor/prompts/mock-interview.md`
- Scoring rubrics: `interview/scoring-rubrics/`
- Mock interview module: [Mock Interviews](/docs/mock-interviews/overview)
- Coding module: [Coding Preparation](/docs/coding-preparation/overview)
