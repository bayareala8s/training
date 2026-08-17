# Security Review Checklist

**Student:** _______________ **Date:** _______________

| # | Item | Done | Notes |
|---|------|------|-------|
| 1 | No secrets in Git | ☐ | |
| 2 | JWT secret in Secrets Manager | ☐ | |
| 3 | ECS tasks use IAM roles (no access keys) | ☐ | |
| 4 | Security groups least privilege | ☐ | |
| 5 | ECR image scanning enabled | ☐ | |
| 6 | HTTPS on ALB / API Gateway | ☐ | |
| 7 | Passwords hashed (bcrypt) | ☐ | |
| 8 | Input validation on all POST bodies | ☐ | |
| 9 | Dependency scan in CI (optional) | ☐ | |
| 10 | CloudTrail enabled in account | ☐ | |

**Threat modeled flows:** Login | Place Order | Admin Product Create

**Top risk identified:** _______________________________________________

**Mitigation:** _______________________________________________
