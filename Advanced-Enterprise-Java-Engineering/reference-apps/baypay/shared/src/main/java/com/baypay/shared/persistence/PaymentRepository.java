package com.baypay.shared.persistence;

import com.baypay.shared.domain.Payment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

/** Persistence for {@link Payment}. Money rules stay on the entity, not here. */
public interface PaymentRepository extends JpaRepository<Payment, UUID> {

    Optional<Payment> findByIdempotencyKey(String idempotencyKey);
}
