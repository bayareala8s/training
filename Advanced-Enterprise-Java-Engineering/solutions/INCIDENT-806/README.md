# INCIDENT-806 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Jordan moved `pay-prod-east-2` to a **512Mi** pod and set `JAVA_TOOL_OPTIONS=-Xmx512m` (also `-Xms512m`) so the heap would “use the limit.” Heap max is **100% of the cgroup**. Native memory, thread stacks, metaspace (~90 MB), and direct buffers sit **on top of** that heap. RSS reaches 512Mi while Java heap used is still ~400 MB. The kubelet **OOMKills** the container (exit 137). There is **no** Java heap `OutOfMemoryError` first.

east-1 stays on 2Gi / `-Xmx1536m` and is healthy. This is not INCIDENT-802’s retained map (the process does not live long enough). It is not INCIDENT-805’s allocation storm (pauses stay short).

## Stabilization

1. **Raise the memory limit** (e.g. back toward 2Gi or at least 768Mi–1Gi) **or** drop `-Xmx` (for example `-XX:MaxRAMPercentage=75` and no pinned 512m) and restart the canary.
2. Drain or take east-2 out of the LB until the new pairing is up.
3. Do **not** set the new `-Xmx` equal to the new limit.
4. Do **not** bounce Postgres.
5. Do not bounce `dmgr-east`.
6. Do not treat a Java heap dump as the first stabilize move — the process is already gone.

## Remediation

- **Never** set `-Xmx` equal to the container limit.
- Keep `UseContainerSupport` **and** leave headroom (percentage or reviewed fixed heap).
- Document the budget: heap + metaspace + stacks + native + OS page cache headroom.
- Canary resize must include a flag review, not only a YAML limit change.
- Optional: NMT summary in staging when shrinking a pod.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | 3 restarts; 512Mi limit; RSS ~508 MiB; heap used ~402/512 MB; no Java OOME; east-1 fine |
| Kube events | Repeated `OOMKilled` at 512Mi; exit 137; no heap OOME event |
| JVM flags | `-Xmx512m` / `MaxHeapSize=536870912`; limit 512Mi; last GC 389M used of 512M |

A worksheet that says only “container OOM” without comparing `-Xmx` to the limit scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `pay-prod-east-2` after the 512Mi canary resize. The pod is being OOMKilled at the cgroup limit. We have not seen a Java heap OutOfMemoryError. `pay-prod-east-1` still completing. We are raising the limit or lowering the heap so they are not the same number, then restarting the canary. Next update 20 minutes.
