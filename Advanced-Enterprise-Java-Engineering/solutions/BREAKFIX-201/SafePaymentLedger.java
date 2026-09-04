package com.baypay.labs.breakfix201;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Instructor reference for BREAKFIX-201. Do not ship to students before the attempt.
 *
 *   javac -d . SafePaymentLedger.java && java com.baypay.labs.breakfix201.SafePaymentLedger
 */
public class SafePaymentLedger {

    public record Entry(String paymentId, String idempotencyKey, String accountId, long amountCents) {
    }

    private final ConcurrentHashMap<String, Long> balances = new ConcurrentHashMap<>();
    private final ConcurrentLinkedQueue<Entry> journal = new ConcurrentLinkedQueue<>();
    private final ConcurrentHashMap<String, String> seenKeys = new ConcurrentHashMap<>();

    public boolean authorize(String paymentId, String idempotencyKey, String accountId, long amountCents) {
        if (amountCents <= 0) {
            throw new IllegalArgumentException("amountCents must be positive");
        }
        String existing = seenKeys.putIfAbsent(idempotencyKey, paymentId);
        if (existing != null) {
            return false;
        }
        balances.merge(accountId, amountCents, Long::sum);
        journal.offer(new Entry(paymentId, idempotencyKey, accountId, amountCents));
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

    public static void main(String[] args) throws InterruptedException {
        String accountId = "22222222-2222-2222-2222-222222222221";
        SafePaymentLedger uniqueLedger = new SafePaymentLedger();
        runParallel(8, 1000, i -> uniqueLedger.authorize("pay-unique-" + i, "key-unique-" + i, accountId, 100L));

        SafePaymentLedger replayLedger = new SafePaymentLedger();
        runParallel(8, 1000, i -> replayLedger.authorize("pay-replay-" + i, "harbor-8841", accountId, 8400L));

        System.out.println("Case A balance=" + uniqueLedger.balanceCents(accountId)
                + " journal=" + uniqueLedger.journalSize()
                + " sum=" + uniqueLedger.journalSumCents());
        System.out.println("Case B balance=" + replayLedger.balanceCents(accountId)
                + " journal=" + replayLedger.journalSize()
                + " sum=" + replayLedger.journalSumCents());
    }

    private static void runParallel(int threads, int tasks, IntWork work) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        AtomicInteger next = new AtomicInteger();
        for (int t = 0; t < threads; t++) {
            pool.execute(() -> {
                int i;
                while ((i = next.getAndIncrement()) < tasks) {
                    work.run(i);
                }
            });
        }
        pool.shutdown();
        if (!pool.awaitTermination(30, TimeUnit.SECONDS)) {
            pool.shutdownNow();
            throw new IllegalStateException("harness timed out");
        }
    }

    @FunctionalInterface
    private interface IntWork {
        void run(int i);
    }
}
