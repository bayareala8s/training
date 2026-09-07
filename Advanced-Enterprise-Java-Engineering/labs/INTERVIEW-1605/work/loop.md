# INTERVIEW-1605 full mock loop

**Sitting start (UTC):** 2026-09-07T19:10:38Z  
**Plan:** 25 min slot 1 · 25 min slot 2 rapid-fire · 20 min design slice · break 0  
**Sitting end (UTC):** 2026-09-07T19:12:00Z (same calendar day / one block; slot files are the artifact — wall clock was compressed)  
**Payment:** Avery Chen / `c1605e55-0000-4000-8000-111111111605`  
**No reveal on slot 1 until both drafts exist. No portal. No Bedrock. No apply.**  
**`solutions/INTERVIEW-1605/` not opened before timestamps.**

---

## Schedule

| Slot | Mode | Clock | What |
|---|---|---|---|
| 1 | Practice / timed | **IQ-093 timed ~8 min** | `AEJE-IQ-087` + `AEJE-IQ-093` · Engineer + Staff |
| 2 | Rapid fire | 60–90s × 10 | `--count 10 --seed 17` |
| 3 | Design slice | ~8 min spoken / 20 min write | 99.99% create (1604 page + addendum) |

---

## Slot 1 — practice / timed (no reveal first)

### AEJE-IQ-087  [Production Engineering]  Engineer + Staff

**Question:** RED P99 far above 400 ms; USE CPU idle. Page vs ticket?

**Engineer:** P99 on `POST /api/v1/payments` is the merchant tail — Harbor Market feels Avery `c1605e55-…1605` as stuck even if CPU is quiet. I read **Hikari pending**, servlet busy/max, heap, and **scrape duration** before I care about CPU. I page on **SLO burn** and saturation that predicts it (pending, thread pool maxed). I ticket CPU > 80% and scrape gaps.

**Staff:** CPU idle + high P99 is a **split**, not a contradiction: the JVM can wait on a pool, a scrape, or a hop while the core sits. Primary page is never “CPU > 80%.” Who owns: Priya spends the 99.9% create budget; Riley checks pending/threads. I will not bounce `dmgr-east` or Postgres from a quiet CPU tile.

**Follow-up (Staff):** USE rows more likely than CPU: **Hikari pending**, Tomcat busy, heap. CPU > 80% is the wrong primary page even on a hot afternoon — it is a ticket unless it coincides with burn.

### AEJE-IQ-093  [HA/Security]  Engineer + Staff  · **timed: yes · ~8 min**

**Question:** Design 99.99% for `POST /api/v1/payments`. Domains, paper multi-AZ `us-west-2`, what is not the extra nine.

**Engineer:** Domains: task, AZ, ALB, identity/TLS, datastore, region. This quarter: two Fargate tasks in two AZs, multi-AZ ALB, paper multi-AZ Postgres, HTTPS `payments.apps.baypay.example`, health **8080**. I do not apply RDS/NAT/EKS. Leftover `PaymentCluster` is not the extra nine.

**Staff:** Single-region multi-AZ **is** allowed to be the 99.99% *design* (~52 min/year). Region loss is **DR**, not a free nine. Module 13 dashboard stays **99.9%** while I present this — architecture goal ≠ operated SLO. “Just add `us-east-1`” is the wrong only answer. I will not upgrade the tile in this sitting.

**Follow-up (Staff):** Multi-AZ is complete for four nines *in-region*. The Grafana tile stays 99.9% unless Priya + Finance sign ~4 min/month.

---

## Slot 2 — rapid fire `--count 10 --seed 17`

| # | Id | ~s | Score | Landing (4–8 sentences compressed) |
|---|---|---|---|---|
| 1 | AEJE-IQ-067 | 75 | ok | Logs ≠ traces. Need `paymentId` / `Idempotency-Key` / `traceparent` — not PAN. Metric alarm is not a refund line. PMI on `PaymentCluster` is the wrong estate. |
| 2 | AEJE-IQ-054 | 70 | ok | Golden: probes, heap-vs-limit, secrets, non-root. Team chart only with expiry. Refuse forever-fork of readiness. |
| 3 | AEJE-IQ-039 | 80 | thin | Feature set is surface area, not “enable all.” Teaching four first; JMS/WS is a new plane. Same idea as Boot starters. |
| 4 | AEJE-IQ-047 | 70 | ok | Writable `/tmp` (scratch). Refuse writable `/`, fat JAR, `--privileged`. |
| 5 | AEJE-IQ-038 | 80 | ok | STARTED ≠ synced. Symptom class: mixed members / same key 409 vs 5xx. Roll back **one** member. No instructor RCA. Refuse cluster-wide stop. |
| 6 | AEJE-IQ-023 | 90 | ok | Caught exception inside `@Transactional` can commit the 200 and skip ledger. Fix: fail the tx / don’t swallow. `this.refund()` skips proxy. Checked vs unchecked rollback. No heroic double-write. |
| 7 | AEJE-IQ-099 | 75 | ok | ADR **no** on promo-service in front of authorize. Alternative: module + flag. Reopen on evidenced SLO/team. Write the ADR so it is not a hallway veto. |
| 8 | AEJE-IQ-091 | 75 | ok | First screen: rate, 5xx, P99, burn, Hikari pending — not CPU. `paymentId` in **logs**, not labels. Avery off graphs. |
| 9 | AEJE-IQ-070 | 70 | ok | Student lab: no NAT/EKS/RDS/always-on GPU. Prod: no unused ALB, no second CP as tourism. ND is not spare capacity. Tag destroy owner. |
| 10 | AEJE-IQ-085 | 80 | ok | `ss` + dump together. ESTABLISHED + BLOCKED ≠ down. Hikari waiters in both. No `dmgr-east` bounce. |

---

## Slot 3 — design slice (8-minute spoken)

**Prompt:** 99.99% create (already on PF-design.md). This sitting: say the decision, three trade-offs, one refusal. Payment `c1605e55-…1605`.

Spoken: Multi-AZ single-region `us-west-2` is four nines this quarter. Region is DR. Tile stays 99.9%. No apply. No `PaymentCluster`. Extract is not this slice.

What I cut vs full 1604: six-row table detail, mermaid walkthrough, ECS vs EKS paragraph length.

---

## Mode-switch note

Leaving practice I dropped Principal essays and kept mechanism + owner. In rapid fire I refused to whiteboard IQ-099 / IQ-093 — “ADR no / take it to the design slice.” The design slice stayed **one decision** (multi-AZ single-region), not five JVMs and not a second-region apply.

---

## Reveal (after slots 1–3)

Slot-1 ids only, after drafts. Gaps: IQ-087 bank may want dependency latency named more explicitly; IQ-093 may want KMS grant as a domain sentence. Did not rewrite history. Did not paste bank text as spoken.

---

## Comms close

Priya / Riley / Jordan / Sam: Phase A loop finished in one block — two-voice practice with an 8-minute item, ten short landings (`--seed 17`), and a 99.99% create slice on PF-design. Portal and Bedrock were not required. Avery’s `POST /api/v1/payments` (`c1605e55-…1605`) stayed the spine. We did not apply `us-west-2`, bounce `dmgr-east`, or disable TLS. Bank stayed 100. Lucky hallway RCA was not the troubleshoot slot (we picked rapid fire).
