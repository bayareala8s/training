# INCIDENT-803 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Java-level deadlock on `pay-prod-east-2` after `NightlyReversalJob` started in the **same JVM** as the API.

| Thread | Holds | Waits for | Call site |
|---|---|---|---|
| `nightly-reversal-1` | ledger lock (`0xf0ae1880`) | account lock (`0xf0acc801`) | `NightlyReversalJob.reverseOne` |
| `http-nio-8080-exec-16` | account lock (`0xf0acc801`) | ledger lock (`0xf0ae1880`) | `PaymentApplicationService.create` |

`PaymentApplicationService.create` locks **account then ledger**. `NightlyReversalJob` locks **ledger then account**. After 02:11 Pacific both hold one and wait for the other. Other HTTP creates queue on the account lock. Completions drop to zero. CPU is idle. Health stays UP. Hikari is 3/50. east-1 (job not enabled) keeps completing.

**Distinct from INC-JVM-202:** that pack is payment-worker vs refund-worker on `InMemoryLockManager` on the Module 2 canary host. This pack is nightly job vs HTTP create on `pay-prod-east-2`. Same Coffman shape, different actors.

## Stabilization

1. Kill / disable `NightlyReversalJob` on east-2, **or** bounce **that** JVM after the dump is captured.
2. Drain the canary from the load balancer until creates complete again.
3. Do not enable the job on east-1.
4. Do **not** bounce Postgres.
5. Do not bounce `dmgr-east`.
6. Do not raise Tomcat max threads.

A bounce unsticks *this* circle and will recur the next night if both orders remain.

## Remediation

- One documented lock order for every money path (account then ledger), **or**
- No nested in-process locks — use **database transactions**.
- Do not run the nightly reversal in the API JVM.
- Add a test that starts a create and a reversal on crossed orders and fails if a dump reports a deadlock.
- Review checklist: any new job that touches both locks must use the same wrapper.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | east-2 completions 0, CPU 4%, in-flight up; east-1 healthy; Hikari 3/50 |
| Logs | Job start 02:00; crossed `LOCK_ACQUIRED` / `LOCK_WAIT` on ledger vs account; Avery still in flight |
| Thread dump | Deadlock block; `NightlyReversalJob` vs `PaymentApplicationService.create`; monitors match logs |

A worksheet that says only “deadlock” without quoting these two call sites scores poorly on Diagnostic method even if the word matches the lab title. Copying INC-JVM-202’s worker names is a miss.

## Comms (acceptable example)

SEV-2 on payment creates, `pay-prod-east-2` only, after the nightly job started. Completions are zero; CPU is idle; the database pool is not exhausted. `pay-prod-east-1` still completing. We are stopping the nightly job and/or recycling that JVM, then draining the canary. Next update 20 minutes.
