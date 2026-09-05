package com.baypay.worker;

import com.baypay.shared.domain.AuditEvent;
import com.baypay.shared.domain.LedgerTransaction;
import com.baypay.shared.domain.Payment;
import com.baypay.shared.domain.PaymentStatus;
import com.baypay.shared.domain.TransactionEvent;
import com.baypay.shared.domain.event.PaymentCompletedEvent;
import com.baypay.shared.persistence.AuditEventRepository;
import com.baypay.shared.persistence.LedgerTransactionRepository;
import com.baypay.shared.persistence.PaymentRepository;
import com.baypay.shared.persistence.TransactionEventRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import java.time.Clock;
import java.time.Instant;
import java.util.UUID;

/**
 * In-process ledger posting. Called from the payment module on the same
 * transaction so POST /payments returns COMPLETED. A later extraction
 * replaces this call with a queue publish.
 */
@Service
public class PaymentPostingService {

    private static final Logger log = LoggerFactory.getLogger(PaymentPostingService.class);

    private final PaymentRepository payments;
    private final LedgerTransactionRepository ledger;
    private final TransactionEventRepository transactionEvents;
    private final AuditEventRepository audits;
    private final ApplicationEventPublisher events;
    private final Clock clock;

    public PaymentPostingService(
            PaymentRepository payments,
            LedgerTransactionRepository ledger,
            TransactionEventRepository transactionEvents,
            AuditEventRepository audits,
            ApplicationEventPublisher events,
            Clock clock) {
        this.payments = payments;
        this.ledger = ledger;
        this.transactionEvents = transactionEvents;
        this.audits = audits;
        this.events = events;
        this.clock = clock;
    }

    /**
     * AUTHORIZED → PROCESSING → ledger row → COMPLETED, then
     * {@link PaymentCompletedEvent} for the notifier. Hold no lock across I/O
     * if this is later extracted (L-2.2).
     */
    public Payment postAuthorized(Payment payment) {
        Instant now = Instant.now(clock);
        payment.transitionTo(PaymentStatus.PROCESSING, now);
        LedgerTransaction posted = LedgerTransaction.payment(
                UUID.randomUUID(), payment.id(), payment.money(), now);
        ledger.save(posted);
        transactionEvents.save(new TransactionEvent(
                UUID.randomUUID(), posted.id(), "PAYMENT_POSTED", payment.money().toString(), now));
        payment.transitionTo(PaymentStatus.COMPLETED, now);
        payments.save(payment);
        audits.save(new AuditEvent(
                UUID.randomUUID(), "transaction-worker", "PAYMENT_POSTED", "Payment",
                payment.id(), posted.id().toString(), now));
        events.publishEvent(new PaymentCompletedEvent(payment.id(), payment.customerId()));
        log.info("Posted payment {} as ledger {}", payment.id(), posted.id());
        return payment;
    }
}
