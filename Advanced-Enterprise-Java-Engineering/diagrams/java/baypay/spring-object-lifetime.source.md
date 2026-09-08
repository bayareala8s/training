# Spring object lifetime — BayPay process

Teaching picture for [reference-apps/baypay](../../../reference-apps/baypay/README.md).
Not a new AEJE-D catalog ID. BayPay is fictional.

**Slide:** [spring-object-lifetime.png](spring-object-lifetime.png)  
**Edit:** [spring-object-lifetime.svg](spring-object-lifetime.svg)

```mermaid
flowchart TB
  HM[Harbor Market POST] --> TT[Tomcat worker thread]
  subgraph JVM[One JVM heap]
    subgraph CTX[ApplicationContext singletons until shutdown]
      C[PaymentController]
      S[PaymentApplicationService proxy]
      R[JpaRepository proxies]
      B[Clock Authorizer Hikari]
    end
    subgraph REQ[One POST — not beans]
      JSON[CreatePaymentRequest]
      M[Money]
      P[Payment entity]
      EM[EntityManager]
    end
  end
  TT --> C
  C --> S
  S --> JSON
  JSON --> M --> P --> EM
  EM --> DB[(H2 or Postgres)]
```

Read top to bottom: **client is not a bean → process holds the context → request objects are garbage after 201 → the row is what remains.**
