# Portfolio artifact — JVM incident RCA

**Course:** Advanced Enterprise Java Engineering  
**Module:** 08 — JVM Troubleshooting  
**Artifact id:** PF-05  
**Sources:** pick **one** of INCIDENT-801 / INC-JVM-801 through INCIDENT-806 / INC-JVM-806  
**Case study:** BayPay Financial Services (fictional)

Export this file (or a copy) when you submit. Do not paste instructor solution text. All names and ids you cite must come from the synthetic pack you chose. Locked instructor RCAs live only under `solutions/`.

**Student:**  
**Date:** 2026-09-06  
**Cohort / reviewer (if any):**  

**Incident chosen (circle one):**  
801 CPU 98 percent · 802 Memory leak · 803 Deadlock · 804 Thread-pool exhaustion · 805 Excessive GC · **806 Container OOM**

**Pack path:** `incidents/jvm/INC-JVM-806/`

---

## 1. Symptom

What merchants and the pager showed. Quote numbers from the **dashboard** (replica, time, SLO):

SEV-2 at **16:48 Pacific / 23:48 UTC on 2026-10-15** on **`pay-prod-east-2`**. Pager: canary unavailable **3 times in 90 minutes**; load-balancer **502 bursts**. Dashboard: restart count **0 → 3** (15:20 after resize through 16:48). 502 / 5m peaked at **22** while east-2 was restarting (16:41). Harbor Market: Avery Chen payment `c806d666-0000-4000-8000-111111111806` **HTTP 502** then **201** on retry (same `Idempotency-Key`). Last good scrape before the 16:41 kill: heap **402 / 512 MB**, cgroup RSS **508 MiB**, Java `OutOfMemoryError` count **0**, GC pause p99 **22 ms**. Creates that landed while the pod was up were fine (p99 210 ms, Hikari 10/50).

What `pay-prod-east-1` was doing at the same time:

**Ready the whole window**, **0 restarts**, memory limit **2Gi**, heap **510 / 1536 MB**, RSS 890 MiB, error rate **0**. Avery’s retry **201** on east-1. First sentence of the page: **east-1 is not in the incident.**

---

## 2. Hypothesis timeline

Write in gate order. A lucky label that matches the lab title does not replace this table.

| Gate | File opened | Hypothesis after that file | Evidence that supported or killed it |
|---|---|---|---|
| 1 | `evidence/dashboard.md` (+ timeline) | Canary-only death after Jordan’s 512Mi resize + `-Xmx512m`. RSS near the cgroup while heap still had room → **cgroup kill**, not Java heap OOME, not 802’s two-day climb. Next: is the kube reason `OOMKilled`? | Restarts 3; heap 402/512 vs RSS 508/512Mi; OOME **0**; east-1 2Gi/1536m never restarted. Process did not live long enough for 802. |
| 2 | `evidence/kube-events.md` | Kernel killed the container at the **memory limit**. Still not a closed heap RCA — need flags vs 512Mi. | `OOMKilled` ×3 “limit 512Mi, usage 512Mi”; Last State Terminated **exit 137**; **no** Java OOME event. Pod `Running` again (502s were the restart window). |
| 3 | `evidence/jvm-flags.md` | **`-Xmx` equals the cgroup.** Native (metaspace, stacks, direct, GC) sits in the same 512Mi. `UseContainerSupport` on but heap is pinned. | `JAVA_TOOL_OPTIONS=-Xmx512m -Xms512m`; `MaxHeapSize=536870912`; heap_info used ~389 MB; last young GC `412M->389M(512M) 18.4ms` ~1 min before 16:41 kill. east-1 2Gi + 1536m leaves ~512Mi outside the heap. |

---

## 3. Root cause (your words)

Mechanism, instance, and version or flag. Quote stacks, classes, events, or flags. Do not import a different Module 8 pack’s story unless you say why you ruled it out:

On **`pay-prod-east-2`** (image `payment-service:3.8.2`, ticket **BAYPAY-8066**), Jordan moved the canary to a **512Mi** pod and set `JAVA_TOOL_OPTIONS=-Xmx512m -Xms512m` so the heap would “use the limit.” Effective `MaxHeapSize=536870912` (**512 MiB**), same as the cgroup. `UseContainerSupport` was **on**, so it did not matter: the explicit `-Xmx` pinned the heap to 100% of the box. RSS is heap **plus** metaspace (~88–90 MB), ~131 thread stacks, direct buffers (~44 MB), and GC/code native. Last scrape: heap **402 MB used**, RSS **508 MiB**. Last recovered young GC: **389 MB used of 512 MB**. The kubelet then **`OOMKilled`** the container (usage 512Mi / limit 512Mi, **exit 137**). Java never threw `OutOfMemoryError`. Merchants saw 502s only while the pod was gone; east-1 completed the same `Idempotency-Key`.

What this is **not** (one sentence, with evidence):

**Not** a Java heap OOME (count 0; last GC 389M/512M), **not** INC-802’s unbounded cache (no two-day old-gen climb; process dies in minutes), **not** INC-805’s DEBUG allocation storm (pause p99 22 ms), **not** Hikari/DB (10/50, DB CPU 16%), **not** a Module 5 cell problem (`dmgr-east` is a different estate).

---

