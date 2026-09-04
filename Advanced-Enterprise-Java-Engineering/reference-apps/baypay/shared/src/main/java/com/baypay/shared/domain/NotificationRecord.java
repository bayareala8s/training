package com.baypay.shared.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "notifications")
public class NotificationRecord {

    public enum Channel {
        EMAIL,
        WEBHOOK
    }

    public enum Status {
        PENDING,
        SENT,
        FAILED
    }

    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID customerId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 16)
    private Channel channel;

    @Column(nullable = false, length = 128)
    private String template;

    @Column(nullable = false, length = 512)
    private String payload;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 16)
    private Status status;

    @Column(nullable = false)
    private Instant createdAt;

    protected NotificationRecord() {
    }

    public NotificationRecord(
            UUID id,
            UUID customerId,
            Channel channel,
            String template,
            String payload,
            Status status,
            Instant createdAt) {
        this.id = id;
        this.customerId = customerId;
        this.channel = channel;
        this.template = template;
        this.payload = payload;
        this.status = status;
        this.createdAt = createdAt;
    }

    public UUID id() {
        return id;
    }

    public UUID customerId() {
        return customerId;
    }

    public Channel channel() {
        return channel;
    }

    public String template() {
        return template;
    }

    public String payload() {
        return payload;
    }

    public Status status() {
        return status;
    }

    public Instant createdAt() {
        return createdAt;
    }
}
