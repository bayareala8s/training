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
**Date:**  
**Cohort / reviewer (if any):**  
**Engines used (none / docker / kind / oc — files only is expected):**  

---

## 1. Current estate (AEJE-D-071)

Cite **AEJE-D-071**. Use locked names only.

Draw or paste mermaid/ASCII for `BayPayCell`. Must show: `dmgr-east`, `node-pay-1`, `node-pay-2`, `node-ref-1`, node agents, `Pay1` / `Pay2` / `Pay3`, `Ref1` / `Ref2`, and `ihs-east` **outside** the cell.

```text
(your drawing)
```

| Path | Hops (your words) |
|---|---|
| Serving (Avery Chen `11111111-1111-1111-1111-111111111111` → money) | |
| Control (Morgan Hale → config) | |

| Cluster | Member | Node | Application | Context |
|---|---|---|---|---|
| `PaymentCluster` | `Pay1` | | | |
| `PaymentCluster` | `Pay2` | | | |
| `PaymentCluster` | `Pay3` | | | |
| `RefundCluster` | `Ref1` | | | |
| `RefundCluster` | `Ref2` | | | |

| Bind | Smell or note |
|---|---|
| `jdbc/baypay` | |
| `jdbc/baypayXA` | |
| `baypayDbAlias` | |
| SIBus `BayPayBus` | |
| `jms/paymentEvents` / `jms/refundEvents` | |

Why is `dmgr-east` down a change-freeze and not a Harbor Market outage?

---

## 2. Target estate (AEJE-D-072)

Cite **AEJE-D-072**. This is not “the cell, but in Kubernetes.”

| Element on AEJE-D-072 | What you mapped it to (process, object, or file) |
|---|---|
| Merchants TLS / edge | |
| `payment-service` `:8080` | |
| Secrets | |
| Teaching DB | |

One paragraph: what is **absent** from AEJE-D-072 (`dmgr-east`, node agents, cell JNDI, SIBus) and why that absence is the point.

---

## 3. Liberty waves (0–3)

Wave numbers and rollback one-liners must match TOPOLOGY.md. Wave 1 names `refund.ear` / `RefundCluster`. Wave 2 names a **single** Liberty payment replica behind `ihs-east`. Wave 3 keeps a last ND backup until **wave 3 + 14 days**.

| Wave | Scope (your words, locked names) | Success signal | Rollback | Who calls rollback |
|---|---|---|---|---|
| 0 | | | N/A | |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

Liberty features you expect (`servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`) and isolated binds (`jdbc/baypay-payment`, `jdbc/baypay-refund`):

Why Wave 1 is refund, not payment (4–6 sentences):

---

## 4. Wave 1 rollback card (refund)

Assume Harbor Market refund volume is already on Liberty `refund-service.war` and error rate or latency breaches the hold.

```text
Evidence to collect:
Drain / traffic action at ihs-east:
Restore on ND:
Confirm:
Re-enter Liberty only when:
Never:
```

What exactly is restored onto `RefundCluster`? Is “bounce `dmgr-east`” on this card? It must not be.

---

## 5. Wave 2 rollback card (payment canary)

Avery Chen may be in the canary bucket. Money stays on `PaymentCluster` if the Liberty replica misbehaves.

```text
Evidence to collect:
Drain the canary (plugin / IHS):
What stays at 100%:
What you do not bounce:
Confirm edition / JNDI on ND:
Re-enter canary only when:
Never:
```

How does `ihs-east` send a **fraction** of `/payment` without sticky `JSESSIONID`?

What JNDI name does the canary use, and which cell-wide name must it **not** reuse?

---

## 6. Container design (paper)

| Field | Your answer |
|---|---|
| Image name | |
| Build-stage base | |
| Runtime-stage base (must not be a full JDK) | |
| UID | |
| Port | |
| Where `BAYPAY_DB_*` live | |
| `JAVA_TOOL_OPTIONS` / heap story | |
| Why `-Xmx` must **not** equal the container / cgroup limit | |

One paragraph: why packaging `dmgr-east` or a WAS profile in Docker is **not** modernization.

---

## 7. Kubernetes / OpenShift design (paper)

Use CLUSTER.md names. Sketch intended `baypay-prod` objects. Placeholders only for secrets (`${BAYPAY_DB_PASSWORD}`, `***`).

```yaml
# namespace / Project, Deployment labels, Service selector,
# Ingress host or Route payment-route, ConfigMap, Secret keys, probes
```

| Question | Your answer |
|---|---|
| Replicas when healthy | |
| Probe paths (liveness vs readiness) | |
| Ingress vs OpenShift Route — same job or different product? | |
| What you would **not** schedule as a Pod | |

---

## 8. Test and rollback plan

No live ND or required kind/OCP. Name the tests.

| Gate | What you test | Pass signal | Rollback if red |
|---|---|---|---|
| Before Wave 1 | | | |
| Wave 1 hold | | | |
| Before Wave 2 (include create / replay / frozen `…222`) | | | |
| Wave 2 canary hold | | | |
| Probes on target | | | |
| Wave 3 + 14-day backup drill | | | |
| Heap vs memory limit | | | |

Optional engine you actually ran (if any) — one line:

---

## 9. What you would NOT do

In 8–12 sentences, refuse: a new traditional ND cell as a “safe rollback environment,” ND-in-Docker, cell-wide `jdbc/baypay` on Liberty, SIBus recreation as a goal, sticky payment sessions, bouncing `dmgr-east`, `-Xmx` equal to the cgroup limit, and any required paid OpenShift or AWS apply for this capstone. Name Boot or Liberty as the exit. Cite AEJE-D-071 as current and AEJE-D-072 as target.

---

## 10. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, Morgan Hale, Jordan Voss, and Sam Okada, in one sitting, why Wave 1 is refund, why Wave 2 is a canary rather than a cluster flip, why the image is `payment-service` and not `BayPayCell`, and why this page costs $0.

---

## Honesty

- [ ] I did not open `solutions/CAPSTONE-2/` before I wrote waves and the ND-in-Docker refusal
- [ ] Every cell name comes from TOPOLOGY.md
- [ ] Every kube name comes from CLUSTER.md
- [ ] I cited AEJE-D-071 as current and AEJE-D-072 as target
- [ ] Wave 1 is refund; Wave 2 is one payment canary
- [ ] I did not recommend a new traditional ND cell
- [ ] I did not recommend ND-in-Docker
- [ ] I did not set `-Xmx` equal to a container / cgroup limit
- [ ] I did not put a live password in this file
- [ ] I did not require Docker, kind, or OCP to claim I finished
