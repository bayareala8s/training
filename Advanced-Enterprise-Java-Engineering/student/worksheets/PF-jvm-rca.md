# Portfolio artifact — JVM incident RCA

**Course:** Advanced Enterprise Java Engineering  
**Module:** 08 — JVM Troubleshooting  
**Artifact id:** PF-05  
**Sources:** pick **one** of INCIDENT-801 / INC-JVM-801 through INCIDENT-806 / INC-JVM-806  
**Case study:** BayPay Financial Services (fictional)

Export this file (or a copy) when you submit. Do not paste instructor solution text. All names and ids you cite must come from the synthetic pack you chose. Locked instructor RCAs live only under `solutions/`.

**Student:**  
**Date:**  
**Cohort / reviewer (if any):**  

**Incident chosen (circle one):**  
801 CPU 98 percent · 802 Memory leak · 803 Deadlock · 804 Thread-pool exhaustion · 805 Excessive GC · 806 Container OOM

**Pack path:** `incidents/jvm/INC-JVM-80N/`

---

## 1. Symptom

What merchants and the pager showed. Quote numbers from the **dashboard** (replica, time, SLO):

What `pay-prod-east-1` was doing at the same time:

---

## 2. Hypothesis timeline

Write in gate order. A lucky label that matches the lab title does not replace this table.

| Gate | File opened | Hypothesis after that file | Evidence that supported or killed it |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## 3. Root cause (your words)

Mechanism, instance, and version or flag. Quote stacks, classes, events, or flags. Do not import a different Module 8 pack’s story unless you say why you ruled it out:

What this is **not** (one sentence, with evidence):

---

## 4. Stabilize vs remediate

| Stabilize (restores capacity *now*) | Remediate (keeps the next canary safe) |
|---|---|
|  |  |

What you explicitly **did not** do (Postgres, `dmgr-east`, region failover, Tomcat 2000, and so on):

---

## 5. Evidence table

| Gate | File | One quote (timestamp + text) | What it proved |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Omitted evidence you wanted, and what you expected it to show:

---

## 6. Communication samples

### Internal bridge (five lines max)

What we know / do not know / next update:

### Merchant-safe note

No invented cause. No confidential-sounding runbook language:

---

## 7. Architecture / trade-off

One policy you would enforce next week, and the cost of that policy:

---

## 8. Interview talking points

Write four bullets you would actually say, labeled Engineer / Senior / Staff / Principal:

- Engineer:
- Senior:
- Staff:
- Principal:

---

## Honesty

- [ ] I did not open `solutions/INCIDENT-80N/` before attempting the worksheet
- [ ] I requested evidence in the documented gate order
- [ ] Every numeric claim has a source (dashboard, log, dump, histogram, events, or flags)
- [ ] I did not paste an instructor RCA
- [ ] If I had done INC-JVM-202 or INC-EE-402, I did not copy those thread or pool names unless they appear in **this** pack
