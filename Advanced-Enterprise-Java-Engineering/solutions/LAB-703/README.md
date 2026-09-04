# LAB-703 — Instructor solution

**Do not treat these log lines as a student’s evidence.** They are **synthetic**, Java 21 unified-logging style, for annotation practice and grading keys. Real student files will differ in timestamps, heap sizes, and GC ids.

Students must paste **their** 3–5 lines. This page teaches how to read them.

## Annotated example — G1, modest heap

Flags in the student lab: `-Xmx64m -Xlog:gc*:file=gc-g1.log:time,uptime,level,tags`.

```text
[2026-09-03T19:01:04.120-0700][0.184s][info][gc,start ] GC(0) Pause Young (Normal) (G1 Evacuation Pause)
[2026-09-03T19:01:04.125-0700][0.189s][info][gc       ] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 18M->6M(64M) 4.821ms
[2026-09-03T19:01:04.125-0700][0.189s][info][gc,cpu   ] GC(0) User=0.01s Sys=0.00s Real=0.01s
[2026-09-03T19:01:06.440-0700][2.504s][info][gc       ] GC(7) Pause Young (Normal) (G1 Evacuation Pause) 41M->12M(64M) 6.110ms
[2026-09-03T19:01:08.002-0700][4.066s][info][gc,start ] GC(8) Pause Young (Concurrent Start) (G1 Evacuation Pause)
```

| Fragment | Reading |
|---|---|
| `Pause Young` | Stop-the-world young / evacuation. Eden (+ some survivors) collected. |
| `G1 Evacuation Pause` | G1 copied live objects out of collection-set regions. |
| `18M->6M(64M)` | Used heap **before** 18 MiB → **after** 6 MiB; **capacity** 64 MiB (`-Xmx` here). |
| `4.821ms` | Pause duration (mutator threads waited ~that long). |
| `Real=0.01s` | Wall time of the pause (cpu tags). |
| `Concurrent Start` | Young pause that **kicks off** concurrent mark — still a young STW, not a Full GC. |

A student who calls every G1 line “no pause because G1 is concurrent” fails Technical.

## Annotated example — Serial, smaller heap

Flags: `-Xmx32m -XX:+UseSerialGC -Xlog:gc*:file=gc-serial.log:time,uptime,level,tags`.

```text
[2026-09-03T19:02:11.010-0700][0.210s][info][gc,start ] GC(0) Pause Young (Allocation Failure)
[2026-09-03T19:02:11.016-0700][0.216s][info][gc       ] GC(0) Pause Young (Allocation Failure) 15M->4M(32M) 5.102ms
[2026-09-03T19:02:14.880-0700][4.080s][info][gc,start ] GC(12) Pause Full (Allocation Failure)
[2026-09-03T19:02:14.923-0700][4.123s][info][gc       ] GC(12) Pause Full (Allocation Failure) 28M->8M(32M) 43.210ms
[2026-09-03T19:02:14.923-0700][4.123s][info][gc,cpu   ] GC(12) User=0.04s Sys=0.00s Real=0.04s
```

| Fragment | Reading |
|---|---|
| `Pause Young (Allocation Failure)` | Eden full; young collection. Serial young is STW. |
| `15M->4M(32M)` | Same triple: before → after → capacity. |
| `Pause Full` | Whole-heap collection (old + young). Longer pause. |
| `28M->8M(32M) 43.210ms` | Reclaimed a lot; ~43 ms mutator pause. |
| `Allocation Failure` | Trigger, not a Java `OutOfMemoryError` by itself. |

Young vs old/full is the required classification. Serial + 32m makes Full lines likely; G1 + 64m may stay young-only. A student who only saw young and **said** “I would shrink `-Xmx` or switch Serial to see Full” still meets the honesty bar in the student guide.

## What you are not grading

- JFR GUI screenshots (explicitly not required).
- Choosing Serial for prod-east `payment-service` (wrong Production awareness).
- Module 8 excessive-GC RCA structure.
- Matching the synthetic timestamps above.

## How to grade

- Two runs, real files, 3–5 lines annotated.
- At least one young line parsed (`before->after(capacity)` + ms).
- Pause explained as mutator STW, not “heap corruption.”
- Run 2 rationale (visibility), not a collector religion.

## Verify locally

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
OUT=/tmp/aeje-lab703
mkdir -p "$OUT" /tmp/aeje-lab703-logs
"$JAVA_HOME/bin/javac" --release 21 -d "$OUT" \
  labs/LAB-703/starter/GcVisibleHarness.java
"$JAVA_HOME/bin/java" -Xmx64m \
  -Xlog:gc*:file=/tmp/aeje-lab703-logs/gc-g1.log:time,uptime,level,tags \
  -cp "$OUT" com.baypay.labs.lab703.GcVisibleHarness 200 256
"$JAVA_HOME/bin/java" -Xmx32m -XX:+UseSerialGC \
  -Xlog:gc*:file=/tmp/aeje-lab703-logs/gc-serial.log:time,uptime,level,tags \
  -cp "$OUT" com.baypay.labs.lab703.GcVisibleHarness 200 256
wc -l /tmp/aeje-lab703-logs/gc-g1.log /tmp/aeje-lab703-logs/gc-serial.log
```
