# L-2.1 visuals — Threads and the Java Memory Model

Three teaching pictures for [L-2.1](../../../course/modules/02-advanced-java-concurrency/lessons/L-2.1.md). BayPay is fictional.

| # | File | What to see |
|---|---|---|
| 1 | [threads-stack-heap.svg](threads-stack-heap.svg) | Each thread has a private stack. `Payment` lives on the shared heap. |
| 2 | [stale-authorized.svg](stale-authorized.svg) | Shared heap is not a shared view. Course catalog twin: [AEJE-D-005](../AEJE-D-005.svg). |
| 3 | [happens-before-edges.svg](happens-before-edges.svg) | `volatile`, `synchronized` unlock/lock, and `Lock.unlock`/`lock`. |

Open the SVG (or the mermaid in `*.source.md`). PNG is a raster sibling for slides.

Read left to right: **who owns the stack → why the worker can miss the write → which API creates the edge.**
