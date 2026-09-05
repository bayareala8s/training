package com.baypay.refund.api;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.util.UUID;

/** HTTP refund command. Currency is taken from the payment, not this body. */
public record CreateRefundRequest(
        @NotNull UUID paymentId,
        @NotNull @DecimalMin(value = "0.01", inclusive = true) BigDecimal amount,
        @Size(max = 256) String reason
) {
}
