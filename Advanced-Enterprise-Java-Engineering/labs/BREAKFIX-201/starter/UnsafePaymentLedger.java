import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * BayPay BREAKFIX-201 starter. Fictional in-memory authorize path.
 *
 * Compile and run from this directory:
 *   javac UnsafePaymentLedger.java && java UnsafePaymentLedger
 *
 * Java 21. No Maven required.
 */
public class UnsafePaymentLedger {

    public record Entry(String paymentId, String idempotencyKey, String accountId, long amountCents) {
    }

    private final ConcurrentHashMap<String, Long> balances = new ConcurrentHashMap<>();
    private final List<Entry> journal = new ArrayList<>();
    private final ConcurrentHashMap<String, Boolean> seenKeys = new ConcurrentHashMap<>();

    public void authorize(String paymentId, String idempotencyKey, String accountId, long amountCents) {
        if (amountCents <= 0) {
            throw new IllegalArgumentException("amountCents must be positive");
        }
        if (Boolean.TRUE.equals(seenKeys.get(idempotencyKey))) {
            return;
        }
        long current = balances.getOrDefault(accountId, 0L);
        balances.put(accountId, current + amountCents);
        journal.add(new Entry(paymentId, idempotencyKey, accountId, amountCents));
        seenKeys.put(idempotencyKey, Boolean.TRUE);
    }

    public long balanceCents(String accountId) {
        return balances.getOrDefault(accountId, 0L);
    }

    public int journalSize() {
        return journal.size();
    }

    public long journalSumCents() {
        long sum = 0L;
        int unreadable = 0;
        Object[] snapshot;
        try {
            snapshot = journal.toArray();
        } catch (RuntimeException e) {
            System.err.println("journal toArray failed: " + e);
            return -1L;
        }
        for (Object slot : snapshot) {
            if (slot instanceof Entry entry) {
                sum += entry.amountCents();
            } else {
                unreadable++;
            }
        }
        if (unreadable > 0) {
            System.err.println("journal contained " + unreadable + " unreadable slots");
        }
        return sum;
    }

    public static void main(String[] args) throws InterruptedException {
        String accountId = "22222222-2222-2222-2222-222222222221";
        int threads = 8;
        int uniquePosts = 1000;
        long amount = 100L;

        UnsafePaymentLedger uniqueLedger = new UnsafePaymentLedger();
        runParallel(threads, uniquePosts, (i) -> uniqueLedger.authorize(
                "pay-unique-" + i,
                "key-unique-" + i,
                accountId,
                amount));

        UnsafePaymentLedger replayLedger = new UnsafePaymentLedger();
        runParallel(threads, uniquePosts, (i) -> replayLedger.authorize(
                "pay-replay-" + i,
                "harbor-8841",
                accountId,
                8400L));

        System.out.println("=== BREAKFIX-201 UnsafePaymentLedger ===");
        System.out.println("Account: " + accountId);
        System.out.println();
        System.out.println("Case A — " + uniquePosts + " distinct idempotency keys, " + threads + " threads");
        System.out.println("  expected balance cents : " + (uniquePosts * amount));
        System.out.println("  actual balance cents   : " + uniqueLedger.balanceCents(accountId));
        System.out.println("  expected journal size  : " + uniquePosts);
        System.out.println("  actual journal size    : " + uniqueLedger.journalSize());
        System.out.println("  journal sum cents      : " + uniqueLedger.journalSumCents());
        System.out.println();
        System.out.println("Case B — " + uniquePosts + " parallel retries of key harbor-8841, amount 8400");
        System.out.println("  expected balance cents : 8400");
        System.out.println("  actual balance cents   : " + replayLedger.balanceCents(accountId));
        System.out.println("  expected journal size  : 1");
        System.out.println("  actual journal size    : " + replayLedger.journalSize());
        System.out.println();
        System.out.println("A correct ledger matches expected on both cases, every run.");
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
