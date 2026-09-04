# CAPSTONE-2 — Instructor solution

**Do not share these files with students before they have a wave table and an ND-in-Docker refusal of their own.**

`hideAnswerUpfront` is false on the student guide, so they may see a **checklist** and the compact wave table. This folder is the scored narrative. A student brief that uses the locked names and refuse-list passes even if mermaid layout differs.

## Philosophy

Traditional WebSphere ND is BayPay’s **source estate**. Teach it so engineers can operate, diagnose, and **leave** it. Liberty (or `reference-apps/baypay`, Java 21, Spring Boot 3.5.5) is the target. Do **not** recommend a new ND cell. Do **not** put `BayPayCell` in Docker. Do **not** require live ND, Docker, kind, or OpenShift to pass.

**AEJE-D-071** = current (merchants → `ihs-east` → `PaymentCluster` / `RefundCluster` → `db-east`).  
**AEJE-D-072** = target (TLS edge → `payment-service` `:8080` → secrets → teaching DB).

## Current estate (from TOPOLOGY.md)

```text
Merchants / Avery Chen
  → ihs-east.baypay.example  (plugin-cfg.xml)
    → PaymentCluster  payment.ear  /payment
         Pay1 @ node-pay-1 / was-pay-1.baypay.example
         Pay2, Pay3 @ node-pay-2 / was-pay-2.baypay.example
    → RefundCluster   refund.ear   /refund
         Ref1, Ref2 @ node-ref-1 / was-ref-1.baypay.example
      → SIBus BayPayBus  (jms/paymentEvents, jms/refundEvents)
        → db-east.baypay.example:5432 / baypay
```

Control plane (not serving): `dmgr-east` @ `was-dmgr-east.baypay.example`. Node agents `nodeagent-pay-1`, `nodeagent-pay-2`, `nodeagent-ref-1`. `STARTED` is not throughput.

JNDI smells: cell-scoped `jdbc/baypay` (shared historically, including reporting risk); `jdbc/baypayXA` not on every node; J2C alias `baypayDbAlias`. WAS pool teaching default **maxConnections = 50** on PaymentCluster. Do not treat `3 × 50` as a fact until Morgan Hale confirms scope.

People: Priya Nair (SRE), Riley Okonkwo (app on-call), Morgan Hale (WAS admin), Jordan Voss (release), Sam Okada (platform). Avery Chen `11111111-1111-1111-1111-111111111111`, active `…221`, frozen `…222`.

What students must **not** copy for greenfield: new DMGR, new SIBus, sticky `JSESSIONID` on `/payment`, cell-wide pool, a second `BayPayCell`.

## Liberty waves (locked)

| Wave | Scope | Success signal | Rollback | Owner (teaching) |
|---|---|---|---|---|
| 0 | Inventory + compatibility (`javax` vs `jakarta`, SIBus cannot lift, ears → wars) | Classified lift / rewrite / defer / drop | N/A | Morgan + Jordan |
| 1 | Refund on Liberty: `refund-service.war`, features `servlet-6.0` `jdbc-4.3` `jndi-1.0` `persistence-3.1`, bind `jdbc/baypay-refund` | Refund error rate / latency hold; `ihs-east` `/refund` | Restore `refund.ear` on `RefundCluster` | Jordan; Riley confirms money |
| 2 | **One** Liberty (or Boot) payment replica behind `ihs-east`; bind `jdbc/baypay-payment`; sessionless `/payment` | Canary 5xx / P99 hold vs `PaymentCluster` | Drain canary; **100%** `PaymentCluster` | Priya + Jordan; never bounce `dmgr-east` |
| 3 | Decommission `node-pay-*` / `node-ref-1` after SLO hold | Payment + refund SLOs green | Last ND backup retained until **wave 3 + 14 days** | Morgan retains backup; Jordan does not delete night-of |

Refund first: lower volume on `RefundCluster` (`Ref1`, `Ref2` only). Payment canary: Avery’s volume is not a rehearsal. Big-bang flip of `Pay1`/`Pay2`/`Pay3` is a Sev-1 with no ND to drain back to.

SIBus: **defer** recreation. Do not rebuild `BayPayBus` on Liberty as a goal. `BAYPAY_DB_*` lives in `server.env` / variables / later Secret — never committed XML.

## Rollback cards (minimum content)

