/**
 * Composition root for the modular monolith. {@code Clock} and
 * {@link com.baypay.payment.application.PaymentAuthorizer} are beans so tests
 * can freeze time and swap the authorizer without editing the service.
 */
package com.baypay.payment.config;
