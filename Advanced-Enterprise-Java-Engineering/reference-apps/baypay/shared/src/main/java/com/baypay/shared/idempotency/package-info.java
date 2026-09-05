/**
 * Write-once replay protection for POST /payments and POST /refunds.
 *
 * <p>Same {@code Idempotency-Key} and same body hash → return the original resource.
 * Same key and a different body → {@code IDEMPOTENCY_CONFLICT} (HTTP 409).
 * Two JVM instances do not share this table's heap view; the unique row is the
 * multi-instance control. Lesson: L-1.5, Module 2.
 */
package com.baypay.shared.idempotency;
