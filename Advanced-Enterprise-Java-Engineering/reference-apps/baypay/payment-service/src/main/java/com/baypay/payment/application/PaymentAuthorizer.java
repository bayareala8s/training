package com.baypay.payment.application;

import com.baypay.shared.domain.Account;
import com.baypay.shared.domain.Payment;

import java.math.BigDecimal;

/**
 * SOLID D/L seam (L-1.2): the application service depends on this type, not a
 * card-network SDK. Any implementation — including a test double — must decline
 * a frozen account. An always-{@code approve()} double is a lying subtype.
 *
 * <p>Authorization is a {@link Decision}, not an exception: decline is a
 * business outcome (L-1.4).
 */
public interface PaymentAuthorizer {

    record Decision(boolean approved, String reason) {
        public static Decision approve() {
            return new Decision(true, null);
        }

        public static Decision decline(String reason) {
            return new Decision(false, reason);
        }
    }

    Decision authorize(Payment payment, Account account);

    /** Deterministic teaching authorizer. No network I/O. */
    class DefaultPaymentAuthorizer implements PaymentAuthorizer {
        static final BigDecimal AUTHORIZATION_CEILING = new BigDecimal("1000000.00");

        @Override
        public Decision authorize(Payment payment, Account account) {
            if (!account.isActive()) {
                return Decision.decline("account is not ACTIVE");
            }
            if (!account.currency().equals(payment.money().currency())) {
                return Decision.decline("account currency does not match payment");
            }
            if (payment.money().amount().compareTo(AUTHORIZATION_CEILING) > 0) {
                return Decision.decline("amount exceeds authorization ceiling");
            }
            return Decision.approve();
        }
    }
}
