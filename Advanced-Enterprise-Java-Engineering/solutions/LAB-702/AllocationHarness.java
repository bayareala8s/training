package com.baypay.labs.lab702;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Instructor reference for LAB-702. Same CLI as the starter, plus an optional
 * third argument {@code gc} (hint only) and {@code money} to allocate a
 * Money-like pair (cents + BigDecimal) so students can see extra objects.
 *
 * <p>Escape analysis may scalar-replace a non-escaping {@code PaymentLike} in
 * {@code die} mode. It does not always do so, and the {@code "pay-" + i}
 * {@link String} still allocates.
 */
public final class AllocationHarness {

    public record PaymentLike(String id, long amountCents, String currency) {
    }

    /** Teaching stand-in for {@code com.baypay.shared.domain.Money} (cents + scale). */
    public record MoneyLike(long amountCents, String currency, BigDecimal decimal) {
        static MoneyLike usd(long cents) {
            return new MoneyLike(cents, "USD", BigDecimal.valueOf(cents, 2));
        }
    }

    public static void main(String[] args) {
        String mode = args.length > 0 ? args[0].toLowerCase(Locale.ROOT) : "retain";
        int n = args.length > 1 ? Integer.parseInt(args[1]) : 250_000;
        String extra = args.length > 2 ? args[2].toLowerCase(Locale.ROOT) : "";
        if (!"retain".equals(mode) && !"die".equals(mode)) {
            System.err.println("Usage: AllocationHarness <retain|die> [count] [gc|money]");
            System.exit(2);
        }
        if (n < 1) {
            System.err.println("count must be >= 1");
            System.exit(2);
        }

        boolean useMoney = "money".equals(extra);
        boolean hintGc = "gc".equals(extra);

        Runtime runtime = Runtime.getRuntime();
        long beforeUsed = usedHeap(runtime);
        long startNs = System.nanoTime();

        List<Object> retained = "retain".equals(mode) ? new ArrayList<>(n) : null;
        long sinkCents = 0L;
        int moneyScaleSink = 0;
        for (int i = 0; i < n; i++) {
            long cents = 100L + (i % 9_900);
            if (useMoney) {
                MoneyLike money = MoneyLike.usd(cents);
                PaymentLike payment = new PaymentLike("pay-" + i, money.amountCents(), money.currency());
                if (retained != null) {
                    retained.add(payment);
                    retained.add(money);
                } else {
                    sinkCents += payment.amountCents();
                    moneyScaleSink += money.decimal().scale();
                }
            } else {
                PaymentLike payment = new PaymentLike("pay-" + i, cents, "USD");
                if (retained != null) {
                    retained.add(payment);
                } else {
                    sinkCents += payment.amountCents();
                }
            }
        }

        long elapsedMs = (System.nanoTime() - startNs) / 1_000_000L;
        if (hintGc) {
            System.gc();
        }
        long afterUsed = usedHeap(runtime);

        System.out.println("mode=" + mode);
        System.out.println("count=" + n);
        System.out.println("variant=" + (useMoney ? "money" : "record"));
        System.out.println("gcHint=" + hintGc);
        System.out.println("elapsedMs=" + elapsedMs);
        System.out.println("runtimeUsedBeforeBytes=" + beforeUsed);
        System.out.println("runtimeUsedAfterBytes=" + afterUsed);
        System.out.println("runtimeUsedDeltaBytes=" + (afterUsed - beforeUsed));
        System.out.println("runtimeTotalBytes=" + runtime.totalMemory());
        System.out.println("runtimeMaxBytes=" + runtime.maxMemory());
        System.out.println("retainedSize=" + (retained == null ? 0 : retained.size()));
        System.out.println("dieSinkCents=" + sinkCents);
        System.out.println("moneyScaleSink=" + moneyScaleSink);
    }

    private static long usedHeap(Runtime runtime) {
        return runtime.totalMemory() - runtime.freeMemory();
    }
}
