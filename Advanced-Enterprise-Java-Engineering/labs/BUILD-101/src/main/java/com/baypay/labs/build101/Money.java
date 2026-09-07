package com.baypay.labs.build101;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;
import java.util.Set;

/**
 * Immutable value object. amount &gt; 0, USD|EUR|GBP, scale exactly 2.
 * plus/minus return a new instance; the original never changes.
 */
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
        try {
            this.amount = amount.setScale(2, RoundingMode.UNNECESSARY);
        } catch (ArithmeticException extraScale) {
            throw new IllegalArgumentException("amount scale must be at most 2", extraScale);
        }
        this.currency = currency;
    }

    public static Money of(String amount, String currency) {
        return new Money(new BigDecimal(amount), currency);
    }

    public BigDecimal amount() {
        return amount;
    }

    public String currency() {
        return currency;
    }

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money minus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.subtract(other.amount), currency);
    }

    private void requireSameCurrency(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("currency mismatch: " + currency + " vs " + other.currency);
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof Money money)) {
            return false;
        }
        return amount.compareTo(money.amount) == 0 && currency.equals(money.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(amount.stripTrailingZeros(), currency);
    }
}
