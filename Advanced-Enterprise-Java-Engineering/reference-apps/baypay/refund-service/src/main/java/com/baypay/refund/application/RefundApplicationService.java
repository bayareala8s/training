package com.baypay.refund.application;

import com.baypay.refund.api.CreateRefundRequest;
import com.baypay.shared.domain.AuditEvent;
import com.baypay.shared.domain.LedgerTransaction;
import com.baypay.shared.domain.Money;
import com.baypay.shared.domain.Payment;
import com.baypay.shared.domain.PaymentStatus;
import com.baypay.shared.domain.Refund;
import com.baypay.shared.domain.RefundStatus;
import com.baypay.shared.domain.TransactionEvent;
import com.baypay.shared.domain.event.RefundCompletedEvent;
import com.baypay.shared.error.DomainValidationException;
import com.baypay.shared.error.ErrorCode;
import com.baypay.shared.error.ResourceNotFoundException;
import com.baypay.shared.idempotency.IdempotencyKeys;
import com.baypay.shared.idempotency.IdempotencyRecord;
import com.baypay.shared.idempotency.IdempotencyService;
import com.baypay.shared.persistence.AuditEventRepository;
import com.baypay.shared.persistence.LedgerTransactionRepository;
import com.baypay.shared.persistence.PaymentRepository;
import com.baypay.shared.persistence.RefundRepository;
import com.baypay.shared.persistence.TransactionEventRepository;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

@Service
public class RefundApplicationService {

    private final PaymentRepository payments;
    private final RefundRepository refunds;
    private final LedgerTransactionRepository ledger;
    private final TransactionEventRepository transactionEvents;
    private final AuditEventRepository audits;
    private final IdempotencyService idempotency;
    private final ApplicationEventPublisher events;
    private final Clock clock;

    public RefundApplicationService(
            PaymentRepository payments,
            RefundRepository refunds,
            LedgerTransactionRepository ledger,
            TransactionEventRepository transactionEvents,
            AuditEventRepository audits,
            IdempotencyService idempotency,
            ApplicationEventPublisher events,
            Clock clock) {
        this.payments = payments;
        this.refunds = refunds;
        this.ledger = ledger;
        this.transactionEvents = transactionEvents;
        this.audits = audits;
        this.idempotency = idempotency;
        this.events = events;
        this.clock = clock;
    }

    public record CreateResult(Refund refund, boolean replay) {
    }

    @Transactional
    public CreateResult create(CreateRefundRequest request, String rawIdempotencyKey) {
        String key = IdempotencyKeys.require(rawIdempotencyKey);
        String hash = IdempotencyKeys.sha256(
                IdempotencyService.REFUND_CREATE,
                request.paymentId() + "|" + request.amount().toPlainString() + "|"
                        + (request.reason() == null ? "" : request.reason()));
        Optional<IdempotencyRecord> replay = idempotency.findReplay(IdempotencyService.REFUND_CREATE, key, hash);
        if (replay.isPresent()) {
            Refund existing = refunds.findById(replay.get().resourceId())
                    .orElseThrow(() -> new ResourceNotFoundException(
                            ErrorCode.REFUND_NOT_FOUND, "Replay pointed at missing refund"));
            return new CreateResult(existing, true);
        }

        Instant now = Instant.now(clock);
        Payment payment = payments.findById(request.paymentId())
                .orElseThrow(() -> new ResourceNotFoundException(
                        ErrorCode.PAYMENT_NOT_FOUND, "Payment not found: " + request.paymentId()));
        if (payment.status() != PaymentStatus.COMPLETED && payment.status() != PaymentStatus.REVERSED) {
            throw new DomainValidationException(
                    ErrorCode.PAYMENT_NOT_REFUNDABLE,
                    "Payment status " + payment.status() + " is not refundable");
        }

        Money refundMoney = new Money(request.amount(), payment.money().currency());
        BigDecimal refunded = refunds.findByPaymentIdAndStatus(payment.id(), RefundStatus.COMPLETED).stream()
                .map(r -> r.money().amount())
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        if (refunded.add(refundMoney.amount()).compareTo(payment.money().amount()) > 0) {
            throw new DomainValidationException(
                    ErrorCode.REFUND_EXCEEDS_REMAINING,
                    "Refund exceeds remaining refundable amount");
        }

        Refund refund = Refund.requested(
                UUID.randomUUID(), payment.id(), refundMoney, request.reason(), key, now);
        refund.markProcessing(now);
        refund.complete(now);
        refunds.save(refund);

        LedgerTransaction posted = LedgerTransaction.refund(
                UUID.randomUUID(), payment.id(), refund.id(), refundMoney, now);
        ledger.save(posted);
        transactionEvents.save(new TransactionEvent(
                UUID.randomUUID(), posted.id(), "REFUND_POSTED", refundMoney.toString(), now));

        if (refunded.add(refundMoney.amount()).compareTo(payment.money().amount()) == 0) {
            payment.transitionTo(PaymentStatus.REVERSED, now);
            payments.save(payment);
        }

        idempotency.remember(
                IdempotencyService.REFUND_CREATE, key, hash, refund.id(), HttpStatus.CREATED.value(), now);
        audits.save(new AuditEvent(
                UUID.randomUUID(), "system", "REFUND_COMPLETED", "Refund", refund.id(), refundMoney.toString(), now));
        events.publishEvent(new RefundCompletedEvent(refund.id(), payment.id(), payment.customerId()));
        return new CreateResult(refund, false);
    }

    @Transactional(readOnly = true)
    public Refund get(UUID refundId) {
        return refunds.findById(refundId)
                .orElseThrow(() -> new ResourceNotFoundException(
                        ErrorCode.REFUND_NOT_FOUND, "Refund not found: " + refundId));
    }
}
