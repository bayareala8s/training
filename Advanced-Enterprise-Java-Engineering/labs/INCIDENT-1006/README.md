# INCIDENT-1006 — Service routing failure

**Type:** INCIDENT  
**Module:** 10 — Kubernetes and OpenShift  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/kubernetes/INC-K8S-1006](../../incidents/kubernetes/INC-K8S-1006/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

11:33 Pacific on a synthetic `baypay-prod` late morning in November 2026. Harbor Market reports HTTP 503 on `payments.apps.baypay.example` after a label cleanup. The pager names `payment-service`. Teaching-cluster paste shows an Ingress and a Service. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. A 503 from Ingress is not a domain decline. Finance does not care that the Deployment lists three replicas. They care that the Service selected zero pods.

Do not bounce Postgres. Do not bounce `dmgr-east`. Intended labels live in [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). A live cluster is **not** required.

---

## Learning objectives

- Follow gated evidence: Service YAML first, then Deployment labels, then Endpoints.
- Treat **empty Endpoints** as a selector story you still have to prove, not as “the app is down.”
- Separate Ready-but-unselected pods from Ready-0 probe failures (INCIDENT-1003).
- Write stabilization that aligns selector and labels without a cluster-wide delete.
- Produce a comms update that does not invent a CrashLoop the files do not show.

---

## Architecture

```text
Merchants / Avery Chen
  → Ingress payments.apps.baypay.example
       → Service payment-service
            spec.selector   (must match pod labels)
            → Endpoints
                 → Pods from Deployment payment-service
                      metadata.labels
```

A Service is a label query. You do not need a live cluster. The contracts are selector keys, pod labels, and whether Endpoints list addresses. OpenShift Route `payment-route` uses the same Service in CLUSTER.md.

---

## Prerequisites

- Locked cluster names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md).
- Incident worksheet: [student-worksheet.md](../../incidents/kubernetes/INC-K8S-1006/student-worksheet.md).
- Optional PAKS: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`. Lessons stand alone without it.
- You may read INCIDENT-1003 first so you can say why this pack is or is not a probe story.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/kubernetes/INC-K8S-1006/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is Service YAML. Gate 2 is Deployment labels. Gate 3 is Endpoints. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1006/` until you have filled the worksheet through remediation.

Do not run `kubectl` against a paid or shared cluster. The files are the cluster.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note who changed labels, and when 503s began.
2. **Gate 1:** open `evidence/service.yaml` only. Record `spec.selector`. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/deploy-labels.yaml`. Update the hypothesis. Quote pod labels; do not close the RCA on “503” alone.
4. **Gate 3:** open `evidence/endpoints.txt` only if it answers a question you already wrote about selection.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence on kustomize `commonLabels` versus a policy test that selector equals pod labels — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “selector mismatch” with no quoted selector and label pair scores low on Diagnostic method (see rubric). Skipping to Endpoints before a written question also scores low. Opening the solution first fails Diagnostic method.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Ingress 503 and pods look fine: the Service may not select them. Table selector versus labels.
- You want `describe` probes: they are omitted. Write how you would tell this apart from INCIDENT-1003.
- You are about to bounce Postgres or delete the Ingress: re-read CLUSTER.md.
- You want to change every label in the namespace: write the blast radius. Prefer aligning the pair that Endpoints use.
- You copied INCIDENT-1003’s 404 probe: this pack’s first file is Service YAML, not probe status.
- You copied INCIDENT-1001’s CrashLoop: three Ready replicas can still have empty Endpoints.
- You want to `kubectl apply` a live fix: write the change on paper. This lab does not require a cluster.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which label key is wrong.

---

## Interview questions

1. Why is “the Deployment has replicas” a weak first sentence when Endpoints are empty?
2. What does a Service `selector` actually query?
3. Why can Ingress return 503 while every pod is Ready?
4. When do you change the Service selector versus relabel the pods?
5. How would a policy test catch this before merchants see 503?

---

## Architecture/trade-off questions

1. kustomize `commonLabels` versus hand-edited selectors — who owns the single source of labels?
2. Should a CI test apply the YAML to a dry-run and assert Endpoints length greater than zero?
3. Why is renaming `app=payment` to `app=payment-service` a two-object change, not one?
4. What do you lose if you select on a unique-per-roll hash that the Service never updates?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API. No paid OpenShift.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1006/` and `instructor/rubrics/INCIDENT-1006.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

A Service is a label query, not a Deployment name. Selector, pod labels, and empty Endpoints have to be read together. Stabilization (align selector and labels) is a different sentence from remediation (kustomize `commonLabels`; policy test). A lucky “routing” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-K8S-1006 worksheet to your notes if this is the Module 10 incident you will write up. The Module 10 portfolio artifact is [student/worksheets/PF-k8s.md](../../student/worksheets/PF-k8s.md): you pick **one** of INCIDENT-1001 through INCIDENT-1006 and write the scored RCA plus a healthy YAML sketch there.
