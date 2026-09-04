package com.baypay.shared.persistence;

import com.baypay.shared.domain.LedgerTransaction;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface LedgerTransactionRepository extends JpaRepository<LedgerTransaction, UUID> {
}
