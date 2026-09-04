package com.baypay.labs.build101;

/**
 * Instructor reference for BUILD-101. Do not copy this file into the student starter folder.
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
