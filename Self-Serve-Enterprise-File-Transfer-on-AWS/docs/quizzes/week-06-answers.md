# Answer key — Week 6 quiz

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | Self-serve = guardrailed product surface, not console access. |
| 2 | **B** | `sub` binds resources to the authenticated user. |
| 3 | **B** | Async jobs return 202; poll GET job status. |
| 4 | **B** | Never expose secrets/IAM keys. |
| 5 | **B** | Approval workflow prevents unvetted production paths. |
| 6 | **B** | JWT authorizer validates Cognito-issued tokens. |
| 7 | **B** | AuthZ must enforce connection prefix scope. |
| 8 | **B** | Catalog + job state; secrets stay in Secrets Manager. |
| 9 | **B** | Idempotent job API avoids duplicate orchestration. |
| 10 | **A** | Cross-tenant read must be denied. |
| 11 | **Sample:** **Connection:** `connection_id`, `type`, `status`. **Job:** `job_id`, `state`, `correlation_id`. | |
| 12 | **Sample:** Prevents data leakage across partners/tenants; users should only see authorized connections and job metadata. | |
