package com.baypay.labs.breakfix201;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Thread-safe canary ledger. Claim the idempotency key first ({@code putIfAbsent}),
 * then add the amount atomically. The starter's check-then-act on {@code seenKeys}
 * and get/put on {@code balances} both race.
 */
public class SafePaymentLedger {

    public record Entry(String paymentId, String idempotencyKey, String accountId, long amountCents) {
    }

    private final ConcurrentHashMap<String, Long> balances = new ConcurrentHashMap<>();
    private final CopyOnWriteArrayList<Entry> journal = new CopyOnWriteArrayList<>();
    private final ConcurrentHashMap<String, Boolean> seenKeys = new ConcurrentHashMap<>();

    public boolean authorize(String paymentId, String idempotencyKey, String accountId, long amountCents) {
        if (amountCents <= 0) {
            throw new IllegalArgumentException("amountCents must be positive");
        }
        if (seenKeys.putIfAbsent(idempotencyKey, Boolean.TRUE) != null) {
            return false;
        }
        balances.merge(accountId, amountCents, Long::sum);
        journal.add(new Entry(paymentId, idempotencyKey, accountId, amountCents));
        return true;
    }

    public long balanceCents(String accountId) {
        return balances.getOrDefault(accountId, 0L);
    }

    public int journalSize() {
        return journal.size();
    }

    public long journalSumCents() {
        long sum = 0L;
        for (Entry entry : journal) {
            sum += entry.amountCents();
        }
        return sum;
    }
}
