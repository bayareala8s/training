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

import java.time.Instant;
import java.util.UUID;

/**
 * Posted ledger row. Named LedgerTransaction so the JPA type does not collide
 * with jakarta.transaction.Transaction in student reading.
 */
@Entity
@Table(name = "ledger_transactions")
public class LedgerTransaction {

    public enum Type {
        PAYMENT,
        REFUND
    }

    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID paymentId;

    private UUID refundId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 16)
    private Type type;

    @Embedded
    @AttributeOverrides({
            @AttributeOverride(name = "amount", column = @Column(name = "amount", nullable = false, precision = 19, scale = 2)),
            @AttributeOverride(name = "currency", column = @Column(name = "currency", nullable = false, length = 3))
    })
    private Money money;

    @Column(nullable = false)
    private Instant postedAt;

    protected LedgerTransaction() {
    }

    public static LedgerTransaction payment(UUID id, UUID paymentId, Money money, Instant postedAt) {
        LedgerTransaction tx = new LedgerTransaction();
        tx.id = id;
        tx.paymentId = paymentId;
        tx.type = Type.PAYMENT;
        tx.money = money;
        tx.postedAt = postedAt;
        return tx;
    }

    public static LedgerTransaction refund(UUID id, UUID paymentId, UUID refundId, Money money, Instant postedAt) {
        LedgerTransaction tx = new LedgerTransaction();
        tx.id = id;
        tx.paymentId = paymentId;
        tx.refundId = refundId;
        tx.type = Type.REFUND;
        tx.money = money;
        tx.postedAt = postedAt;
        return tx;
    }

    public UUID id() {
        return id;
    }

    public UUID paymentId() {
        return paymentId;
    }

    public UUID refundId() {
        return refundId;
    }

    public Type type() {
        return type;
    }

    public Money money() {
        return money;
    }

    public Instant postedAt() {
        return postedAt;
    }
}
