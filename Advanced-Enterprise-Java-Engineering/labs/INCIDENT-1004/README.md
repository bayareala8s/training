# INCIDENT-1004 — Bad Secret

**Type:** INCIDENT  
**Module:** 10 — Kubernetes and OpenShift  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/kubernetes/INC-K8S-1004](../../incidents/kubernetes/INC-K8S-1004/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

13:18 Pacific on a synthetic `baypay-prod` afternoon in November 2026. Harbor Market reports create-payment failures after a Secret change window. The pager names `payment-service`. Teaching-cluster paste shows a Secret named `baypay-db` and pods that start, then fail to talk to the database — or fail fast on datasource bind. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. An empty or missing password is not a domain decline. Finance does not care that the Secret object exists. They care that the process received the **name** it was written to read.

Do not bounce Postgres to “refresh credentials.” Do not bounce `dmgr-east`. Do not write a real password into your worksheet. Locked names live in [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). A live cluster is **not** required.

---

## Learning objectives

- Follow gated evidence: Secret **keys** first (values redacted), then logs, then Deployment env YAML.
- Treat “the Secret is present” as existence, not as a matching env contract.
- Separate CreateContainerConfigError from an app that started with an empty password.
- Write stabilization that restores the key or the `env.valueFrom` mapping without committing a live secret.
- Produce a comms update that never pastes a password.

---

## Architecture

```text
Merchants / Avery Chen
  → Ingress payments.apps.baypay.example
       → Service payment-service
            → Deployment env
                 name: BAYPAY_DB_PASSWORD  (process contract)
                 valueFrom.secretKeyRef    (key name in baypay-db)
            → Secret baypay-db             (keys only in this pack)
                 → Spring datasource password
                 → baypay DB
```

The process reads `BAYPAY_DB_PASSWORD`. Kubernetes injects whatever **key** the Deployment names. You do not need a live cluster. The contracts are key names, env names, and the log line after start. Never decode Secret values in this course.

---

## Prerequisites

- Locked cluster names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md).
- Incident worksheet: [student-worksheet.md](../../incidents/kubernetes/INC-K8S-1004/student-worksheet.md).
- Optional PAKS: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`. Lessons stand alone without it.
- You may reread Module 6 `BAYPAY_DB_*` naming. This pack is the kube injection of those names.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/kubernetes/INC-K8S-1004/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is Secret keys with values as `***`. Gate 2 is logs. Gate 3 is Deployment env YAML. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1004/` until you have filled the worksheet through remediation.

Do not run `kubectl` against a paid or shared cluster. The files are the cluster. Do not invent a password.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note who changed the Secret, and when failures began.
2. **Gate 1:** open `evidence/secret-keys.txt` only. Record key **names**. Do not guess values. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote bind or auth lines; do not promote “bad Secret” to a closed RCA without the env mapping.
4. **Gate 3:** open `evidence/deployment-env.yaml` only if it answers a question you already wrote about env name versus Secret key.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence on a contract test or Kyverno rule for required keys — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “wrong key” with no env-name-versus-Secret-key table scores low on Diagnostic method (see rubric). Pasting a fabricated password fails Security. Opening the solution first fails Diagnostic method.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- The Secret exists and the app still fails: existence is not a key match. Table the names.
- You want the decoded value: it is not in this pack. Write `***` and move on.
- You are about to bounce Postgres or rotate the DB role: re-read CLUSTER.md. This pack is injection, not a stolen password.
- You want to commit `changeme` into git as a “fix”: that fails Security / reliability.
- You copied INCIDENT-1001’s missing ConfigMap URL: check whether logs are bind-on-password or bind-on-url.
- You assume CreateContainerConfigError: the pack may show a started JVM. Quote last State.
- You want to `kubectl apply` a live fix: write the change on paper. This lab does not require a cluster.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which key name is wrong.

---

## Interview questions

1. Why is “the Secret is mounted” a weak first sentence when the process reads a different env name?
2. What is the difference between `env.name` and `secretKeyRef.key`?
3. Why can `optional: true` turn a missing key into an empty password instead of a blocked pod?
4. When do you add the correct key to the Secret versus change the Deployment mapping?
5. Why must a worksheet never contain a live password even in a fictional estate?

---

## Architecture/trade-off questions

1. Contract test / Kyverno versus a human checklist for required Secret keys — who owns the gate?
2. `envFrom` versus explicit `env.valueFrom` — what do you gain and what name collisions do you accept?
3. Why is “never commit real secrets” still true when the course only uses `changeme` / `${}` / `***`?
4. Should the app fail-fast on empty `BAYPAY_DB_PASSWORD`, or is a Postgres auth error an acceptable start?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete. Delete any local note that accidentally contains a guessed password.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API. No paid OpenShift.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1004/` and `instructor/rubrics/INCIDENT-1004.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

A Secret object is not a password contract. Key names, env names, and the log after start have to be read together. Stabilization (add the correct key or fix `env.valueFrom`) is a different sentence from remediation (contract test / Kyverno; never commit real secrets). A lucky “bad Secret” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-K8S-1004 worksheet to your notes if this is the Module 10 incident you will write up. The Module 10 portfolio artifact is [student/worksheets/PF-k8s.md](../../student/worksheets/PF-k8s.md): you pick **one** of INCIDENT-1001 through INCIDENT-1006 and write the scored RCA plus a healthy YAML sketch there.
