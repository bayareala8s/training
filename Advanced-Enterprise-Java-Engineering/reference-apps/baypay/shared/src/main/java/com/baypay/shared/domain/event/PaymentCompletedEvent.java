package com.baypay.shared.domain.event;

import java.util.UUID;

/** Published after the ledger row exists. The notifier records a SENT row. */
public record PaymentCompletedEvent(UUID paymentId, UUID customerId) {
}
