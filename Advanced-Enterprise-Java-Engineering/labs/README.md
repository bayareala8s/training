# Labs

Sixty-eight lab packs. Most are paper, dumps, YAML, or Terraform. Five Java labs now have a Maven reactor and JUnit contract tests.

## Runnable Java labs

| Lab | What you implement | Command |
|---|---|---|
| BUILD-101 | `Money`, `Payment`, `PaymentStatus`, `PaymentStateMachine` | `../reference-apps/baypay/mvnw -pl BUILD-101 test` |
| BUILD-102 | `PaymentValidator.validate` | `../reference-apps/baypay/mvnw -pl BUILD-102 test` |
| FIX-103 | `CleanPaymentValidator` (starter stays messy) | `../reference-apps/baypay/mvnw -pl FIX-103 test` |
| CHALLENGE-104 | `FasterPostingLoop` (`NaivePostingLoop` stays naive) | `../reference-apps/baypay/mvnw -pl CHALLENGE-104 test` |
| BREAKFIX-201 | `SafePaymentLedger` (starter stays racy) | `../reference-apps/baypay/mvnw -pl BREAKFIX-201 test` |

From `labs/`:

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
../reference-apps/baypay/mvnw test
```

Stubs compile. Tests fail until you implement the types. Instructor solutions stay under `solutions/` and are overlaid only by `qa/smoke_runnable_labs.py`.

BUILD-301–305 and FIX-304 work inside `reference-apps/baypay` (`./mvnw test`). LAB-701–703 are `javac` harnesses, not Spring.

## Not turned into live clusters

ARCHITECT, most INCIDENT, DR, COST, INTERVIEW (CLI exists), AI-1501–1504 (JSON contract), WebSphere, and OpenShift stay simulation-first. AWS labs stay at `terraform validate` unless you choose to apply in `us-west-2` and destroy the same day.
