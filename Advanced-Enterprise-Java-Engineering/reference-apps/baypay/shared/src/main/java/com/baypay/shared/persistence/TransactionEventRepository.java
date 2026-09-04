package com.baypay.shared.persistence;

import com.baypay.shared.domain.TransactionEvent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface TransactionEventRepository extends JpaRepository<TransactionEvent, UUID> {
}
