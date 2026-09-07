# Portfolio — Modernize BayPay (ND → Liberty → containers → K8s/OCP)

**Artifact:** [CAPSTONE-2](../../capstones/02-modernize-baypay/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**After:** Modules 4–10  
**Diagrams:** AEJE-D-071 (current) · AEJE-D-072 (target)  
**Sources:** [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md) · [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md)

Export this page (or a copy) as your CAPSTONE-2 portfolio artifact. Fill every section in your own words. Do not paste instructor solution text. Do not put `BAYPAY_DB_PASSWORD` values, PAN, or a live kubeconfig in this file. Live ND, Docker, kind, and OpenShift are optional — say whether you used them. The grade path is paper.

Traditional ND is the **source estate**. Liberty or Spring Boot 3.5.5 is the **target**. Do not invent a Wave 4 that stands up a second `BayPayCell`. Do not recommend ND-in-Docker.

**Your name:**  
**Date:** 2026-09-07  
**Cohort / reviewer (if any):**  
**Engines used (none / docker / kind / oc — files only is expected):** none — files only (TOPOLOGY.md, CLUSTER.md, AEJE-D-071 / AEJE-D-072). Optional Boot `./mvnw test` from CAPSTONE-1 is extra, not this grade path.

---

## 1. Current estate (AEJE-D-071)

Cite **AEJE-D-071**. Use locked names only.

Draw or paste mermaid/ASCII for `BayPayCell`. Must show: `dmgr-east`, `node-pay-1`, `node-pay-2`, `node-ref-1`, node agents, `Pay1` / `Pay2` / `Pay3`, `Ref1` / `Ref2`, and `ihs-east` **outside** the cell.

```text
Merchants / Avery Chen
        │ HTTPS
        ▼
 ihs-east.baypay.example     ← TLS + plugin-cfg.xml   (OUTSIDE BayPayCell)
        │
        ├── /payment (no JSESSIONID) ──► Pay1   Pay2   Pay3
        └── /refund                  ──► Ref1   Ref2

 BayPayCell                                          AEJE-D-071 = CURRENT
   dmgr-east @ was-dmgr-east.baypay.example
        │  sync / admin only — not merchant HTTP
        ├── nodeagent-pay-1 @ node-pay-1 / was-pay-1.baypay.example
        │         └── Pay1  payment.ear  /payment
        ├── nodeagent-pay-2 @ node-pay-2 / was-pay-2.baypay.example
        │         ├── Pay2  payment.ear  /payment
        │         └── Pay3  payment.ear  /payment
        └── nodeagent-ref-1 @ node-ref-1 / was-ref-1.baypay.example
                  ├── Ref1  refund.ear   /refund
                  └── Ref2  refund.ear   /refund

 JNDI (cell-scoped historically): jdbc/baypay  jdbc/baypayXA
                                   jms/paymentEvents  jms/refundEvents
                                   baypayDbAlias
 SIBus BayPayBus

                    jdbc/*  ──►  db-east.baypay.example:5432 / baypay
                                      └── Reporting (nightly; not inside Pay1)
```

| Path | Hops (your words) |
|---|---|
| Serving (Avery Chen `11111111-1111-1111-1111-111111111111` → money) | Client → `ihs-east` (TLS, `plugin-cfg.xml`) → `PaymentCluster` (`Pay1`/`Pay2`/`Pay3`) or `RefundCluster` (`Ref1`/`Ref2`) → `jdbc/baypay` / `BayPayBus` → `db-east:5432`. Avery never hits `dmgr-east`. |
| Control (Morgan Hale → config) | Operator → `dmgr-east` → `nodeagent-pay-1` / `nodeagent-pay-2` / `nodeagent-ref-1` → application servers. `STARTED` on a JVM is not Harbor Market throughput. |

| Cluster | Member | Node | Application | Context |
|---|---|---|---|---|
| `PaymentCluster` | `Pay1` | `node-pay-1` | `payment.ear` | `/payment` |
| `PaymentCluster` | `Pay2` | `node-pay-2` | `payment.ear` | `/payment` |
| `PaymentCluster` | `Pay3` | `node-pay-2` | `payment.ear` | `/payment` |
| `RefundCluster` | `Ref1` | `node-ref-1` | `refund.ear` | `/refund` |
| `RefundCluster` | `Ref2` | `node-ref-1` | `refund.ear` | `/refund` |

| Bind | Smell or note |
|---|---|
| `jdbc/baypay` | Cell-scoped historically. Shared pool is the modernization smell. Incident-default `maxConnections = 50` — if cell-scoped, three Pay members share one 50. |
| `jdbc/baypayXA` | XA leftover; not on every node. Do not assume Pay1–Pay3 all have it. Do not add it on Liberty. |
| `baypayDbAlias` | J2C alias — username/password for the DataSource, not “the database.” |
| SIBus `BayPayBus` | Messaging engine lives on a node. Do not lift the bus as a Wave 1/2 goal. Do not add a new bus for greenfield. |
| `jms/paymentEvents` / `jms/refundEvents` | Same bus. Teaching Boot equivalent is in-process events. Liberty canary does not recreate these names. |

What I would **not** copy for a new service: a second DMGR, a new SIBus, sticky `JSESSIONID` on `/payment`, or a new traditional cell. AEJE-D-071 is leftover inventory.

Why is `dmgr-east` down a change-freeze and not a Harbor Market outage?

Merchants already have a path: `ihs-east` → cluster members → `db-east`. `dmgr-east` is the management JVM on `was-dmgr-east.baypay.example`. When it is down, Morgan cannot sync, deploy, or trust the console — that is a freeze. Avery’s POST can still return 201. “The cell is down” is the wrong first sentence.

---

## 2. Target estate (AEJE-D-072)

Cite **AEJE-D-072**. This is not “the cell, but in Kubernetes.”

| Element on AEJE-D-072 | What you mapped it to (process, object, or file) |
|---|---|
| Merchants TLS / edge | Ingress host or OpenShift Route `payment-route` on `payments.apps.baypay.example` (TLS Secret `payment-tls`). Not `ihs-east` forever, and not `dmgr-east`. |
| `payment-service` `:8080` | Boot fat JAR or Liberty `payment-service.war` — one process. Deployment `payment-service` in `baypay-prod`, labels `app=payment-service`. |
| Secrets | Secret `baypay-db` keys `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD` at **runtime**. Never `ENV` in the image. Never `baypayDbAlias` copied into XML. |
| Teaching DB | Teaching / course DB behind `BAYPAY_DB_*`. Paper target is not “schedule `db-east` as a Pod named `dmgr-east`.” |

One paragraph: what is **absent** from AEJE-D-072 (`dmgr-east`, node agents, cell JNDI, SIBus) and why that absence is the point.

AEJE-D-072 has no `dmgr-east`, no `nodeagent-*`, no cell-scoped `jdbc/baypay`, and no `BayPayBus`. That is the point: the target is a process with a port, a Secret, and a database — not a profile and a node agent scheduled as Pods. If you redraw the cell inside Kubernetes you have not left AEJE-D-071; you have containerized the leftover.

---

## 3. Liberty waves (0–3)

Wave numbers and rollback one-liners must match TOPOLOGY.md. Wave 1 names `refund.ear` / `RefundCluster`. Wave 2 names a **single** Liberty payment replica behind `ihs-east`. Wave 3 keeps a last ND backup until **wave 3 + 14 days**.

| Wave | Scope (your words, locked names) | Success signal | Rollback | Who calls rollback |
|---|---|---|---|---|
| 0 | Inventory + compatibility. Classify `payment.ear` / `refund.ear` binds. Isolated names decided. No merchant traffic moves. No Liberty replica in `plugin-cfg.xml`. | Assessment complete: SIBus not “lifted,” `dmgr-east` marked drop, greenfield refusal written. | N/A | Riley Okonkwo can **halt** Wave 1 start if blockers are open. |
| 1 | `refund-service.war` on Liberty (`jdbc/baypay-refund`). Context `/refund` behind `ihs-east`. `refund.ear` stays **installed** on `RefundCluster` (`Ref1`, `Ref2` @ `node-ref-1`). Lower volume than payment. | `/refund` error rate and p99 hold vs ND baseline; logs show isolated bind, not `jdbc/baypay`; `Ref1`/`Ref2` still STARTED. | Restore `refund.ear` on `RefundCluster`; plugin `/refund` back to `Ref1`/`Ref2`. | Riley Okonkwo calls. Morgan Hale executes plugin + ear start. |
| 2 | **One** Liberty `/payment` replica (`payment-service.war`, `jdbc/baypay-payment`) behind `ihs-east` beside `Pay1`/`Pay2`/`Pay3`. Low plugin weight. Not a flip of `PaymentCluster`. | Canary 5xx and p99 within hold; Avery create `201`; same `Idempotency-Key` replays; frozen `…222` still `DECLINED`; ND still serves the majority. | Drain the canary; **100% `PaymentCluster`**. Leave Wave 1 refund on Liberty unless `/refund` is also failing. | Riley Okonkwo (money). Priya Nair confirms 100% ND at `ihs-east`. Morgan changes weight. |
| 3 | After SLO hold: drain remaining ND serving; stop `Pay1`/`Pay2`/`Pay3` / `Ref1`/`Ref2` / node agents; then retire `dmgr-east`. Decommission `node-pay-1`, `node-pay-2`, `node-ref-1`. | Named bake stays green. Last ND backup exists and is restore-tested on paper. | Keep last ND backup until **wave 3 + 14 days**. Git is not that backup. | Priya Nair calls “hold failed, restore.” Jordan Voss does not delete backups the night SLO turns green. |

Liberty features you expect (`servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`) and isolated binds (`jdbc/baypay-payment`, `jdbc/baypay-refund`):

`server.xml` enables those four features. Binds are **isolated**: `jdbc/baypay-payment` and `jdbc/baypay-refund`. Credentials come from `BAYPAY_DB_*` / `server.env`, not a copied `baypayDbAlias`. Cell-wide `jdbc/baypay` stays on the ND ears we are leaving. Dual-run means two pools, one database — not one name.

Why Wave 1 is refund, not payment (4–6 sentences):

Harbor Market talks about pay because that is the product. Volume and blast radius say otherwise. `/refund` is the lower-traffic URI on TOPOLOGY.md, so a Liberty bind or feature miss hurts fewer merchants than a bad `/payment` replica. `refund.ear` staying installed on `Ref1`/`Ref2` makes rollback a plugin restore, not a cluster invention. Avery’s create path stays on `PaymentCluster` until Wave 2 proves one canary. Payment is not a rehearsal — a Wave 1 payment flip is a Sev-1 you chose. Riley will not let `/payment` go dark for a modernization weekend; refund first is how you keep that promise.

---

## 4. Wave 1 rollback card (refund)

Assume Harbor Market refund volume is already on Liberty `refund-service.war` and error rate or latency breaches the hold.

```text
Evidence to collect:
  /refund 5xx and p99 vs ND baseline (Priya). Liberty messages.log:
  jdbc/baypay-refund checkout, missing servlet-6.0/jdbc-4.3, or anyone
  who pretended BayPayBus lifted. Confirm RefundCluster Ref1/Ref2 still
  STARTED (Morgan) — ear must still be installed.

Drain / traffic action at ihs-east:
  Liberty refund member weight 0 (or remove from plugin-cfg.xml).
  100% of /refund to Ref1 and Ref2. Not sticky JSESSIONID.

Restore on ND:
  Start refund.ear on RefundCluster if it was stopped.
  Do not bounce dmgr-east. Do not rebuild the ear from Git first.

Confirm:
  POST /refund 2xx on Ref1 or Ref2. Context /refund.
  Harbor Market can retry the failed refund (same business key).

Re-enter Liberty only when:
  Refund error rate back to ND baseline for a named hold (24h),
  RCA is bind / feature / probe (not “restarted Liberty”),
  Wave 0 blockers that bit us are re-scored.

Never:
  Bounce dmgr-east. Uninstall refund.ear in Wave 1.
  Bounce db-east. Stand up BayPayCell-2. Re-enter the same night.
```

What exactly is restored onto `RefundCluster`? Is “bounce `dmgr-east`” on this card? It must not be.

**`refund.ear`** on **`Ref1` and `Ref2`**, context `/refund`. Plugin + start. Bounce `dmgr-east` is **not** on this card — the DMGR is not on the serving path.

---

## 5. Wave 2 rollback card (payment canary)

Avery Chen may be in the canary bucket. Money stays on `PaymentCluster` if the Liberty replica misbehaves.

```text
Evidence to collect:
  Canary 5xx / p99 vs Pay1/Pay2/Pay3. Waiters or NameNotFound on
  jdbc/baypay-payment. Same Idempotency-Key that 201’d then 500’d
  or posted twice. Avery “works on retry to ND” is enough to drain.

Drain the canary (plugin / IHS):
  Weight 0 or delete the Liberty payment member from plugin-cfg.xml.
  ihs-east lists only Pay1, Pay2, Pay3 for /payment.

What stays at 100%:
  PaymentCluster (Pay1, Pay2, Pay3) on node-pay-1 / node-pay-2.
  Wave 1 Liberty /refund stays up if refund SLOs hold.

What you do not bounce:
  dmgr-east. db-east. Pay1 (the canary is the defect).
  node-pay-2 (would take Pay2 and Pay3 together).

Confirm edition / JNDI on ND:
  Pay1/Pay2/Pay3 same last-known-good edition.
  Cell jdbc/baypay still serves ND payment.
  Canary must not have been bound to jdbc/baypay.

Re-enter canary only when:
  PaymentCluster 5xx flat for a named hold (24h);
  RCA is bind / feature / probe, not TCP-only STARTED;
  Idempotency-Key + frozen …222 re-tested on both runtimes.

Never:
  Flip Pay1/Pay2/Pay3 in the same window.
  Sticky JSESSIONID so Avery “stays on the canary.”
  Bounce dmgr-east. Delete PaymentCluster because the canary looked green.
```

How does `ihs-east` send a **fraction** of `/payment` without sticky `JSESSIONID`?

One Liberty member, **low plugin weight**, majority weight on `Pay1`/`Pay2`/`Pay3`. Weighted / round-robin. Retries use `Idempotency-Key` and the shared ledger, not JVM affinity. `/payment` is sessionless in this course.

What JNDI name does the canary use, and which cell-wide name must it **not** reuse?

Canary: `jdbc/baypay-payment`. Must **not** reuse `jdbc/baypay` (or add `jdbc/baypayXA`). Database is shared; pools are not.

---

## 6. Container design (paper)

| Field | Your answer |
|---|---|
| Image name | `registry.baypay.example/baypay/payment-service:<tag>` — never `:latest` |
| Build-stage base | `eclipse-temurin:21-jdk` (Maven / `./mvnw` only) |
| Runtime-stage base (must not be a full JDK) | `eclipse-temurin:21-jre` |
| UID | `10001` (`USER 10001`, non-root) |
| Port | `EXPOSE 8080` |
| Where `BAYPAY_DB_*` live | Runtime env / Secret `baypay-db`. Never `ENV` in the image. Never baked XML. |
| `JAVA_TOOL_OPTIONS` / heap story | `-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0`. No `-Xmx` in the image. |
| Why `-Xmx` must **not** equal the container / cgroup limit | Heap is not the only native consumer (metaspace, threads, direct buffers, the JRE). `-Xmx` = limit is how you OOMKilled a “correctly sized” canary. Container support + a percentage leaves headroom. Never set `-Xmx` equal to the container memory limit. |

One paragraph: why packaging `dmgr-east` or a WAS profile in Docker is **not** modernization.

That is ND-in-Docker: you still have a cell, a node agent, and a control plane that Avery does not use, plus a cgroup that will fight a traditional JVM. AEJE-D-072 is one `payment-service` process on `:8080`. Sam Okada will not accept a Dockerfile that packages `dmgr-east` “so we keep the cell.” Package the Boot JAR or the Liberty WAR. One process, not a profile.

---

## 7. Kubernetes / OpenShift design (paper)

Use CLUSTER.md names. Sketch intended `baypay-prod` objects. Placeholders only for secrets (`${BAYPAY_DB_PASSWORD}`, `***`).

```yaml
# paper only — CLUSTER.md names
apiVersion: v1
kind: Namespace   # OpenShift: Project
metadata:
  name: baypay-prod
---
# Deployment payment-service
#   replicas: 3
#   labels: app=payment-service
#   image: registry.baypay.example/baypay/payment-service:<tag>
#   containerPort: 8080
#   securityContext: runAsNonRoot: true, runAsUser: 10001
#   envFrom: ConfigMap payment-config + Secret baypay-db
#   livenessProbe:  GET /actuator/health/liveness
#   readinessProbe: GET /actuator/health/readiness
# Service payment-service  ClusterIP  8080  selector app=payment-service
# Ingress host payments.apps.baypay.example  tls: payment-tls
#   — or OpenShift Route payment-route (same host, same job)
# Secret baypay-db: BAYPAY_DB_USER, BAYPAY_DB_PASSWORD: ***
```

| Question | Your answer |
|---|---|
| Replicas when healthy | 3 |
| Probe paths (liveness vs readiness) | Liveness `/actuator/health/liveness` (restart the process). Readiness `/actuator/health/readiness` (leave the Service Endpoints). Probe is not `POST /api/v1/payments`. |
| Ingress vs OpenShift Route — same job or different product? | Same job, two APIs. Ingress on Kubernetes; Route `payment-route` on OpenShift. Host stays `payments.apps.baypay.example`. Do not treat them as two products you must both install. |
| What you would **not** schedule as a Pod | `dmgr-east`, a node agent, `BayPayCell`, or a WAS profile. OpenShift is a Project / SCC / Route overlay, not a second platform this paper must stand up. |

---

## 8. Test and rollback plan

No live ND or required kind/OCP. Name the tests.

| Gate | What you test | Pass signal | Rollback if red |
|---|---|---|---|
| Before Wave 1 | Contract on Boot (`./mvnw test`) or equivalent WAR tests; isolated `jdbc/baypay-refund` bind on paper; `refund.ear` still installed on `Ref1`/`Ref2` | Suite green; Wave 0 blockers closed; plugin change reviewed | Do not start Wave 1 |
| Wave 1 hold | `/refund` 5xx and p99 vs ND baseline; Liberty log shows `jdbc/baypay-refund` | Hold stays green for the named bake | Restore `refund.ear` on `RefundCluster` |
| Before Wave 2 (include create / replay / frozen `…222`) | Create `201` `COMPLETED`; identical `Idempotency-Key` → `200` same `paymentId`; frozen `22222222-2222-2222-2222-222222222222` → `422` `DECLINED`; missing key `400` | Same matrix on ND majority and on the canary build | Do not add the canary to `plugin-cfg.xml` |
| Wave 2 canary hold | Canary 5xx / p99 vs `Pay1`/`Pay2`/`Pay3`; replay and frozen still hold; pool waiters ~0 on `jdbc/baypay-payment` | Fraction of `/payment` within hold; majority still ND | Drain canary; 100% `PaymentCluster` |
| Probes on target | Liveness and readiness fail-closed; TCP-only STARTED is not a pass | Ready only when JNDI + process are up | Remove from Endpoints / plugin; do not bounce `dmgr-east` |
| Wave 3 + 14-day backup drill | Paper restore of last `dmgr-east` / node repository; plugin history; LTPA | Drill completes; backup retained until **wave 3 + 14 days** | Stop decommission; restore from that backup — Git cannot |
| Heap vs memory limit | `UseContainerSupport` + `MaxRAMPercentage`; image has no `-Xmx` = limit | Canary does not OOMKilled under the cgroup | Fix flags; do not “just raise `-Xmx` to the limit” |

Optional engine you actually ran (if any) — one line:

None. Paper + locked files. CAPSTONE-1 `./mvnw test` already proved the Boot create/replay/frozen/list contract this page cites.

---

## 9. What you would NOT do

In 8–12 sentences, refuse: a new traditional ND cell as a “safe rollback environment,” ND-in-Docker, cell-wide `jdbc/baypay` on Liberty, SIBus recreation as a goal, sticky payment sessions, bouncing `dmgr-east`, `-Xmx` equal to the cgroup limit, and any required paid OpenShift or AWS apply for this capstone. Name Boot or Liberty as the exit. Cite AEJE-D-071 as current and AEJE-D-072 as target.

AEJE-D-071 is the **current** leftover cell. We operate it and leave it. Rollback targets `refund.ear` on `RefundCluster` and 100% `PaymentCluster` — not a new `BayPayCell-2` and not a second DMGR “so we have somewhere safe.” Packaging `dmgr-east` or a WAS profile in Docker is ND-in-Docker, not modernization; the image is `registry.baypay.example/baypay/payment-service:<tag>`. Liberty does not keep cell-wide `jdbc/baypay`; isolated `jdbc/baypay-payment` / `jdbc/baypay-refund` are the binds, because reporting must not saturate the payment pool. Recreating `BayPayBus` is not a Wave goal; the canary does not lift SIBus. `/payment` stays sessionless — sticky `JSESSIONID` is not a canary strategy. Bouncing `dmgr-east` is never rollback or stabilize; Avery does not travel that hop. `-Xmx` equal to the container / cgroup limit is refused; heap is not the only native consumer. This capstone does not require Docker, kind, paid OpenShift, or an AWS apply (that is CAPSTONE-3, and even there `validate` is the bar). The exit is Open Liberty or the Spring Boot 3.5.5 reference app. AEJE-D-072 is the **target**: TLS edge → `payment-service` `:8080` → secrets → teaching DB.

---

## 10. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, Morgan Hale, Jordan Voss, and Sam Okada, in one sitting, why Wave 1 is refund, why Wave 2 is a canary rather than a cluster flip, why the image is `payment-service` and not `BayPayCell`, and why this page costs $0.

Wave 1 is refund because Harbor Market refund volume is lower and `refund.ear` stays installed on `Ref1`/`Ref2` — restore is a plugin move, not a weekend outage on Avery’s create. Wave 2 is **one** Liberty payment replica behind `ihs-east` with low weight; flipping `Pay1`/`Pay2`/`Pay3` together is a Sev-1 you scheduled. If the canary 5xx’s we drain it and leave 100% on `PaymentCluster` — we do not bounce `Pay1` or `dmgr-east`. The image is `payment-service` on `:8080`, non-root, secrets at runtime, `UseContainerSupport` — not the cell in a pod. AEJE-D-071 is inventory; AEJE-D-072 is a process. This page costs $0 because the grade path is TOPOLOGY.md, CLUSTER.md, and the rollback cards, not a licensed ND install or a paid cluster.

---

## Honesty

- [x] I did not open `solutions/CAPSTONE-2/` before I wrote waves and the ND-in-Docker refusal
- [x] Every cell name comes from TOPOLOGY.md
- [x] Every kube name comes from CLUSTER.md
- [x] I cited AEJE-D-071 as current and AEJE-D-072 as target
- [x] Wave 1 is refund; Wave 2 is one payment canary
- [x] I did not recommend a new traditional ND cell
- [x] I did not recommend ND-in-Docker
- [x] I did not set `-Xmx` equal to a container / cgroup limit
- [x] I did not put a live password in this file
- [x] I did not require Docker, kind, or OCP to claim I finished
