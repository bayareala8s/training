# INCIDENT-1002 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Sam Okada set the Deployment memory **limit to 512Mi** and `JAVA_TOOL_OPTIONS=-Xmx512m` so the heap would “use the limit.” Heap max is **100% of the cgroup**. Native memory, thread stacks, metaspace, and direct buffers sit **on top of** that heap. The kubelet **OOMKills** the container (Last State `OOMKilled`, exit **137**). There is **no** Java heap `OutOfMemoryError` first.

Last GC scrap: ~401M used of 512M before the kill. Same **class** as INCIDENT-806; evidence is `kubectl describe` + events + last-state flags, not the Module 8 dashboard. Do not copy 806’s 389 MB figure.

This is not INCIDENT-1001 (Exit 1 bind) and not a leak (process does not live long enough).

## Stabilization

1. **Raise the memory limit** (e.g. back toward 2Gi or at least 768Mi–1Gi) **or** drop `-Xmx` (for example `-XX:MaxRAMPercentage=75`) and restart.
2. Do **not** set the new `-Xmx` equal to the new limit.
3. Do **not** bounce Postgres.
4. Do not bounce `dmgr-east`.
5. Do not treat a Java heap dump as the first stabilize move — the process is already gone.

## Remediation

- **Never** set `-Xmx` equal to the container limit.
- Keep `UseContainerSupport` **and** leave headroom (percentage or reviewed fixed heap).
- Document the budget: heap + metaspace + stacks + native + OS headroom.
- A “right-size” roll must include a flag review, not only a YAML limit change.
- Optional: NMT summary in staging when shrinking a pod.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| describe.txt | Last State OOMKilled; exit 137; limit 512Mi; `JAVA_TOOL_OPTIONS=-Xmx512m` |
| events.txt | Repeated OOMKilled at 512Mi; no Java OOME event |
| jvm-flags.txt | MaxHeapSize 512Mi; limit 512Mi; last GC ~401M/512M |

A worksheet that says only “container OOM” without comparing `-Xmx` to the limit scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `payment-service` in `baypay-prod` after the 512Mi right-size. Pods are OOMKilled at the cgroup limit. We have not seen a Java heap OutOfMemoryError. We are raising the limit or lowering the heap so they are not the same number, then restarting. Next update 20 minutes.
