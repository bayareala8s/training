package com.baypay.shared.domain;

import com.baypay.shared.error.DomainValidationException;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class MoneyTest {

    @Test
    void rejectsZeroAndUnsupportedCurrency() {
        assertThrows(DomainValidationException.class, () -> new Money(BigDecimal.ZERO, "USD"));
        assertThrows(DomainValidationException.class, () -> Money.of("10.00", "JPY"));
    }

    @Test
    void addsSameCurrency() {
        assertEquals(Money.of("15.50", "USD"), Money.of("10.00", "USD").plus(Money.of("5.50", "USD")));
    }

    @Test
    void rejectsCurrencyMismatch() {
        assertThrows(DomainValidationException.class, () -> Money.of("1.00", "USD").plus(Money.of("1.00", "EUR")));
    }
}
