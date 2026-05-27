# Quiz — Week 4: Workflow orchestration

**Questions:** 12 · **Time limit:** 30 minutes · **Open book**  
**Module reference:** [Module 4](../modules/week-04.md)

---

### Question 1 (Multiple choice)

**Orchestration** with Step Functions differs from **choreography** because:

- A) Choreography uses a central state machine only  
- B) Orchestration defines explicit order, retries, and a single execution history for the workflow  
- C) Choreography always requires Transfer Family  
- D) Orchestration eliminates audit requirements  

### Question 2 (Multiple choice)

For enterprise MFT with audits and multi-step SLAs, the course **default** workflow type is:

- A) Express Workflows only  
- B) Standard Workflows  
- C) SWF only  
- D) EventBridge Pipes only  

### Question 3 (Multiple choice)

In ASL, a **`Retry`** block is most appropriate for:

- A) Invalid file format detected by business rules  
- B) Transient errors such as Lambda service exceptions  
- C) Partner credential rotation  
- D) Successful completions  

### Question 4 (Multiple choice)

A **`Catch`** block in Step Functions is used to:

- A) Increase Lambda memory automatically  
- B) Route failures to recovery/notification states instead of failing silently  
- C) Disable CloudWatch logs  
- D) Encrypt S3 objects  

### Question 5 (Multiple choice)

**Express Workflows** are generally **not** the default for regulated MFT because:

- A) They cannot invoke Lambda  
- B) They have a max duration around 5 minutes and less verbose history for long-running audit needs  
- C) They cost more per year of execution  
- D) They require EC2  

### Question 6 (Multiple choice)

The **`correlation_id`** should originate at:

- A) CloudWatch randomly after failure only  
- B) Job submission / workflow input edge and propagate unchanged through states  
- C) S3 lifecycle rules only  
- D) Partner DNS  

### Question 7 (Multiple choice)

**Map state** in Step Functions is most useful when:

- A) A single file never needs processing  
- B) Processing a batch/manifest of many files with controlled concurrency  
- C) Replacing Cognito  
- D) Hosting SFTP  

### Question 8 (Multiple choice)

Alarm on **`ExecutionsFailed`** (Step Functions) in addition to Lambda **`Errors`** because:

- A) Lambda always fails when Step Functions succeeds  
- B) Lambda tasks may succeed while the workflow still ends in Failed  
- C) Step Functions does not support Lambda  
- D) Alarms are optional for MFT  

### Question 9 (Multiple choice)

**Idempotency at workflow start** can be implemented by:

- A) Ignoring duplicate `x-idempotency-key` values  
- B) Storing idempotency key in DynamoDB and returning existing execution ARN on duplicate submit  
- C) Deleting the S3 bucket  
- D) Using FTP instead of SFTP  

### Question 10 (Multiple choice)

A **Choice** state after validation should branch on:

- A) Random number only  
- B) Explicit `valid` flag or business result—not transient Lambda noise  
- C) S3 bucket region only  
- D) Cognito hosted UI theme  

### Question 11 (Short answer)

When should you use **Catch** versus **Retry**?

*Your answer:*

_____________________________________________

### Question 12 (Short answer)

Why is Step Functions execution history valuable for **audit** in MFT?

*Your answer:*

_____________________________________________
