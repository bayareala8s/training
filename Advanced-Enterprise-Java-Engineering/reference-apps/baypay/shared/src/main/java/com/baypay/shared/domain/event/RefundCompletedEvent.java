package com.baypay.shared.domain.event;

import java.util.UUID;

public record RefundCompletedEvent(UUID refundId, UUID paymentId, UUID customerId) {
}
