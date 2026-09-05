# BUILD-101 — Instructor solution

Students re-implement the BayPay transaction domain. Production truth is already in `reference-apps/baypay/shared`. This note states the invariants you grade, plus a JPA-free excerpt that matches those types.

## Invariants to require

### Money

- `amount` is a `BigDecimal` with `signum() > 0`.
- Currency is exactly `USD`, `EUR`, or `GBP` (not `usd`, not `JPY`).
- Scale is 2; `setScale(2, RoundingMode.UNNECESSARY)` so `10.001` fails.
- `plus` / `minus` require the same currency and return a **new** instance.
- `equals` uses `amount.compareTo == 0`; `hashCode` uses `stripTrailingZeros`.

### PaymentStatus

| From | Allowed next |
|---|---|
| RECEIVED | VALIDATING |
| VALIDATING | AUTHORIZED, DECLINED |
| AUTHORIZED | PROCESSING, FAILED |
| PROCESSING | COMPLETED, FAILED |
| COMPLETED | REVERSED |
| DECLINED, FAILED, REVERSED | none |

- Terminal: `COMPLETED`, `DECLINED`, `FAILED`, `REVERSED`.
- Refundable: `COMPLETED`, `REVERSED` (matches `PaymentStatus.isRefundable()`).
- Prefer `EnumSet` in `allowedNext()`.

### Payment

- Factory `received(...)` sets `RECEIVED`, stores `idempotencyKey`, stamps `createdAt`/`updatedAt`.
- No public `setStatus`. `transitionTo` calls `PaymentStateMachine.assertTransition`.
- `decline` / `fail` set `failureReason` after a legal transition.

### Naming

Spec entity “Transaction” is `LedgerTransaction` in Java. Students who mention that in the worksheet get the production-awareness point.

JPA-free instructor sources in this folder: `Money.java`, `PaymentStatus.java`, `PaymentStateMachine.java`, `Payment.java`. Contract tests live in `labs/BUILD-101/src/test` and are smoked with `qa/smoke_runnable_labs.py`.

### SOLID (grade the vocabulary, not extra interfaces)

Students should be able to spell the five letters and point at BayPay, not invent a `MoneyReader`.

| Letter | Keep | Block |
|---|---|---|
| S | `Payment` owns lifecycle; email is `NotificationListener` | God `Payment` that posts, emails, and authorizes |
| O | New edges in `PaymentStatus.allowedNext()`; `CAD` in the currency set | Controller `if`s or a public `setStatus` |
| L | Any `PaymentAuthorizer` declines a frozen account | Always-`approve()` test double |
| I | Callers that need `isActive()` do not take `AccountGod` | One 40-method account interface |
| D | Service depends on `PaymentAuthorizer` | Service constructs a card-network SDK |

## Reference files

- `reference-apps/baypay/shared/src/main/java/com/baypay/shared/domain/Money.java`
- `.../Payment.java`
- `.../PaymentStatus.java`
- `.../PaymentStateMachine.java`
- Tests: `MoneyTest.java`, `PaymentStateMachineTest.java`

## Minimal JPA-free excerpt

Students may omit annotations. A complete excerpt:

```java
package com.baypay.labs.build101;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;
import java.util.EnumSet;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

public final class Money {
    private static final Set<String> SUPPORTED = Set.of("USD", "EUR", "GBP");
    private final BigDecimal amount;
    private final String currency;

    public Money(BigDecimal amount, String currency) {
        if (amount == null || amount.signum() <= 0) {
            throw new IllegalArgumentException("amount must be greater than zero");
        }
        if (currency == null || !SUPPORTED.contains(currency)) {
            throw new IllegalArgumentException("currency must be one of " + SUPPORTED);
        }
        this.amount = amount.setScale(2, RoundingMode.UNNECESSARY);
        this.currency = currency;
    }

    public static Money of(String amount, String currency) {
        return new Money(new BigDecimal(amount), currency);
    }

    public Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(amount.add(other.amount), currency);
    }

    public BigDecimal amount() {
        return amount;
    }

    public String currency() {
        return currency;
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof Money m && amount.compareTo(m.amount) == 0 && currency.equals(m.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(amount.stripTrailingZeros(), currency);
    }
}

enum PaymentStatus {
    RECEIVED, VALIDATING, AUTHORIZED, PROCESSING, COMPLETED, DECLINED, FAILED, REVERSED;

    boolean isTerminal() {
        return this == COMPLETED || this == DECLINED || this == FAILED || this == REVERSED;
    }

    Set<PaymentStatus> allowedNext() {
        return switch (this) {
            case RECEIVED -> EnumSet.of(VALIDATING);
            case VALIDATING -> EnumSet.of(AUTHORIZED, DECLINED);
            case AUTHORIZED -> EnumSet.of(PROCESSING, FAILED);
            case PROCESSING -> EnumSet.of(COMPLETED, FAILED);
            case COMPLETED -> EnumSet.of(REVERSED);
            case DECLINED, FAILED, REVERSED -> EnumSet.noneOf(PaymentStatus.class);
        };
    }
}

final class PaymentStateMachine {
    private PaymentStateMachine() {
    }

    static void assertTransition(PaymentStatus from, PaymentStatus to) {
        if (!from.allowedNext().contains(to)) {
            throw new IllegalStateException("Cannot transition payment from " + from + " to " + to);
        }
    }
}

final class Payment {
    private final UUID id;
    private final UUID customerId;
    private final UUID accountId;
    private final Money money;
    private PaymentStatus status;
    private String failureReason;
    private final String idempotencyKey;
    private Instant updatedAt;

    static Payment received(
            UUID id, UUID customerId, UUID accountId, Money money, String reference, String idempotencyKey, Instant now) {
        Objects.requireNonNull(reference);
        Payment payment = new Payment(id, customerId, accountId, money, idempotencyKey, now);
        payment.status = PaymentStatus.RECEIVED;
        return payment;
    }

    private Payment(UUID id, UUID customerId, UUID accountId, Money money, String idempotencyKey, Instant now) {
        this.id = id;
        this.customerId = customerId;
        this.accountId = accountId;
        this.money = money;
        this.idempotencyKey = idempotencyKey;
        this.updatedAt = now;
    }

    void transitionTo(PaymentStatus next, Instant now) {
        PaymentStateMachine.assertTransition(status, next);
        this.status = next;
        this.updatedAt = now;
    }

    void decline(String reason, Instant now) {
        transitionTo(PaymentStatus.DECLINED, now);
        this.failureReason = reason;
    }

    UUID id() {
        return id;
    }

    UUID customerId() {
        return customerId;
    }

    UUID accountId() {
        return accountId;
    }

    Money money() {
        return money;
    }

    PaymentStatus status() {
        return status;
    }

    String failureReason() {
        return failureReason;
    }

    String idempotencyKey() {
        return idempotencyKey;
    }
}
```

## Common student misses

- `BigDecimal.equals` instead of `compareTo`.
- `List<String>` statuses.
- Public `setStatus`.
- Allowing `RECEIVED → COMPLETED` “for the support tool.”
- Forgetting `COMPLETED → REVERSED`.
