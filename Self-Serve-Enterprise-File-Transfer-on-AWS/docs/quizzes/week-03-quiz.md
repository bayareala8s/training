# Quiz — Week 3: Event-driven automation

**Questions:** 12 · **Time limit:** 30 minutes · **Open book**  
**Module reference:** [Module 3](../modules/week-03.md)

---

### Question 1 (Multiple choice)

Amazon S3 event notifications are best described as:

- A) Exactly-once guaranteed  
- B) At-least-once (duplicates possible)  
- C) Never delivered to Lambda  
- D) Only available for DELETE events  

### Question 2 (Multiple choice)

The primary purpose of a **DynamoDB idempotency table** in the Lab 3 pattern is to:

- A) Store SFTP passwords  
- B) Prevent duplicate processing of the same event or business key  
- C) Replace S3 versioning  
- D) Host the Transfer Family server  

### Question 3 (Multiple choice)

Failed validation (wrong extension, zero-byte file) should most often route files to:

- A) `archive/` immediately without logging  
- B) `quarantine/` with reason captured in logs or sidecar metadata  
- C) Delete permanently with no audit  
- D) Public S3 website  

### Question 4 (Multiple choice)

Keeping **validation Lambda** functions fast (&lt; 1–2 minutes) is recommended because:

- A) Lambda cannot run more than 1 second  
- B) Long work belongs in Step Functions or batch jobs; edge validation should stay lightweight  
- C) S3 events require sub-second handlers only  
- D) Transfer Family charges per Lambda line of code  

### Question 5 (Multiple choice)

A strong **business idempotency key** for duplicate uploads of the same filename is:

- A) Random UUID per Lambda cold start only  
- B) `partner_id + object key + ETag` (or content hash)  
- C) AWS account ID alone  
- D) CloudWatch log group name  

### Question 6 (Multiple choice)

**S3 → EventBridge → Lambda** compared to **S3 → Lambda** direct notification is often preferred in production for:

- A) Eliminating all IAM  
- B) Fan-out, cross-account routing, and decoupled rules  
- C) Disabling encryption  
- D) Removing the need for idempotency  

### Question 7 (Multiple choice)

When a Lambda processing an S3 event lacks **`kms:Decrypt`** on a CMK-encrypted object, a typical symptom is:

- A) SFTP authentication failure  
- B) AccessDenied reading the object  
- C) Step Functions Express timeout only  
- D) Cognito JWT invalid signature  

### Question 8 (Multiple choice)

**Structured JSON logs** should always include for operations triage:

- A) Partner passwords  
- B) `correlation_id` and safe context (key, partner_id, status)  
- C) Full file binary content  
- D) IAM root user access keys  

### Question 9 (Multiple choice)

Re-uploading the same payroll file twice without idempotency most likely causes:

- A) Lower storage costs  
- B) Duplicate downstream processing (e.g., double payment risk)  
- C) Automatic quarantine only  
- D) Transfer server deletion  

### Question 10 (Multiple choice)

Filtering S3 notifications by **prefix** (e.g., `partners/demo/inbound/`) is important to:

- A) Increase duplicate events  
- B) Avoid invoking processors on archive/quarantine/unrelated paths  
- C) Disable versioning  
- D) Remove need for IAM  

### Question 11 (Short answer)

Why must consumers treat S3 event delivery as **at-least-once**?

*Your answer:*

_____________________________________________

### Question 12 (Short answer)

Name **two** validation rules used in Lab 3 (technical validation).

*Your answer:*

_____________________________________________
