package com.baypay.labs.build101;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

/**
 * Instructor reference for BUILD-101. JPA-free excerpt of production Payment.
 * Do not copy this file into the student starter folder.
 */
public final class Payment {

    private final UUID id;
    private final UUID customerId;
    private final UUID accountId;
    private final Money money;
    private PaymentStatus status;
    private String reference;
    private String failureReason;
    private final String idempotencyKey;
    private final Instant createdAt;
    private Instant updatedAt;

    public static Payment received(
            UUID id,
            UUID customerId,
            UUID accountId,
            Money money,
            String reference,
            String idempotencyKey,
            Instant now) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(customerId, "customerId");
        Objects.requireNonNull(accountId, "accountId");
        Objects.requireNonNull(money, "money");
        Objects.requireNonNull(reference, "reference");
        Objects.requireNonNull(idempotencyKey, "idempotencyKey");
        Objects.requireNonNull(now, "now");
        return new Payment(id, customerId, accountId, money, reference, idempotencyKey, now);
    }

    private Payment(
            UUID id,
            UUID customerId,
            UUID accountId,
            Money money,
            String reference,
            String idempotencyKey,
            Instant now) {
        this.id = id;
        this.customerId = customerId;
        this.accountId = accountId;
        this.money = money;
        this.status = PaymentStatus.RECEIVED;
        this.reference = reference;
        this.idempotencyKey = idempotencyKey;
        this.createdAt = now;
        this.updatedAt = now;
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
