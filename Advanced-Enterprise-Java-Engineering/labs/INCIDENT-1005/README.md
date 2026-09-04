# INCIDENT-1005 — TLS / certificate issue

**Type:** INCIDENT  
**Module:** 10 — Kubernetes and OpenShift  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/kubernetes/INC-K8S-1005](../../incidents/kubernetes/INC-K8S-1005/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

08:05 Pacific on a synthetic `baypay-prod` morning in November 2026. Harbor Market browsers fail the handshake to `payments.apps.baypay.example`. The pager names Ingress TLS. Teaching-cluster paste shows pods Ready. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) never reaches `POST /api/v1/payments` if TLS dies at the edge. Finance does not care that Ready is 1/1. They care that merchants cannot complete a handshake.

Do not bounce Postgres. Do not bounce `dmgr-east`. Do not paste a private key into the worksheet. Locked names live in [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). A live cluster is **not** required.

---

## Learning objectives

- Follow gated evidence: Ingress YAML first, then openssl dates, then the client curl paste.
- Treat **Ready pods** as an application fact, not as proof the edge certificate works.
- Separate expired `notAfter` from a host / CN mismatch when both appear.
- Write stabilization that rotates the cert or fixes the host without restarting healthy pods first.
- Produce a comms update that does not invent a CrashLoop the describe files do not show.

---

## Architecture

```text
Merchants / Avery Chen
  → TLS  (secret payment-tls)
       → Ingress host payments.apps.baypay.example
            → Service payment-service
                 → Ready pods (see pack)
```

OpenShift Route `payment-route` is the same host in CLUSTER.md. This pack uses Ingress TLS. You do not need a live cluster. The contracts are `secretName`, `notAfter`, subject CN, and the curl error. Application logs may be silent.

---

## Prerequisites

- Locked cluster names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md).
- Incident worksheet: [student-worksheet.md](../../incidents/kubernetes/INC-K8S-1005/student-worksheet.md).
- Optional PAKS: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`. Lessons stand alone without it.
- You do not need cert-manager installed. Write it as a remediating control if the evidence supports expiry.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/kubernetes/INC-K8S-1005/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is Ingress YAML. Gate 2 is openssl dates. Gate 3 is a TLS curl paste. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1005/` until you have filled the worksheet through remediation.

Do not run `kubectl` against a paid or shared cluster. The files are the cluster.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note when the certificate was last issued, and when browsers failed.
2. **Gate 1:** open `evidence/ingress.yaml` only. Record host, `secretName`, and backend Service. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/openssl-dates.txt`. Update the hypothesis. Quote `notAfter` and subject; do not close the RCA on “TLS” alone.
4. **Gate 3:** open `evidence/curl-tls.txt` only if it answers a question you already wrote about the client handshake.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence on cert-manager or expiry alerts versus a calendar reminder — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “expired cert” with no host/CN or `notAfter` quote scores low on Diagnostic method (see rubric). Skipping to curl before a written question also scores low. Opening the solution first fails Diagnostic method.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Pods are Ready and merchants fail: the edge can fail while the app is healthy. Table it.
- You want application logs: they are omitted. Write why a handshake failure might never reach Spring.
- You are about to bounce Postgres or the Deployment: re-read CLUSTER.md.
- You want to disable TLS to “restore HTTP”: write the compliance cost. That is not the first stabilize sentence.
- You copied INCIDENT-1003’s 503 story: handshake errors are not HTTP 503.
- You copied INCIDENT-1001’s CrashLoop: Ready 1/1 contradicts a restart loop.
- You want to `kubectl apply` a live cert: write the rotation on paper. This lab does not require a cluster. No private keys.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you whether expiry or name mismatch is the first sentence.

---

## Interview questions

1. Why is “the pods are Ready” a weak first sentence when the client never completes TLS?
2. What does `notAfter` in the past prove that a 503 would not?
3. Why can CN=`*.baypay.internal` fail for host `payments.apps.baypay.example` even if the cert is unexpired?
4. When do you rotate the Secret versus change the Ingress host?
5. What belongs in a merchant-safe note when the failure is a handshake?

---

## Architecture/trade-off questions

1. cert-manager versus a ticket that expires with the cert — who owns the calendar?
2. Should Ingress and OpenShift Route share one Secret, or is a split a blast-radius control?
3. Why is “turn off TLS for an hour” a security incident even if it restores HTTP 201?
4. What alert would you page on at 14 days, and what do you accept as noise?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete. Do not keep a generated private key.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API. No paid OpenShift. No public CA purchase.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1005/` and `instructor/rubrics/INCIDENT-1005.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Ready pods do not prove the edge certificate. Ingress host, `notAfter`, subject CN, and the client handshake have to be read together. Stabilization (rotate the cert or fix the host) is a different sentence from remediation (cert-manager or expiry alerts). A lucky “TLS” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-K8S-1005 worksheet to your notes if this is the Module 10 incident you will write up. The Module 10 portfolio artifact is [student/worksheets/PF-k8s.md](../../student/worksheets/PF-k8s.md): you pick **one** of INCIDENT-1001 through INCIDENT-1006 and write the scored RCA plus a healthy YAML sketch there.
