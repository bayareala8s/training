# Portfolio — JVM memory and GC observation notes

**Course:** Advanced Enterprise Java Engineering  
**Module:** 07 — JVM Internals and Performance  
**Labs:** LAB-701 · LAB-702 · LAB-703 · LAB-704  
**Case study:** BayPay Financial Services (fictional)

Export this page (or a copy) as your Module 7 portfolio artifact. Use **your** `jcmd` output, harness stdout, GC log lines, and arithmetic. Do not paste instructor synthetic logs or range tables as if they were your run.

**Your name:**  
**Date:**  
**JAVA_HOME used:** `/opt/homebrew/opt/openjdk@21` or other:  
**Path chosen in LAB-701:** MemoryProbe / payment-service / both:

---

## Heap (LAB-701)

**Process pid:**  
**Start command (include NMT flags):**  

### `GC.heap_info` excerpt

Paste 6–15 lines or a table of total / used / young / metaspace:

```
(paste here)
```

**Used vs committed (your words):**  

**MemoryProbe only — retainedApproxBytes vs heap used:**  

**payment-service only — what is larger than the probe, and why that is expected:**  

---

## NMT (LAB-701)

`jcmd <pid> VM.native_memory summary` — record **committed** (and reserved if you want) for:

| Category | Reserved | Committed | What you think this bucket is |
|---|---|---|---|
| Total |  |  | |
| Java Heap |  |  | |
| Class |  |  | |
| Thread |  |  | |
| Code |  |  | |
| GC |  |  | |
| Internal |  |  | |
| (optional extra) |  |  | |

**Thread vs `java.lang.Thread` objects:**  

**Class vs `Payment` instances:**  

**Why Internal + GC + Code still matter when someone says “we set `-Xmx`”:**  

---

## Allocation comparison (LAB-702)

| Mode | N | elapsedMs | usedBefore | usedAfter | usedDelta | retainedSize |
|---|---|---|---|---|---|---|
| retain |  |  |  |  |  |  |
| die |  |  |  |  |  |  |

**Live set vs garbage (6–10 sentences allowed in notes; a paragraph is enough here):**  

**What escape analysis might eliminate — and the sentence that it does not always:**  

**One allocation die mode still performs:**  

---

## GC (LAB-703)

**Run 1 flags (G1 / file name):**  
**Run 2 flags (Serial and/or smaller `-Xmx` / file name):**  

### 3–5 annotated log lines

```
(paste line)
```
Annotation (young vs full/old, before→after→capacity, pause):  

```
(paste line)
```
Annotation:  

```
(paste line)
```
Annotation:  

```
(optional)
```

**Why run 2 was easier to see:**  

**What a pause means for a payment mutator thread:**  

---

## Container (LAB-704)

**Cgroup / container memory max:** 512 MiB  

**Convention used (512 × 0.25 vs 1024-based bytes):**  

| Percentage | Multiplication shown | Max heap |
|---|---|---|
| 25 (default) |  |  |
| 75 |  |  |

**Four or more non-heap consumers against the same 512 MiB:**  

**Why `-Xmx512m` on a 512 MiB limit is wrong (include a sum):**  

**Recommended flag set + native-headroom sentence:**  

**Same rule on `Pay1` if memory-capped (one sentence; not a new ND cell):**  

**Docker extra (optional):** used / not used. If used, paste `Max. heap size`:  

---

## Interview snippet (Staff, 6–8 sentences)

Explain heap vs NMT vs GC pause vs container budget as one briefing Priya Nair could reuse. Mention that Module 7 is observation, not a Module 8 incident RCA.
