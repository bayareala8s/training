package com.baypay.labs.build101;

/**
 * Single place that rejects illegal edges such as RECEIVED → COMPLETED.
 */
public final class PaymentStateMachine {

    private PaymentStateMachine() {
    }

    public static void assertTransition(PaymentStatus from, PaymentStatus to) {
        if (!from.canTransitionTo(to)) {
            throw new IllegalStateException("Cannot transition payment from " + from + " to " + to);
        }
    }
}
