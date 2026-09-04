package com.baypay.shared.persistence;

import com.baypay.shared.domain.Refund;
import com.baypay.shared.domain.RefundStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface RefundRepository extends JpaRepository<Refund, UUID> {

    Optional<Refund> findByIdempotencyKey(String idempotencyKey);

    List<Refund> findByPaymentIdAndStatus(UUID paymentId, RefundStatus status);
}
