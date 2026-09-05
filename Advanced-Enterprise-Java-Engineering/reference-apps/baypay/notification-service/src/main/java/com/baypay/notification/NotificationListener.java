package com.baypay.notification;

import com.baypay.shared.domain.NotificationRecord;
import com.baypay.shared.domain.event.PaymentCompletedEvent;
import com.baypay.shared.domain.event.RefundCompletedEvent;
import com.baypay.shared.persistence.NotificationRecordRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.context.event.EventListener;

import java.time.Clock;
import java.time.Instant;
import java.util.UUID;

/**
 * SOLID S: email/webhook records live here, not on {@code Payment}.
 * In-process {@code @EventListener}; fictional SENT row, no real mail host.
 */
@Component
public class NotificationListener {

    private static final Logger log = LoggerFactory.getLogger(NotificationListener.class);

    private final NotificationRecordRepository notifications;
    private final Clock clock;

    public NotificationListener(NotificationRecordRepository notifications, Clock clock) {
        this.notifications = notifications;
        this.clock = clock;
    }

    @EventListener
    public void onPaymentCompleted(PaymentCompletedEvent event) {
        record(event.customerId(), "payment-completed", "paymentId=" + event.paymentId());
    }

    @EventListener
    public void onRefundCompleted(RefundCompletedEvent event) {
        record(event.customerId(), "refund-completed", "refundId=" + event.refundId());
    }

    private void record(UUID customerId, String template, String payload) {
        Instant now = Instant.now(clock);
        NotificationRecord notification = new NotificationRecord(
                UUID.randomUUID(),
                customerId,
                NotificationRecord.Channel.EMAIL,
                template,
                payload,
                NotificationRecord.Status.SENT,
                now);
        notifications.save(notification);
        log.info("Notification {} sent template={} customer={}", notification.id(), template, customerId);
    }
}
