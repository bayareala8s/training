# LAB-704 — Instructor solution

**Do not replace the student’s multiplication with this page until they have attempted it.**

Primary path is paper. Docker is extra. No Kubernetes. No AWS.

## Arithmetic (512 MiB cgroup)

Treat 1 MiB = 1024 × 1024 bytes unless the student consistently uses 512 × percentage in MiB. Both are acceptable if consistent.

```text
limit        = 512 MiB
             = 512 × 1024 × 1024
             = 536 870 912 bytes

default heap = MaxRAMPercentage 25
             = 0.25 × 512 MiB
             = 128 MiB
             = 134 217 728 bytes

explicit 75% = 0.75 × 512 MiB
             = 384 MiB
             = 402 653 184 bytes

headroom @75%= 512 − 384
             = 128 MiB   (native + slack, not “unused waste”)
```

Java 21 default `MaxRAMPercentage` is **25**. `UseContainerSupport` is on by default; the cgroup max is the RAM basis inside a container. Host `-XshowSettings:vm` on a developer Mac is **not** this calculation.

## Why `-Xmx512m` on a 512 MiB container is wrong

`-Xmx` caps the **Java heap** only. Resident set also includes:

| Consumer | Teaching estimate on a small payment JVM |
|---|---|
| Thread stacks | `threadCount × stackSize` (often 1 MiB/thread on many platforms) — 40 threads ≈ 40 MiB |
| Metaspace / class | 30–80 MiB for Spring + JDK is common (LAB-701 Path B) |
| Code cache | tens of MiB after JIT |
| GC structures | scales with heap; not free at 512m heap |
| Internal + NIO direct | unbounded if someone uses huge direct buffers |

A minimum honest sum:

```text
512 MiB heap
+  40 MiB stacks (example)
+  40 MiB metaspace (example)
+  20 MiB code/GC/internal slack
= 612 MiB  >  512 MiB cgroup
```

The kernel cgroup OOM killer SIGKILLs the process. You often get **no** `java.lang.OutOfMemoryError: Java heap space` and no heap dump. That is the operational punchline.

Do not recommend `-Xmx` equal to the container limit. RUNTIME.md already states this.

## Recommended flag set (lab / teaching)

For a **512 MiB** limit on a teaching replica:

```text
-XX:MaxRAMPercentage=75
```

Equivalent explicit heap (clearer on some ops wikis):

```text
-Xmx384m
```

Plus an explicit **native headroom** story (write it even if you do not set every flag):

```text
# ~128 MiB remains for:
#   thread stacks, metaspace, code cache, GC bitmaps, VM internal, direct buffers
# Optional later caps (not required to pass):
#   -XX:MaxMetaspaceSize=96m
#   -XX:ReservedCodeCacheSize=48m
#   (know your thread count before shrinking -Xss)
```

75% is a **similar** choice, not a BayPay prod mandate. A direct-buffer-heavy or very high-thread process should use a **lower** percentage (50, even the default 25) so native stays inside 512 MiB.

Refuse:

- `-Xmx512m` / `-Xmx` = cgroup max  
- “Liberty or WAS uses no native, so heap can be 512”  
- A new traditional ND cell as a memory strategy  

Same JVM rules apply on `Pay1` if that process is memory-capped.

## Optional Docker

```bash
docker run --rm -m 512m eclipse-temurin:21-jdk \
  java -XX:MaxRAMPercentage=75.0 -XshowSettings:vm -version
```

Expect Max heap near **384 MiB** (ergonomic rounding may show ~384m or a nearby value). Absence of Docker is **not** a fail.

A run with `-Xmx512m` inside `-m 512m` may live until native grows — it is still the wrong spec. Do not require students to OOM-kill a container.

## How to grade

- 128 MiB and 384 MiB (or byte-accurate equivalents) with multiplication shown.
- Explicit rejection of heap = 512 MiB limit.
- Flag set includes 75% or ~384m **and** native headroom.
- Docker optional.
- No Module 8 container-OOM incident write-up required.

## Verify locally (paper + optional host VM settings)

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
"$JAVA_HOME/bin/java" -XshowSettings:vm -version
# Confirm students did not copy the host Max heap as the 512 MiB answer.
```
