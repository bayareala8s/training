package com.baypay.shared.error;

/**
 * Stable machine codes on Problem Details. HTTP status is chosen in
 * {@code ApiExceptionHandler}, not here.
 */
public enum ErrorCode {
    VALIDATION_FAILED,
    PAYMENT_NOT_FOUND,
    REFUND_NOT_FOUND,
    CUSTOMER_NOT_FOUND,
    ACCOUNT_NOT_FOUND,
    ACCOUNT_NOT_ACTIVE,
    ACCOUNT_CUSTOMER_MISMATCH,
    ILLEGAL_STATE_TRANSITION,
    PAYMENT_NOT_REFUNDABLE,
    REFUND_EXCEEDS_REMAINING,
    IDEMPOTENCY_KEY_REQUIRED,
    IDEMPOTENCY_CONFLICT,
    CURRENCY_MISMATCH,
    AUTHORIZATION_DECLINED
}
