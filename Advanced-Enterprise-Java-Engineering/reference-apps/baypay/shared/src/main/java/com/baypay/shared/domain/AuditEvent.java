package com.baypay.shared.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "audit_events")
public class AuditEvent {

    @Id
    private UUID id;

    @Column(nullable = false, length = 64)
    private String actor;

    @Column(nullable = false, length = 64)
    private String action;

    @Column(nullable = false, length = 32)
    private String resourceType;

    @Column(nullable = false)
    private UUID resourceId;

    @Column(length = 512)
    private String detail;

    @Column(nullable = false)
    private Instant occurredAt;

    protected AuditEvent() {
    }

    public AuditEvent(
            UUID id,
            String actor,
            String action,
            String resourceType,
            UUID resourceId,
            String detail,
            Instant occurredAt) {
        this.id = id;
        this.actor = actor;
        this.action = action;
        this.resourceType = resourceType;
        this.resourceId = resourceId;
        this.detail = detail;
        this.occurredAt = occurredAt;
    }

    public UUID id() {
        return id;
    }

    public String actor() {
        return actor;
    }

    public String action() {
        return action;
    }

    public String resourceType() {
        return resourceType;
    }

    public UUID resourceId() {
        return resourceId;
    }

    public String detail() {
        return detail;
    }

    public Instant occurredAt() {
        return occurredAt;
    }
}
