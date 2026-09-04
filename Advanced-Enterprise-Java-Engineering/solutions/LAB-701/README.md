# LAB-701 — Instructor solution

**Do not share this file with students before they capture their own `jcmd` output.**

Numbers below are **ranges**. Laptop JDK builds, compressed oops, and Path A vs Path B move the decimals. Grade the **reading**, not a matching megabyte.

## How to read `GC.heap_info`

Typical G1 (Java 21) shape:

```text
garbage-first heap   total 65536K, used 18432K [...]
  region size 1024K, 12 young (12288K), 2 survivors (2048K)
 Metaspace       used 12000K, committed 13000K, reserved ...
  class space    used 1500K, committed 1664K, reserved ...
```

| Token | Meaning |
|---|---|
| `total` / committed heap | Memory reserved for Java objects now (can grow toward `-Xmx`) |
| `used` | Live-ish occupancy + waste in regions; not RSS |
| young / survivors | Eden + survivor regions; not “the leak” |
| Metaspace used/committed | Class metadata, not `new Payment()` |

Serial / Parallel wording differs (`def new generation`, `tenured`); the used vs committed lesson is the same.

## Expected ranges — MemoryProbe (Path A)

Default: 8 × 1 MiB retained, NMT summary on, JDK 21, no Spring.

| Signal | Typical range (order of magnitude) | Fail if |
|---|---|---|
| Heap used | **8–40 MiB** (8000K–40000K) | Used stays ~1–2 MiB as if allocate never ran |
| Heap committed / total | **16–128 MiB** on default ergonomics | Student treats reserved 8g+ as “we use 8 GB” |
| Metaspace used | **4–20 MiB** | Student calls metaspace “the Payment list” |
| Young regions | Non-zero on G1 | — |

Used will exceed 8 MiB: object headers, `ArrayList` backing store, TLABs, leftover compiler / setup allocations. Same **order of magnitude** as `retainedApproxBytes` is the pass bar.

## Expected ranges — payment-service (Path B)

Idle Boot + JPA, NMT on, no load script required.

| Signal | Typical range | Notes |
|---|---|---|
| Heap used | **40–250 MiB** | Framework, Hibernate, caches |
| Heap committed | **64–512 MiB** | Ergonomics; not a leak by itself |
| Metaspace / NMT Class committed | **30–80 MiB** common | Spring + JDK classes |
| NMT Thread committed | **20–80 MiB** | Many more threads than MemoryProbe |

A Path B heap used **below** ~20 MiB usually means the student attached to the wrong pid (Maven wrapper, not the forked JVM).

## How to read NMT (`VM.native_memory summary`)

NMT reports **reserved** vs **committed** per category. Grade **committed** first.

| Category | What it is | What it is not |
|---|---|---|
| Java Heap | The `-Xmx` / ergonomic heap | Process RSS |
| Class | Metaspace + class space (metadata, bytecodes) | Instances of `Payment` |
| Thread | Per-thread **stacks** (and related) | `java.lang.Thread` Java objects (those are heap) |
| Code | JIT code cache | Source files |
| GC | Collector structures (card table, regions, mark bitmaps) | “GC paused so this is waste” |
| Internal | VM internal native (symbols, handles, miscellaneous) | “Bug if non-zero” |
| Total | Sum of tracked committed | Still not a perfect RSS match (shared mappings, malloc outside NMT) |

Teaching sentences students should be able to reproduce:

1. Heap used/committed answers “Java objects.”
2. Thread committed answers “stacks × threads.”
3. Class committed answers “metadata / metaspace.”
4. Internal + GC + Code are why `-Xmx` is not the process or cgroup size (LAB-704).

## Enablement

`-XX:NativeMemoryTracking=summary` at **start**. `UnlockDiagnosticVMOptions` matches RUNTIME.md. `jcmd` from the same JDK 21 (`/opt/homebrew/opt/openjdk@21`).

## How to grade

- Technical: real excerpts, six NMT categories, used vs committed distinguished.
- Diagnostic: pid + flags recorded; NMT-disabled error handled by restart, not ignored.
- Production: BayPay / `payment-service` or honest Path A; same rules on `Pay1`; no AWS.
- Do not require JFR, heap dumps, or Module 8 RCA language.
- A student who only pastes Java Heap and says “looks fine” fails Diagnostic and Technical.

## Verify locally

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd labs/LAB-701
mkdir -p /tmp/aeje-lab701
"$JAVA_HOME/bin/javac" --release 21 -d /tmp/aeje-lab701 starter/MemoryProbe.java
# Manual: start with NMT, jcmd GC.heap_info and VM.native_memory summary, Ctrl+C
```
