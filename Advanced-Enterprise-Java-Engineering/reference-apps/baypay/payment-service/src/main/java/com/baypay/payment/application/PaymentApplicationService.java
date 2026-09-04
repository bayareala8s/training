package com.baypay.payment.application;

import com.baypay.payment.api.CreatePaymentRequest;
import com.baypay.shared.domain.Account;
import com.baypay.shared.domain.AuditEvent;
import com.baypay.shared.domain.Customer;
import com.baypay.shared.domain.Money;
import com.baypay.shared.domain.Payment;
import com.baypay.shared.domain.PaymentStatus;
import com.baypay.shared.error.ErrorCode;
import com.baypay.worker.PaymentPostingService;
import com.baypay.shared.error.ResourceNotFoundException;
import com.baypay.shared.idempotency.IdempotencyKeys;
import com.baypay.shared.idempotency.IdempotencyRecord;
import com.baypay.shared.idempotency.IdempotencyService;
import com.baypay.shared.persistence.AccountRepository;
import com.baypay.shared.persistence.AuditEventRepository;
import com.baypay.shared.persistence.CustomerRepository;
import com.baypay.shared.persistence.PaymentRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Clock;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

@Service
public class PaymentApplicationService {

    private final CustomerRepository customers;
    private final AccountRepository accounts;
    private final PaymentRepository payments;
    private final AuditEventRepository audits;
    private final IdempotencyService idempotency;
    private final PaymentAuthorizer authorizer;
    private final PaymentPostingService posting;
    private final Clock clock;

    public PaymentApplicationService(
            CustomerRepository customers,
            AccountRepository accounts,
            PaymentRepository payments,
            AuditEventRepository audits,
            IdempotencyService idempotency,
            PaymentAuthorizer authorizer,
            PaymentPostingService posting,
            Clock clock) {
        this.customers = customers;
        this.accounts = accounts;
        this.payments = payments;
        this.audits = audits;
        this.idempotency = idempotency;
        this.authorizer = authorizer;
        this.posting = posting;
        this.clock = clock;
    }

    public record CreateResult(Payment payment, boolean replay) {
    }

    @Transactional
    public CreateResult create(CreatePaymentRequest request, String rawIdempotencyKey) {
        String key = IdempotencyKeys.require(rawIdempotencyKey);
        String hash = IdempotencyKeys.sha256(IdempotencyService.PAYMENT_CREATE, canonical(request));
        Optional<IdempotencyRecord> replay = idempotency.findReplay(IdempotencyService.PAYMENT_CREATE, key, hash);
        if (replay.isPresent()) {
            Payment existing = payments.findById(replay.get().resourceId())
                    .orElseThrow(() -> new ResourceNotFoundException(
                            ErrorCode.PAYMENT_NOT_FOUND, "Replay pointed at missing payment"));
            return new CreateResult(existing, true);
        }

        Instant now = Instant.now(clock);
        Customer customer = customers.findById(request.customerId())
                .orElseThrow(() -> new ResourceNotFoundException(
                        ErrorCode.CUSTOMER_NOT_FOUND, "Customer not found: " + request.customerId()));
        Account account = accounts.findById(request.accountId())
                .orElseThrow(() -> new ResourceNotFoundException(
                        ErrorCode.ACCOUNT_NOT_FOUND, "Account not found: " + request.accountId()));
        if (!account.belongsTo(customer.id())) {
            throw new com.baypay.shared.error.DomainValidationException(
                    ErrorCode.ACCOUNT_CUSTOMER_MISMATCH,
                    "Account does not belong to customer");
        }

        Money money = new Money(request.amount(), request.currency());
        Payment payment = Payment.received(
                UUID.randomUUID(),
                customer.id(),
                account.id(),
                money,
                request.reference(),
                key,
                now);
        payment.transitionTo(PaymentStatus.VALIDATING, now);

        PaymentAuthorizer.Decision decision = authorizer.authorize(payment, account);
        if (!decision.approved()) {
            payment.decline(decision.reason(), now);
            payments.save(payment);
            idempotency.remember(IdempotencyService.PAYMENT_CREATE, key, hash, payment.id(), 422, now);
            audit("system", "PAYMENT_DECLINED", payment.id(), decision.reason(), now);
            return new CreateResult(payment, false);
        }

        payment.transitionTo(PaymentStatus.AUTHORIZED, now);
        payments.save(payment);
        idempotency.remember(
                IdempotencyService.PAYMENT_CREATE, key, hash, payment.id(), HttpStatus.CREATED.value(), now);
        audit("system", "PAYMENT_AUTHORIZED", payment.id(), payment.money().toString(), now);
        Payment posted = posting.postAuthorized(payment);
        return new CreateResult(posted, false);
    }

    @Transactional(readOnly = true)
    public Payment get(UUID paymentId) {
        return payments.findById(paymentId)
                .orElseThrow(() -> new ResourceNotFoundException(
                        ErrorCode.PAYMENT_NOT_FOUND, "Payment not found: " + paymentId));
    }

    private void audit(String actor, String action, UUID paymentId, String detail, Instant now) {
        audits.save(new AuditEvent(UUID.randomUUID(), actor, action, "Payment", paymentId, detail, now));
    }

    private static String canonical(CreatePaymentRequest request) {
        return request.customerId()
                + "|" + request.accountId()
                + "|" + request.amount().toPlainString()
                + "|" + request.currency()
                + "|" + (request.reference() == null ? "" : request.reference());
    }
}
