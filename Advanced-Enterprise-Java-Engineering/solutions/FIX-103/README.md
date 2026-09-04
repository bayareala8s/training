# FIX-103 — Instructor solution

**Do not walk the room to this list in the first 20 minutes.** Students should inventory smells first.

## Root causes in `MessyPaymentValidator`

The contractor’s class fails closed only by accident, and sometimes fails *open* after an internal error.

1. **God method.** One `validate` performs parsing, currency policy, ownership, status, ceiling, and caching.
2. **Raw types.** `List scratch` and `Map cache` accept anything; they also retain request data on the instance.
3. **Mutable shared state.** `lastOk` / `lastReason` are public and reused. Two calls on one instance race (Module 2) and tests become order-dependent.
4. **Swallowed exceptions.** The outer `catch (Exception e) { return false; }` turns a null amount (`ClassCastException` / NPE) into a boolean. The inner catch around status ignores a null status and may leave `lastOk == true`.
5. **Null-unsafe.** `(BigDecimal) amount` then `parsed.doubleValue()`; `customerId.toString()`; `accountStatus.toString()`.
6. **String identity.** `ccy == "USD"` and `toLowerCase() != "active"` compare references. Interning makes demos lie.
7. **`double` money.** `parsed.doubleValue() <= 0` and `> 1000000.0d` drift.
8. **Case folding.** `"usd"` is accepted; production `Money` rejects it.

The intended business rules remain BUILD-102: throw (or fail loudly) on bad money / mismatch; **decline** a well-formed frozen account; approve Avery’s active `25.00 USD`.

## Clean shape

See `CleanPaymentValidator.java`. Typed `UUID` / `BigDecimal` / `AccountView`, a `Decision` record, `compareTo` on the ceiling, exact currency set, no instance fields.

## Facilitation

- If a student only reformats the God method, cap Technical at 15/25.
- If they remove swallows but keep `lastOk`, cap Diagnostic and Reliability.
- Full marks require tests that fail on the starter for null amount and pass on the clean class.
