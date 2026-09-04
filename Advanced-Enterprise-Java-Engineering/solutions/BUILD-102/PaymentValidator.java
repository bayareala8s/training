package com.baypay.labs.build102;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

/**
 * Instructor reference for BUILD-102. Mirrors PaymentApplicationService
 * plus DefaultPaymentAuthorizer without Spring.
 */
public final class PaymentValidator {

    public static final BigDecimal AUTHORIZATION_CEILING = new BigDecimal("1000000.00");
    private static final Set<String> CURRENCIES = Set.of("USD", "EUR", "GBP");

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
        Objects.requireNonNull(command, "command");
        command.customer().orElseThrow(() -> new IllegalArgumentException("CUSTOMER_NOT_FOUND"));
        AccountView account = command.account().orElseThrow(
                () -> new IllegalArgumentException("ACCOUNT_NOT_FOUND"));
        if (!account.id().equals(command.accountId()) || !account.belongsTo(command.customerId())) {
            throw new IllegalArgumentException("ACCOUNT_CUSTOMER_MISMATCH");
        }
        requireMoney(command.amount(), command.currency());
        if (!account.active()) {
            return Decision.decline("account is not ACTIVE", "ACCOUNT_NOT_ACTIVE");
        }
        if (!account.currency().equals(command.currency())) {
            return Decision.decline("account currency does not match payment", "CURRENCY_MISMATCH");
        }
        if (command.amount().compareTo(AUTHORIZATION_CEILING) > 0) {
            return Decision.decline("amount exceeds authorization ceiling", "AUTHORIZATION_DECLINED");
        }
        return Decision.approve();
    }

    private static void requireMoney(BigDecimal amount, String currency) {
        if (amount == null || amount.signum() <= 0) {
            throw new IllegalArgumentException("VALIDATION_FAILED");
        }
        if (currency == null || !CURRENCIES.contains(currency)) {
            throw new IllegalArgumentException("VALIDATION_FAILED");
        }
    }
}
