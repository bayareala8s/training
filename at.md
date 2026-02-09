Below is the **same level of end-to-end detail** for the **S3 → S3** flow when **West is down**, written in an ARC-ready way.

I’ll cover:

* steady state
* what “West down” means for S3→S3
* how Route 53/DNS applies (API layer, not S3 itself)
* what happens to in-flight transfers
* what customers/partners experience
* timing vs RTO/RPO targets

---

# End-to-End Failover Workflow

## Scenario: **S3 → S3 transfer**, primary execution in **us-gov-west**, then **West goes down**

---

## 0️⃣ Pre-conditions (steady state)

### Data & control endpoints

* **Source bucket**: `source-bucket` (could be customer-owned or partner-owned)
* **Target bucket**: `target-bucket` (could be platform-owned or customer-owned)
* Buckets may be:

  * in the same region
  * cross-region
  * replicated (CRR) depending on design

### Service endpoints

* Customer calls a single API DNS name:

  * `eft.company.gov` (Route 53 routes to West/East API endpoints)

### Backend in both regions (Active-Active)

* Orchestration services running in **West** and **East**
* Job metadata and ownership in **DynamoDB Global Tables**
* Queues/events in each region (EventBridge/SQS)
* Execution workers (ECS/Lambda) in each region

---

## 1️⃣ Normal operation (before failure)

### Step-by-step (S3 → S3)

1. Customer submits a job:

   * “Copy from `source-bucket/prefix/...` to `target-bucket/prefix/...`”
2. API request goes to `eft.company.gov`
3. Route 53 returns **West** (healthy)
4. West orchestration:

   * validates request
   * writes job metadata to DynamoDB Global Tables
   * acquires execution ownership lease
   * schedules transfer execution
5. Execution worker starts:

   * reads object(s) from source bucket
   * writes to target bucket
   * uses multipart for large objects
6. Job status updates continuously

✅ Everything runs normally

---

## 2️⃣ Failure occurs: **us-gov-west goes down**

This affects:

* West API endpoint
* West orchestration services
* West execution workers

**But note:**
S3 itself is a regional managed service; the “West down” scenario here means **your service stack in West** is unavailable (or the region has a broader outage).

---

## 3️⃣ DNS & Route 53 response (for your API)

Even though S3 doesn’t use your Route 53, **your customers do** for the API.

1. Route 53 health checks fail for West API (`api-west`)
2. Route 53 marks West unhealthy
3. Route 53 stops returning West
4. New client requests resolve to East

⏱ Typical DNS convergence: **1–3 minutes**

---

## 4️⃣ Customer experience during failure

### If the customer is calling your API

* A request in progress may fail (timeout/5xx)
* Client retries the same API DNS name:

  * `eft.company.gov`
* Request is routed to East
* No client configuration change required

✅ Transparent failover at the API layer

---

## 5️⃣ Backend failover behavior (how jobs recover)

### 5.1 Ownership takeover (prevents duplicates)

1. West-held lease eventually expires (time-bound)
2. East acquires execution ownership
3. East begins/resumes job progression

This ensures:

* only one active executor per partition
* no duplicate object copies
* clean retry behavior

---

## 6️⃣ What happens to **in-flight S3→S3 copies**?

This depends on whether you’re copying:

* **single object**
* **multipart large object**
* **multiple objects in a batch**

### Case A — Small object copy completed before outage

* Object is already in target bucket
* Job can be marked succeeded when East takes over

✅ No impact, maybe minor status delay

---

### Case B — Large object copy was in progress (multipart)

When West fails mid-transfer:

* Multipart upload may be incomplete in the target bucket
* Incomplete multipart uploads are not visible as a completed object
* East re-executes the copy step

**Your worker logic should do:**

* Check if a valid completed object exists (size/etag/checksum)
* If not, restart multipart upload
* Optionally abort stale multipart uploads after a threshold

✅ No partial file exposure
✅ Safe retry
⏱ Possible delay

---

### Case C — Batch copy (many objects)

* Some objects may already be copied successfully
* East resumes and copies remaining objects
* Idempotency prevents re-copy issues

✅ Safe resume
✅ No duplicates (or duplicates overwritten deterministically if versioning rules allow)
⏱ Delay proportional to remaining work

---

## 7️⃣ RPO implications (S3→S3 case)

For S3→S3 transfers, RPO depends on **what data is considered critical**:

### Orchestration metadata (jobs/endpoints/leases)

* Stored in DynamoDB Global Tables
* **RPO: near-zero (target)**

### Object data in destination bucket

* If the destination is directly written in East or replicated:

  * the object exists once upload completes
* If your design uses S3 CRR for staging:

  * **RPO can be up to 15 minutes** for staged data replication

In most S3→S3 implementations, the destination object is the “truth” once written, so RPO is mainly about **job state**, not object state.

---

## 8️⃣ What customers/partners experience (plain English)

| Aspect            | Experience                                   |
| ----------------- | -------------------------------------------- |
| API calls         | Retry may be needed                          |
| Job execution     | Resumes in East after lease takeover         |
| Object integrity  | No partial objects exposed                   |
| Data loss         | No (objects either exist or re-copy happens) |
| Duplicate objects | Prevented via ownership + idempotency        |
| Delay             | Possible during failover                     |

---

## 9️⃣ Timing summary (end-to-end)

| Step                        | Typical Time            |
| --------------------------- | ----------------------- |
| DNS failover for API        | ~1–3 minutes            |
| Lease expiration + takeover | ~10 minutes             |
| Re-execution / resume       | depends on object sizes |
| **Target recovery (RTO)**   | **15 minutes (target)** |

---

## 🔟 ARC-ready summary (memorize this)

> *For S3-to-S3 transfers, Route 53 fails over the API traffic from West to East within minutes. Job metadata is replicated across regions, and East takes over execution after lease expiration. Any in-progress multipart copies are safely retried without exposing partial objects. The outcome is correctness-first recovery: no data loss, no duplicates, and only a short delay during regional failover.*

---

## If ARC asks: “Do customers need to change anything?”

Answer:

> *No. Clients continue using the same API DNS name. Only retries may be required depending on when the outage occurs.*

---

## If you want, I can tailor this to your exact model

Two quick variants exist for S3→S3:

1. **Direct copy** (worker reads source and writes target)
2. **Stage then copy** (source → staging bucket → target)

Tell me which one you’re using and I’ll tighten the wording to match precisely.
