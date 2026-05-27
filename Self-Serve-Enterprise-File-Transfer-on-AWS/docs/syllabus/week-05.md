# Week 5 — Connectors & partner routing

> **Full module content:** **[Module 5 — Connectors & partner routing](../modules/week-05.md)**

## Learning objectives

- Configure Transfer Family **SFTP connectors** for remote endpoints.
- Execute S3 → SFTP and SFTP → S3 flows.
- Document a partner matrix: protocol, direction, schedule, credentials.
- Understand connector networking (VPC, allow lists).

## Topics

1. Managed server vs. connector — decision matrix  
2. Connector IAM and Secrets Manager integration  
3. Multi-hop patterns: land → transform → deliver  
4. Partner onboarding runbook (template)  
5. **Lab 9:** ECS Fargate for large files — [Module 9](../modules/week-09-ecs-fargate.md) · [Lab 9](../labs/lab-09-ecs-fargate-large-files.md)  

## Readings

- Transfer Family connectors user guide  
- Course: BayRelay-style patterns (4 transfer types) — optional reading in README  

## Lab

**Lab 5:** [../labs/lab-05-sftp-connector.md](../labs/lab-05-sftp-connector.md)

## Deliverable

- **Partner matrix** spreadsheet (min. 3 fictional partners)  
- Demo log: one successful connector transfer  

## Discussion prompts

1. How do you rotate partner credentials without downtime?  
2. Egress IP stability for partner allow lists — options on AWS?  

## Quiz (week 5)

**12 questions** — [Quiz](../quizzes/week-05-quiz.md) · [Answer key](../quizzes/week-05-answers.md)
