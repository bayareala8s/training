# INTERVIEW-1601 practice notes

**Date:** 2026-09-07  
**Path:** files only — `python3 interview-bank/simulator.py --mode practice --id …` **without** `--reveal` first.  
**Demo:** Avery Chen `11111111-1111-1111-1111-111111111111`, account `…221`, payment `c1601a11-0000-4000-8000-111111111601`.  
**Bank:** 100 ids. Did not add AEJE-IQ-101. No portal, no Bedrock, no AWS apply.  
**`solutions/INTERVIEW-1601/`:** not opened before these drafts.

---

## AEJE-IQ-012  [Java/JVM]  — Engineer + Staff

**Question:** When do you keep one JVM vs extract payment / refund / worker because Jordan wants “a payments platform”?

### Engineer

Today `payment-service` is a Java 21 / Spring Boot 3.5.5 **modular monolith**. Avery’s `POST /api/v1/payments` for `c1601a11-…1601` authorizes, writes idempotency, and posts ledger intent **in one process** so a retry with the same `Idempotency-Key` cannot debit `…221` twice because of a half-deployed second JVM. I keep one JVM while those units of work share a database and a transaction boundary. I extract when I have **evidence**: a team that cannot ship without blocking Harbor Market, a scaling axis that is not “more Fargate tasks,” or a failure domain that is *already* independent (worker lag that must not take down authorize). I measure create P99, Hikari `jdbc/baypay` pending, and duplicate-capture rate — not “service count.” I refuse `PaymentCluster` / `dmgr-east` as the extract target.

### Staff

I keep one JVM **this quarter** unless Finance funds a second deployable *and* we can state the new failure domain. Splitting for a slide does not improve authorize: posting in-process still shares the writer; a second JVM adds a network hop, a second image, a second scrape, and a split-brain idempotency store unless we design it. Who decides: Priya (SLO / error budget) + Sam (ops cost) + Jordan (release blast). What fails this question: “microservices because that is what a platform looks like,” extracting onto leftover ND, or applying EKS to host three empty services. Principal add (one line): I fund extract only when the **ledger-intent contract** survives the cut.

**Follow-up (Staff):** Posting in-process keeps **one** Hikari pool and **one** idempotency row for Avery’s retry — those domains do *not* automatically improve when the worker is a second process. Operational cost of a second JVM before the code is cleaner: second task def, second ALB rule or port, second scrape budget, second on-call page, and a deploy that can authorize without posting (INCIDENT-style two-unit gap).

---

## AEJE-IQ-064  [AWS]  — Engineer + Staff  · **timed: yes · ~8 min**

**Question:** ECS/Fargate vs EKS vs OpenShift this quarter. Teaching default ECS/Fargate `us-west-2`. What do you refuse to apply?

### Engineer

This quarter I run `payment-service` on **ECS on Fargate** in `us-west-2`: task `8080`, health `/actuator/health/liveness` and `/actuator/health/readiness`, ALB in front of `payments.apps.baypay.example`. I do **not** apply EKS, NAT, or multi-AZ RDS “so the answer is honest.” OpenShift wins when Route/SCC is already home. EKS wins when the estate already runs kube and we will not pay a second control plane as a lab. Avery’s create still needs Idempotency-Key and frozen `…222` in the app — the scheduler does not authorize.

### Staff

**ECS/Fargate** is the teaching apply and the Staff default when we do not already operate kube. **EKS** when kube is the home and we already pay the CP. **OpenShift** when the shop is already there — I will not dual-home IHS + ALB. “Stay where we are” is the Staff answer if Morgan’s `BayPayCell` is the *source* estate we are leaving, not a third platform. Skills and CP cost change the answer: a two-person SRE team does not buy an EKS bill to look modern. I refuse NAT/EKS/RDS apply in a 90-minute lab (COST-1105). Principal add: I will not stand up a second CP as rollback.

**Follow-up (Staff):** Skills — if nobody can debug a kube Service/Endpoints miss (INC-K8S-1006 class), Fargate is cheaper than a page. “Stay where we are” means **Fargate this quarter**, not “stay on `dmgr-east`.”

---

## AEJE-IQ-086  [Production Engineering]  — Engineer + Senior

**Question:** 99.9% monthly SLI on successful `POST /api/v1/payments`. Authorize vs settle. What must you not relabel 99.99%?

