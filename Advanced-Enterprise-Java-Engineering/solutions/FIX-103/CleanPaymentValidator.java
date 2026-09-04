package com.baypay.labs.fix103;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Instructor reference for FIX-103. Do not place in the student lab folder.
 */
public final class CleanPaymentValidator {

    public static final BigDecimal AUTHORIZATION_CEILING = new BigDecimal("1000000.00");
    private static final Set<String> CURRENCIES = Set.of("USD", "EUR", "GBP");

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
        Objects.requireNonNull(customerId, "customerId");
        Objects.requireNonNull(accountId, "accountId");
        Objects.requireNonNull(account, "account");
        if (!account.id().equals(accountId)) {
            throw new IllegalArgumentException("ACCOUNT_NOT_FOUND");
        }
        if (!account.customerId().equals(customerId)) {
            throw new IllegalArgumentException("ACCOUNT_CUSTOMER_MISMATCH");
        }
        requireMoney(amount, currency);
        if (!account.active()) {
            return Decision.decline("account is not ACTIVE", "ACCOUNT_NOT_ACTIVE");
        }
        if (!account.currency().equals(currency)) {
            return Decision.decline("account currency does not match payment", "CURRENCY_MISMATCH");
        }
        if (amount.compareTo(AUTHORIZATION_CEILING) > 0) {
            return Decision.decline("amount exceeds authorization ceiling", "AUTHORIZATION_DECLINED");
        }
        return Decision.approve();
    }

    private static void requireMoney(BigDecimal amount, String currency) {
        if (amount == null || amount.signum() <= 0) {
            throw new IllegalArgumentException("VALIDATION_FAILED: amount must be greater than zero");
        }
        if (currency == null || !CURRENCIES.contains(currency)) {
            throw new IllegalArgumentException("VALIDATION_FAILED: currency must be USD, EUR, or GBP");
        }
    }
}
