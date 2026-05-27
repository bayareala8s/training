# Week 3 — Event-driven automation

> **Full module content:** **[Module 3 — Event-driven automation](../modules/week-03.md)**

## Learning objectives

- Trigger Lambda on S3 `ObjectCreated` events.
- Validate file metadata (size, extension, manifest).
- Implement idempotency for duplicate notifications.
- Route files to processing prefixes or quarantine.

## Topics

1. Event-driven vs. scheduled batch  
2. S3 event notifications + EventBridge  
3. Lambda design: idempotency table, partial failures  
4. Virus scan / validation hooks (conceptual + stub)  
5. Error handling: quarantine prefix, SNS alert  

## Readings

- S3 Event Notifications  
- Lambda best practices — idempotency  
- Course: `COURSE.md` §3 (processing pipelines)  

## Lab

**Lab 3:** [../labs/lab-03-s3-event-processor.md](../labs/lab-03-s3-event-processor.md)

## Deliverable

- Lambda source + sample CloudWatch log showing validate/route  
- Brief README: failure modes and retries  

## Discussion prompts

1. At-least-once S3 events — what breaks without idempotency?  
2. When should validation be sync vs. async?  

## Quiz (week 3)

**12 questions** — [Quiz](../quizzes/week-03-quiz.md) · [Answer key](../quizzes/week-03-answers.md)
