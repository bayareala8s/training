package com.baypay.labs.build102;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * BUILD-102 student stub. Keep the records; implement {@link #validate(Command)}.
 */
public final class PaymentValidator {

    public static final BigDecimal AUTHORIZATION_CEILING = new BigDecimal("1000000.00");

    public record CustomerView(UUID id) {
    }

    public record AccountView(UUID id, UUID customerId, String currency, String status) {
        boolean active() {
            return "ACTIVE".equals(status);
        }

        boolean belongsTo(UUID customerId) {
            return this.customerId.equals(customerId);
        }
    }

    public record Command(
            UUID customerId,
            UUID accountId,
            BigDecimal amount,
            String currency,
            Optional<CustomerView> customer,
            Optional<AccountView> account) {
        public Command {
            Objects.requireNonNull(customer, "customer");
            Objects.requireNonNull(account, "account");
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

    public Decision validate(Command command) {
        throw new UnsupportedOperationException("implement BUILD-102 PaymentValidator.validate");
    }
}
