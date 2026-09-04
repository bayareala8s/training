package com.baypay.labs.build101;

import java.time.Instant;
import java.util.UUID;

/**
 * BUILD-101 student stub. Factory received(...) starts at RECEIVED. No public setStatus.
 */
public final class Payment {

    public static Payment received(
            UUID id,
            UUID customerId,
            UUID accountId,
            Money money,
            String reference,
            String idempotencyKey,
            Instant now) {
        throw new UnsupportedOperationException("implement BUILD-101 Payment.received");
    }

    public void transitionTo(PaymentStatus next, Instant now) {
        throw new UnsupportedOperationException("implement BUILD-101 Payment.transitionTo");
    }

    public void decline(String reason, Instant now) {
        throw new UnsupportedOperationException("implement BUILD-101 Payment.decline");
    }

    public void fail(String reason, Instant now) {
        throw new UnsupportedOperationException("implement BUILD-101 Payment.fail");
    }

    public UUID id() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public UUID customerId() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public UUID accountId() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public Money money() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public PaymentStatus status() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public String reference() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public String failureReason() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public String idempotencyKey() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public Instant createdAt() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }

    public Instant updatedAt() {
        throw new UnsupportedOperationException("implement BUILD-101");
    }
}
