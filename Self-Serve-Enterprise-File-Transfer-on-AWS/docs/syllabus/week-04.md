# Week 4 — Workflow orchestration

> **Full module content:** **[Module 4 — Workflow orchestration](../modules/week-04.md)**

## Learning objectives

- Model a multi-step transfer as a Step Functions state machine.
- Use retries, catch blocks, and choice states.
- Pass correlation IDs through the workflow.
- Integrate Lambda tasks for copy, checksum, notify.

## Topics

1. Orchestration vs. choreography  
2. Step Functions: Standard vs. Express (when to use which)  
3. State design: copy → verify → notify → complete  
4. DLQ and operational visibility  
5. Map state for batch files (overview)  

## Readings

- Step Functions error handling  
- Course capstone preview: `../capstone.md`  

## Lab

**Lab 4:** [../labs/lab-04-step-functions-workflow.md](../labs/lab-04-step-functions-workflow.md)

## Deliverable

- ASL definition (or console export) + successful execution ARN in run report  

## Discussion prompts

1. Where do you need human approval in enterprise transfers?  
2. How long should state history be retained for audits?  

## Quiz (week 4)

**12 questions** — [Quiz](../quizzes/week-04-quiz.md) · [Answer key](../quizzes/week-04-answers.md)
