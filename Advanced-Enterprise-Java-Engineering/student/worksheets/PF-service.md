# Portfolio — BayPay payment service (list-by-customer)

**Artifact:** [CAPSTONE-1](../../capstones/01-build-baypay/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**After:** Modules 1–3  
**Diagram:** AEJE-D-071 (current WebSphere estate — cite as what you did **not** rebuild)  
**Reference app:** `reference-apps/baypay` (Java 21, Spring Boot 3.5.5)

Export this page (or a copy) as your CAPSTONE-1 portfolio artifact. Fill every section in your own words. Do not paste instructor solution text. Do not put PAN, CVV, access keys, or `BAYPAY_DB_PASSWORD` in this file.

**Your name:**  
**Date:**  
**Cohort / reviewer (if any):**  
**Reference commit / branch:**  

---

## 1. Baseline proof

Record the command you ran **before** you claimed the list was done.

| Field | Your answer |
|---|---|
| `JAVA_HOME` you used | |
| Working directory | |
| Command (`./mvnw test`) | |
| Result (green / red, suite names) | |
| `PaymentApiIT` still green after your list? | |

One paragraph: what was already true about POST create and GET by id before you added anything.

---

## 2. The gap you named

`PaymentController` shipped with POST create and GET by id. It did **not** list by customer.

| Field | Your answer |
|---|---|
| File you opened first | |
| Methods you found | |
| Repository methods you found | |
| Why Harbor Market cannot use GET-by-id alone for Avery’s statement | |

Avery Chen `11111111-1111-1111-1111-111111111111` · active account `22222222-2222-2222-2222-222222222221` · frozen `22222222-2222-2222-2222-222222222222`.

---

## 3. List-by-customer contract

Cite the path `GET /api/v1/payments?customerId=`.

| Case | Status + body you implemented | Test name |
|---|---|---|
| Avery with two (or more) payments | | |
| Known customer, zero payments | | |
| Missing `customerId` | | |
| Unparseable UUID | | |
| Unknown customer UUID | | |
| Sort (teaching: newest first) | | |

Bean Validation (or equivalent) — where does it live, and what handler returns `400`?

Why is there **no** unfiltered `GET /api/v1/payments`?

---

## 4. POST contracts you refused to drop

| Contract | Still true? (yes/no + evidence) |
|---|---|
| `Idempotency-Key` required | |
| First create `201` + `COMPLETED` (happy path) | |
| Identical replay `200` + same `paymentId` | |
| Same key, different body `409` `IDEMPOTENCY_CONFLICT` | |
| Frozen account `422` + `DECLINED` | |
| Missing key `400` `IDEMPOTENCY_KEY_REQUIRED` | |
| GET by id `200` / `404` `PAYMENT_NOT_FOUND` | |

Canonical hash string (field order):

```text
(your words)
```

---

## 5. Logs you refused

| Field or habit | Why you refused it |
|---|---|
| PAN / full card number | |
| CVV / expiry | |
| Raw create JSON `toString()` | |
| Dumping every payment row to INFO | |

What you **do** log (paymentId, correlation id, status):

One paragraph: why Avery’s UUID on a list query is not a PAN, and why that still does not belong on a Micrometer label in later modules.

---

## 6. Estate you did not rebuild

Cite **AEJE-D-071**. Traditional ND is the source estate.

| Locked name | What it is | Why it is not this capstone’s runtime |
|---|---|---|
| `BayPayCell` | | |
| `dmgr-east` | | |
| `PaymentCluster` | | |
| `ihs-east` | | |

One sentence: what you would tell Jordan Voss who asks for “an ear on Pay1 so the list matches the diagram.”

---

## 7. Excerpt (short)

Paste **only** the list method signature plus five to fifteen lines, or describe it. No full module dump. No secrets.

```text
(your excerpt)
```

IT class and method names you added:

---

## 8. Interview snippet (Staff, 6–8 sentences)

Explain to Priya Nair, Riley Okonkwo, and Jordan Voss, in one sitting, how Harbor Market lists Avery Chen’s payments, why POST still requires `Idempotency-Key`, and why AEJE-D-071 is inventory you are leaving rather than the service you just shipped.

---

## Honesty

- [ ] I ran `./mvnw test` in `reference-apps/baypay` with Java 21 / `JAVA_HOME`
- [ ] I did not open `solutions/CAPSTONE-1/` before I had my own list test
- [ ] I did not paste instructor Java as my only implementation
- [ ] POST still requires `Idempotency-Key`
- [ ] I did not log PAN, CVV, or a live password
- [ ] I did not install WebSphere ND or put the list on `PaymentCluster`
- [ ] I did not create a second Spring app
- [ ] I did not set `-Xmx` equal to a container / cgroup limit as the run story
