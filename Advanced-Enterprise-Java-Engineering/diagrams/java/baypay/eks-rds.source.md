# BayPay EKS + RDS PostgreSQL

**Type:** deploy (design)  
**Region:** `us-west-2`  
**Image:** `baypay/payment-service:<immutable-tag>` (**same OCI image as ECS**)  
**Student apply:** **do not apply EKS**, NAT, or RDS Multi-AZ

Teaching edge: `https://payments.apps.baypay.example` (Ingress). OpenShift Route `payment-route` is the same job.

```mermaid
flowchart TB
  Merch["Harbor Market / Avery Chen\nPOST /api/v1/payments + Idempotency-Key"]
  Ing["Ingress\npayments.apps.baypay.example"]
  Svc["Service ClusterIP :8080\nselector app=payment-service"]
  Pod["Pod in baypay-prod\nDeployment payment-service ×3"]
  JAR["payment-service JAR\nsame image as ECS · profile prod"]
  Sec["Secret baypay-db\nBAYPAY_DB_*"]
  RDS[("RDS PostgreSQL\nbaypay :5432\nprivate subnets")]
  ECR["ECR\nbaypay/payment-service:tag"]

  Merch --> Ing --> Svc --> Pod --> JAR
  ECR --> Pod
  Sec -->|"envFrom"| JAR
  JAR -->|"jdbc 5432"| RDS
```

Alt text: Merchants hit Ingress on payments.apps.baypay.example. A ClusterIP Service on 8080 selects payment-service pods. Those pods run the same Spring Boot image as Fargate. A Secret injects JDBC credentials. The JAR talks to RDS PostgreSQL on 5432.
