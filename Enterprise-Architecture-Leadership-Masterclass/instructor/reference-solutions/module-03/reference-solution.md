# Reference Solution — Module 03 (Instructor Only)

**Do not distribute to students.**  
**Case study / dataset:** NorthStar Financial Services (fictional)  
**Purpose:** Analysis guidance and grading calibration—not a single correct TIME sheet.

---

## 1. How to use the CSV (critical)

The `Recommended disposition` column is a **seed**. Excellent student work:

- Challenges ≥3 seeds with dimension-based rationale
- Ties conclusions to Module 02 capabilities and ExCo themes
- Uses dependencies to constrain Eliminate/Migrate timing
- Avoids rewriting the entire estate in Year 1

---

## 2. Sample TIME scoring insights (illustrative)

### Portfolio patterns worth teaching

| Pattern | Apps (IDs) | Insight |
| ------- | ---------- | ------- |
| Duplicate partner gateways | NS-APP-017, NS-APP-018 | Strong Eliminate/consolidate candidates after successor path; high combined cost (~$1.09M) and security surface |
| Dual customer masters + hub | NS-APP-011, NS-APP-012, NS-APP-010 | Structural acquisition debt; Customer360 (010) often **Invest** as target despite Fair health; 011/012 **Migrate/Eliminate** only with data capability uplift |
| Integration hubs | NS-APP-021 (ESB), NS-APP-020 (API), NS-APP-023 (Event) | ESB **Migrate** (not instant Eliminate); API/Event **Invest** as landing path; 62 integrations = wave planning mandatory |
| Fraud tooling overlap | NS-APP-005, NS-APP-006 | Batch FraudSentinel **Eliminate/Migrate**; FraudGuard **Invest** as realtime path—require explicit target fraud capability |
| Channel modernization | NS-APP-013 Invest; NS-APP-014 Eliminate; NS-APP-043 Eliminate | Mobile good; classic web EOL; shadow SaaS is governance/security debt |
| Commodity tolerate | NS-APP-044 Workday, NS-APP-045 SAP | Good health / non-differentiating—**Tolerate**; do not consume transformation oxygen |
| Core banking reality | NS-APP-001 | Mission critical + poor health → **Migrate** multi-year; Eliminate is fantasy without coexistence |
| Failed MDM | NS-APP-033 | Seed Eliminate is reasonable; pair with Invest in lakehouse/Customer360 data capability—not another blind MDM buy |

### Example overturn (teach live)

**Seed:** KYC Partner Hub (NS-APP-009) = Migrate.  
**Overturn candidate:** Keep near-term **Invest** in controls/integration quality if Partner Integration value stream is Year-1 CX critical—then Migrate once API partner onboarding matures.  
**Point:** Strategic fit and value-stream timing can outweigh “Fair” health alone.

### Example confirm (teach live)

**Seed:** Partner File Gateway A/B = Eliminate.  
**Confirm** with cost + security + duplication—but add constraint: Eliminate only after Partner Portal/API path handles top partner volume (dependency sequencing).

### Suggested TIME distribution for a scoped “strategic slice” (~20 apps)

Approximate healthy narrative: Invest ~30–40%, Migrate ~25–35%, Eliminate ~15–25%, Tolerate ~15–25%. Exact counts less important than coherent story.

---

## 3. Sample top-10 risks (analysis guidance)

Students’ lists will vary; score on impact clarity, evidence, and TIME-aligned response—not identical ranking.

| Rank | Risk | Evidence cues | Business impact | Response theme |
| ---: | ---- | ------------- | --------------- | -------------- |
| 1 | Fragmented customer identity/master data | Apps 010/011/012; onboarding defects | KYC errors, CX cycle time, regulatory exposure | Invest Customer360 + identity; migrate LOB masters |
| 2 | Dual partner file gateways | 017/018 cost, security, integrations | OpEx waste; incident/security surface | Consolidate; Eliminate one path with wave plan |
| 3 | ESB concentration risk | 021 integrations=62, poor health | Systemic outage/change risk | Migrate to API/Event backbone in waves |
| 4 | Core banking fragility + skills | 001 poor health, COBOL stack | Prolonged operational & change risk | Long Migrate program; Invest containment |
| 5 | Channel EOL / classic web | 014 EOL 2026 | Customer access & security risk | Eliminate with mobile/web target path |
| 6 | Shadow SaaS confidential data | 043 poor health, high security | Data leakage; compliance failure | Eliminate / bring under IAM & DP controls |
| 7 | Identity inconsistency (workforce vs customer) | 024–026 patterns | Access gaps; audit findings | Invest enterprise identity capability |
| 8 | Fraud tooling ambiguity | 005 EOL vs 006 invest | Fraud loss / ops confusion | Clarify target; Eliminate batch legacy |
| 9 | Failed MDM + warehouse aging | 033, 031 | Blocks analytics & golden record | Eliminate 033; Migrate EDW toward lakehouse |
| 10 | Incident visibility split | 039 vs 040 | Longer MTTR; weak resilience narrative | Eliminate legacy NOC; Invest observability |

**Residual risk teaching point:** Even after ranking, coexistence means temporary dual-run cost and control debt—call it out.

---

## 4. Excellent vs developing submissions

| Excellent | Developing |
| --------- | ---------- |
| Scoped slice + explicit decision | Scores all rows shallowly |
| ≥3 disposition challenges | Copies CSV seeds |
| Hubs + duplicate clusters | No dependency notes |
| Top-10 with business impact | CVE/tech laundry list |
| Module 02 theme linkage | Isolated inventory work |
| Feasible sequencing | Big-bang retire dates |

---

## 5. Numeric anchors (for office hours)

Approximate fictional spend signals instructors can cite:

- Core banking + card processor alone > $6M annual run cost
- Dual gateways ~ $1.1M combined
- ESB ~ $0.87M with highest integration count in sample

Use as prioritization intuition—not precision accounting.
