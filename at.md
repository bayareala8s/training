This is actually a **very solid and rigorous exercise by your ARC team**, and it’s good news for you — it means they’re treating this as a **quantitative resiliency review**, not a hand-wavy one.

What you need to do now is **frame their math correctly**, explain **why Active-Active changes the equation**, and show **why 99.9% is still the right SLA commitment**, even if the *theoretical* availability could be higher.

Below is a **clear, Principal-level explanation** you can use in the document *and* in the meeting.

---

# How SLA Is Calculated Across AWS Services and Regions

### (Series vs Parallel, and Why Active-Active Matters)

---

## 1. How ARC Approached the Calculation (Acknowledge First)

Start by validating their approach:

> *The ARC team evaluated availability by looking at the SLA of each AWS managed service in the stack and calculating overall availability using series and parallel reliability models across us-gov-west and us-gov-east.*

This shows respect and alignment.

---

## 2. Series vs Parallel – The Key Concept

### Series Model (Single Region)

In a **single-region architecture**, services are effectively in **series**:

```
API Gateway → Lambda → Step Functions → DynamoDB → ECS → S3
```

Mathematically:

> **Total Availability = A₁ × A₂ × A₃ × … × Aₙ**

So even if each service has very high availability, the **product is always lower**.

Example (simplified):

| Service        | SLA    |
| -------------- | ------ |
| API Gateway    | 99.95% |
| Lambda         | 99.95% |
| Step Functions | 99.9%  |
| DynamoDB       | 99.99% |
| ECS            | 99.9%  |

**Single-region effective availability (illustrative):**

```
0.9995 × 0.9995 × 0.999 × 0.9999 × 0.999 ≈ 99.3–99.5%
```

This is why **single-region stacks struggle to meet higher SLAs**.

---

## 3. What Changes with Active-Active (Critical Explanation)

In your design, **us-gov-west and us-gov-east are both active**.

That changes the model from **series-only** to **parallel at the regional level**.

### Parallel Model (Regions)

If:

* Region West availability = Aw
* Region East availability = Ae

Then **system availability** becomes:

> **A = 1 − (1 − Aw) × (1 − Ae)**

This is standard reliability engineering.

---

## 4. Why Active-Active Dramatically Improves Availability

### Example (Illustrative)

Assume:

* Effective regional availability (after series math) ≈ **99.5%**

Then:

```
A = 1 − (0.005 × 0.005)
  = 1 − 0.000025
  = 99.9975%
```

So **mathematically**, Active-Active can yield availability **higher than 99.9%**.

---

## 5. Why We Still Commit to SLA = 99.9% (Very Important)

This is where you **sound like a Principal Architect**, not a marketer.

### Key Point

> **SLA is a contractual and operational commitment, not a mathematical maximum.**

We intentionally **do not over-commit** to the theoretical number.

---

### Reasons (ARC-Grade)

#### 1. External Dependencies Are Excluded

* External partner SFTP systems
* External networks
* Partner throttling or outages

Even if AWS is up, partners may not be.

---

#### 2. Asynchronous Workload Semantics

* File transfers are not real-time
* Availability ≠ instantaneous delivery
* Delays are acceptable; data loss is not

---

#### 3. Correlated Failures Exist

The math assumes **independence**, but in reality:

* Control plane dependencies
* Human errors
* Configuration issues
* Upstream API misuse

These reduce *practical* availability.

---

#### 4. SLA Must Align with Business MTD

* Monthly downtime budget at 99.9% ≈ **43 minutes**
* MTD = **30 minutes**
* RTO = **15 minutes**

This alignment is intentional and defensible.

---

## 6. How to Explain This to ARC (Say This Verbatim)

> *“The math shows that Active-Active across us-gov-west and us-gov-east materially improves availability by placing regions in parallel rather than series. While the theoretical availability exceeds 99.9%, we intentionally commit to a 99.9% SLA to account for external partner dependencies, correlated failures, and asynchronous delivery semantics. This ensures our SLA is achievable, auditable, and aligned with business tolerance.”*

Then pause.

---

## 7. How This Ties Back to RTO, RPO, MTD

| Metric | Value                         | Why It Fits             |
| ------ | ----------------------------- | ----------------------- |
| SLA    | 99.9%                         | Conservative, auditable |
| RTO    | ≤ 15 min                      | Automated Active-Active |
| RPO    | 0 (metadata), ≤15 min (files) | DynamoDB + S3 CRR       |
| MTD    | 30 min                        | Business tolerance      |

✔ SLA supports MTD
✔ RTO < MTD
✔ RPO ≤ RTO

---

## 8. One-Line Close (If ARC Pushes Further)

> *“We designed for higher availability than we commit to, which is exactly how enterprise SLAs should be set.”*

That line lands very well with **Risk and Audit**.

---

## What I can do next

If you want, I can:

* Rewrite this into a **formal appendix section**
* Add a **small math callout box** to your resiliency section
* Help you respond if ARC asks **“why not advertise higher SLA?”**
* Prep a **Risk Committee version** of this explanation

Just tell me who the next audience is.





