/**
 * Refund use cases. A refund is legal only against COMPLETED or REVERSED
 * payments and must not exceed remaining refundable amount. Same idempotency
 * rules as payment create.
 */
package com.baypay.refund.application;
