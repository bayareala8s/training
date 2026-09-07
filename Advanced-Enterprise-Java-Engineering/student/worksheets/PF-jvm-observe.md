# Portfolio — JVM memory and GC observation notes

**Course:** Advanced Enterprise Java Engineering  
**Module:** 07 — JVM Internals and Performance  
**Labs:** LAB-701 · LAB-702 · LAB-703 · LAB-704  
**Case study:** BayPay Financial Services (fictional)

Export this page (or a copy) as your Module 7 portfolio artifact. Use **your** `jcmd` output, harness stdout, GC log lines, and arithmetic. Do not paste instructor synthetic logs or range tables as if they were your run.

**Your name:**  
**Date:** 2026-09-06  
**JAVA_HOME used:** `/opt/homebrew/opt/openjdk@21` (OpenJDK 21.0.2)  
**Path chosen in LAB-701:** MemoryProbe (Path A). payment-service in terminal 40 was already up **without** NMT; NMT must be set at start, so I did not attach folklore to that pid.

---

## Heap (LAB-701)

**Process pid:** `25946`  
**Start command (include NMT flags):**  

```text
java -XX:+UnlockDiagnosticVMOptions -XX:NativeMemoryTracking=summary \
  -cp out com.baypay.labs.lab701.MemoryProbe
```

Default retain: 8 × 1 MiB → `retainedApproxBytes=8388608`.

### `GC.heap_info` excerpt

```
 garbage-first heap   total 133120K, used 18917K [0x0000000780000000, 0x0000000800000000)
  region size 1024K, 2 young (2048K), 0 survivors (0K)
 Metaspace       used 405K, committed 576K, reserved 1114112K
  class space    used 29K, committed 128K, reserved 1048576K
```

| View | Number (this run) |
|---|---|
| Heap used | **18917K** (~18.5 MiB) |
| Heap committed (`total`) | **133120K** (~130 MiB) |
| Young regions | 2 × 1024K, 0 survivors |
| Metaspace used / committed | 405K / 576K |

**Used vs committed (your words):** Used is occupancy — bytes of Java objects the collector still sees in the heap (here ~18.5 MiB). Committed is virtual memory HotSpot has already taken from the OS for G1 regions (`total 133120K`). Reserved address space for the heap is larger still (NMT Java Heap reserved 2 GiB default). Used ≤ committed ≤ reserved. “The heap looks fine” without used **and** committed is not a reading.

**MemoryProbe only — retainedApproxBytes vs heap used:** Retained payload is **8 MiB**. Heap used is **~18.5 MiB**. Same order of magnitude; they do not match byte-for-byte. The gap is object headers, the `ArrayList` + `byte[]` wrappers, TLAB slack, and everything else a quiet JDK 21 process allocated before I ran `jcmd`. Used ≫ a few hundred KiB, so the hold list is actually live.

**payment-service only — what is larger than the probe, and why that is expected:** Not captured this run (Boot process lacked NMT). Expected later: committed heap, Class/Thread/Code all larger because Spring + JPA + Tomcat load far more classes and threads than eight `byte[]` chunks.

GC logs and container math: **LAB-703 / LAB-704**. This page is heap + NMT only.

---

## NMT (LAB-701)

`jcmd 25946 VM.native_memory summary` — **committed** first (reserved is address space, not RSS).

| Category | Reserved | Committed | What you think this bucket is |
|---|---|---|---|
| Total | 3605834KB | **246378KB** (~241 MiB) | All NMT-tracked committed; still not identical to OS RSS (file mappings, etc.) |
| Java Heap | 2097152KB | **133120KB** | Matches `GC.heap_info` total. This is `-Xmx` land — not the process. |
| Class | 1048674KB | **226KB** | Class metadata bookkeeping (713 classes). Close cousin of metaspace; **not** `Payment` instances. |
| Thread | 37130KB | **37130KB** | **Stacks** for 18 threads (~37 MiB), not `java.lang.Thread` objects. |
| Code | 247751KB | **7639KB** | Code cache (interpreter / C1 / C2). Quiet probe, still ~7.6 MiB committed. |
| GC | 91181KB | **52845KB** | G1 card tables, marking, region structures. **~52 MiB** — larger than the 8 MiB live set. |
| Internal | 214KB | **214KB** | VM internal malloc (small here; still a real category). |
| Metaspace (extra) | 65548KB | **460KB** | Aligns with heap_info metaspace committed 576K (rounding / split vs Class). |
| Shared class space | 16384KB | **12944KB** | CDS / default class data archive — also not `-Xmx`. |

