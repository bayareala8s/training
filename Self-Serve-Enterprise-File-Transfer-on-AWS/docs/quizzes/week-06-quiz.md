# Quiz — Week 6: Self-serve platform experience

**Questions:** 12 · **Time limit:** 30 minutes · **Open book**  
**Module reference:** [Module 6](../modules/week-06.md)

---

### Question 1 (Multiple choice)

The primary goal of a **self-serve** file transfer platform is:

- A) Give all users full AWS Console admin access  
- B) Expose guardrailed actions (catalog, jobs, status) without sharing raw cloud credentials  
- C) Eliminate audit logs  
- D) Replace S3 with EFS for all partners  

### Question 2 (Multiple choice)

For owner-scoped authorization in Lab 6, the JWT claim most commonly used is:

- A) `aud` only  
- B) `sub` (subject) matched to `owner_sub` on connections/jobs  
- C) `iss` only  
- D) `email_verified` alone without identity binding  

### Question 3 (Multiple choice)

`POST /v1/jobs` should typically return **HTTP 202 Accepted** because:

- A) Jobs are always synchronous &lt; 100 ms  
- B) Transfer processing is asynchronous; client polls job status  
- C) Cognito requires 202  
- D) S3 cannot receive uploads  

### Question 4 (Multiple choice)

Which must **never** appear in a self-serve API response to business users?

- A) `job_id` and `state`  
- B) IAM access keys or full Secrets Manager secret values  
- C) `connection_id` and `name`  
- D) `correlation_id`  

### Question 5 (Multiple choice)

A new connection created by a business user should often start in status:

- A) `ACTIVE` immediately with production prefixes  
- B) `PENDING_APPROVAL` until platform admin approves  
- C) `DELETED`  
- D) `PUBLIC`  

### Question 6 (Multiple choice)

API Gateway **JWT authorizer** validates:

- A) Only the request body size  
- B) Token signature, issuer, audience, and expiration from Cognito  
- C) S3 bucket policy only  
- D) SFTP host keys  

### Question 7 (Multiple choice)

Before starting a job, the API must verify that `source_key`:

- A) Matches any object in the account  
- B) Is allowed by the connection’s configured prefix / partner scope  
- C) Is always empty string  
- D) Is stored in CloudFront  

### Question 8 (Multiple choice)

**DynamoDB** in the self-serve model stores:

- A) Only CloudTrail logs  
- B) Connection catalog metadata and job state (not raw partner secrets in client responses)  
- C) SFTP binary payloads  
- D) ACM certificates  

### Question 9 (Multiple choice)

Header **`x-idempotency-key`** on job submission prevents:

- A) All SFTP traffic  
- B) Duplicate Step Functions executions when clients retry POST  
- C) KMS encryption  
- D) Cognito MFA  

### Question 10 (Multiple choice)

**GET /v1/jobs/{job_id}** must return **403** when:

- A) The job exists but `job.owner_sub` does not match caller’s JWT `sub`  
- B) The job succeeded  
- C) correlation_id is present  
- D) The connection is ACTIVE  

### Question 11 (Short answer)

Name **two** entities in the self-serve domain model and one key field on each.

*Your answer:*

_____________________________________________

### Question 12 (Short answer)

Why should the UI/API **not** expose bucket-wide S3 listing to business users?

*Your answer:*

_____________________________________________