Perfect — here’s a **clean, ARC-ready “Math Callout Box”** you can drop directly into your **Resiliency & Reliability section**.
It’s intentionally **compact, precise, and audit-safe**.

---

### 📐 **Availability Calculation – Active-Active Regions (Callout Box)**

> **Availability Modeling Approach**
>
> Overall service availability is derived using standard reliability engineering principles.
>
> Within a single AWS region, managed services (API Gateway, Lambda, Step Functions, DynamoDB, ECS, S3) are treated as **series dependencies**, where effective regional availability is the product of individual service SLAs.
>
> Because the Self-Serve File Transfer Services are deployed in **Active-Active mode** across **us-gov-west-1** and **us-gov-east-1**, the two regions operate in **parallel** from an availability perspective.
>
> **Parallel Availability Formula:**
>
> [
> A_{system} = 1 - (1 - A_{west}) \times (1 - A_{east})
> ]
>
> Where:
>
> * (A_{west}) = effective availability of the us-gov-west-1 regional stack
> * (A_{east}) = effective availability of the us-gov-east-1 regional stack
>
> This parallel deployment materially increases overall availability compared to a single-region design.
>
> While the theoretical availability exceeds **99.9%**, the service intentionally commits to a **99.9% SLA** to account for external partner dependencies, correlated failures, and asynchronous file-transfer semantics, ensuring the SLA remains achievable, auditable, and aligned with business tolerance.

---

### Why ARC likes this box

* ✅ Shows you **understand the math**
* ✅ Explicitly calls out **series vs parallel**
* ✅ Explains **why SLA < theoretical max**
* ✅ Avoids over-committing
* ✅ Reads cleanly for **Risk & Audit**

---

### If you want it even tighter (1–2 lines shorter)

I can compress this further for a **slide footer** or **executive summary**.

### If you want to go deeper

I can also add:

* A **numeric example** (with rounded SLAs)
* A **footnote** referencing AWS SLA docs
* A **Risk Committee–specific version**

Just tell me where this box is going (doc section, slide, appendix).





Here’s a **concrete, numeric example** you can paste into the doc (or use verbally) to show exactly how ARC’s **series + parallel** math works for **Active-Active us-gov-west + us-gov-east**.

---

## Concrete Example: SLA Math (Series within Region, Parallel across Regions)

### Step 1 — Pick rounded per-service SLAs (illustrative)

Assume the regional stack relies on these AWS services for the “happy path”:

| Service (per region) | Rounded SLA (Aᵢ) |
| -------------------- | ---------------: |
| API Gateway          |  99.95% = 0.9995 |
| Lambda               |  99.95% = 0.9995 |
| Step Functions       |  99.90% = 0.9990 |
| DynamoDB             |  99.99% = 0.9999 |
| SQS                  |  99.90% = 0.9990 |
| EventBridge          |  99.90% = 0.9990 |
| S3                   |  99.90% = 0.9990 |
| ECS/Fargate          |  99.90% = 0.9990 |

> Note: These are **rounded** numbers for demonstration. Your ARC team can substitute the exact SLAs they collected.

---

### Step 2 — Compute **effective availability of one region** (series model)

When services are required in sequence, regional availability is:

[
A_{region} = \prod A_i
]

Now multiply:

* 0.9995 × 0.9995 = **0.99900025**
* × 0.9990 = **0.99800124975**
* × 0.9999 = **0.997901449625025**
* × 0.9990 = **0.9969035481753999**
* × 0.9990 = **0.9959066446272245**
* × 0.9990 = **0.9949107379825973**
* × 0.9990 = **0.9939158272446147**

So:

[
A_{west} \approx 0.9939 = 99.39%
]

Assume East is similar:

[
A_{east} \approx 0.9939
]

---

### Step 3 — Compute **system availability** (parallel regions)

Because both regions are active, overall availability is:

[
A_{system} = 1 - (1 - A_{west})(1 - A_{east})
]

Plug in:

* (1 − 0.9939158) = **0.0060842**
* 0.0060842 × 0.0060842 = **0.0000370**
* 1 − 0.0000370 = **0.9999630**

So:

[
A_{system} \approx 0.999963 = 99.9963%
]

---

## What this proves (the message to ARC)

* **Single region** (series dependencies) can end up around **~99.4%** in this simplified example.
* **Active-Active two regions** (parallel) boosts overall availability to **~99.996%** *theoretically*.

---

## Why we still commit to **99.9% SLA** (tie-back you can say)

Even if the theoretical number is higher, we commit to **99.9%** because:

* independence assumptions don’t fully hold (correlated failures, ops/config errors)
* partner SFTP and external network dependencies are excluded
* file transfer is asynchronous; we prioritize correctness + auditability over marketing a higher SLA

---

### Optional mini-line to add under the example (Audit-safe)

> *This calculation illustrates why Active-Active materially improves availability. Actual committed SLA remains 99.9% to ensure the commitment is achievable and auditable under real-world conditions.*

If you want, paste me the exact per-service SLAs your ARC team used and I’ll run the **exact same math** with those numbers and give you the final availability result for West, East, and combined.
