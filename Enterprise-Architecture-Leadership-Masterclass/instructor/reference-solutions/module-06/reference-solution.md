# Reference Solution — Module 06 (Instructor Only)

**Do not distribute to students.**  
**Lab:** Build NorthStar’s Integration Reference Architecture  
**Case study:** NorthStar Financial Services (fictional)

Companion detail files in this folder:

| File | Contents |
| ---- | -------- |
| `reference-pattern-matrix.md` | Scored interface matrix |
| `reference-adrs.md` | ADR-M06-01 / ADR-M06-02 |
| `lab-walkthrough.md` | Happy-path commands |

---

## 1. Decision framing (expected student quality)

NorthStar needs concurrent interaction styles: low-latency account APIs, buffered payment processing, partner bulk exchange, and scheduled regulatory/analytics workflows. A single ESB-for-everything decision fails multi-criteria selection and concentrates blast radius.

---

## 2. Pattern matrix (summary)

| Interface | Primary | Secondary | Key criteria |
| --------- | ------- | --------- | ------------ |
| Account lookup/create | Sync API | Event on create | User latency; consistency |
| Payment submitted | Event → queue + DLQ | Status API read | Buffering; retries; poison isolation |
| Partner files | File landing (S3 sim) | Event on arrival | Partner ecosystem; bulk |
| Regulatory / analytics batch | Step Functions workflow | Manual ops | Ordered stages; notify |

Full scoring: `reference-pattern-matrix.md`.

---

## 3. Ownership model

| Concern | Owner |
| ------- | ----- |
| Account aggregate meaning | Accounts / Customer domain |
| Payment event semantics & schema | Payments LOB |
| Partner file contract (format/SLA) | Partner channel product + EA |
| Event bus, API GW, DLQ ops patterns | Shared integration platform |
| Customer golden record | Master-data capability (not partner files) |

---

## 4. Data-flow expectations

Payments path: producer → EventBridge → SQS (+ DLQ) → payment worker → side effects / notify.  
Partner path: file arrive (S3 `incoming/`) → partner Lambda → domain event → optional analytics stage.  
Students should show authoritative systems of record separately from exchange formats.

Diagram reference: `modules/module-06-integration-data/diagrams/`.

---

## 5. ADR expectations

**ADR-M06-01 — Sync vs events for account create side effects**  
Decision: sync write for create/lookup; emit `AccountCreated` asynchronously for fan-out. Consequences: consumers must tolerate eventual consistency; no dual-write to shared DB.

**ADR-M06-02 — Transfer Family / MFT vs S3 landing**  
Decision (lab): S3 landing simulation. Production: Transfer/MFT when partner protocol, compliance, or managed connectivity justify idle cost. Lab must not deploy Transfer Family.

See `reference-adrs.md`.

---

## 6. Lab evidence checklist (instructor grading)

- [ ] Terraform outputs captured (API URL, bus name, bucket, state machine ARN)
- [ ] Account API POST/GET evidence
- [ ] Payment event path evidence
- [ ] Partner file S3 evidence
- [ ] Step Functions execution evidence (or documented blocker + architecture narrative)
- [ ] SNS subscription confirmed
- [ ] Cleanup confirmation (`cleanup-lab06.sh` or destroy log)
- [ ] Cost note (~<$5 if cleaned promptly)

Happy path: `lab-walkthrough.md`.

---

## 7. Exemplar executive one-liner

> NorthStar’s integration reference architecture separates sync customer journeys from buffered payment events and partner file landing, with domain-owned event semantics, platform-owned mechanisms, and explicit cost control on managed file transfer.
