# ARB Proposal Pack — Retail Payments Fast-Path Modernization

> **Fiction notice:** NorthStar Financial Services and all named people, systems, vendors, and costs in this pack are fictional and created for BayLearn instruction.

**Proposal ID:** NS-ARB-2026-091  
**Proposing unit:** Retail Payments Business Unit  
**Sponsor:** Priya Nandakumar, President, Retail Payments  
**Solution architect (proposer):** Marcus Chen  
**Requested disposition date:** Before Monday delivery kickoff  
**Funding already committed (BU):** $2.4M Year-1 (licenses + contractors)

---

## 1. Executive summary (as submitted by the BU)

Retail Payments will modernize the merchant onboarding and settlement experience in two quarters by adopting a **second public cloud** (CloudNova), a **proprietary high-performance database** (VectorForge DB), a **custom integration framework** (PayWireFX) built by our contractors, and **direct production access** for named contractor engineers to accelerate incident response during hypercare.

We request Architecture Review Board **approval** so we do not miss the Q4 merchant NPS commitment.

---

## 2. Business drivers

| Driver | BU claim |
| ------ | -------- |
| Merchant onboarding cycle time | Reduce from 12 days to 3 days |
| Settlement exception handling | Cut manual touches 40% |
| Competitive pressure | Two peers launched “instant merchant” features |
| Delivery date | Soft launch in 16 weeks; hard commitment to board in 22 weeks |
| Talent | Contractors already skilled on CloudNova + VectorForge |

Strategic themes cited: customer experience, speed to market. Cost reduction is **not** claimed in Year-1.

---

## 3. Current-state touchpoints (BU narrative)

- Merchant onboarding workflow spans 7 applications (mix of on-prem and primary cloud)
- Settlement files exchanged with partners via two legacy file platforms
- Customer/merchant identifiers duplicated across Payments and Core Banking domains
- Existing enterprise API gateway and event backbone are “too slow to adopt” per BU (no measured evidence attached)

---

## 4. Proposed architecture (divergent choices)

### 4.1 Second cloud provider — CloudNova

| Item | Proposal detail |
| ---- | --------------- |
| Choice | Run new merchant services exclusively on CloudNova |
| Rationale given | Contractors know it; “feature velocity”; marketing credits offered |
| Identity | Separate CloudNova IdP; sync from corporate IdP “later” |
| Networking | Site-to-site VPN to on-prem; peering to primary cloud “phase 2” |
| Logging/SIEM | CloudNova native logs retained 30 days; forward to enterprise SIEM “if required” |
| DR | Single CloudNova region at launch; second region “next year” |
| FinOps | BU-owned account; tagging “best effort” |

### 4.2 Proprietary database — VectorForge DB

| Item | Proposal detail |
| ---- | --------------- |
| Choice | VectorForge DB as system of record for merchant profile and fee schedules |
| Rationale given | Vendor benchmark shows 3× throughput vs. managed PostgreSQL on primary cloud |
| Licensing | 3-year enterprise agreement; early termination fees apply after year 1 |
| Encryption | Vendor-managed keys by default; customer-managed keys “roadmap” |
| Backup/PITR | Daily snapshots; point-in-time recovery is premium SKU (not purchased) |
| Exit | Export tools available; schema is proprietary extensions-heavy |
| Data classification | Includes merchant KYC attributes and beneficial ownership (sensitive) |

### 4.3 Custom integration framework — PayWireFX

| Item | Proposal detail |
| ---- | --------------- |
| Choice | Contractor-built framework for API orchestration, retries, and partner file mapping |
| Rationale given | Enterprise integration platform “won’t meet timelines”; team control |
| Language | Go + custom DSL for mappings |
| Ownership | Contractors (Acme Digital Partners); two NorthStar FTEs to “shadow” |
| Observability | Custom metrics; not yet on enterprise OpenTelemetry standard |
| Reuse | BU hopes other payment teams will adopt later |
| Alternatives dismissed | Enterprise API gateway + event backbone; iPaaS; partner-specific adapters |

### 4.4 Direct production access for contractors

| Item | Proposal detail |
| ---- | --------------- |
| Choice | Standing Kubernetes/cluster-admin equivalent access for 8 contractor engineers |
| Rationale given | Hypercare speed; “break-glass always slows us down” |
| Duration | 9 months from kickoff |
| MFA | SMS-based MFA |
| Session recording | Not planned |
| Just-in-time access | Rejected as “overhead” |
| Change tickets | Optional for “minor” production fixes |

---

## 5. Cost snapshot (BU-provided; unaudited)

| Category | Year-1 | Notes |
| -------- | -----: | ----- |
| CloudNova consumption | $420k | Credits offset $80k |
| VectorForge licenses | $610k | Includes premium support |
| PayWireFX build (contractors) | $900k | Fixed capacity team |
| Integration & data migration | $320k | |
| Training / dual-running | $150k | |
| **Total called out** | **$2.4M** | Excludes primary-cloud opportunity cost and parallel ops |

**Not included:** enterprise security tooling duplication, second SIEM pipeline, additional DR testing, platform team support tax, exit costs from VectorForge.

---

## 6. Risks acknowledged by proposer (partial)

- New operational skill requirements for CloudNova
- Temporary divergence from enterprise standards
- Vendor concentration for VectorForge

**Risks not acknowledged:** identity split-brain, audit evidence gaps, irreversible data platform lock-in, shadow integration standard, privileged contractor access, precedent for other BUs.

---

## 7. Attachments claimed (not all provided)

| Attachment | Status in pack |
| ---------- | -------------- |
| Architecture diagrams (L1) | Provided — see Appendix A narrative |
| Threat model | “In progress” |
| DR test plan | Not provided |
| Data retention & residency mapping | One paragraph |
| Comparison vs. enterprise golden path | Slide with three bullets |
| Security questionnaire | Incomplete |

---

## Appendix A — Diagram narrative (proposer)

Internet → CloudNova edge → PayWireFX services → VectorForge DB  

Async partner files enter via PayWireFX SFTP module → mapping DSL → VectorForge  

Callbacks to core banking via VPN using stored credentials in PayWireFX config repo (encrypted at rest with shared team key).

---

## Appendix B — Decision requests (explicit)

1. Approve CloudNova as production hosting for Retail Payments merchant domain.  
2. Approve VectorForge DB as system of record for merchant profile/fees.  
3. Approve PayWireFX as the integration standard for this domain (and intended reuse).  
4. Approve standing production administrative access for named contractors for 9 months.  

---

## Appendix C — Stakeholder pressure notes (facilitator context; students may use)

- BU President: “We already signed VectorForge; ARB should not unwind commercial commitments.”
- CISO proxy: “I have not signed off on contractor prod admin.”
- Platform lead (primary cloud): “We can onboard a new landing-zone namespace in 3 weeks if scope is controlled.”
- Data office: “Merchant KYC in a proprietary store conflicts with golden-record program.”

---

## Instructor note

Students must treat this pack as **advocacy**, not truth. Measured evidence is thin by design. Healthy ARB outcomes typically **reject or heavily condition** all four requests while offering an alternate path that can still hit a revised date.
