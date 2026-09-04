package com.baypay.refund.api;

import com.baypay.refund.application.RefundApplicationService;
import com.baypay.shared.domain.Refund;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
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

@RestController
@RequestMapping("/api/v1/refunds")
@Tag(name = "Refunds")
public class RefundController {

    private final RefundApplicationService refunds;

    public RefundController(RefundApplicationService refunds) {
        this.refunds = refunds;
    }

    @PostMapping
    @Operation(summary = "Create a refund. Idempotency-Key is required.")
    public ResponseEntity<RefundResponse> create(
            @Valid @RequestBody CreateRefundRequest request,
            @RequestHeader(name = "Idempotency-Key", required = false) String idempotencyKey) {
        RefundApplicationService.CreateResult result = refunds.create(request, idempotencyKey);
        Refund refund = result.refund();
        RefundResponse body = RefundResponse.from(refund);
        if (result.replay()) {
            return ResponseEntity.ok(body);
        }
        return ResponseEntity.created(URI.create("/api/v1/refunds/" + refund.id())).body(body);
    }

    @GetMapping("/{refundId}")
    @Operation(summary = "Get a refund by id")
    public RefundResponse get(@PathVariable UUID refundId) {
        return RefundResponse.from(refunds.get(refundId));
    }
}
