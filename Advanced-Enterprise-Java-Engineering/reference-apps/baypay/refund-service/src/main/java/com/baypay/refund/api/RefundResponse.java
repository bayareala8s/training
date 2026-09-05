package com.baypay.refund.api;

import com.baypay.shared.domain.Refund;
import com.baypay.shared.domain.RefundStatus;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

/** API view of a {@link Refund}. */
public record RefundResponse(
        UUID refundId,
        UUID paymentId,
        BigDecimal amount,
        String currency,
        RefundStatus status,
        String reason,
        Instant createdAt,
        Instant updatedAt
) {
    public static RefundResponse from(Refund refund) {
        return new RefundResponse(
                refund.id(),
                refund.paymentId(),
                refund.money().amount(),
                refund.money().currency(),
                refund.status(),
                refund.reason(),
                refund.createdAt(),
                refund.updatedAt());
    }
}
