/**
 * Payment use cases. {@link com.baypay.payment.application.PaymentApplicationService}
 * orchestrates; it does not re-implement currency rules.
 *
 * <p>{@link com.baypay.payment.application.PaymentAuthorizer} is the SOLID D/L
 * seam: tests (and a future card network) inject a different implementation
 * that must still decline a frozen account.
 */
package com.baypay.payment.application;