**Thread vs `java.lang.Thread` objects:** NMT **Thread** is native **stack** reservation/commit (here 37080KB stacks + a little malloc). `java.lang.Thread` instances are tiny Java objects on the **heap**. Eighteen stack mappings dwarf eighteen heap `Thread` objects. Do not read Thread committed as “how many Thread objects we leaked.”

**Class vs `Payment` instances:** NMT **Class** (and Metaspace) is **metadata** — the loaded `Payment` *class*, constant pool, method metadata. `Payment` *instances* (Avery’s authorizations) live on the **Java heap**. Histogram counts instances; NMT Class does not grow when you authorize more payments of the same class.

**Why Internal + GC + Code still matter when someone says “we set `-Xmx`”:** `-Xmx` caps the Java heap (here committed heap 130 MiB, used 18 MiB). This process still committed **~52 MiB GC + ~7.6 MiB Code + ~37 MiB stacks + metaspace/CDS**. Total NMT committed **~241 MiB** — almost **2×** the heap commit, **13×** used heap. Jordan’s next container conversation cannot treat `-Xmx` as the cgroup number. LAB-704: never set `-Xmx` equal to the container limit.

---

## Allocation comparison (LAB-702)

Same `N` pair used for the write-up: **1_000_000**, `-Xmx256m`. `N=250_000` / `-Xmx128m` was **ambiguous** (retain Δ 23.6 MiB vs die Δ 22.5 MiB) — coarse `Runtime` + TLAB + delayed GC. Raised `N` as the lab allows.

| Mode | N | elapsedMs | usedBefore | usedAfter | usedDelta | retainedSize |
|---|---|---|---|---|---|---|
| retain | 1_000_000 | 159 | 2110112 | 95829840 | **93719728** (~89.4 MiB) | **1000000** |
| die | 1_000_000 | 42 | 2110112 | 25304576 | **23194464** (~22.1 MiB) | **0** |

`dieSinkCents=5049010000` (die). Extra runs: retain 250k Δ 23553096 / retainedSize 250000; die 250k Δ 22504520 / retainedSize 0 / sink 1253125000; second die 250k elapsed 60 ms (not faster — do not call that escape analysis).

**Live set vs garbage:** **Retain** keeps every `PaymentLike` reachable from an `ArrayList`, so the live set is ~N records plus the backing array; used-heap delta grew with N (~23.6 MiB at 250k, ~89.4 MiB at 1M). **Die** drops the reference each iteration, so those records (and most of their payload) become young-gen garbage; Eden can be reused, and end-of-run used-heap stayed nearer the start (~22 MiB delta at 1M vs ~89 MiB retain). Die used-heap can even shrink if a young collection runs mid-loop — that is reuse, not a leak proof in reverse. `dieSinkCents` exists so the JIT cannot dead-code-eliminate the loop: we read `amountCents()` into a live long. A Payment-like **record is still a heap object** in the common case (interpreter and usually C1/C2); `record` is not “stack allocated.” A Money-like value still allocates when you “just add numbers”: production `Money` wraps `BigDecimal` (plus currency); this harness uses `long` cents but still allocates the record and the id `String`. Escape analysis **might** scalar-replace a non-escaping `PaymentLike` in die mode after C2; **it does not always**, and it does not delete the strings. `Runtime.totalMemory()-freeMemory()` is a coarse mode comparison, not a profiler and not NMT.

**What escape analysis might eliminate — and the sentence that it does not always:** EA might scalar-replace the `PaymentLike` wrapper in die (fields in registers) if the object does not escape. **It does not always.** Do not design BayPay money code around stack allocation.

