package com.baypay.shared.idempotency;

import com.baypay.shared.error.BayPayException;
import com.baypay.shared.error.ErrorCode;

/** Same Idempotency-Key, different canonical body. Mapped to HTTP 409. */
public class IdempotencyConflictException extends BayPayException {

    public IdempotencyConflictException(String key) {
        super(
                ErrorCode.IDEMPOTENCY_CONFLICT,
                "Idempotency-Key '" + key + "' was reused with a different request body");
    }
}
