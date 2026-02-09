Below is a **complete, end-to-end, ARC-ready workflow** that explains **exactly what happens when a customer connects to the SFTP server in us-gov-west and that region goes down**.
This is written so you can **paste it into the document** *and* **walk it verbally in ARC**.

---

# End-to-End Failover Workflow

### Scenario: Customer connects to SFTP (us-gov-west) → West goes down

---

## 0️⃣ Pre-conditions (steady state)

* **Two AWS Transfer Family (SFTP) servers**

  * `sftp-west.company.gov` → us-gov-west
  * `sftp-east.company.gov` → us-gov-east
* **Route 53 DNS**

  * `sftp.company.gov` points to **both** endpoints
  * Health checks enabled
  * Low TTL (e.g., 60s)
* **Backend services**

  * Active-Active orchestration in both regions
  * DynamoDB Global Tables for metadata & leases
  * S3 with CRR for staged files

---

## 1️⃣ Normal operation (before failure)

1. Customer resolves:

   ```
   sftp.company.gov
   ```
2. Route 53 returns **us-gov-west** (healthy)
3. Customer establishes SFTP session with **Transfer Family – West**
4. File upload or download proceeds normally
5. Backend services track:

   * Job metadata
   * Transfer state
   * Ownership/lease

👉 Everything is operating normally.

---

## 2️⃣ Failure occurs: us-gov-west goes down

This could be:

* Regional outage
* Transfer Family endpoint unavailable
* Network isolation

### Immediate impact

* Existing SFTP sessions to West **drop**
* New connection attempts to West **fail**

This is expected and unavoidable.

---

## 3️⃣ DNS & Route 53 response (control shift)

1. Route 53 health checks fail for:

   ```
   sftp-west.company.gov
   ```
2. Route 53 marks **West UNHEALTHY**
3. Route 53 **stops returning West** in DNS responses
4. DNS cache TTL begins expiring across clients

⏱ Typical DNS convergence: **1–3 minutes**

---

## 4️⃣ Customer reconnects (this is key)

### What the customer does

* Customer retries connection
* Uses **same hostname**:

  ```
  sftp.company.gov
  ```

### What DNS now returns

* Route 53 returns:

  ```
  sftp-east.company.gov
  ```

### Result

* Customer establishes a **new SFTP session to East**
* No hostname or configuration change required by customer

👉 Failover is **transparent at the DNS layer**.

---

## 5️⃣ Backend orchestration during the outage

While DNS is shifting traffic:

1. **DynamoDB Global Tables**

   * Metadata remains available in both regions
   * Lease ownership from West eventually expires
2. **Lease expiration**

   * Prevents split-brain execution
3. **East region acquires ownership**

   * Becomes execution authority
4. **Transfer jobs resume or retry**

   * Based on last known safe state

⏱ Lease-driven takeover contributes to overall **RTO = 15 minutes (target)**

---

## 6️⃣ What happens to the file being transferred?

### Case A — File already fully uploaded before failure

* File exists in S3 (West)
* CRR replicates to East (≤ 15 minutes)
* Backend resumes downstream processing

✅ No data loss
⏱ Possible delay

---

### Case B — File partially uploaded when West failed

* Partial file is **discarded**
* Customer reconnects to East
* Customer re-uploads file

✅ No partial file exposure
✅ No corruption
⏱ Re-upload required (expected SFTP behavior)

---

## 7️⃣ What the customer experiences (plain English)

| Aspect             | Customer Experience |
| ------------------ | ------------------- |
| Connection         | Session drops       |
| Reconnect          | Works after retry   |
| Hostname change    | ❌ None              |
| Credentials change | ❌ None              |
| Data loss          | ❌ No                |
| Duplicate files    | ❌ No                |
| Delay              | ✅ Possible          |

You can say this verbatim in ARC:

> *During a regional failure, customers experience a dropped SFTP session and need to reconnect. Once DNS converges, they reconnect to the East region using the same hostname, with no configuration changes.*

---

## 8️⃣ Why this design is correct (ARC framing)

* **SFTP is stateful** → session loss is expected on failure
* **DNS is the correct failover mechanism** for SFTP
* **Active-Active backend** ensures:

  * No duplicate processing
  * No data corruption
  * Deterministic recovery
* **Correctness prioritized over speed**

---

## 9️⃣ Timing summary (end-to-end)

| Step                            | Time       |
| ------------------------------- | ---------- |
| Failure detection               | ~1–2 min   |
| DNS convergence                 | ~1–3 min   |
| Lease expiration & takeover     | ~10 min    |
| **Total recovery target (RTO)** | **15 min** |

---

## 🔟 ARC-ready summary (memorize this)

> *When us-gov-west fails, existing SFTP sessions drop. Route 53 health checks remove West from DNS, and customers reconnect using the same hostname to us-gov-east. Backend services recover automatically using Active-Active orchestration and lease-based ownership, ensuring no data loss or duplication, with a target RTO of 15 minutes.*

Pause after saying that.

---

## If ARC asks: *“Can we make this seamless without reconnect?”*

Answer calmly:

> *No — SFTP sessions are stateful. Session reconnection is expected and documented behavior during regional failures.*

That answer is **100% correct**.

---

If you want next, I can:

* Turn this into a **one-page ARC appendix**
* Add a **sequence diagram with SFTP + DNS**
* Help you explain **why Global Accelerator is not appropriate for SFTP**
* Prep a **partner-facing explanation**

Just tell me where this will be used (doc / slide / spoken).
