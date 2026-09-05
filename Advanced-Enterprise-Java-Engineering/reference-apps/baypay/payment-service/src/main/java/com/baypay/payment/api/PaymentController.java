package com.baypay.payment.api;

import com.baypay.payment.application.PaymentApplicationService;
import com.baypay.shared.domain.Payment;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.net.URI;
import java.util.UUID;

/**
 * HTTP edge for payments. Replay → 200; decline → 422; first success → 201.
 * {@code Idempotency-Key} is required (header may be missing; the service rejects it).
 */
@RestController
@RequestMapping("/api/v1/payments")
@Tag(name = "Payments")
public class PaymentController {

    private final PaymentApplicationService payments;

    public PaymentController(PaymentApplicationService payments) {
        this.payments = payments;
    }

    @PostMapping
    @Operation(summary = "Create a payment. Idempotency-Key is required.")
    public ResponseEntity<PaymentResponse> create(
            @Valid @RequestBody CreatePaymentRequest request,
            @RequestHeader(name = "Idempotency-Key", required = false) String idempotencyKey) {
        PaymentApplicationService.CreateResult result = payments.create(request, idempotencyKey);
        Payment payment = result.payment();
        PaymentResponse body = PaymentResponse.from(payment);
        if (result.replay()) {
            return ResponseEntity.ok(body);
        }
        if (payment.status() == com.baypay.shared.domain.PaymentStatus.DECLINED) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(body);
        }
        return ResponseEntity.created(URI.create("/api/v1/payments/" + payment.id())).body(body);
    }

    @GetMapping("/{paymentId}")
    @Operation(summary = "Get a payment by id")
    public PaymentResponse get(@PathVariable UUID paymentId) {
        return PaymentResponse.from(payments.get(paymentId));
    }
}
