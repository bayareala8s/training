# Week 4 — Enterprise Scenarios & Case Studies

## Scenario A — SaaS company: leaked GitHub PAT with admin AWS keys

**Context:** A developer stored `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` in repository secrets for a “quick” Terraform workflow. A compromised dependabot fork exfiltrated secrets. Attacker ran crypto miners in dev and attempted privilege escalation in prod (blocked by SCP).

**Impact:**

- $47k AWS bill in 72 hours
- Mandatory OIDC migration; all static keys revoked org-wide

**Lesson:** **OIDC short-lived credentials** scoped to repo/branch/environment beat long-lived keys.

**Discussion questions:**

1. What trust policy `sub` pattern limits apply to `main` only?
2. How do you rotate after static key leak vs OIDC misconfiguration?

---

## Scenario B — Enterprise platform: plan/apply separation saves production

**Context:** A PR showed two `forces replacement` on production NAT gateways due to an innocent variable typo. CI plan job failed checks; reviewer caught diff in PR comment. Apply job never ran.

**Outcome:** Zero downtime; engineer fixed typo; new green plan merged.

**Lesson:** **Plan on every PR** is change advisory for infrastructure—not bureaucracy.

**Discussion questions:**

1. Should apply use saved plan files (`-out`) in this org? Why?
2. Who must approve plans touching `prod` environment?

---

## Scenario C — Government contractor: Checkov gate blocks launch

**Context:** Security mandated Checkov hard-fail on `CKV_AWS_*` high findings. A team’s module passed validate but failed on public S3 ACL check. They documented accepted risk for a static website bucket with compensating CloudFront OAC controls—exception ticket required.

**Pattern:**

| Finding | Action |
|---------|--------|
| Fixable misconfig | Remediate in module, release patch |
| False positive | `.checkov.yml` skip with ticket ID |
| True risk accepted | Exception register + expiry date |

**Lesson:** Policy-as-code needs a **human exception process**, not silent ignores.

**Discussion questions:**

1. Where should skip annotations live—module or root?
2. How often should accepted risks be re-reviewed?

---

## Scenario D — Monorepo scale: path filters and noisy CI

**Context:** 400-engineer monorepo ran Terraform CI on every commit; queue times exceeded 45 minutes. Platform added `paths` filters and matrix jobs per environment directory.

**Outcome:** Median feedback under 8 minutes; full org scan nightly.

**Lesson:** **Pipeline design** is performance and developer experience—not only security.

**Discussion questions:**

1. What paths should trigger plan for `modules/vpc` changes?
2. When is a nightly full plan better than per-PR scoped plans?

---

## Lab tie-in

Week 4 labs implement Scenario B’s controls using [`labs/week-04/workflows/terraform-ci.yml`](../../labs/week-04/workflows/terraform-ci.yml) and OIDC guide—see [04-hands-on-labs.md](04-hands-on-labs.md).
