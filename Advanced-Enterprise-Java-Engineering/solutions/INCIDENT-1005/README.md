# INCIDENT-1005 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Ingress TLS Secret `payment-tls` serves host `payments.apps.baypay.example`. The certificate **expired** (`notAfter=15 Oct 2026`; page is **17 Nov 2026**). Subject **CN=`*.baypay.internal`** does not match `payments.apps.baypay.example` (SAN has only `*.baypay.internal` / `payment.baypay.internal`). Browsers and curl fail the **handshake** (`curl: (60) certificate has expired`, plus name mismatch). **Pods are Ready.** Spring is never reached.

Either expiry or the CN/host miss would fail clients. Students should quote **both**. This is not INCIDENT-1003 (HTTP 503 after handshake) and not a CrashLoop.

## Stabilization

1. **Rotate** Secret `payment-tls` with a cert that is unexpired **and** whose SAN includes `payments.apps.baypay.example`, **or** fix the Ingress host to a name the cert actually covers (not the first choice if merchants already use the apps host).
2. Do **not** disable TLS to restore HTTP.
3. Do not bounce Ready pods or Postgres.
4. Do not bounce `dmgr-east`.
5. Do not paste `tls.key` into the bridge.

## Remediation

- **cert-manager** (or equivalent) plus **expiry alerts** (page at 14 days, not a spreadsheet row).
- Same host on Ingress and OpenShift Route `payment-route`; one rotation runbook.
- SAN must include `payments.apps.baypay.example`. Wildcard `*.baypay.internal` is a different DNS tree.
- Store the key in the platform secret store; teaching YAML uses `${PAYMENT_TLS_CERT_PEM}` / `${PAYMENT_TLS_KEY_PEM}`.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| ingress.yaml | host `payments.apps.baypay.example`; `secretName: payment-tls` |
| openssl-dates.txt | `notAfter=Oct 15 2026`; CN=`*.baypay.internal`; host not in SAN |
| curl-tls.txt | curl 60 expired; subject CN; no HTTP status |

A worksheet that says only “TLS” without `notAfter` or CN versus host scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on `payments.apps.baypay.example`. Clients fail the TLS handshake. Pods remain Ready. The Ingress certificate is expired and the name does not match the payments host. We are rotating `payment-tls`. We are not turning TLS off. Next update 20 minutes.
