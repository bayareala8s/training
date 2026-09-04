package com.baypay.shared.domain;

import com.baypay.shared.error.BayPayException;
import com.baypay.shared.error.ErrorCode;

public final class PaymentStateMachine {

    private PaymentStateMachine() {
    }

    public static void assertTransition(PaymentStatus from, PaymentStatus to) {
        if (!from.canTransitionTo(to)) {
            throw new BayPayException(
                    ErrorCode.ILLEGAL_STATE_TRANSITION,
                    "Cannot transition payment from " + from + " to " + to);
        }
    }
}
