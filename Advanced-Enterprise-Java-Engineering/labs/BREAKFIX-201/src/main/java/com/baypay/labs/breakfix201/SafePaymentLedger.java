package com.baypay.labs.breakfix201;

/**
 * BREAKFIX-201 student stub. Repair the race in {@code starter/UnsafePaymentLedger.java}
 * here. The starter stays in the default package so {@code javac && java} still works.
 */
public class SafePaymentLedger {

    public record Entry(String paymentId, String idempotencyKey, String accountId, long amountCents) {
    }

    public boolean authorize(String paymentId, String idempotencyKey, String accountId, long amountCents) {
        throw new UnsupportedOperationException("implement BREAKFIX-201 SafePaymentLedger.authorize");
    }

    public long balanceCents(String accountId) {
        throw new UnsupportedOperationException("implement BREAKFIX-201");
    }

    public int journalSize() {
        throw new UnsupportedOperationException("implement BREAKFIX-201");
    }

    public long journalSumCents() {
        throw new UnsupportedOperationException("implement BREAKFIX-201");
    }
}
