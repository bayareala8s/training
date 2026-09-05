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

/**
 * Refund entity against a COMPLETED (or already REVERSED) payment.
 * Amount currency must match the payment; remaining refundable is enforced
 * in {@code RefundApplicationService}, not here.
 */
@Entity
@Table(name = "refunds")
public class Refund {

    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID paymentId;

    @Embedded
    @AttributeOverrides({
            @AttributeOverride(name = "amount", column = @Column(name = "amount", nullable = false, precision = 19, scale = 2)),
            @AttributeOverride(name = "currency", column = @Column(name = "currency", nullable = false, length = 3))
    })
    private Money money;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 16)
    private RefundStatus status;

    @Column(length = 256)
    private String reason;

    @Column(nullable = false, unique = true, length = 128)
    private String idempotencyKey;

    @Column(nullable = false)
    private Instant createdAt;

    @Column(nullable = false)
    private Instant updatedAt;

    @Version
    private long version;

    protected Refund() {
    }

    public static Refund requested(
            UUID id,
            UUID paymentId,
            Money money,
            String reason,
            String idempotencyKey,
            Instant now) {
        Refund refund = new Refund();
        refund.id = id;
        refund.paymentId = paymentId;
        refund.money = money;
        refund.status = RefundStatus.REQUESTED;
        refund.reason = reason;
        refund.idempotencyKey = idempotencyKey;
        refund.createdAt = now;
        refund.updatedAt = now;
        return refund;
    }

    public void markProcessing(Instant now) {
        this.status = RefundStatus.PROCESSING;
        this.updatedAt = now;
    }

    public void complete(Instant now) {
        this.status = RefundStatus.COMPLETED;
        this.updatedAt = now;
    }

    public void fail(String reason, Instant now) {
        this.status = RefundStatus.FAILED;
        this.reason = reason;
        this.updatedAt = now;
    }

    public UUID id() {
        return id;
    }

    public UUID paymentId() {
        return paymentId;
    }

    public Money money() {
        return money;
    }

    public RefundStatus status() {
        return status;
    }

    public String reason() {
        return reason;
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
