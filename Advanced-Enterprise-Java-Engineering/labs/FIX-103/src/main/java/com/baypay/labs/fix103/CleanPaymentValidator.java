package com.baypay.labs.fix103;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.UUID;

/**
 * FIX-103 student stub. Refactor away from {@code starter/MessyPaymentValidator.java}.
 * Keep these types; implement {@link #validate}.
 */
public final class CleanPaymentValidator {

    public static final BigDecimal AUTHORIZATION_CEILING = new BigDecimal("1000000.00");

    public record AccountView(UUID id, UUID customerId, String currency, String status) {
        public AccountView {
            Objects.requireNonNull(id, "id");
            Objects.requireNonNull(customerId, "customerId");
            Objects.requireNonNull(currency, "currency");
            Objects.requireNonNull(status, "status");
        }

        boolean active() {
            return "ACTIVE".equals(status);
        }
    }

    public record Decision(boolean approved, String reason, String errorCode) {
        public static Decision approve() {
            return new Decision(true, null, null);
        }

        public static Decision decline(String reason, String errorCode) {
            return new Decision(false, reason, errorCode);
        }
    }

    public Decision validate(
            UUID customerId,
            UUID accountId,
            BigDecimal amount,
            String currency,
            AccountView account) {
        throw new UnsupportedOperationException("implement FIX-103 CleanPaymentValidator.validate");
    }
}
