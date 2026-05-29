# Java Track — Spring Boot

Implement the same APIs as the Python reference using Spring Boot 3.

## Structure (per service)

```text
user-service/
├── src/main/java/com/bayareala8s/user/
│   ├── UserApplication.java
│   ├── controller/
│   ├── model/
│   ├── repository/
│   └── security/
├── src/main/resources/application.yml
├── Dockerfile
└── pom.xml
```

## Contracts

Implement against:

- `contracts/openapi/user-service.yaml`
- `contracts/openapi/product-service.yaml`
- `contracts/openapi/order-service.yaml`

## Labs

Follow `labs/module-XX/` — substitute Maven/Gradle commands for pip/uvicorn.

## Dependencies (suggested)

- Spring Web, Spring Data JPA
- Spring Security + JWT
- AWS SDK v2 for EventBridge and DynamoDB

## Reference

Compare behavior with `starters/python/` services running in Docker Compose.
