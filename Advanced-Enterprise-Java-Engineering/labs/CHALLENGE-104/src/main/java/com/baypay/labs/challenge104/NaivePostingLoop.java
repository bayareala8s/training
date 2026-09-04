package com.baypay.labs.challenge104;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Random;

/**
 * Deliberately slow BayPay backfill used by CHALLENGE-104.
 * Nested list scans, boxed doubles, and per-row allocations.
 * Leave this file naive; put your faster class elsewhere.
 */
public class NaivePostingLoop {

    public static final long SEED = 20260903L;
    public static final int DEFAULT_PAYMENTS = 8_000;
    public static final int DEFAULT_EXISTING = 4_000;
    public static final int DEFAULT_ACCOUNTS = 500;

    public record InboundPayment(String paymentId, String accountId, Double amountCents) {
    }

    public static final class LedgerRow {
        public String paymentId;
        public String accountId;
        public Double amountCents;

        public LedgerRow(String paymentId, String accountId, Double amountCents) {
            this.paymentId = paymentId;
            this.accountId = accountId;
            this.amountCents = amountCents;
        }
    }

    public static final class Balance {
        public String accountId;
        public Double amountCents;

        public Balance(String accountId, Double amountCents) {
            this.accountId = accountId;
            this.amountCents = amountCents;
        }
    }

    public record Result(List<String> postedPaymentIds, List<Balance> balances, long checksum) {
    }

    public Result post(List<InboundPayment> inbound, List<LedgerRow> ledger, List<Balance> startingBalances) {
        List<Balance> working = new ArrayList<>();
        for (int i = 0; i < startingBalances.size(); i++) {
            Balance src = startingBalances.get(i);
            working.add(new Balance(new String(src.accountId), Double.valueOf(src.amountCents.doubleValue())));
        }

        List<String> posted = new ArrayList<>();
        for (InboundPayment payment : inbound) {
            boolean already = false;
            for (int i = 0; i < ledger.size(); i++) {
                LedgerRow row = ledger.get(i);
                if (row.paymentId.equals(payment.paymentId())) {
                    already = true;
                    break;
                }
            }
            if (!already) {
                for (int i = 0; i < posted.size(); i++) {
                    if (posted.get(i).equals(payment.paymentId())) {
                        already = true;
                        break;
                    }
                }
            }
            if (already) {
                continue;
            }

            Balance found = null;
            for (int i = 0; i < working.size(); i++) {
                Balance b = working.get(i);
                if (b.accountId.equals(payment.accountId())) {
                    found = b;
                    break;
                }
            }
            if (found == null) {
                continue;
            }

            Double next = Double.valueOf(found.amountCents.doubleValue() + payment.amountCents().doubleValue());
            found.amountCents = next;
            ledger.add(new LedgerRow(new String(payment.paymentId()), new String(payment.accountId()), next));
            posted.add(new String(payment.paymentId()));
        }
        return new Result(posted, working, checksum(posted, working));
    }

    public static long checksum(List<String> posted, List<Balance> balances) {
        long hash = posted.size() * 31L;
        List<String> sortedIds = new ArrayList<>(posted);
        sortedIds.sort(String::compareTo);
        for (String id : sortedIds) {
            hash = 31 * hash + id.hashCode();
        }
        List<Balance> sorted = new ArrayList<>(balances);
        sorted.sort((a, b) -> a.accountId.compareTo(b.accountId));
        for (Balance b : sorted) {
            hash = 31 * hash + Objects.hash(b.accountId, Math.round(b.amountCents));
        }
        return hash;
    }

    public static Workload generate(int payments, int existing, int accounts, long seed) {
        Random random = new Random(seed);
        List<String> accountIds = new ArrayList<>();
        List<Balance> balances = new ArrayList<>();
        for (int i = 0; i < accounts; i++) {
            String id = "acct-" + i;
            accountIds.add(id);
            balances.add(new Balance(id, Double.valueOf(1_000_000.0d + i)));
        }

        List<LedgerRow> ledger = new ArrayList<>();
        for (int i = 0; i < existing; i++) {
            String paymentId = "hist-" + i;
            String accountId = accountIds.get(i % accounts);
            ledger.add(new LedgerRow(paymentId, accountId, Double.valueOf(100.0d + i)));
        }

        List<InboundPayment> inbound = new ArrayList<>();
        for (int i = 0; i < payments; i++) {
            String paymentId = (i % 17 == 0 && i < existing) ? "hist-" + i : "new-" + i;
            String accountId = accountIds.get(random.nextInt(accounts));
            inbound.add(new InboundPayment(paymentId, accountId, Double.valueOf(25.0d + (i % 50))));
        }
        inbound.add(new InboundPayment(
                "new-avery-demo",
                accountIds.get(0),
                Double.valueOf(2500.0d)));
        return new Workload(inbound, ledger, balances);
    }

    public record Workload(List<InboundPayment> inbound, List<LedgerRow> ledger, List<Balance> balances) {
    }

    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : DEFAULT_PAYMENTS;
        Workload workload = generate(n, DEFAULT_EXISTING, DEFAULT_ACCOUNTS, SEED);
        NaivePostingLoop loop = new NaivePostingLoop();
        long start = System.nanoTime();
        Result result = loop.post(workload.inbound(), workload.ledger(), workload.balances());
        long ms = (System.nanoTime() - start) / 1_000_000L;
        System.out.println("naive posted=" + result.postedPaymentIds().size()
                + " checksum=" + result.checksum()
                + " elapsedMs=" + ms
                + " n=" + n);
    }
}
