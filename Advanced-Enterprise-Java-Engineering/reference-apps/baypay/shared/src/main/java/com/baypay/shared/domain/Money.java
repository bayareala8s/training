package com.baypay.shared.domain;

import com.baypay.shared.error.DomainValidationException;
import com.baypay.shared.error.ErrorCode;
import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;
import java.util.Set;

/**
 * Immutable money value (L-1.2). Two instances with the same numeric value and
 * currency are interchangeable. There is no setter; {@link #plus} / {@link #minus}
 * return a new instance.
 *
 * <p>Rules: {@code amount > 0}, currency in USD|EUR|GBP, scale exactly 2.
 * {@code double} is not money. Extra scale throws ({@code UNNECESSARY}).
 */
@Embeddable
public class Money {

    private static final Set<String> SUPPORTED = Set.of("USD", "EUR", "GBP");

    @Column(name = "amount", nullable = false, precision = 19, scale = 2)
    private BigDecimal amount;

    @Column(name = "currency", nullable = false, length = 3)
    private String currency;

    /** JPA only. Do not use from application code — invariants would be skipped. */
    protected Money() {
    }

    /**
     * Fail closed in the constructor so every caller (API, worker, test) hits
     * the same rules. Bean Validation on the HTTP request is not a substitute.
     */
    public Money(BigDecimal amount, String currency) {
        if (amount == null || amount.signum() <= 0) {
            throw new DomainValidationException("amount must be greater than zero");
        }
        if (currency == null || !SUPPORTED.contains(currency)) {
            throw new DomainValidationException("currency must be one of " + SUPPORTED);
        }
        // UNNECESSARY: 10.001 is rejected, not rounded. Rounding would invent money.
        this.amount = amount.setScale(2, RoundingMode.UNNECESSARY);
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

    public boolean greaterThan(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount) > 0;
    }

    public boolean greaterThanOrEqual(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount) >= 0;
    }

    private void requireSameCurrency(Money other) {
        if (!currency.equals(other.currency)) {
            throw new DomainValidationException(
                    ErrorCode.CURRENCY_MISMATCH,
                    "currency mismatch: " + currency + " vs " + other.currency);
        }
    }

    /**
     * {@code BigDecimal.equals} is scale-sensitive ({@code 10.0} ≠ {@code 10.00}).
     * Payments compare numeric value, so this uses {@code compareTo}.
     */
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

    @Override
    public String toString() {
        return amount.toPlainString() + " " + currency;
    }
}
