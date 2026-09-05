/**
 * Thin HTTP adapters. Bean Validation on the request is the 400 edge;
 * domain rules still run if a worker or test skips HTTP (L-1.2, L-3.x).
 * Controllers do not call {@code Payment.setStatus} — there is no such method.
 */
package com.baypay.payment.api;