### Engineer

SLI = successful creates / (successful + **server** failures). Server = 5xx, timeout, or a dependency that becomes 5xx. Teaching SLO is **99.9%** (~43 minutes / 30 days). P99 teaching latency **< 400 ms**. Avery’s late **201** for `c1601a11-…1601` still misses Harbor Market’s authorize window even if COMPLETED later — that is the **latency** promise, not the availability tile. I do **not** put `customerId` or `Idempotency-Key` on metric labels.

### Senior

Authorize (merchant-facing create) is the Module 13 tile. Settle/complete (ledger completeness) is a **different** promise — recon, not the 99.9% create SLI. I will **not** silently relabel the Grafana tile **99.99%**; that is ARCHITECT-1401’s *architecture* goal (~52 min/year), a contract Priya + Finance would sign, not a dashboard edit. Who pages: SLO burn and Hikari pending — not CPU > 80%.

**Follow-up (Senior):** Frozen `…222` **4xx** does **not** burn the create SLO — that is Avery’s client / policy, not our error budget. A create that returns late 201 and COMPLETED minutes later broke the **P99 / authorize-window** promise; availability may still look green.

---

## AEJE-IQ-031  [WebSphere/Liberty]  — Engineer + Senior

**Question:** Cell, dmgr-east, nodeagent, Pay1. What still serves if dmgr is down? Not greenfield.

### Engineer

`BayPayCell` is the **source estate**. `dmgr-east` is the deployment manager — config and sync, not the merchant path. `nodeagent-pay-2` is the node process that talks to the dmgr. `Pay1` is an application server that can still run `payment.ear` if it is already STARTED. If `dmgr-east` is down, **already-started members still serve** Harbor Bike Co — I do **not** bounce the cell to “restore create.” Avery’s POST on the *target* plane is Fargate `:8080`, not `/payment` on `payment.ear`. I refuse a second ND cell as HA.

### Senior

This is a **decommission** conversation (Module 6), not a greenfield design. Leftover ND is not the 99.99% HA target and not a DR bunker. If `nodeagent-pay-2` is down while Pay2/Pay3 stay STARTED, Morgan cannot **sync / install / start-stop through the agent** on that node — serving can continue. `ihs-east` is a web tier, **not** a federated WAS node. A second cell for FX quote is the same anti-pattern as ARCHITECT-604: another control plane, same fate class. I will not fail over to `dmgr-east` in a Fargate incident.

**Follow-up (Senior):** Morgan loses **node-level admin** on that box, not necessarily in-flight creates on STARTED servers. I refuse a second cell because FX does not need a second dmgr — it needs a module or a later extract with a real SLO.

---

## Timed log

| Id | Clock | Elapsed | Notes |
|---|---|---|---|
| AEJE-IQ-064 | 8 minutes | ~8 | Same two-level bar. Did not drop Staff refusals (no EKS/NAT/RDS apply). |

---

## Reveal gap list (filled after drafts were saved)

Compared with `--reveal` **after** the drafts above. Did not paste bank text back as spoken.

- **IQ-012:** I named idempotency and two-unit risk; I under-named **outbox** and “extract when posting CPU / queue depth harms the HTTP SLO.” Staff bank wants a written **failure-domain map** and “never `-Xmx` = cgroup” on the second process. I will not copy the principal “halfway house” sentence verbatim.
- **IQ-064:** I had Fargate default + refuse NAT/EKS apply. I under-named **one app contract on all three homes** and “stay on OpenShift is first-class.” Over-claim risk: sounding like Fargate is the only production answer. Will not recite “tourism cluster.”
- **IQ-086:** 4xx / 99.9% / no silent 99.99% matched. I under-named a **separate completeness SLI** (AUTHORIZED → COMPLETED) with an owner — I treated settle as “recon” only. Staff: TLS failures stay in the **create** SLI; do not exclude timeouts to help the number.
- **IQ-031:** Mechanism was fine (dmgr down ≠ members down). I under-named **ihs-east + plugin** as the merchant front door on the *source* estate, and Staff ownership (Riley members / Morgan sync / Priya plugin). Will not bounce `dmgr-east` to fix Pay2.
- **Will not live-mock:** bank paragraphs, instructor RCAs as the only story, or one paragraph in both maturity boxes.
