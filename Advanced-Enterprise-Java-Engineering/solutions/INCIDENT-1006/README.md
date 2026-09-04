# INCIDENT-1006 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Service `payment-service` `spec.selector` is **`app=payment`**. After Sam Okada’s label cleanup (BAYPAY-10066), Deployment / pod labels are **`app=payment-service`** (CLUSTER.md intended). The Service selects **zero** pods. **Endpoints are empty.** Ingress returns **503**.

Pods are **Ready 1/1**. This is not INCIDENT-1003 (probe 404, Ready 0/1). The Deployment’s own `matchLabels` match its pods; only the Service selector was left on the old value.

## Stabilization

1. **Align** Service selector to `app=payment-service` **or** relabel pods to `app=payment` — prefer the CLUSTER.md name `app=payment-service` and change the Service.
2. Confirm Endpoints list three addresses, then retest Ingress.
3. Do **not** delete the Ingress.
4. Do not bounce Postgres.
5. Do not bounce `dmgr-east`.
6. Do not change every label in the namespace in one unreviewed apply.

## Remediation

- **kustomize `commonLabels`** (or one overlay) so Service selector and pod labels cannot drift.
- **Policy test**: apply YAML in CI and assert Endpoints length > 0 (or a unit test that selector equals `template.metadata.labels`).
- Label renames are a **two-object** change: Deployment and Service (and Route/Ingress backends stay on the Service name).
- Do not select on a unique-per-roll hash the Service never updates.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| service.yaml | `selector.app: payment` |
| deploy-labels.yaml | pod / template labels `app: payment-service`; Ready 1/1 × 3 |
| endpoints.txt | `subsets: []` / ENDPOINTS none |

A worksheet that says only “selector mismatch” without quoting both values scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `payments.apps.baypay.example`. Ingress 503. Service Endpoints are empty. Pods are Ready; the Service selector does not match pod labels. We are aligning selector and labels. Database is not being bounced. Next update 20 minutes.
