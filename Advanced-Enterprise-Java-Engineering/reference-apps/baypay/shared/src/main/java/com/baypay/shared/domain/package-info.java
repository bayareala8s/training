/**
 * BayPay domain types. Start here in Module 1.
 *
 * <p>{@link com.baypay.shared.domain.Money} is a value object (no identity, no setters).
 * {@link com.baypay.shared.domain.Payment} is an entity (UUID identity; status changes
 * only through {@link com.baypay.shared.domain.Payment#transitionTo}).
 *
 * <p>Invariants live in constructors and the state machine, not in controllers.
 * Lesson: L-1.2 (SOLID and immutability), L-1.3 (EnumSet transitions).
 */
package com.baypay.shared.domain;
