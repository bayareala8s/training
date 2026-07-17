# Lab 07 Architecture Diagram

```mermaid
flowchart LR
  Op[Operator] --> IAM[Least-privilege roles]
  IAM --> S3[Versioned S3 + SSE-KMS]
  KMS[KMS CMK] --> S3
  S3 --> CW[CloudWatch]
  CW --> SNS[SNS]
  IAM --> DDB[Evidence DynamoDB]
  S3 -.->|optional CRR| R[Replica bucket]
```

NorthStar Financial Services is fictional.
