# Assessment Structure

## Weighting

| Assessment | Weight |
|------------|--------|
| Weekly labs | 35% |
| Assignments | 15% |
| Architecture reviews | 10% |
| Final capstone | 30% |
| Participation | 10% |

---

## Weekly Labs (35%)

Each week includes hands-on labs with defined deliverables. Labs are graded on:

- **Completion** — Required resources and workflows implemented
- **Correctness** — Terraform validates; infrastructure matches spec
- **Enterprise practices** — Remote state, naming, tagging, least privilege where applicable
- **Documentation** — README updates, runbooks, or module docs as specified

Submit via pull request to your cohort fork or instructor-designated repository.

---

## Assignments (15%)

Short written or diagram-based work between labs, for example:

- Architecture decision records (ADRs)
- Environment promotion design
- Drift remediation analysis
- Cost or security review summaries

---

## Architecture Reviews (10%)

Structured peer or instructor review covering:

- Multi-account and network design
- Module boundaries and reusability
- CI/CD and approval gates
- State, security, and operational concerns

Use the architecture review template in `.github/PULL_REQUEST_TEMPLATE/architecture-review.md`.

---

## Final Capstone (30%)

See [capstone/README.md](../capstone/README.md) for rubric. Evaluated on:

| Criterion | Points (example split) |
|-----------|-------------------------|
| Architecture & design | 25% |
| Terraform quality & modules | 25% |
| CI/CD & operations | 20% |
| Security & governance | 15% |
| Documentation & presentation | 15% |

---

## Participation (10%)

- Lab discussions and office hours
- PR reviews and cohort collaboration
- Incident simulation exercises (weeks 5–6)

---

## Passing Criteria

- Minimum **70%** overall
- Capstone submitted and presented
- No outstanding critical security issues in final submission (unencrypted secrets, overly permissive IAM, etc.)
