package com.baypay.shared.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    private UUID id;

    @Column(nullable = false)
    private String displayName;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private Instant createdAt;

    protected Customer() {
    }

    public Customer(UUID id, String displayName, String email, Instant createdAt) {
        this.id = id;
        this.displayName = displayName;
        this.email = email;
        this.createdAt = createdAt;
    }

    public UUID id() {
        return id;
    }

    public String displayName() {
        return displayName;
    }

    public String email() {
        return email;
    }

    public Instant createdAt() {
        return createdAt;
    }
}
