# INC-K8S-1002 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Payment pods OOMKilled after memory change  
**Namespace:** `baypay-prod`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Same *class* as INC-JVM-806, **this pack’s numbers only**. Pod `…-xk2q1` is Running/Ready now (restart window) but Last State **Terminated / OOMKilled / Exit 137**. Memory **limit 512Mi** (request 512Mi). `JAVA_TOOL_OPTIONS=-Xmx512m` — heap **equals** the cgroup. Describe events: container exceeded limit 512Mi, usage 512Mi (three times). Image `3.9.1` already present. No `java.lang.OutOfMemoryError` on pod events. Timeline: Sam “right-sized” to 512Mi and set heap to “use the limit” (BAYPAY-10022). Hypothesis: kubelet cgroup kill because heap + native > 512Mi, not a Java heap OOME and not INC-1001 bind/Exit 1. Next: kube events (reason/count), then flags file to confirm `-Xmx` vs limit and whether `UseContainerSupport` / percentage is absent.

Gate 2: Events are **kubelet cgroup kills**, not a Java OOME. Repeated `OOMKilled` / `Killing` on `-xk2q1`, `-m3n4p`, `-q7r8s`: “exceeded its memory limit (limit 512Mi, usage 512Mi).” After last kill, readiness `connection refused` during the restart window — that is the merchant 502, not “pod is Running so we are fine.” Sam’s roll: memory **2Gi → 512Mi**. No `java.lang.OutOfMemoryError` event. Question for gate 3: do last-state JVM flags show `-Xmx512m` with **no** `MaxRAMPercentage` headroom, and is last GC occupancy **below** 512Mi (heap not exhausted — native + heap filled the cgroup)?

Gate 3: Yes. Env is only `-Xmx512m`. Scrap: `-XX:MaxHeapSize=536870912` (512 MiB) **equals** the 512Mi limit. `UseContainerSupport` is on but **`-Xmx` pins the heap**, so a percentage never applies. Last GC before the 15:01 PT kill: `428M->401M(512M)` — about **401M used of 512M**, not a full Java heap. No Java OOME in the scrap. NMT off. CLUSTER healthy pairing is **2Gi + MaxRAMPercentage=75**. RCA: Sam set heap = cgroup; metaspace / stacks / GC / native sit on top; kubelet 137.

## Supporting evidence

(File, timestamp, quote. Last State, Exit code, events reason, flags, limit.)

- `timeline.json` 21:20Z Sam Okada: right-sized memory to 512Mi; `JAVA_TOOL_OPTIONS` so heap “uses the limit” (BAYPAY-10022). 22:31Z Priya: restart count 2 in 50 min; asked for describe/events before raising the limit again. 23:10Z pager: unavailable 3 times in 90 min; Ingress 502 burst. 23:12Z Harbor Market / Avery `c1002b22-…-111002` 502 then 201; same Idempotency-Key. 23:13Z Riley: do not set `-Xmx` equal to a new limit without a headroom number.
- Gate 1 `evidence/describe.txt`: Last State `OOMKilled` Exit **137**; Limits.memory **512Mi**; `JAVA_TOOL_OPTIONS: -Xmx512m`; current State Running / Ready True; Restart Count 3; “exceeded its memory limit (limit 512Mi, usage 512Mi)” ×3. No Java OOME on events. Same Last State on `-m3n4p` and `-q7r8s`.
- Gate 2 `evidence/events.txt`: same OOMKilled / Killing on three pods; Readiness `connection refused` during last restart window; comment: Deployment memory **2Gi → 512Mi**. No `java.lang.OutOfMemoryError`.
- Gate 3 `evidence/jvm-flags.txt`: `MaxHeapSize=536870912`; last GC `428M->401M(512M)` at 23:00:41Z; NMT off; contrast healthy `limit 2Gi` + `MaxRAMPercentage=75`. Do not copy 806’s 389 MB — this scrap is **401M**.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: events (gate 2) to see whether kills are kubelet `OOMKilled` vs a Java exception, and whether all replicas share it. After gate 2: JVM flags (gate 3) to compare `-Xmx` / `MaxHeapSize` to the 512Mi limit and last GC used vs committed. Omitted app logs might show a Java OOME if one existed — events + scrap say it does not. Heap histogram / NMT would show native beside 401M heap next week (`NativeMemoryTracking=off` now). Deployment history omitted; timeline already names the 2Gi→512Mi roll. Do not invent 806’s 389 MB. Do not bounce Postgres.

## Stabilization action

(What restores a living replica *now*? Limit vs flags? What do you explicitly not do?)

Change the **pairing**, then roll — do not only restart. Either (a) restore memory limit toward **2Gi** and set `JAVA_TOOL_OPTIONS=-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0` (CLUSTER healthy), or (b) stay on 512Mi **only if** you **drop** `-Xmx512m` and use 75% (~384 MiB heap) so ~128 MiB remains for native — and watch whether Boot still fits. Do **not** set `-Xmx` equal to whatever new limit you pick (Riley). Do **not** raise `-Xmx` to 2g on a 2Gi box. Do **not** bounce Postgres or `dmgr-east`. Do **not** treat “pod is Running” as restored while the same flags remain. Paper change only — no paid cluster.

## Remediation

(What remains after the page is quiet?)

A memory-limit change requires a **flag-review ticket**, not a YAML-only “right-size.” Never ship `-Xmx` = limit (or `MaxRAMPercentage=100`). Prefer `MaxRAMPercentage` when the same image runs at more than one limit; a reviewed `-Xmx384m` on a locked 512Mi contract is clearer but still needs headroom. Turn on NMT (or a one-shot debug image) next week instead of “just add 2Gi” forever. Avery’s 502→201 on the same Idempotency-Key is the correct client behavior — do not double-post. Matching heap to the limit is a reliability smell, not efficient packing.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 `baypay-prod` / `payment-service`: intermittent Ingress 502 while replicas restart. Harbor Market / Avery `c1002b22-…-111002` 502 then 201; same Idempotency-Key.  
Last State **OOMKilled / Exit 137**. Limit **512Mi**, usage 512Mi. Not a Java heap OOME (last GC **401M of 512M**).  
Sam’s BAYPAY-10022 set limit 2Gi→512Mi and `JAVA_TOOL_OPTIONS=-Xmx512m` (heap = cgroup).  
Restoring a pairing with native headroom (limit and/or drop `-Xmx`; 75% — not `-Xmx` = new limit). Restart alone is not the fix.  
Not treating this as a leak or a database outage. Next update when a replica stays Ready across a full GC cycle.
