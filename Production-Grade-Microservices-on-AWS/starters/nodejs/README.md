# Node.js Track — NestJS

Implement the same APIs as the Python reference using NestJS.

## Structure (per service)

```text
user-service/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── users/
│   └── auth/
├── Dockerfile
├── package.json
└── tsconfig.json
```

## Contracts

Use `@nestjs/swagger` to generate OpenAPI matching files in `contracts/openapi/`.

## Labs

Follow `labs/module-XX/` — use `npm run start:dev` instead of uvicorn.

## AWS

Use `@aws-sdk/client-eventbridge` in order-service for Module 5+.

## Reference

Run Python stack via `docker compose` to verify compatible request/response shapes.
