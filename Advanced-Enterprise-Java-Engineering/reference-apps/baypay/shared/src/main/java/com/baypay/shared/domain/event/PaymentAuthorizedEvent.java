package com.baypay.shared.domain.event;

import java.util.UUID;

public record PaymentAuthorizedEvent(UUID paymentId) {
}
