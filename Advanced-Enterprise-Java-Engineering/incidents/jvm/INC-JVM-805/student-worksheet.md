# INC-JVM-805 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Long GC pauses on canary  
**Instance:** `pay-prod-east-2` (canary) vs `pay-prod-east-1`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: SEV-2 is **`pay-prod-east-2` only** after Jordan set `logging.level.com.baypay=DEBUG` (14:50). Allocation **1.8 GB/s** (was 44 MB/s), young interval **0.11 s**, pause p99 **420 ms** / max **640 ms**. **Old gen flat ~228 MB** — not INC-802’s climb. Log **4200 lines/s**. east-1 INFO, 38 MB/s, pause 16 ms, Avery 201. Hikari/DB fine. First guess: **allocation storm** from DEBUG on the hot path, not “G1 is broken,” not a leak. Next: `gc.log` — young vs full, used→used. Then histogram — **churned `String`/`char[]`** vs retained `IdempotencyRecord`. Do not set DEBUG on east-1. Do not switch collectors in the window.

Gate 2: GC log is **young evacuation**, not a broken collector. Before DEBUG: `22M->18M(1536M) 14ms`. After: `520M->34M(1536M) 398ms`, then `512M->40M 510ms`, `488M->35M **640ms**`. Heap after: used 980M, **old 228M**. Remark 18 ms. **No Full GC**, no humongous storm. G1 is reclaiming Eden of short-lived junk; mutators wait 400–640 ms. Not “G1 is broken.” Next: histogram — if `#instances` of `String`/`[C`/`[B` are huge and `IdempotencyRecord`/`Payment` are small, that is **churn**, not 802 retain.

Gate 3: Histogram is **churn**, not retain. After a young GC: **`[C` 1.84M / 147 MB**, **`String` 920k**, `Object[]` 410k. `Payment` 2.4k, `IdempotencyRecord` **1.1k** (not 1.1M). Second histogram 20s later: `[C]`/`String` within **8%** after another young GC — turning over, not climbing old gen. `LoggingEvent` only 640 live (buffers flush; the tax is allocation). Mechanism: global `com.baypay=DEBUG` on the create path allocates gigabytes of log strings per second; G1 young-pauses 400–640 ms. Not a leak, not a collector swap.

## Supporting evidence

| File | Quote |
|---|---|
| timeline 21:50 | Jordan: `logging.level.com.baypay=DEBUG` on **east-2 only** to trace Avery `c805d555-…` |
| timeline 22:10 | Priya: log volume ~40/s → **thousands/s** |
| dashboard 15:33 | alloc **1.8 GB/s**, pause p99 **420 ms**, young **0.11 s**, old gen **228 MB flat** |
| dashboard | east-1 INFO, 38 MB/s, pause 16 ms; Avery 201 without stall |
| gc.log 21:48 | Young `22M->18M(1536M) **14ms**` (before overlay) |
| gc.log 22:33 | Young `488M->35M(1536M) **640ms**`; heap used 980M **old 228M**; no Full |
| histogram | `[C]` 1.84M; `String` 920k; `IdempotencyRecord` 1108 |

No thread dump in this pack. Local `-Xlog:gc*` is the same dialect as this excerpt.

## Next investigation

Heap histogram: are top classes **ephemeral** (`String`, `[C`, `[B`, log builders) or a **retained** domain type (`IdempotencyRecord`)? Instance counts vs old-gen flat will tell churn vs leak. Thread dump omitted (not a hang). App `logs.txt` omitted — timeline + 4200 lines/s is enough for the config change. Local literacy: `-Xlog:gc*` on `reference-apps/baypay` is the same unified format as this excerpt.

## Stabilization action

**Revert `logging.level.com.baypay` to INFO on east-2** (the overlay that changed at 14:50). Keep east-1 INFO. Do not drain unless pause stays high after the revert (creates still complete; merchants feel stalls). 

Do **not**: set DEBUG on east-1; switch collectors; tune `-XX:MaxGCPauseMillis` (allocation is what changed); bounce Postgres / `dmgr-east`; announce a leak.

## Remediation

- **Structured fields** on the hot path, not a whole `Payment` / graph dump at DEBUG.
- **Rate-limit DEBUG per logger**, not a global `com.baypay` level.
- Trace Avery with **correlation-id sampling**, not DEBUG-all.
- Refuse to log request bodies / PII at INFO on `/payments` (801 already burned a core on body scan).
- `MaxGCPauseMillis` is a weak remediation if the next on-call can flip DEBUG again.

## Communication update

SEV-2 is **`pay-prod-east-2` only**. Creates still complete (Avery `c805d555-…` is not duplicated); merchants feel ~0.4–0.6 s stalls. east-1 pause p99 is 16 ms. Old generation is flat — this is not the two-day cache climb. We are turning **DEBUG off** on east-2 and leaving east-1 at INFO. We are not changing the collector or the database. Next update when east-2 allocation is back near 40 MB/s and pause p99 is back under 20 ms.
