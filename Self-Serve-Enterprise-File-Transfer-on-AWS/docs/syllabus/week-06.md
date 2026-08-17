# Week 6 — Self-serve platform experience

> **Full module content:** **[Module 6 — Self-serve platform experience](../modules/week-06.md)**

## Learning objectives

- Design a **connection catalog** and **job** domain model.
- Expose REST APIs via API Gateway + Lambda.
- Authenticate users with Cognito (hosted UI or API flow).
- Enforce authorization: users see only their connections/jobs.

## Topics

1. Self-serve vs. ticket-driven operations  
2. DynamoDB single-table vs. multi-table design (simplified model)  
3. API design: `POST /connections`, `POST /jobs`, `GET /jobs/{id}`  
4. UI options: React SPA, minimal HTML, or API-only with Postman  
5. BayServe pattern: catalog visible before execution  

## Readings

- API Gateway + Cognito authorizer patterns  
- Course: `COURSE.md` §10 BayAreaLa8s positioning  

## Lab

**Lab 6:** [../labs/lab-06-self-serve-api.md](../labs/lab-06-self-serve-api.md)

## Deliverable

- Postman collection **or** minimal UI walkthrough video (2 min)  
- OpenAPI snippet (3 core endpoints)  

## Discussion prompts

1. What must **never** appear in a self-serve UI?  
2. How do business users request a **new partner** safely?  

## Quiz (week 6)

**12 questions** — [Quiz](../quizzes/week-06-quiz.md) · [Answer key](../quizzes/week-06-answers.md)
