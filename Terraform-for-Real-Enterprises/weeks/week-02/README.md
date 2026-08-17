# Week 2 – AWS Multi-Account Architecture

> **Full module:** [course-modules/week-02](../../course-modules/week-02/) — detailed lecture, assignment, quiz, instructor notes

## Learning Objectives

- Design dev/test/prod (or similar) account separation with Organizations
- Use cross-account IAM roles for Terraform execution
- Relate landing zone patterns to your Terraform layout

## Topics

- AWS Organizations
- Shared services model
- Environment isolation
- Cross-account IAM roles
- Landing zone concepts

## Labs

| Lab | Description |
|-----|-------------|
| **2.1** | Document target OU/account model (diagram required) |
| **2.2** | Provision or simulate multi-account roles (trust policies, external IDs) |
| **2.3** | Run Terraform from a tooling account into a workload account |

## Deliverables

1. **Multi-account architecture design** — Diagram + account/OU table
2. **Cross-account Terraform workflows** — Provider aliases or role assumption documented

## Suggested Time

8–9 hours

## Submission

PR: `week-02: multi-account design and cross-account apply` including architecture diagram (PNG or Mermaid in repo).
