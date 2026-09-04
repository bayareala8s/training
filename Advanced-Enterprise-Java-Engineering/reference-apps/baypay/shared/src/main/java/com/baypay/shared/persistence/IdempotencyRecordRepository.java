package com.baypay.shared.persistence;

import com.baypay.shared.idempotency.IdempotencyRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface IdempotencyRecordRepository extends JpaRepository<IdempotencyRecord, String> {

    Optional<IdempotencyRecord> findByOperationAndIdempotencyKey(String operation, String idempotencyKey);
}
