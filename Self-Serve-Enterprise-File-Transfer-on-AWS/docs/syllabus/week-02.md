# Week 2 — Security, encryption & governance

> **Full module content:** **[Module 2 — Security, encryption & governance](../modules/week-02.md)**

## Learning objectives

- Apply least-privilege IAM for Transfer Family and S3.
- Enable KMS encryption and understand key policies.
- Place resources in VPC where required; use VPC endpoints for S3.
- Configure CloudTrail and bucket logging for audit evidence.

## Topics

1. Threat model: credential theft, path traversal, data exfiltration  
2. IAM roles for Transfer: session policies, scoped prefixes  
3. KMS: CMK vs. AWS managed; key rotation narrative  
4. Network: public SFTP vs. internal; security groups  
5. Compliance framing: HIPAA, PCI, SOC2 **controls** (not certification)  

## Readings

- Transfer Family IAM requirements  
- S3 encryption + blocking public access  
- Course: `docs/technologies.md`  

## Lab

**Lab 2:** [../labs/lab-02-security-hardening.md](../labs/lab-02-security-hardening.md)

## Deliverable

- **Security baseline checklist** (template in lab) — completed for your sandbox  

## Discussion prompts

1. Shared endpoint vs. endpoint per partner — tradeoffs?  
2. How would you prove **who uploaded what** six months later?  

## Quiz (week 2)

**12 questions** — [Quiz](../quizzes/week-02-quiz.md) · [Answer key](../quizzes/week-02-answers.md)
