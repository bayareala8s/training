# Week 1 — Enterprise MFT on AWS

> **Full module content (lecture, diagrams, case studies, knowledge checks):**  
> **[Module 1 — Enterprise MFT on AWS](../modules/week-01.md)** · ~2.5–3 hr instruction + lab

## Learning objectives

- Compare legacy MFT, custom scripts, and AWS-managed transfer services.
- Describe hub-and-spoke, landing zone, and push/pull patterns.
- Deploy an AWS Transfer Family **SFTP** server with S3 storage backend.
- Upload a test file via SFTP and verify in S3.

## Topics

1. Enterprise file exchange: volume, SLAs, partners, audit  
2. AWS Transfer Family: servers, users, protocols  
3. S3 as system of record: prefixes, versioning, lifecycle  
4. Logical architecture: edge (SFTP) → landing → processing  
5. BayAreaLa8s framing: why self-serve + governance together  

## Readings

- AWS Transfer Family — What is Transfer Family?  
- S3 — Organizing objects with prefixes  
- Course: `COURSE.md` §3 Enterprise use cases  

## Lab

**Lab 1:** [../labs/lab-01-transfer-family-sftp.md](../labs/lab-01-transfer-family-sftp.md)

## Deliverable

- Architecture diagram (1 page): partner → SFTP → S3 → downstream  
- Screenshot: SFTP upload + S3 object listing  

## Discussion prompts

1. Where does your organization still use SFTP vs. API-first integration?  
2. What metadata must you capture per file for audit?  

## Quiz (week 1)

**12 questions** — [Quiz](../quizzes/week-01-quiz.md) · [Answer key](../quizzes/week-01-answers.md) (see `../assessment.md`).
