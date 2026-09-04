package com.baypay.labs.build101;

import java.util.Set;

/**
 * BUILD-101 student stub. Implement isTerminal, isRefundable, allowedNext, canTransitionTo.
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
        throw new UnsupportedOperationException("implement BUILD-101 PaymentStatus.isTerminal");
    }

    public boolean isRefundable() {
        throw new UnsupportedOperationException("implement BUILD-101 PaymentStatus.isRefundable");
    }

    public Set<PaymentStatus> allowedNext() {
        throw new UnsupportedOperationException("implement BUILD-101 PaymentStatus.allowedNext");
    }

    public boolean canTransitionTo(PaymentStatus next) {
        throw new UnsupportedOperationException("implement BUILD-101 PaymentStatus.canTransitionTo");
    }
}
