# Portfolio artifact — Concurrency RCA

**Course:** Advanced Enterprise Java Engineering  
**Module:** 2 — Advanced Java Concurrency  
**Artifact id:** PF-02  
**Sources:** BREAKFIX-201 / INC-JVM-201 and INCIDENT-202 / INC-JVM-202  
**Case study:** BayPay Financial Services (fictional)

Export this file (or a copy) when you submit. Do not paste instructor solution text. All names and ids you cite must come from the synthetic packs.

**Student:**  
**Date:**

---

## 1. BREAKFIX-201 — Duplicate payment

### Symptom

What the merchant and the harness showed (numbers from your runs):

### Hypothesis timeline

| Time | Hypothesis | Evidence that supported or killed it |
|---|---|---|
|  |  |  |

### Root cause (your words)

What compound actions were unsafe, and on which structures:

### Repair

What you changed and how you validated Case A and Case B (three runs):

### Stabilize vs remediate

| Stabilize | Remediate |
|---|---|
|  |  |

### Production follow-up

How the JPA unique `Idempotency-Key` path in `reference-apps/baypay` would have contained this:

---

## 2. INCIDENT-202 — Workers not completing

### Symptom

Dashboard facts (completions, CPU, health, queue):

### Hypothesis v1 (before the dump)

### Hypothesis v2 (after the dump)

Dump quotes (threads, monitors, call sites):

### Root cause (your words)

### Stabilize vs remediate

| Stabilize | Remediate |
|---|---|
|  |  |

### Lock or concurrency policy you would enforce

One sentence a reviewer can check:

---

## 3. Communication samples

### Internal bridge (INC-JVM-201 or 202 — pick one)

What we know / do not know / next update:

### Merchant-safe note

No invented cause. No confidential-sounding runbook language:

---

## 4. ARCHITECT-203 — prevention paragraph

How your design would have prevented both incidents (5–8 sentences). Link to `labs/ARCHITECT-203/work/DESIGN.md` if you wrote one:

---

## 5. Interview talking points

Write four bullets you would actually say, labeled Engineer / Senior / Staff / Principal:

- Engineer:
- Senior:
- Staff:
- Principal:

---

## Honesty

- [ ] I did not open `solutions/` before attempting both labs
- [ ] I requested INC-JVM-201 and INC-JVM-202 evidence in the documented order
- [ ] Every numeric claim has a source (harness, dashboard, or log line)
