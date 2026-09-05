/**
 * In-process Spring events. {@code transaction-worker} publishes;
 * {@code notification-service} listens. Same JVM, same transaction today.
 * A later extraction replaces this with a queue. Lesson: L-1.2 S — Payment
 * does not send email.
 */
package com.baypay.shared.domain.event;
