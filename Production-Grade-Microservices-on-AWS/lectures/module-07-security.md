# Module 7 Lecture — Security & Identity

## JWT

- Header.Payload.Signature
- Stateless verification
- Short expiry; refresh tokens in production systems

## IAM

- **Execution role** — ECS agent
- **Task role** — application AWS API calls

## Secrets Manager vs Parameter Store

Use Secrets Manager for rotation-sensitive secrets (JWT, DB passwords).

## Network

- Private subnets for tasks
- Security groups as firewalls

## Threat Modeling (15 min breakout)

Walk through: stolen JWT, SSRF to metadata, overly permissive task role.

## Lab

`labs/module-07/README.md`
