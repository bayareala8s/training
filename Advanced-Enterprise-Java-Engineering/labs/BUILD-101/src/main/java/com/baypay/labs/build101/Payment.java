package com.baypay.labs.build101;

import java.time.Instant;
import java.util.UUID;

/**
 * Entity. Factory received(...) starts at RECEIVED. No public setStatus.
 */
public final class Payment {

    private UUID id;
    private UUID customerId;
    private UUID accountId;
    private Money money;
    private PaymentStatus status;
    private String reference;
    private String failureReason;
    private String idempotencyKey;
    private Instant createdAt;
    private Instant updatedAt;

    public static Payment received(
            UUID id,
            UUID customerId,
            UUID accountId,
            Money money,
            String reference,
            String idempotencyKey,
            Instant now) {
        Payment payment = new Payment();
        payment.id = id;
        payment.customerId = customerId;
        payment.accountId = accountId;
        payment.money = money;
        payment.status = PaymentStatus.RECEIVED;
        payment.reference = reference;
        payment.idempotencyKey = idempotencyKey;
        payment.createdAt = now;
        payment.updatedAt = now;
        return payment;
    }

    public void transitionTo(PaymentStatus next, Instant now) {
        PaymentStateMachine.assertTransition(status, next);
        this.status = next;
        this.updatedAt = now;
    }

    public void decline(String reason, Instant now) {
        transitionTo(PaymentStatus.DECLINED, now);
        this.failureReason = reason;
    }

    public void fail(String reason, Instant now) {
        transitionTo(PaymentStatus.FAILED, now);
        this.failureReason = reason;
    }

    public UUID id() {
        return id;
    }

    public UUID customerId() {
        return customerId;
    }

    public UUID accountId() {
        return accountId;
    }

    public Money money() {
        return money;
    }

    public PaymentStatus status() {
        return status;
    }

    public String reference() {
        return reference;
    }

    public String failureReason() {
        return failureReason;
    }

    public String idempotencyKey() {
        return idempotencyKey;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public Instant updatedAt() {
        return updatedAt;
    }
}
