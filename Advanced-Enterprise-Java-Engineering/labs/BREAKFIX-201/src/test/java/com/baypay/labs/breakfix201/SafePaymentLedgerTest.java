package com.baypay.labs.breakfix201;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class SafePaymentLedgerTest {

    private static final String ACCOUNT = "22222222-2222-2222-2222-222222222221";

    @Test
    void uniqueKeysAccumulateUnderContention() throws InterruptedException {
        SafePaymentLedger ledger = new SafePaymentLedger();
        runParallel(8, 400, i -> ledger.authorize("pay-unique-" + i, "key-unique-" + i, ACCOUNT, 100L));
        assertEquals(40_000L, ledger.balanceCents(ACCOUNT));
        assertEquals(400, ledger.journalSize());
        assertEquals(ledger.balanceCents(ACCOUNT), ledger.journalSumCents());
    }

    @Test
    void sameIdempotencyKeyPostsOnce() throws InterruptedException {
        SafePaymentLedger ledger = new SafePaymentLedger();
        runParallel(8, 400, i -> ledger.authorize("pay-replay-" + i, "harbor-8841", ACCOUNT, 8400L));
        assertEquals(8400L, ledger.balanceCents(ACCOUNT));
        assertEquals(1, ledger.journalSize());
        assertEquals(ledger.balanceCents(ACCOUNT), ledger.journalSumCents());
    }

    @Test
    void rejectsNonPositiveAmount() {
        SafePaymentLedger ledger = new SafePaymentLedger();
        assertThrows(IllegalArgumentException.class, () -> ledger.authorize("pay-0", "key-0", ACCOUNT, 0L));
        assertThrows(IllegalArgumentException.class, () -> ledger.authorize("pay-neg", "key-neg", ACCOUNT, -1L));
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
