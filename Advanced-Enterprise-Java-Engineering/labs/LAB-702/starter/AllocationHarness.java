package com.baypay.labs.lab702;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Controlled Payment-like allocation for LAB-702.
 * Two modes: {@code retain} keeps every record; {@code die} drops the reference
 * each iteration so the objects are garbage (unless the JIT scalar-replaces them).
 */
public final class AllocationHarness {

    public record PaymentLike(String id, long amountCents, String currency) {
    }

    public static void main(String[] args) {
        String mode = args.length > 0 ? args[0].toLowerCase(Locale.ROOT) : "retain";
        int n = args.length > 1 ? Integer.parseInt(args[1]) : 250_000;
        if (!"retain".equals(mode) && !"die".equals(mode)) {
            System.err.println("Usage: AllocationHarness <retain|die> [count]");
            System.exit(2);
        }
        if (n < 1) {
            System.err.println("count must be >= 1");
            System.exit(2);
        }

        Runtime runtime = Runtime.getRuntime();
        long beforeUsed = usedHeap(runtime);
        long startNs = System.nanoTime();

        List<PaymentLike> retained = "retain".equals(mode) ? new ArrayList<>(n) : null;
        long sinkCents = 0L;
        for (int i = 0; i < n; i++) {
            PaymentLike payment = new PaymentLike("pay-" + i, 100L + (i % 9_900), "USD");
            if (retained != null) {
                retained.add(payment);
            } else {
                sinkCents += payment.amountCents();
            }
        }

        long elapsedMs = (System.nanoTime() - startNs) / 1_000_000L;
        long afterUsed = usedHeap(runtime);

        System.out.println("mode=" + mode);
        System.out.println("count=" + n);
        System.out.println("elapsedMs=" + elapsedMs);
        System.out.println("runtimeUsedBeforeBytes=" + beforeUsed);
        System.out.println("runtimeUsedAfterBytes=" + afterUsed);
        System.out.println("runtimeUsedDeltaBytes=" + (afterUsed - beforeUsed));
        System.out.println("runtimeMaxBytes=" + runtime.maxMemory());
        System.out.println("retainedSize=" + (retained == null ? 0 : retained.size()));
        System.out.println("dieSinkCents=" + sinkCents);
    }

    private static long usedHeap(Runtime runtime) {
        return runtime.totalMemory() - runtime.freeMemory();
    }
}
