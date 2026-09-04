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
@Table(name = "accounts")
public class Account {

    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID customerId;

    @Column(nullable = false, length = 3)
    private String currency;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 16)
    private AccountStatus status;

    @Column(nullable = false)
    private Instant createdAt;

    protected Account() {
    }

    public Account(UUID id, UUID customerId, String currency, AccountStatus status, Instant createdAt) {
        this.id = id;
        this.customerId = customerId;
        this.currency = currency;
        this.status = status;
        this.createdAt = createdAt;
    }

    public UUID id() {
        return id;
    }

    public UUID customerId() {
        return customerId;
    }

    public String currency() {
        return currency;
    }

    public AccountStatus status() {
        return status;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public boolean isActive() {
        return status == AccountStatus.ACTIVE;
    }

    public boolean belongsTo(UUID customer) {
        return customerId.equals(customer);
    }
}
