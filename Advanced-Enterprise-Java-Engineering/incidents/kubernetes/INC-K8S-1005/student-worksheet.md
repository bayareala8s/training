# INC-K8S-1005 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions. No private keys.

**Incident:** TLS handshake failures on payments host  
**Namespace:** `baypay-prod`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Ingress is wired correctly for CLUSTER: host `payments.apps.baypay.example`, `secretName: payment-tls`, backend `payment-service:8080`. Pods Ready 3/3 (timeline) — this is **not** INC-1001/1003. Merchants fail **before HTTP**. Sam issued `payment-tls` 2025-08-01 (BAYPAY-8810) with a **spreadsheet reminder**. Incident 2026-11-17 — first suspect is **expiry** (`notAfter` in the past). Second suspect is **name mismatch** (cert CN/SAN vs this host). Next: openssl dates/subject on `payment-tls`. Then curl only to confirm the client handshake error (expiry vs hostname).

Gate 2: **Both** defects, expiry first in time. `notAfter=Oct 15 23:59:59 2026 GMT` — page is **2026-11-17**, cert already dead. Subject **CN=`*.baypay.internal`**; SAN is only `*.baypay.internal` and `payment.baypay.internal`. Ingress host `payments.apps.baypay.example` is **not** in SAN. `notBefore=Aug 1 2025` matches Sam’s issue date. Question for gate 3: does client curl fail the **handshake** (typical curl **60** — expired and/or hostname) with **no HTTP status**, confirming Ready pods never see Avery? If yes, do not bounce Deployment/Postgres and do not disable TLS.

Gate 3: Yes. `curl: (60) SSL certificate problem: certificate has expired`. Same handshake also: `SSL: no alternative certificate subject name matches target host name 'payments.apps.baypay.example'`. **No HTTP status.** Avery `c1005e55-…-111005` stayed in the browser. RCA: Secret `payment-tls` is an **expired internal wildcard**, not a merchant-host cert. Ready pods unused. Not CrashLoop, not Ingress 503.

## Supporting evidence

(File, timestamp, quote. Ingress host, secretName, notAfter, subject CN, curl error.)

- `timeline.json` 2025-08-01 Sam: issued teaching cert into `payment-tls` (BAYPAY-8810); calendar = spreadsheet, not an alert. 2026-11-17 15:48Z Priya: Ready 3/3; fail before HTTP. 16:05Z pager handshake. 16:07Z Harbor Market / Avery certificate warning. 16:08Z Riley: do not disable TLS; do not paste `tls.key`.
- Gate 1 `evidence/ingress.yaml`: host `payments.apps.baypay.example`; `secretName: payment-tls`; backend `payment-service:8080`.
- Gate 2 `evidence/openssl-dates.txt`: `notAfter=Oct 15 23:59:59 2026 GMT`; `CN = *.baypay.internal`; SAN `*.baypay.internal`, `payment.baypay.internal`.
- Gate 3 `evidence/curl-tls.txt` 16:11Z: `curl: (60) … certificate has expired`; hostname mismatch line; no HTTP status.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: openssl dates/subject (gate 2) — expiry vs CN/SAN vs Ingress host. After gate 2: client curl (gate 3) — handshake error 60 vs HTTP 503. Omitted app logs: handshake never reaches Spring; silence is expected. Omitted describe: timeline already Ready 3/3. `tls.key` omitted forever — do not generate one. OpenShift Route `payment-route` shares the host — same Secret after rotate.

## Stabilization action

(What restores the handshake *now*? Rotate versus host? What do you explicitly not do?)

**Rotate** Secret `payment-tls` with a new cert whose SAN includes `payments.apps.baypay.example` (and the Route host). Do **not** change the Ingress host to `*.baypay.internal` — merchants use the apps name. Do **not** restart Ready pods first. Do **not** bounce Postgres / `dmgr-east`. Do **not** disable TLS to restore HTTP 201 (that is a second incident). Do **not** paste `tls.key`. Paper rotate only.

## Remediation

(What remains after the page is quiet?)

**cert-manager** (or equivalent) owns renewal — not a spreadsheet row on BAYPAY-8810. Page at **14 days** before `notAfter` (accept some noise). New certs need **merchant SAN**, not only `*.baypay.internal`. Ingress and Route may share `payment-tls` (one rotate) or split (smaller blast radius, two calendars). HTTP-only is not a strategy.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 `payments.apps.baypay.example`: TLS handshake fails. Harbor Market / Avery `c1005e55-…-111005` never left the browser (certificate warning).  
Pods **Ready 3/3**. Not CrashLoop, not Ingress 503 — no HTTP status.  
Secret `payment-tls`: `notAfter` **15 Oct 2026** (page 17 Nov); CN/SAN `*.baypay.internal` — host not on the cert.  
Rotating `payment-tls` with merchant SAN. TLS stays on. No `tls.key` in Slack.  
Not bouncing the Deployment or the database. Next update when curl completes the handshake.
