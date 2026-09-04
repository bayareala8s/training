package com.baypay.shared.domain;

import jakarta.persistence.AttributeOverride;
import jakarta.persistence.AttributeOverrides;
import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "payments")
public class Payment {

    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID customerId;

    @Column(nullable = false)
    private UUID accountId;

    @Embedded
    @AttributeOverrides({
            @AttributeOverride(name = "amount", column = @Column(name = "amount", nullable = false, precision = 19, scale = 2)),
            @AttributeOverride(name = "currency", column = @Column(name = "currency", nullable = false, length = 3))
    })
    private Money money;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 16)
    private PaymentStatus status;

    @Column(length = 64)
    private String reference;

    @Column(length = 256)
    private String failureReason;

    @Column(nullable = false, unique = true, length = 128)
    private String idempotencyKey;

    @Column(nullable = false)
    private Instant createdAt;

    @Column(nullable = false)
    private Instant updatedAt;

    @Version
    private long version;

    protected Payment() {
    }

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
