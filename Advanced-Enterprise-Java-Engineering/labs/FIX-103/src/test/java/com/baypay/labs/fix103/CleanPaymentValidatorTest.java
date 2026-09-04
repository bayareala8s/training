package com.baypay.labs.fix103;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CleanPaymentValidatorTest {

    private static final UUID AVERY = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final UUID ACTIVE = UUID.fromString("22222222-2222-2222-2222-222222222221");
    private static final UUID FROZEN = UUID.fromString("22222222-2222-2222-2222-222222222222");
    private static final UUID OTHER = UUID.fromString("33333333-3333-3333-3333-333333333333");

    private final CleanPaymentValidator validator = new CleanPaymentValidator();

    @Test
    void approvesAveryActiveUsd() {
        CleanPaymentValidator.Decision decision = validator.validate(
                AVERY,
                ACTIVE,
                new BigDecimal("25.00"),
                "USD",
                new CleanPaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE"));
        assertTrue(decision.approved());
    }

    @Test
    void declinesFrozenAndCurrencyMismatchAndCeiling() {
        CleanPaymentValidator.Decision frozen = validator.validate(
                AVERY,
                FROZEN,
                new BigDecimal("25.00"),
                "USD",
                new CleanPaymentValidator.AccountView(FROZEN, AVERY, "USD", "FROZEN"));
        assertFalse(frozen.approved());
        assertEquals("ACCOUNT_NOT_ACTIVE", frozen.errorCode());

        CleanPaymentValidator.Decision fx = validator.validate(
                AVERY,
                ACTIVE,
                new BigDecimal("25.00"),
                "GBP",
                new CleanPaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE"));
        assertFalse(fx.approved());
        assertEquals("CURRENCY_MISMATCH", fx.errorCode());

        CleanPaymentValidator.Decision ceiling = validator.validate(
                AVERY,
                ACTIVE,
                new BigDecimal("1000000.01"),
                "USD",
                new CleanPaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE"));
        assertFalse(ceiling.approved());
        assertEquals("AUTHORIZATION_DECLINED", ceiling.errorCode());
    }

    @Test
    void throwsForNullZeroJpyAndMismatch() {
        CleanPaymentValidator.AccountView active =
                new CleanPaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE");
        assertThrows(IllegalArgumentException.class,
                () -> validator.validate(AVERY, ACTIVE, null, "USD", active));
        assertThrows(IllegalArgumentException.class,
                () -> validator.validate(AVERY, ACTIVE, BigDecimal.ZERO, "USD", active));
        assertThrows(IllegalArgumentException.class,
                () -> validator.validate(AVERY, ACTIVE, new BigDecimal("10.00"), "JPY", active));
        assertThrows(IllegalArgumentException.class,
                () -> validator.validate(AVERY, ACTIVE, new BigDecimal("10.00"), "USD",
                        new CleanPaymentValidator.AccountView(ACTIVE, OTHER, "USD", "ACTIVE")));
        assertThrows(IllegalArgumentException.class,
                () -> validator.validate(AVERY, FROZEN, new BigDecimal("10.00"), "USD", active));
        assertThrows(NullPointerException.class,
                () -> validator.validate(AVERY, ACTIVE, new BigDecimal("10.00"), "USD", null));
    }
}
