package com.baypay.shared.domain.event;

import java.util.UUID;

/** Reserved for a later out-of-process worker. Posting today uses a direct call. */
public record PaymentAuthorizedEvent(UUID paymentId) {
}
