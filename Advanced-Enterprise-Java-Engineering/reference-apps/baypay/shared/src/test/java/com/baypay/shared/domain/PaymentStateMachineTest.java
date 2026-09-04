package com.baypay.shared.domain;

import com.baypay.shared.error.BayPayException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PaymentStateMachineTest {

    @ParameterizedTest
    @CsvSource({
            "RECEIVED,VALIDATING",
            "VALIDATING,AUTHORIZED",
            "VALIDATING,DECLINED",
            "AUTHORIZED,PROCESSING",
            "AUTHORIZED,FAILED",
            "PROCESSING,COMPLETED",
            "PROCESSING,FAILED",
            "COMPLETED,REVERSED"
    })
    void allowsDocumentedTransitions(PaymentStatus from, PaymentStatus to) {
        assertTrue(from.canTransitionTo(to));
        assertDoesNotThrow(() -> PaymentStateMachine.assertTransition(from, to));
    }

    @Test
    void rejectsSkippingAuthorization() {
        assertThrows(BayPayException.class,
                () -> PaymentStateMachine.assertTransition(PaymentStatus.RECEIVED, PaymentStatus.COMPLETED));
    }

    @Test
    void declinedIsTerminal() {
        assertTrue(PaymentStatus.DECLINED.isTerminal());
        assertThrows(BayPayException.class,
                () -> PaymentStateMachine.assertTransition(PaymentStatus.DECLINED, PaymentStatus.AUTHORIZED));
    }
}
