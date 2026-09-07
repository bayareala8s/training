import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.LongAdder;

/**
 * Single-JVM authorize slice for ARCHITECT-203. Claim the key, then merge cents.
 * No second monitor — payment and refund cannot deadlock on lock order.
 */
public class ConcurrentPaymentProcessor {

    public record Entry(String paymentId, String idempotencyKey, String accountId, long amountCents) {
    }

    private static final String DEMO_ACCOUNT = "22222222-2222-2222-2222-222222222221";

    private final ConcurrentHashMap<String, Boolean> keys = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<String, Long> balances = new ConcurrentHashMap<>();
    private final ConcurrentLinkedQueue<Entry> journal = new ConcurrentLinkedQueue<>();
    private final Semaphore admission = new Semaphore(32);
    private final LongAdder accepted = new LongAdder();
    private final LongAdder rejected = new LongAdder();

    public boolean authorize(String paymentId, String idempotencyKey, String accountId, long amountCents) {
        return apply(paymentId, idempotencyKey, accountId, amountCents);
    }

    /** Same claim-then-merge path; negative cents. Cannot take a second lock. */
    public boolean refund(String refundId, String idempotencyKey, String accountId, long amountCents) {
        if (amountCents <= 0) {
            throw new IllegalArgumentException("amountCents must be positive");
        }
        return apply(refundId, idempotencyKey, accountId, -amountCents);
    }

    public long balanceCents(String accountId) {
        return balances.getOrDefault(accountId, 0L);
    }

    public int journalSize() {
        return journal.size();
    }

    public long acceptedCount() {
        return accepted.sum();
    }

    public long rejectedCount() {
        return rejected.sum();
    }

    private boolean apply(String id, String idempotencyKey, String accountId, long amountCents) {
        if (amountCents == 0L) {
            throw new IllegalArgumentException("amountCents must be non-zero");
        }
        if (!admission.tryAcquire()) {
            rejected.increment();
            return false;
        }
        try {
            if (keys.putIfAbsent(idempotencyKey, Boolean.TRUE) != null) {
                rejected.increment();
                return false;
            }
            // Crash window: key claimed, cents not yet merged.
            balances.merge(accountId, amountCents, Long::sum);
            // Crash window: total ahead of journal.
            journal.offer(new Entry(id, idempotencyKey, accountId, amountCents));
            accepted.increment();
            return true;
        } finally {
            admission.release();
        }
    }

    public static void main(String[] args) throws Exception {
        for (int run = 1; run <= 3; run++) {
            caseA(run);
            caseB(run);
        }
        System.out.println("ARCHITECT-203 Case A and Case B matched expected values three times.");
    }

    private static void caseA(int run) throws Exception {
        ConcurrentPaymentProcessor p = new ConcurrentPaymentProcessor();
        runParallel(8, 1000, i -> p.authorize("pay-a-" + i, "key-a-" + i, DEMO_ACCOUNT, 100L));
        check("Case A run " + run, 100_000L, 1000, p);
    }

    private static void caseB(int run) throws Exception {
        ConcurrentPaymentProcessor p = new ConcurrentPaymentProcessor();
        runParallel(8, 1000, i -> p.authorize("pay-b-" + i, "harbor-8841", DEMO_ACCOUNT, 8400L));
        check("Case B run " + run, 8400L, 1, p);
    }

    private static void check(String label, long balance, int journal, ConcurrentPaymentProcessor p) {
        if (p.balanceCents(DEMO_ACCOUNT) != balance || p.journalSize() != journal) {
            throw new IllegalStateException(label + " got balance=" + p.balanceCents(DEMO_ACCOUNT)
                    + " journal=" + p.journalSize());
        }
        System.out.println(label + " OK balance=" + balance + " journal=" + journal);
    }

    private static void runParallel(int threads, int tasks, IntWork work) throws Exception {
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
