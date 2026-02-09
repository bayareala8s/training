Great question — this is **exactly** the kind of explanation ARC expects when you state an SLA of **99.9%** and propose **Active-Active** in **us-gov-west & us-gov-east**.

Below is a **clear, defensible, numbers-driven explanation** you can **paste into the document** and also **walk through verbally**.
I’ll explicitly tie **SLA → MTD → RTO → RPO**, show **calculations**, and explain **how Active-Active achieves them**.

---

# Resiliency Targets Explained (SLA → MTD → RTO → RPO)

## 1. Starting Point: SLA = 99.9%

### What 99.9% SLA Means (Mathematically)

99.9% availability allows **0.1% downtime**.

| Time Window | Allowed Downtime at 99.9% |
| ----------- | ------------------------- |
| Per year    | **8 hours 45 minutes**    |
| Per month   | **~43 minutes**           |
| Per week    | **~10 minutes**           |
| Per day     | **~1.4 minutes**          |

> **ARC framing:** SLA defines *how much downtime is acceptable*, not *how recovery happens*.
> RTO, RPO, and MTD must be **well below** these limits.

---

## 2. Maximum Tolerable Downtime (MTD)

### Definition

**MTD** = Maximum time the business can tolerate the service being unavailable **before material business impact**.

### Chosen MTD (Business-Aligned)

| Business Function         | MTD            |
| ------------------------- | -------------- |
| File ingestion / delivery | **30 minutes** |
| Status & visibility       | **15 minutes** |
| New onboarding            | **4 hours**    |

### Why MTD = 30 minutes (Key Point)

* File transfers are **asynchronous**
* A short delay is acceptable
* **Data loss or duplication is not acceptable**
* 30 minutes is **below the monthly SLA budget (43 minutes)**

> **ARC rule:**
> **MTD ≥ RTO** and **MTD < SLA downtime window**
> ✔ Both conditions are met.

---

## 3. Recovery Time Objective (RTO)

### Definition

**RTO** = Time required to restore service after a failure.

### Chosen RTO Targets

| Failure Scenario       | RTO              |
| ---------------------- | ---------------- |
| Single service failure | **< 1 minute**   |
| AZ failure             | **< 5 minutes**  |
| Full regional outage   | **≤ 15 minutes** |

### Why RTO ≤ 15 Minutes (Critical Explanation)

RTO is **not** driven by:

* Server rebuilds
* Manual failover
* Standby promotion

RTO **is driven by lease expiration and automated takeover**.

### RTO Calculation (Region Failure)

| Step                     | Time         |
| ------------------------ | ------------ |
| Failure detection        | ~1–2 min     |
| Lease expiry window      | ~10 min      |
| Re-acquisition & restart | ~2–3 min     |
| **Total RTO**            | **≤ 15 min** |

> **Key ARC statement:**
> *RTO is deterministic and automated, not operator-dependent.*

### Why RTO Fits SLA & MTD

* **RTO (15 min) < MTD (30 min)**
* **Multiple RTO events still stay within SLA budget**
* No cascading downtime

---

## 4. Recovery Point Objective (RPO)

### Definition

**RPO** = Maximum acceptable data loss measured in time.

### Chosen RPO

| Data Type              | RPO           |
| ---------------------- | ------------- |
| Job metadata           | **0**         |
| Endpoint configuration | **0**         |
| Execution ownership    | **0**         |
| File data staged in S3 | **0**         |
| In-flight transfers    | **Near-zero** |

### Why RPO = 0 (Explanation)

* All state stored in **DynamoDB Global Tables**
* All file data stored in **S3 with cross-region replication**
* No critical state held in memory
* Transfers can retry safely

> **ARC framing:**
> *We prefer short delays over any data loss.*

---

## 5. How Active-Active Achieves These Numbers

### Why Active-Active (Not Active-Passive)

| Aspect       | Active-Passive  | Active-Active (Chosen) |
| ------------ | --------------- | ---------------------- |
| Standby cost | High            | Optimized              |
| Failover     | Manual / slower | **Automatic**          |
| RTO          | Higher          | **Lower**              |
| SLA risk     | Higher          | **Lower**              |

---

### Active-Active Execution Model (Plain English)

* Both regions are **live**
* Each transfer job has **one execution owner**
* Ownership enforced using **time-bound leases**
* If a region fails:

  * Lease expires
  * Other region takes over
  * No duplicate execution

---

## 6. SLA ↔ RTO ↔ MTD Alignment (ARC Loves This Table)

| Metric                  | Value    | Relationship        |
| ----------------------- | -------- | ------------------- |
| SLA                     | 99.9%    | Business commitment |
| Monthly downtime budget | ~43 min  | SLA-derived         |
| MTD                     | 30 min   | Business tolerance  |
| RTO                     | ≤ 15 min | Technical recovery  |
| RPO                     | 0        | Data guarantee      |

> **Key takeaway:**
> **RTO < MTD < SLA downtime window** ✔

---

## 7. Impact to Partners (Explicit & Honest)

### What Partners Experience

| Scenario          | Partner Impact |
| ----------------- | -------------- |
| Component failure | None           |
| AZ failure        | Possible delay |
| Region failure    | Short delay    |
| Data loss         | **Never**      |
| Duplicate files   | **Never**      |

### One-Line Partner Guarantee (Use Verbatim)

> *In the worst case, partners experience a short delay in file delivery; files are never lost, duplicated, or partially delivered.*

---

## 8. ARC-Ready Closing Statement (Use Verbatim)

> *With a 99.9% SLA, we selected MTD, RTO, and RPO values that are comfortably within our allowed downtime budget. The Active-Active deployment across us-gov-west and us-gov-east provides automated, deterministic recovery, ensuring business continuity while preserving data integrity.*

---

## 9. If ARC Asks “Why Not 99.99%?”

Say this calmly:

> *99.9% aligns with business needs for asynchronous file transfers. Achieving 99.99% would materially increase cost and complexity without reducing business risk, since data integrity—not real-time availability—is the primary concern.*

---

## What I can do next (high value)

If you want, I can:

* Turn this into a **single ARC slide**
* Map this to your **exact internal resiliency policy wording**
* Help you rehearse a **2-minute spoken explanation**
* Prep answers for **Risk / Audit challenge questions**

Just tell me how the next review is structured.
