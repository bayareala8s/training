package com.baypay.shared.domain;

import java.util.EnumSet;
import java.util.Set;

/**
 * Happy path: RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED.
 * Failure / reversal paths are explicit; callers must not invent transitions.
 */
public enum PaymentStatus {
    RECEIVED,
    VALIDATING,
    AUTHORIZED,
    PROCESSING,
    COMPLETED,
    DECLINED,
    FAILED,
    REVERSED;

    public boolean isTerminal() {
        return this == COMPLETED || this == DECLINED || this == FAILED || this == REVERSED;
    }

    public boolean isRefundable() {
        return this == COMPLETED || this == REVERSED;
    }

    /** Legal next statuses. Adding a state means extending this table, not new controller {@code if}s. */
    public Set<PaymentStatus> allowedNext() {
        return switch (this) {
            case RECEIVED -> EnumSet.of(VALIDATING);
            case VALIDATING -> EnumSet.of(AUTHORIZED, DECLINED);
            case AUTHORIZED -> EnumSet.of(PROCESSING, FAILED);
            case PROCESSING -> EnumSet.of(COMPLETED, FAILED);
            case COMPLETED -> EnumSet.of(REVERSED);
            case DECLINED, FAILED, REVERSED -> EnumSet.noneOf(PaymentStatus.class);
        };
    }

    public boolean canTransitionTo(PaymentStatus next) {
        return allowedNext().contains(next);
    }
}
