package com.baypay.shared.idempotency;

import com.baypay.shared.persistence.IdempotencyRecordRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

/**
 * Persists operation + key + body hash. {@link #findReplay} throws
 * {@link IdempotencyConflictException} when the key is reused with a
 * different hash. The unique row is the multi-instance control, not a heap map.
 */
@Service
public class IdempotencyService {

    public static final String PAYMENT_CREATE = "PAYMENT_CREATE";
    public static final String REFUND_CREATE = "REFUND_CREATE";

    private final IdempotencyRecordRepository records;

    public IdempotencyService(IdempotencyRecordRepository records) {
        this.records = records;
    }

    @Transactional(readOnly = true)
    public Optional<IdempotencyRecord> findReplay(String operation, String key, String requestHash) {
        return records.findByOperationAndIdempotencyKey(operation, key)
                .map(existing -> {
                    if (!existing.matches(requestHash)) {
                        throw new IdempotencyConflictException(key);
                    }
                    return existing;
                });
    }

    @Transactional
    public IdempotencyRecord remember(
            String operation,
            String key,
            String requestHash,
            UUID resourceId,
            int statusCode,
            Instant now) {
        IdempotencyRecord record = new IdempotencyRecord(operation, key, requestHash, resourceId, statusCode, now);
        return records.save(record);
    }
}
