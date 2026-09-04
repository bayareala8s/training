# Portfolio worksheet — Java domain model excerpt

**Artifact:** Module 1 / [BUILD-101](../../labs/BUILD-101/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste secrets; all BayPay data is synthetic.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | |
| JDK used (`java -version`) | |
| Reference commit or branch | |

---

## 2. Bounded context

In 4–6 sentences, explain what a BayPay **payment** is (lifecycle, not a single INSERT). Mention the happy path and the three failure/reversal words.

---

## 3. Entities and values

| Spec name | Java type | Value or entity? | One invariant |
|---|---|---|---|
| Customer | | | |
| Account | | | |
| Payment | | | |
| Refund | | | |
| Transaction | `LedgerTransaction` | | |
| TransactionEvent | | | |
| AuditEvent | | | |
| Money | | | |

Why is the ledger row not named `Transaction` in Java?

---

## 4. Money rules

- Allowed currencies:
- Amount constraint:
- How `equals` / `hashCode` treat `10.0` vs `10.00`:
- What `plus` does on a USD + EUR pair:

---

## 5. Payment state machine

Complete the table.

| From | Allowed next | Terminal? |
|---|---|---|
| RECEIVED | | |
| VALIDATING | | |
| AUTHORIZED | | |
| PROCESSING | | |
| COMPLETED | | |
| DECLINED | | |
| FAILED | | |
| REVERSED | | |

Why is `public void setStatus(PaymentStatus status)` forbidden?

---

## 6. Demo fixtures (synthetic)

| Role | UUID | What the model must do |
|---|---|---|
| Avery Chen | `11111111-1111-1111-1111-111111111111` | |
| Active account | `22222222-2222-2222-2222-222222222221` | |
| Frozen account | `22222222-2222-2222-2222-222222222222` | |

---

## 7. Writes

What header is required on payment and refund creates? What happens on (a) same key and same body, (b) same key and different body, (c) missing key?

---

## 8. Validation outcomes (BUILD-102)

| Situation | Throw or decline? | Code / reason |
|---|---|---|
| Amount ≤ 0 or `JPY` | | |
| Unknown customer | | |
| Account not Avery’s | | |
| Avery frozen + valid USD | | |
| Amount `1000000.01` | | |

---

## 9. Excerpt

Paste **short** constructors / `allowedNext` / `transitionTo` from *your* lab types (not a whole module dump). Ten to forty lines is enough.

---

## 10. Defense (interview)

Write a Senior-level paragraph (not a Principal essay) that answers: “How do you keep BayPay from completing a payment that was never authorized?”

Then add two sentences a Staff engineer would add (operations, extraction, or audit).
