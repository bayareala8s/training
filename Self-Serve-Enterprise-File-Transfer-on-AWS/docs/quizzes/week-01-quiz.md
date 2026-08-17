# Quiz — Week 1: Enterprise MFT on AWS

**Questions:** 12 · **Time limit:** 30 minutes · **Open book**  
**Module reference:** [Module 1](../modules/week-01.md)

---

### Question 1 (Multiple choice)

What is the primary operational advantage of AWS Transfer Family over self-managed SFTP on EC2?

- A) Unlimited free storage  
- B) AWS manages the protocol edge; you focus on IAM, S3, and automation  
- C) No need for IAM roles  
- D) Built-in ERP adapters  

### Question 2 (Multiple choice)

In a **push inbound** pattern, who typically initiates the connection to the SFTP server?

- A) Your Step Functions workflow  
- B) The partner (client)  
- C) Amazon S3  
- D) AWS Lambda on a schedule  

### Question 3 (Multiple choice)

For Transfer Family with **S3 storage**, the partner’s logical home directory is best described as:

- A) An EBS volume mount  
- B) A mapping to S3 key prefixes under a bucket  
- C) A DynamoDB partition key  
- D) An CloudFront origin path only  

### Question 4 (Multiple choice)

Which IAM principal must be trusted in the **access role** used by Transfer Family to reach S3?

- A) `s3.amazonaws.com`  
- B) `lambda.amazonaws.com`  
- C) `transfer.amazonaws.com`  
- D) `ec2.amazonaws.com`  

### Question 5 (Multiple choice)

Why is **S3 versioning** commonly enabled on landing buckets?

- A) To reduce storage cost  
- B) To support audit and recovery when objects are overwritten or deleted  
- C) To replace CloudTrail  
- D) To enable SFTP protocol conversion  

### Question 6 (Multiple choice)

A recommended multi-tenant prefix layout for partner isolation is:

- A) `s3://bucket/all-partners-shared/`  
- B) `s3://bucket/partners/{partner_id}/inbound/`  
- C) `s3://bucket/root/` with public ACL  
- D) Random UUID buckets per file without IAM conditions  

### Question 7 (Multiple choice)

Transfer Family **connectors** (covered in depth in Week 5) are primarily used for:

- A) Accepting partner uploads to your endpoint  
- B) Initiating transfers to or from **remote** SFTP/FTPS endpoints  
- C) Replacing Amazon S3 entirely  
- D) Hosting static websites  

### Question 8 (Multiple choice)

A common cause of **“Unable to AssumeRole”** when testing SFTP upload is:

- A) S3 versioning disabled  
- B) Incorrect or overly restrictive trust policy on the Transfer access role  
- C) Using SSE-KMS  
- D) Enabling Block Public Access  

### Question 9 (Multiple choice)

In the course reference architecture, the **protocol edge** is separated from **processing** primarily to:

- A) Increase partner license fees  
- B) Keep validation/automation off the Transfer endpoint and preserve clear security boundaries  
- C) Avoid using S3  
- D) Eliminate the need for audit logs  

### Question 10 (Multiple choice)

Which protocol is the **default focus** of Lab 1 in this course?

- A) AS2 only  
- B) FTPS only  
- C) SFTP  
- D) FTP without encryption  

### Question 11 (Short answer)

Name **two** metadata or audit questions a landing zone design should eventually answer (e.g., who sent a file).

*Your answer:*

_____________________________________________

### Question 12 (Short answer)

In one sentence, explain the difference between a **Transfer server** and a **connector**.

*Your answer:*

_____________________________________________
