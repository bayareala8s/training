package com.baypay.shared.idempotency;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;
import java.util.UUID;

/**
 * One row per (operation, key). {@code requestHash} is what makes a retry a
 * replay versus a conflict.
 */
@Entity
@Table(name = "idempotency_keys")
public class IdempotencyRecord {

    @Id
    @Column(length = 160)
    private String compositeKey;

    @Column(nullable = false, length = 32)
    private String operation;

    @Column(nullable = false, length = 128)
    private String idempotencyKey;

    @Column(nullable = false, length = 64)
    private String requestHash;

    @Column(nullable = false)
    private UUID resourceId;

    @Column(nullable = false)
    private int statusCode;

    @Column(nullable = false)
    private Instant createdAt;

    protected IdempotencyRecord() {
    }

    public IdempotencyRecord(
            String operation,
            String idempotencyKey,
            String requestHash,
            UUID resourceId,
            int statusCode,
            Instant createdAt) {
        this.compositeKey = operation + ":" + idempotencyKey;
        this.operation = operation;
        this.idempotencyKey = idempotencyKey;
        this.requestHash = requestHash;
        this.resourceId = resourceId;
        this.statusCode = statusCode;
        this.createdAt = createdAt;
    }

    public String compositeKey() {
        return compositeKey;
    }

    public String operation() {
        return operation;
    }

    public String idempotencyKey() {
        return idempotencyKey;
    }

    public String requestHash() {
        return requestHash;
    }

    public UUID resourceId() {
        return resourceId;
    }

    public int statusCode() {
        return statusCode;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public boolean matches(String hash) {
        return requestHash.equals(hash);
    }
}
