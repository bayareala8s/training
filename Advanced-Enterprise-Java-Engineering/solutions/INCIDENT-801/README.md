# INCIDENT-801 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Canary `payment-service` **3.8.1** on `pay-prod-east-2` added a request-body PII scan that calls `String.matches` on the **full POST body**. The pattern is catastrophic on large JSON (nested quantifiers against unbounded input). Many HTTP threads sit `RUNNABLE` in `java.util.regex.Pattern` / `Matcher.matches` / `String.matches` at `RequestBodyPiiScanner.scan`. Process CPU is **98%**. p99 on create climbs to ~9s; some requests time out.

`pay-prod-east-1` on **3.8.0** is healthy (CPU ~12%, p99 ~180 ms). Heap and GC are quiet. Hikari is not exhausted. The database is not the page.

This is a CPU burn on the canary HTTP threads, not a leak, not a deadlock, and not container OOM.

## Stabilization

1. Remove `pay-prod-east-2` from the load balancer, **or** revert the canary to 3.8.0.
2. Do not roll 3.8.1 to east-1.
3. Do **not** bounce Postgres.
4. Do not bounce `dmgr-east` (wrong estate).
5. Optional: bounce the canary JVM only after it is out of rotation, if you need the process idle for a follow-up dump. Traffic restoration is the LB / revert, not a hope that a restart makes `matches()` cheap.

## Remediation

- Delete the regex scan on the unbounded body, or replace it with a **linear** parser (streaming JSON tokens, size-capped field checks).
- Never call `String.matches()` (or `Matcher.matches()`) on unbounded JSON.
- Cap `content-length` for the scan path; reject or skip oversized bodies.
- Gate the canary on CPU and create p99, not only on “process up.”
- Add a unit test with a large Harbor-like payload that must finish in milliseconds.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | east-2 CPU 98%; east-1 healthy on 3.8.0; heap/GC quiet; Hikari 11/50; DB CPU low |
| Logs | 3.8.1 start; `RequestBodyPiiScanner` scan times of several seconds on large `contentLength`; Avery create hung then completed |
| Thread dump | Many `http-nio` threads `RUNNABLE` in `Pattern` / `String.matches` at `RequestBodyPiiScanner.scan` |

A worksheet that says only “regex” or “CPU” with no gate order and no quoted frames scores poorly on Diagnostic method even if the word is right.

## Comms (acceptable example)

SEV-2 on payment creates, `pay-prod-east-2` only. Process CPU 98 percent after the 3.8.1 canary. `pay-prod-east-1` still completing. We are taking the canary out of the load balancer (or reverting 3.8.1). Database and pool gauges are not exhausted. Next update 20 minutes.
