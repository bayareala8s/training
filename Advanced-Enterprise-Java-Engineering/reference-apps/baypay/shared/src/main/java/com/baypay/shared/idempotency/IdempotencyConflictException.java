package com.baypay.shared.idempotency;

import com.baypay.shared.error.BayPayException;
import com.baypay.shared.error.ErrorCode;

public class IdempotencyConflictException extends BayPayException {

    public IdempotencyConflictException(String key) {
        super(
                ErrorCode.IDEMPOTENCY_CONFLICT,
                "Idempotency-Key '" + key + "' was reused with a different request body");
    }
}