**One allocation die mode still performs:** `"pay-" + i` — a new `String` (and concat machinery) every iteration. Die does not eliminate that.

---

## GC (LAB-703)

**Run 1 flags (G1 / file name):** `-Xmx64m -Xlog:gc*:file=logs/gc-g1.log:time,uptime,level,tags` + `GcVisibleHarness 400 256`. Using G1 (Java 21 default). 81 log lines.

**Run 2 flags (Serial and/or smaller `-Xmx` / file name):** `-Xmx32m -XX:+UseSerialGC` + same harness → `logs/gc-serial.log` (young only; dying 256 KiB chunks). Extra to get **Pause Full**: LAB-702 `retain 400000` + `-Xmx24m -XX:+UseSerialGC` → `logs/gc-serial-full.log` (then Java heap OOM — recorded, not a failed lab).

G1 official file showed **only young**. Serial + smaller heap on the dying harness still showed only young. Full appeared when the live set could not fit (retain + 24m).

### 3–5 annotated log lines

```
[2026-09-06T14:56:21.417-0700][0.088s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 23M->1M(64M) 5.793ms
```
Annotation: **G1, Pause Young** (Eden evacuation). Used **23M → 1M**, capacity **64M**. **5.793 ms STW** — mutator threads wait. Healthy shape for dying request-sized junk. Not “the heap is broken.”

```
[2026-09-06T14:56:21.425-0700][0.096s][info][gc] GC(1) Pause Young (Normal) (G1 Evacuation Pause) 36M->1M(64M) 3.168ms
```
Annotation: Second G1 young. **36M → 1M (64M)** in **3.168 ms**. Same story: live set is tiny (`liveMarker` 256 KiB); young GC reclaims almost everything.

```
[2026-09-06T14:56:21.576-0700][0.084s][info][gc] GC(0) Pause Young (Allocation Failure) 9M->1M(30M) 3.202ms
```
Annotation: **Serial**, young (`DefNew` / Allocation Failure). **9M → 1M (30M)** in **3.202 ms STW**. Smaller capacity (30M vs 64M) so young pauses show up sooner and more often. Still not a Full.

```
[2026-09-06T14:56:33.408-0700][0.146s][info][gc] GC(0) Pause Young (Allocation Failure) 7M->7M(23M) 14.353ms
```
Annotation: **Serial + retain** (live set). Young pause **7M → 7M (23M)** in **14.4 ms**. Almost no reclaim — objects are reachable. Young ≠ “heap is empty.”

```
[2026-09-06T14:56:33.484-0700][0.222s][info][gc] GC(3) Pause Full (Allocation Failure) 19M->19M(23M) 40.474ms
```
Annotation: **Serial Pause Full**. Whole-heap STW. **19M → 19M (23M)** in **40.5 ms** — about **7×** the G1 young pause. Used did not drop (live set). Later Fulls hit **23M→23M(23M) ~47–55 ms**, then `OutOfMemoryError: Java heap space`. Correct GC, then a true heap exhaust. Not a Module 8 leak RCA from one OOM.

**Why run 2 was easier to see:** Serial + `-Xmx32m` (then 24m) made Allocation Failure young lines frequent and put a **Pause Full** on disk once I retained. G1 at 64m on dying chunks only evacuated Eden. Serial is a **visibility** tool, not what `payment-service` / prod-east should run.

**What a pause means for a payment mutator thread:** The payment thread **waits** at a safepoint for the STW duration (here ~3–6 ms young, ~40–55 ms full). It is not proof the heap is corrupt. A 5 ms young pause can be healthy; a 50 ms full can still be “correct” GC when the live set fills the heap.

Would **not**: require JFR GUI for this lab; tune `-XX:MaxGCPauseMillis` without a latency SLO; paste a Module 8 canary RCA from these laptop files.

---

## Container (LAB-704)

**Cgroup / container memory max:** 512 MiB  

