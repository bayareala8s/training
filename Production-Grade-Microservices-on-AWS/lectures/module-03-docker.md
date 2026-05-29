# Module 3 Lecture — Containerization

## Topics

1. **Images vs containers** — immutable artifact vs running process
2. **Dockerfile layers** — cache, order matters (deps before code)
3. **Multi-stage builds** — slim production images
4. **Compose** — local distributed system
5. **ECR** — private registry on AWS
6. **Security** — scan on push, no secrets in layers

## Demo

`docker compose up --build` → `./scripts/demo-platform.sh`

## Pitfalls

- Running as root in production
- Huge images (slow deploy, attack surface)
- `:latest` only in dev

## Lab

`labs/module-03/README.md`
