---
id: how-to-use-this-system
title: How to Use This System
sidebar_position: 2
slug: /start-here/how-to-use-this-system
---

# How to Use This System

## Study Modes

### Deep Reading

Work through chapters in order within each domain. Complete knowledge checks and hands-on exercises. Update your progress in `progress/completed-topics.yaml`.

### Interview Sprint

Follow the [12-Week Learning Path](./12-week-learning-path). Prioritize interview questions and system-design exercises. Practice answers aloud using [Real-World Scenarios](/docs/real-world-scenarios/overview) for production-grounded walkthroughs. If your recruiter confirms coding rounds, add [Coding Preparation](/docs/start-here/coding-preparation) in weeks 8–9.

### Reference Lookup

Use the [Glossary](/docs/reference/glossary) and cheat sheets in the repository `cheat-sheets/` directory for rapid review before interviews.

## Weekly Routine

| Day | Activity |
|-----|----------|
| Monday | Read theory and create notes |
| Tuesday | Work through algorithms and diagrams |
| Wednesday | Study production implementations |
| Thursday | Complete a hands-on lab |
| Friday | Answer interview questions aloud |
| Saturday | Complete one system-design exercise |
| Sunday | Review flashcards, update weak areas, record a mock explanation |

## Content Types

| Type | Location | Purpose |
|------|----------|---------|
| Chapters | `docs/` | Deep technical content |
| **Real-world scenarios** | [Real-World Scenarios](/docs/real-world-scenarios/overview) | Step-by-step interview walkthroughs (Stripe, Netflix, Uber, etc.) |
| **Coding preparation** | [Coding Preparation](/docs/coding-preparation/overview) | Principal-level coding expectations, problem bank, mocks |
| Case studies | `case-studies/` | Production system analysis |
| Labs | `labs/` | Hands-on implementation |
| Interview | `interview/` | Questions, guides, rubrics |
| Flashcards | `flashcards/` | Rapid recall |
| Cheat sheets | `cheat-sheets/` | Pre-interview review |

## Using Cursor

The `.cursor/rules/`, `.cursor/prompts/`, and `.cursor/agents/` directories contain authoring guidance. Use the chapter generation prompt when creating new content.

## Tracking Progress

- `progress/skills-matrix.yaml` — skill levels by domain
- `progress/interview-readiness.yaml` — weighted readiness scores
- `progress/weak-areas.yaml` — topics needing more study

Run `python3 scripts/generate_progress_report.py` for a summary.
