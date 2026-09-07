# INC-JVM-806 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Canary pod restarting  
**Instance:** `pay-prod-east-2` (canary) vs `pay-prod-east-1`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: SEV-2 is **`pay-prod-east-2` only** after Jordan resized to **512Mi** and set `-Xmx512m` (“use the limit”). Three restarts in 90 minutes; 502s line up with the pod leaving. Last scrape: heap **402/512 MB**, RSS **508 MiB**, Java OOME **0**, GC p99 22 ms. east-1 2Gi / `-Xmx1536m`, no restarts, Avery **201**. This is **not** heap exhaustion and **not** 802 (process does not live two days). First guess: **cgroup kill** — native (metaspace 88 + threads + direct 44 + GC) on top of a heap allowed to be 512. Next: kube events — is the reason **`OOMKilled`**? Then flags — confirm `-Xmx` **equals** the limit. Do not set `-Xmx` equal to a new limit without a headroom number.

Gate 2: Events are **cgroup**, not a Java heap OOME. Three **`OOMKilled`**: “exceeded its memory limit (limit **512Mi**, usage **512Mi**)”. Last State **Terminated / OOMKilled / exit 137**. Pod is **Running** again (merchants still saw 502s in the window). **No** `java.lang.OutOfMemoryError` event. `OOMKilled` is not a closed heap RCA — kernel vs `-Xmx` still needs flags. Next: `jvm-flags.md` — is `-Xmx` **512m** on a **512Mi** cgroup? What was last GC used? That would confirm LAB-704: heap + native > limit while heap used was 402 MB.

Gate 3: Flags confirm **heap = cgroup**. `JAVA_TOOL_OPTIONS=-Xmx512m -Xms512m`. `UseContainerSupport` **on**, `MaxHeapSize=536870912` (**512 MiB**). Last `GC.heap_info`: used **398112K (~389 MB)** of 512M; metaspace used **90 MB**. Previous container last young GC **412M->389M(512M) 18ms** ~1 min before 16:41 `OOMKilled`. No Java OOME. `UseContainerSupport` does not save you when `-Xmx` is **pinned to the limit**. east-1 `2Gi` + `-Xmx1536m` leaves ~512Mi native — never killed. Mechanism: RSS (heap committed + metaspace + stacks + direct + GC native) hit **512Mi** while Java heap still had ~110 MB free.

## Supporting evidence

| File | Quote |
|---|---|
| timeline 22:15 | Jordan: 512Mi pod + `JAVA_TOOL_OPTIONS=-Xmx512m` so heap “uses the limit” |
| dashboard | Restarts **3**; heap **402/512**, RSS **508 MiB**, Java OOME **0** |
| dashboard | east-1 2Gi / 1536m, Avery `c806d666-…` **201** |
| kube-events | `OOMKilled` limit 512Mi usage 512Mi ×3; exit **137** |
| jvm-flags | `-Xmx512m -Xms512m`; MaxHeapSize **536870912** |
| jvm-flags last GC | Young `412M->389M(512M) 18.4ms` before kill |

No histogram / thread dump / app logs (137 often leaves no Java dump). NMT was **off**.

## Next investigation

JVM flags / last GC: confirm `JAVA_TOOL_OPTIONS` / `MaxHeapSize` versus cgroup **512Mi**. If `-Xmx512m` (or MaxHeapSize ≈ 512Mi) and last successful GC shows used **~400 MB**, the kill is **native headroom**, not “heap full.” Histogram omitted (process dies too fast for 802). App logs omitted — 137 often means **no** Java heap dump. NMT next week if we keep a 512Mi canary.

## Stabilization action

**Drain `pay-prod-east-2`** so 502s stop (east-1 already 201’d Avery). Then either **raise the cgroup** (e.g. match east-1 2Gi) **or shrink the heap** on 512Mi (`-Xmx384m` / `MaxRAMPercentage=75`) and **drop `-Xms512m`**. Restart after the flag/limit change. Do **not** set `-Xmx` equal to a new limit “to use all the RAM.”

Do **not**: bounce Postgres; bounce `dmgr-east`; announce a leak; raise `-Xmx` further on 512Mi.

## Remediation

- **Never** `-Xmx` = cgroup. Leave ~25% native headroom (LAB-704): stacks, metaspace (~90 MB here), direct (~44 MB), GC, code.
- Percentage of the limit (`MaxRAMPercentage=75`) **or** a reviewed `-Xmx384m` — when the limit changes, **who owns the number** is written down (Jordan vs Priya).
- A smaller canary is acceptable **if** flags leave headroom. Matching east-1’s 2Gi is the other honest choice (cost vs risk).
- Next week: **NMT** on the canary, not “just add 2Gi” with no categories.
- Matching `-Xmx` to the limit is a reliability smell, not efficient packing.

## Communication update

SEV-2 is the **512Mi canary only**. `pay-prod-east-1` is up and already returned 201 for Avery `c806d666-…` (same Idempotency-Key). East-2 was **OOMKilled** (exit 137) three times; there is **no** Java `OutOfMemoryError`. Heap was ~390 MB of 512 when the kernel hit the limit. We are draining east-2 and will not set `-Xmx` equal to the memory limit again. Next update when the canary is either off the balancer or running with heap **below** 512Mi.
