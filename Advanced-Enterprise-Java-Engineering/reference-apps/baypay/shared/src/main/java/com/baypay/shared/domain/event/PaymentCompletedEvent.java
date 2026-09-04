package com.baypay.shared.domain.event;

import java.util.UUID;

public record PaymentCompletedEvent(UUID paymentId, UUID customerId) {
}
