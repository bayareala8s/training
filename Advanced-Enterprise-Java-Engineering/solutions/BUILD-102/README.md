# BUILD-102 — Instructor solution

Production split:

1. **Load** customer and account (`Optional` → `ResourceNotFoundException`).
2. **Own** — `account.belongsTo(customerId)` or `ACCOUNT_CUSTOMER_MISMATCH`.
3. **Construct `Money`** — throws `DomainValidationException` for amount/currency.
4. **Decide** — `PaymentAuthorizer.DefaultPaymentAuthorizer`:
   - not `ACTIVE` → decline `"account is not ACTIVE"`
   - currency mismatch → decline
   - amount `> 1000000.00` → decline
   - else approve

Declines are not exceptions. Missing rows are.

See `PaymentValidator.java` in this folder. Demo fixtures:

| | |
|---|---|
| Avery | `11111111-1111-1111-1111-111111111111` |
| Active | `22222222-2222-2222-2222-222222222221` / `ACTIVE` / `USD` |
| Frozen | `22222222-2222-2222-2222-222222222222` / `FROZEN` / `USD` |

## Tests you can run mentally

- Avery + active + `25.00` + `USD` → approve.
- Avery + frozen + `25.00` + `USD` → decline `ACCOUNT_NOT_ACTIVE`.
- Empty customer Optional → throw `CUSTOMER_NOT_FOUND`.
- Active account whose `customerId` is not Avery → throw `ACCOUNT_CUSTOMER_MISMATCH`.
- `JPY` → throw `VALIDATION_FAILED`.
- `0.00` → throw.
- `1000000.00` → approve; `1000000.01` → decline ceiling.

## Common misses

- Treating freeze as not-found (or the reverse).
- `orElse(null)` then NPE.
- Accepting `usd`.
- Inclusive ceiling (`>=` instead of `>`).
- Catching `Exception` to return decline.
