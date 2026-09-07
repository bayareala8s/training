package com.baypay.shared.persistence;

import com.baypay.shared.domain.LedgerTransaction;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface LedgerTransactionRepository extends JpaRepository<LedgerTransaction, UUID> {

    List<LedgerTransaction> findByPaymentId(UUID paymentId);

    Optional<LedgerTransaction> findByRefundId(UUID refundId);
}
