package com.baypay.labs.build101;

import java.util.EnumSet;
import java.util.Set;

/**
 * Instructor reference for BUILD-101. Do not copy this file into the student starter folder.
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
