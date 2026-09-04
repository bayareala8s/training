package com.baypay.labs.build102;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PaymentValidatorTest {

    private static final UUID AVERY = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final UUID ACTIVE = UUID.fromString("22222222-2222-2222-2222-222222222221");
    private static final UUID FROZEN = UUID.fromString("22222222-2222-2222-2222-222222222222");
    private static final UUID OTHER = UUID.fromString("33333333-3333-3333-3333-333333333333");

    private final PaymentValidator validator = new PaymentValidator();

    @Test
    void approvesAveryActiveUsd() {
        PaymentValidator.Decision decision = validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("25.00"),
                "USD",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE"))));
        assertTrue(decision.approved());
    }

    @Test
    void declinesFrozenWithoutThrowing() {
        PaymentValidator.Decision decision = validator.validate(command(
                AVERY,
                FROZEN,
                new BigDecimal("25.00"),
                "USD",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(FROZEN, AVERY, "USD", "FROZEN"))));
        assertFalse(decision.approved());
        assertEquals("ACCOUNT_NOT_ACTIVE", decision.errorCode());
    }

    @Test
    void declinesCurrencyMismatchAndCeiling() {
        PaymentValidator.Decision fx = validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("25.00"),
                "GBP",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE"))));
        assertFalse(fx.approved());
        assertEquals("CURRENCY_MISMATCH", fx.errorCode());

        PaymentValidator.Decision ceiling = validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("1000000.01"),
                "USD",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE"))));
        assertFalse(ceiling.approved());
        assertEquals("AUTHORIZATION_DECLINED", ceiling.errorCode());
    }

    @Test
    void throwsForBadMoneyAndMissingOrMismatchedIdentity() {
        assertThrows(IllegalArgumentException.class, () -> validator.validate(command(
                AVERY,
                ACTIVE,
                BigDecimal.ZERO,
                "USD",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE")))));
        assertThrows(IllegalArgumentException.class, () -> validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("10.00"),
                "JPY",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE")))));
        assertThrows(IllegalArgumentException.class, () -> validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("10.00"),
                "USD",
                Optional.empty(),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, AVERY, "USD", "ACTIVE")))));
        assertThrows(IllegalArgumentException.class, () -> validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("10.00"),
                "USD",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.empty())));
        assertThrows(IllegalArgumentException.class, () -> validator.validate(command(
                AVERY,
                ACTIVE,
                new BigDecimal("10.00"),
                "USD",
                Optional.of(new PaymentValidator.CustomerView(AVERY)),
                Optional.of(new PaymentValidator.AccountView(ACTIVE, OTHER, "USD", "ACTIVE")))));
    }

    private static PaymentValidator.Command command(
            UUID customerId,
            UUID accountId,
            BigDecimal amount,
            String currency,
            Optional<PaymentValidator.CustomerView> customer,
            Optional<PaymentValidator.AccountView> account) {
        return new PaymentValidator.Command(customerId, accountId, amount, currency, customer, account);
    }
}
