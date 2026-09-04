package com.baypay.labs.build101;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class Build101ContractTest {

    private static final UUID CUSTOMER = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final UUID ACCOUNT = UUID.fromString("22222222-2222-2222-2222-222222222221");

    @Test
    void rejectsZeroNegativeNullAndUnsupportedCurrency() {
        assertThrows(IllegalArgumentException.class, () -> new Money(BigDecimal.ZERO, "USD"));
        assertThrows(IllegalArgumentException.class, () -> new Money(new BigDecimal("-1.00"), "USD"));
        assertThrows(IllegalArgumentException.class, () -> new Money(null, "USD"));
        assertThrows(IllegalArgumentException.class, () -> Money.of("10.00", "JPY"));
        assertThrows(IllegalArgumentException.class, () -> Money.of("10.00", "usd"));
        assertThrows(IllegalArgumentException.class, () -> Money.of("10.001", "USD"));
    }

    @Test
    void plusMinusAndNumericEquals() {
        Money ten = Money.of("10.0", "USD");
        Money tenScaled = Money.of("10.00", "USD");
        assertEquals(ten, tenScaled);
        assertEquals(ten.hashCode(), tenScaled.hashCode());
        assertEquals(Money.of("15.50", "USD"), Money.of("10.00", "USD").plus(Money.of("5.50", "USD")));
        assertEquals(Money.of("4.50", "USD"), Money.of("10.00", "USD").minus(Money.of("5.50", "USD")));
        Money first = Money.of("1.00", "USD");
        Money second = first.plus(Money.of("1.00", "USD"));
        assertEquals(Money.of("1.00", "USD"), first);
        assertEquals(Money.of("2.00", "USD"), second);
        assertThrows(IllegalArgumentException.class, () -> Money.of("1.00", "USD").plus(Money.of("1.00", "EUR")));
        assertThrows(IllegalArgumentException.class, () -> Money.of("1.00", "USD").minus(Money.of("1.00", "GBP")));
    }

    @Test
    void statusMachineMatchesBayPayEdges() {
        assertEquals(Set.of(PaymentStatus.VALIDATING), PaymentStatus.RECEIVED.allowedNext());
        assertTrue(PaymentStatus.VALIDATING.canTransitionTo(PaymentStatus.AUTHORIZED));
        assertTrue(PaymentStatus.VALIDATING.canTransitionTo(PaymentStatus.DECLINED));
        assertTrue(PaymentStatus.AUTHORIZED.canTransitionTo(PaymentStatus.PROCESSING));
        assertTrue(PaymentStatus.AUTHORIZED.canTransitionTo(PaymentStatus.FAILED));
        assertTrue(PaymentStatus.PROCESSING.canTransitionTo(PaymentStatus.COMPLETED));
        assertTrue(PaymentStatus.PROCESSING.canTransitionTo(PaymentStatus.FAILED));
        assertTrue(PaymentStatus.COMPLETED.canTransitionTo(PaymentStatus.REVERSED));
        assertFalse(PaymentStatus.RECEIVED.canTransitionTo(PaymentStatus.COMPLETED));
        assertTrue(PaymentStatus.COMPLETED.isTerminal());
        assertTrue(PaymentStatus.DECLINED.isTerminal());
        assertTrue(PaymentStatus.FAILED.isTerminal());
        assertTrue(PaymentStatus.REVERSED.isTerminal());
        assertFalse(PaymentStatus.RECEIVED.isTerminal());
        assertTrue(PaymentStatus.COMPLETED.isRefundable());
        assertTrue(PaymentStatus.REVERSED.isRefundable());
        assertFalse(PaymentStatus.AUTHORIZED.isRefundable());
        assertThrows(
                IllegalStateException.class,
                () -> PaymentStateMachine.assertTransition(PaymentStatus.RECEIVED, PaymentStatus.COMPLETED));
        PaymentStateMachine.assertTransition(PaymentStatus.RECEIVED, PaymentStatus.VALIDATING);
    }

    @Test
    void paymentFactoryAndTransitions() {
        Instant now = Instant.parse("2026-09-04T12:00:00Z");
        UUID id = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
        Payment payment = Payment.received(
                id, CUSTOMER, ACCOUNT, Money.of("25.00", "USD"), "harbor-demo", "idem-harbor-1", now);
        assertEquals(PaymentStatus.RECEIVED, payment.status());
        assertEquals("idem-harbor-1", payment.idempotencyKey());
        assertEquals(id, payment.id());
        assertEquals(CUSTOMER, payment.customerId());
        assertEquals(ACCOUNT, payment.accountId());
        assertEquals(now, payment.createdAt());
        assertThrows(IllegalStateException.class, () -> payment.transitionTo(PaymentStatus.COMPLETED, now));

        payment.transitionTo(PaymentStatus.VALIDATING, now.plusSeconds(1));
        payment.decline("synthetic decline for Avery frozen path", now.plusSeconds(2));
        assertEquals(PaymentStatus.DECLINED, payment.status());
        assertEquals("synthetic decline for Avery frozen path", payment.failureReason());
        assertTrue(payment.status().isTerminal());
        assertThrows(IllegalStateException.class, () -> payment.fail("already declined", now.plusSeconds(3)));
    }

    @Test
    void failIsLegalFromAuthorized() {
        Instant now = Instant.parse("2026-09-04T13:00:00Z");
        Payment payment = Payment.received(
                UUID.fromString("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
                CUSTOMER,
                ACCOUNT,
                Money.of("10.00", "USD"),
                "fog-coffee",
                "idem-fail-1",
                now);
        payment.transitionTo(PaymentStatus.VALIDATING, now);
        payment.transitionTo(PaymentStatus.AUTHORIZED, now);
        payment.fail("processor timeout", now);
        assertEquals(PaymentStatus.FAILED, payment.status());
        assertEquals("processor timeout", payment.failureReason());
    }
}
