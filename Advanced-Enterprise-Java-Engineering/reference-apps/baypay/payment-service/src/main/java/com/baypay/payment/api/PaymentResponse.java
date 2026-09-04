package com.baypay.payment.api;

import com.baypay.shared.domain.Payment;
import com.baypay.shared.domain.PaymentStatus;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

public record PaymentResponse(
        UUID paymentId,
        UUID customerId,
        UUID accountId,
        BigDecimal amount,
        String currency,
        PaymentStatus status,
        String reference,
        String failureReason,
        Instant createdAt,
        Instant updatedAt
) {
    public static PaymentResponse from(Payment payment) {
        return new PaymentResponse(
                payment.id(),
                payment.customerId(),
                payment.accountId(),
                payment.money().amount(),
                payment.money().currency(),
                payment.status(),
                payment.reference(),
                payment.failureReason(),
                payment.createdAt(),
                payment.updatedAt());
    }
}
