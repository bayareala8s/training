package com.baypay.shared.domain.event;

import java.util.UUID;

/** In-process signal that a refund posted. Same S-shaped split as payment completion. */
public record RefundCompletedEvent(UUID refundId, UUID paymentId, UUID customerId) {
}
