# Quiz — Week 5: Connectors & partner routing

**Questions:** 12 · **Time limit:** 30 minutes · **Open book**  
**Module reference:** [Module 5](../modules/week-05.md)

---

### Question 1 (Multiple choice)

You must **push** a file from S3 to a **partner’s remote SFTP server**. The correct AWS construct is:

- A) Transfer Family **server** only  
- B) Transfer Family **connector**  
- C) S3 static website  
- D) Cognito User Pool  

### Question 2 (Multiple choice)

Partners require your outbound connections to come from a **fixed IP** for firewall rules. You should document:

- A) Lambda cold start ID only  
- B) NAT gateway or Elastic IP egress used by the connector/VPC path  
- C) S3 bucket ARN  
- D) DynamoDB table name  

### Question 3 (Multiple choice)

Remote SFTP passwords for connectors should be stored in:

- A) GitHub repository  
- B) AWS Secrets Manager  
- C) S3 public prefix `credentials/`  
- D) Step Functions ASL Comments field  

### Question 4 (Multiple choice)

**Trusted host keys** on a connector protect against:

- A) S3 versioning conflicts  
- B) Man-in-the-middle attacks against the remote SFTP host  
- C) Lambda timeout  
- D) KMS rotation only  

### Question 5 (Multiple choice)

The **partner matrix** deliverable is primarily:

- A) A Terraform state file  
- B) Operational documentation of direction, schedule, credentials store, and prefixes per partner  
- C) A Cognito JWT  
- D) CloudFront distribution config  

### Question 6 (Multiple choice)

Pattern **`S3_TO_SFTP`** means:

- A) Partner uploads to your SFTP server  
- B) Staged S3 object is delivered to remote SFTP via connector (or equivalent path)  
- C) Only cross-region replication  
- D) Deleting all inbound prefixes  

### Question 7 (Multiple choice)

**Multi-hop** routing (land → transform → deliver) requires special attention to:

- A) Disabling all logging  
- B) Idempotency and correlation_id at each hop  
- C) Using one shared IAM role with `s3:*` for all partners  
- D) Avoiding Secrets Manager  

### Question 8 (Multiple choice)

Compared to a **Transfer server**, a **connector**:

- A) Only accepts inbound partner uploads  
- B) Initiates sessions to remote endpoints you configure  
- C) Replaces IAM entirely  
- D) Cannot use S3  

### Question 9 (Multiple choice)

During **partner onboarding**, network teams most often need:

- A) Your egress IP allow-list data and host key fingerprints  
- B) Root AWS account password  
- C) All S3 object ACLs set to public-read  
- D) Step Functions Map state JSON  

### Question 10 (Multiple choice)

**SFTP_TO_SFTP** in a four-pattern model typically requires:

- A) Direct connector magic with no staging  
- B) Staging through S3 (or similar) with two controlled steps  
- C) Only CloudWatch dashboards  
- D) Disabling encryption  

### Question 11 (Short answer)

When would you choose a **managed server** instead of a **connector** for a partner relationship?

*Your answer:*

_____________________________________________

### Question 12 (Short answer)

List **three** columns you would include in a production partner matrix (any valid columns from the course template).

*Your answer:*

_____________________________________________