**Wave 1:** Evidence (refund 5xx, latency, Harbor Market tickets) → drain `/refund` at `ihs-east` back to `Ref1`/`Ref2` → restore `refund.ear` on `RefundCluster` → confirm edition and `jdbc/baypay` on ND → re-enter Liberty only after hold. Never: bounce `dmgr-east`, new cell, SIBus rebuild as “fix.”

**Wave 2:** Evidence (canary 5xx / P99 vs cluster) → drain the **one** Liberty payment replica at the plugin → 100% `/payment` on `PaymentCluster` → confirm ND edition and JNDI → re-enter canary only after hold. Never: bounce `Pay1` as the first move, bounce `dmgr-east`, sticky `JSESSIONID`, flip all three payment members.

## Container (paper, CLUSTER.md)

```text
Image:    registry.baypay.example/baypay/payment-service:<tag>
Build:    eclipse-temurin:21-jdk + ./mvnw
Runtime:  eclipse-temurin:21-jre  (not a full JDK)
User:     10001 (non-root)
Port:     8080
Secrets:  BAYPAY_DB_* at runtime — never Dockerfile ENV
JVM:      UseContainerSupport; MaxRAMPercentage (e.g. 75%); NEVER -Xmx = cgroup/limit
Probes:   /actuator/health/liveness  /actuator/health/readiness
```

This packages the **teaching process**. It does **not** package `dmgr-east`, a node agent, or a traditional WAS profile. ND-in-Docker is a failed Production awareness score.

## Kubernetes / OpenShift (paper)

```text
Namespace / Project:  baypay-prod
Deployment:           payment-service  (3 replicas when healthy)
Labels:               app=payment-service
Service:              payment-service ClusterIP 8080
Ingress host:         payments.apps.baypay.example
OpenShift Route:      payment-route (same host) — overlay, not a second product
ConfigMap:            payment-config
Secret:               baypay-db   (BAYPAY_DB_USER, BAYPAY_DB_PASSWORD)
TLS Secret:           payment-tls
```

Do not schedule the cell. Do not bounce `dmgr-east` for a kube page. OpenShift SCC / Project / Route are overlays on the same objects. kind/OCP are optional.

## Test and rollback (paper is enough)

| Gate | Test | Pass signal | Rollback if red |
|---|---|---|---|
| Before Wave 1 | Compatibility inventory + refund contract (status, amounts) | Classifications complete; WAR starts on paper `server.xml` | Stay on `refund.ear` |
| Wave 1 hold | Refund error rate, latency vs `RefundCluster` | Hold window green | Restore `refund.ear` |
| Before Wave 2 | Payment contract: `./mvnw test` or equivalent; idempotent replay; frozen `…222` → decline | Suite green | Do not attach canary |
| Wave 2 hold | Canary 5xx / P99 vs `PaymentCluster`; plugin weight | Hold green | Drain canary |
| Target probes | Liveness vs readiness mapped; fail-closed ready | Ready matches dependencies | Keep canary out |
| Wave 3 | SLO hold + 14-day backup existence | Backup restore drill documented | Do not decommission |
| Heap vs limit | `-Xmx` **not** equal to memory limit | Percentage + container support | Reject the JVM flags |

No live cell. No required Docker/kind/OCP. CAPSTONE-1 list-by-customer is not required here; payment create/replay/decline is the contract you cite.

## What must not appear

- New traditional ND cell / second DMGR as rollback environment
- ND-in-Docker or “cell in a Pod”
- Wave 1 = payment; Wave 2 = flip all payment members
- Bounce `dmgr-east` as stabilize or rollback
- Sticky `JSESSIONID` canary
- Cell-wide `jdbc/baypay` on Liberty
- `-Xmx` equal to cgroup / container limit
- Required AWS apply, EKS, ROSA, NAT, RDS Multi-AZ (those are later capstones)
- Invented hostnames outside `.baypay.example`

## Scoring notes

Technical accuracy is locked names + wave numbers + rollback targets. Diagnostic method is TOPOLOGY.md / CLUSTER.md first, `solutions/` later. Production awareness is ND as rollback **target** then exit, plus not ND-in-Docker. Trade-off is refund-first, canary vs DNS, Git vs ND backup, Liberty vs Boot. Security / reliability is secrets out of XML/image, sessionless `/payment`, heap ≠ limit. Communication is PF-modernize.md. Efficiency is paper in 4–8 hours without a licensed cell.

A beautiful kube YAML that still recommends a new `BayPayCell` cannot pass Production awareness.