**Convention used (512 × 0.25 vs 1024-based bytes):** **1024-based** throughout: `1 MiB = 1024 × 1024` bytes. `512 MiB = 512 × 1,048,576 = 536,870,912` bytes. Host `java -XshowSettings:vm` said Max heap **2.00G** — that is **machine** RAM, not the 512 MiB answer.

| Percentage | Multiplication shown | Max heap |
|---|---|---|
| 25 (default) | `536,870,912 × 0.25 = 134,217,728` bytes = `512 × 0.25` | **128 MiB** |
| 75 | `536,870,912 × 0.75 = 402,653,184` bytes = `512 × 0.75` | **384 MiB** |

**Four or more non-heap consumers against the same 512 MiB:** (1) **thread stacks** (NMT Thread — LAB-701: 18 threads, **37 MiB** committed on a tiny probe; Boot Tomcat + Hikari is more); (2) **metaspace / class** (NMT Class + Metaspace + CDS); (3) **code cache** (NMT Code ~7.6 MiB even on MemoryProbe); (4) **GC / Internal** native (LAB-701 GC **~52 MiB**); (5) **NIO direct** buffers. All count toward cgroup RSS, none are `-Xmx`.

**Why `-Xmx512m` on a 512 MiB limit is wrong (include a sum):** Heap is already the whole box. Add LAB-701’s *floor* (no Spring): `512 + 37 (stacks) + 52 (GC) + 8 (code) + 13 (CDS) ≈ **622 MiB > 512**`. A Boot-shaped guess is worse: `512 + (80 threads × 1 MiB) + 150 (metaspace) + 50 (code/GC/direct) + 32 slack = **824 MiB > 512**`. The kernel then **SIGKILL / cgroup OOM**. Java often never writes `OutOfMemoryError: Java heap space` or a heap dump. Eden can still look free.

**Recommended flag set + native-headroom sentence:**

```text
-XX:+UseContainerSupport
-XX:MaxRAMPercentage=75.0
# equivalent explicit: -Xmx384m
# not -Xmx512m, not -Xms512m
# later, after measure: -XX:MaxMetaspaceSize=…  and watch thread count × -Xss
```

The remaining **~128 MiB (25%)** is **native headroom** — stacks, metaspace, code, GC, direct — not wasted RAM.

**Same rule on `Pay1` if memory-capped (one sentence; not a new ND cell):** Heap still ≠ the memory cap; I would not stand up a second traditional ND cell to “fix memory.”

**Docker extra (optional):** **used.** `docker run --rm -m 512m eclipse-temurin:21-jdk java -XX:MaxRAMPercentage=75.0 -XshowSettings:vm -version`

```
Max. Heap Size (Estimated): 371.25M
```

Paper 75% is **384 MiB**. Temurin 21.0.12 reported **371.25M** on a 512m cgroup — same neighborhood, not host 2.00G. Image / cgroup accounting differ slightly; I still refuse heap = 512.

---

## Interview snippet (Staff, 6–8 sentences)

Explain heap vs NMT vs GC pause vs container budget as one briefing Priya Nair could reuse. Mention that Module 7 is observation, not a Module 8 incident RCA.

`GC.heap_info` is occupancy versus committed heap (LAB-701: used 18.5 MiB, committed 130 MiB). NMT is categories: Java Heap is `-Xmx` land; Thread is stacks; Class is metadata; GC+Code+Internal are why RSS exceeds the heap (this laptop’s tiny probe already committed ~241 MiB NMT). A GC **pause** is STW wait for mutators (young ~3–6 ms here; Serial Full ~40–55 ms) — not “the heap is broken,” and one histogram is not a leak. The **512 MiB cgroup** is the whole-process budget: default `MaxRAMPercentage` 25 → **128 MiB** heap; 75 → **384 MiB**; `-Xmx512m` plus stacks/GC/code already sums **over 512** and the kernel kills. Module 7 is observe-and-explain, not a Module 8 container-OOM RCA. Same arithmetic on a memory-capped `Pay1`; still no new ND cell and no bounce of `dmgr-east`.
