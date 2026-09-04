package com.baypay.shared.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "transaction_events")
public class TransactionEvent {

    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID transactionId;

    @Column(nullable = false, length = 64)
    private String eventType;

    @Column(length = 512)
    private String detail;

    @Column(nullable = false)
    private Instant occurredAt;

    protected TransactionEvent() {
    }

    public TransactionEvent(UUID id, UUID transactionId, String eventType, String detail, Instant occurredAt) {
        this.id = id;
        this.transactionId = transactionId;
        this.eventType = eventType;
        this.detail = detail;
        this.occurredAt = occurredAt;
    }

    public UUID id() {
        return id;
    }

    public UUID transactionId() {
        return transactionId;
    }

    public String eventType() {
        return eventType;
    }

    public String detail() {
        return detail;
    }

    public Instant occurredAt() {
        return occurredAt;
    }
}
