# BayPay ECS / Fargate + RDS PostgreSQL

**Type:** deploy (design)  
**Region:** `us-west-2`  
**Image:** `baypay/payment-service:<immutable-tag>` (same JAR as EKS)  
**Student apply:** ECS/Fargate + ALB optional; **do not apply RDS / NAT / EKS**

Teaching edge: `pay-alb-student.baypay.example` (real apply uses the AWS ALB DNS).

```mermaid
flowchart TB
  Merch["Harbor Market / Avery Chen\nPOST /api/v1/payments + Idempotency-Key"]
  ALB["ALB :80\npublic subnets + IGW"]
  TG["Target group :8080\nGET /actuator/health/liveness matcher 200"]
  Task["Fargate task 256 / 512\nassign_public_ip = true"]
  JAR["payment-service JAR\nprofile prod · Hikari"]
  SM["Secrets Manager\nbaypay/payment/db"]
  RDS[("RDS PostgreSQL\nbaypay :5432\nprivate subnets")]
  ECR["ECR\nbaypay/payment-service:tag"]

  Merch --> ALB --> TG --> Task --> JAR
  ECR --> Task
  SM -->|"valueFrom BAYPAY_DB_*"| JAR
  JAR -->|"jdbc 5432"| RDS
```

Alt text: Merchants hit an ALB in us-west-2. The target group health-checks Actuator liveness on 8080. A Fargate task runs the Spring Boot fat JAR from ECR. Secrets Manager injects the JDBC URL. The JAR talks to RDS PostgreSQL on 5432 in private subnets.