## 4. Stabilize vs remediate

| Stabilize (restores capacity *now*) | Remediate (keeps the next canary safe) |
|---|---|
| Drain **east-2** from the LB. Keep east-1. Then either **raise the limit** (honest 2Gi like east-1) **or** shrink heap on 512Mi (`-Xmx384m` / `MaxRAMPercentage=75`) and **drop `-Xms512m`**. Restart after the change. | Policy: **never** `-Xmx` (or `-Xms`) equal to the cgroup. ~25% native headroom. Written owner when the limit changes (Jordan vs Priya). Smaller canary is allowed **only** with that headroom. NMT on the next 512Mi experiment — not “just add 2Gi.” |

What you explicitly **did not** do (Postgres, `dmgr-east`, region failover, Tomcat 2000, and so on):

Did not bounce Postgres, `dmgr-east`, or the region. Did not announce a leak. Did not raise `-Xmx` further on 512Mi. Did not set `-Xmx` equal to a *new* limit “to use all the RAM.” Did not copy INC-202 / INC-402 thread or pool names (they are not in this pack).

---

## 5. Evidence table

| Gate | File | One quote (timestamp + text) | What it proved |
|---|---|---|---|
| 1 | dashboard.md 16:41–16:48 | Restarts **3**; heap **402/512 MB**; RSS **508 MiB**; Java OOME **0** | Process died with heap **not** full; east-1 2Gi / 1536m never restarted |
| 2 | kube-events.md 27m / Last State | `OOMKilled` … `limit 512Mi, usage 512Mi`; exit **137** | Kernel / cgroup kill, not a Java exception |
| 3 | jvm-flags.md | `JAVA_TOOL_OPTIONS=-Xmx512m -Xms512m`; `MaxHeapSize=536870912`; last GC `412M->389M(512M) 18.440ms` | Heap flag **equals** limit; last successful GC still had ~120 MB Java-heap free |

Omitted evidence you wanted, and what you expected it to show:

**Histogram / thread dump / app logs** omitted. A histogram would have been useful only to *rule out* 802 (`IdempotencyRecord` millions) — the process did not live two days. App logs often **absent** after 137 (no Java heap dump). **NMT** was off; next week’s 512Mi canary should start with `NativeMemoryTracking=summary` so stacks/metaspace/direct have numbers, not slogans.

---

## 6. Communication samples

### Internal bridge (five lines max)

What we know / do not know / next update:

SEV-2 is **`pay-prod-east-2` only** (512Mi canary, BAYPAY-8066). east-1 is up; Avery `c806d666-…` already **201** on retry. East-2 was **OOMKilled** three times (exit 137); **no** Java `OutOfMemoryError`. Last heap used ~390 MB of 512 when RSS hit the limit. We are draining east-2 and will not set `-Xmx` equal to the memory limit. Next update when the canary is off the balancer or running with heap **below** 512Mi.

### Merchant-safe note

No invented cause. No confidential-sounding runbook language:

Some Harbor Market creates got **502** when one replica restarted. Retries with the **same payment key** succeeded. We have taken that replica out of rotation. No action needed on your side; do not submit a second different key for the same checkout.

---

## 7. Architecture / trade-off

One policy you would enforce next week, and the cost of that policy:

**Policy:** canary `memory` limit and `-Xmx` are a **pair**. Heap ≤ **75%** of the limit (or explicit `-Xmx384m` on 512Mi); `-Xms` must not fill the box. Jordan cannot merge a limit change without Priya’s headroom line.

**Cost:** a 512Mi canary holds a **smaller live set** than east-1 (1536m heap). You either accept that (true cheap canary) or you pay for **2Gi** and keep 1536m. You do not get “east-1 heap on a 512Mi sticker.”

---

## 8. Interview talking points

Write four bullets you would actually say, labeled Engineer / Senior / Staff / Principal:

- Engineer: `OOMKilled` / exit **137** is the **kernel**. `OutOfMemoryError: Java heap space` is **HotSpot**. This pack had the first and not the second. Heap used was ~390 MB.
- Senior: Three things outside `-Xmx` on this scrape: **metaspace ~90 MB**, **direct ~44 MB**, **131 stacks** — plus GC/code. RSS 508 on a 512Mi box is the story. `UseContainerSupport` does not help if `-Xmx512m` is in `JAVA_TOOL_OPTIONS`.
- Staff: Stabilize is **drain east-2**, then raise the limit **or** drop heap to ~384m. Remediate is a written rule: **never heap = cgroup**. A lucky “container OOM” label without the 402-vs-508 and `MaxHeapSize=536870912` quotes is not Diagnostic method.
- Principal: A smaller canary is a **product choice** (cost vs blast). Matching `-Xmx` to the limit is not packing — it is a planned 137. I fund NMT on the next 512Mi experiment, not a second traditional ND cell and not a region failover.

---

## Honesty

- [x] I did not open `solutions/INCIDENT-80N/` before attempting the worksheet
- [x] I requested evidence in the documented gate order
- [x] Every numeric claim has a source (dashboard, log, dump, histogram, events, or flags)
- [x] I did not paste an instructor RCA
- [x] If I had done INC-JVM-202 or INC-EE-402, I did not copy those thread or pool names unless they appear in **this** pack
