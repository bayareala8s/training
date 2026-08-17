# Quiz — Week 2: Security, encryption & governance

**Questions:** 12 · **Time limit:** 30 minutes · **Open book**  
**Module reference:** [Module 2](../modules/week-02.md)

---

### Question 1 (Multiple choice)

In the STRIDE-lite model used in this course, storing partner SFTP passwords in a Git repository primarily risks:

- A) Denial of service  
- B) Information disclosure and spoofing  
- C) Data replication lag  
- D) Increased S3 request cost  

### Question 2 (Multiple choice)

The best reason to choose **SSE-KMS (CMK)** over default SSE-S3 for a landing bucket in enterprise designs is:

- A) KMS is always free  
- B) Customer-managed keys, key policies, and stronger audit/separation-of-duties narrative  
- C) KMS removes need for IAM  
- D) SSE-S3 is not supported on S3  

### Question 3 (Multiple choice)

To list objects only under `partners/demo/`, an IAM policy should combine `s3:ListBucket` with:

- A) `s3:prefix` condition on the bucket ARN  
- B) Public read ACL  
- C) `Action: s3:*` on `Resource: *`  
- D) Disabling Block Public Access  

### Question 4 (Multiple choice)

Which setting should be **ON** for all four options on production landing buckets?

- A) S3 Transfer Acceleration only  
- B) S3 Block Public Access  
- C) Anonymous read via bucket policy  
- D) Static website hosting  

### Question 5 (Multiple choice)

**CloudTrail** data events for S3 are valuable because they:

- A) Replace the need for file validation  
- B) Provide API-level object audit (who called PutObject/GetObject)  
- C) Encrypt objects in transit  
- D) Automatically quarantine malware  

### Question 6 (Multiple choice)

A bucket policy denying `aws:SecureTransport=false` is intended to:

- A) Block SFTP uploads  
- B) Reject unencrypted HTTP access to the S3 API  
- C) Disable KMS  
- D) Prevent versioning  

### Question 7 (Multiple choice)

Partner SFTP credentials for **connectors** (Week 5) should be stored in:

- A) Lambda environment variables in plain text  
- B) README.md in the repo  
- C) AWS Secrets Manager (referenced by the connector)  
- D) S3 public prefix  

### Question 8 (Multiple choice)

**S3 access logging** (to a separate logging bucket) primarily provides:

- A) Replacement for CloudTrail management events  
- B) HTTP-level access records for requests made to the bucket  
- C) Automatic virus scanning  
- D) Step Functions execution history  

### Question 9 (Multiple choice)

Tightening the Transfer role trust policy with an incorrect `aws:SourceArn` condition often causes:

- A) Lower S3 storage cost  
- B) Unable to AssumeRole errors during SFTP data access  
- C) Automatic connector creation  
- D) Cognito token expiration  

### Question 10 (Multiple choice)

An **S3 gateway VPC endpoint** helps workloads in private subnets by:

- A) Exposing the bucket to the public internet  
- B) Allowing S3 access without traffic going through the public internet/NAT for that path  
- C) Replacing IAM  
- D) Enabling SFTP on port 22  

### Question 11 (Short answer)

List **two** independent evidence sources that help prove **who uploaded** a specific file.

*Your answer:*

_____________________________________________

### Question 12 (Short answer)

What is the purpose of the **`s3:prefix`** condition in IAM when isolating partners?

*Your answer:*

_____________________________________________
